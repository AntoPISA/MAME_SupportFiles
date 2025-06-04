import os
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog, messagebox
from shutil import copy2
from collections import OrderedDict
from xml.dom import minidom
from PIL import Image, ImageTk
import io

# --- Funzioni principali ---

def select_folder():
    folder = filedialog.askdirectory(title="Seleziona la cartella con i file XML")
    return folder

def extract_number_from_filename(filename):
    name = os.path.splitext(filename)[0]
    parts = name.split("_")
    if len(parts) >= 3:
        try:
            return int(parts[1])
        except ValueError:
            pass
    return None

def get_description_from_header(root):
    """Cerca la <description> solo sotto <header>"""
    header = root.find('header')
    if header is not None:
        desc_elem = header.find('description')
        if desc_elem is not None and desc_elem.text:
            return desc_elem.text.strip()
    return "Nessuna descrizione disponibile"

def prettify_driver(driver_elem):
    if driver_elem is None:
        return "<driver non presente>"
    rough_string = ET.tostring(driver_elem, encoding='utf-8', method='xml')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ").strip()
    # Rimuove la dichiarazione XML se c'è
    lines = [line for line in pretty_xml.split('\n') if not line.strip().startswith('<?xml')]
    return '\n'.join(lines)

# --- GUI ---

class XMLUpdaterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MAME XML Driver Fix v1.0")
        self.root.geometry("650x550")  # Dimensione corretta
        self.root.resizable(False, False)

        # Percorso logo (cartella 'pic/logo.jpg')
        self.logo_path = os.path.join(os.path.dirname(__file__), "pic", "logo.jpg")

        # Lista valori suggeriti
        self.options = {
            'status': ['good', 'imperfect', 'preliminary'],
            'emulation': ['good', 'preliminary'],
            'color': ['good', 'imperfect', 'preliminary'],
            'sound': ['good', 'imperfect', 'preliminary'],
            'graphic': ['good', 'imperfect', 'preliminary'],
            'savestate': ['supported', 'unsupported']
        }

        # Variabili dei campi
        self.entries = {}
        self.vars = {}

        # UI
        self.create_widgets()

    def create_widgets(self):
        # Titolo con logo
        title_frame = tk.Frame(self.root)
        title_frame.pack(pady=10)

        # Carica il logo dalla cartella pic/
        if os.path.exists(self.logo_path):
            img = Image.open(self.logo_path)
            img = img.resize((64, 64))
            logo_img = ImageTk.PhotoImage(img)
            tk.Label(title_frame, image=logo_img).pack(side=tk.LEFT, padx=10)
            self.logo_label = logo_img  # Per evitare garbage collection

        tk.Label(title_frame, text="MAME XML Driver Fix v1.0", font=("Arial", 16, "bold")).pack(side=tk.LEFT)

        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=10)

        row = 0

        # Cartella
        tk.Label(main_frame, text="Cartella:", font=("Arial", 10)).grid(row=row, column=0, sticky="w", padx=10, pady=5)
        self.folder_entry = tk.Entry(main_frame, width=40)
        self.folder_entry.grid(row=row, column=1, columnspan=2, padx=10, pady=5)

        # Bottone Sfoglia
        row += 1
        tk.Button(main_frame, text="Sfoglia", command=self.browse_folder).grid(row=row, column=1, columnspan=2, padx=10, pady=5)

        row += 1
        tk.Label(main_frame, text="Game/Macchina da correggere *", fg="red").grid(
            row=row, column=0, sticky="w", padx=10, pady=5)
        self.vars['game_name'] = tk.StringVar()
        self.entries['game_name'] = tk.Entry(main_frame, textvariable=self.vars['game_name'], width=40)
        self.entries['game_name'].grid(row=row, column=1, columnspan=2, padx=10, pady=5)

        row += 1
        tk.Label(main_frame, text="Da numero file *", fg="red").grid(row=row, column=0, sticky="w", padx=10, pady=5)
        self.vars['from_version'] = tk.StringVar()
        self.entries['from_version'] = tk.Entry(main_frame, textvariable=self.vars['from_version'], width=40)
        self.entries['from_version'].grid(row=row, column=1, columnspan=2, padx=10, pady=5)

        row += 1
        tk.Label(main_frame, text="Fino a numero file *", fg="red").grid(row=row, column=0, sticky="w", padx=10, pady=5)
        self.vars['to_version'] = tk.StringVar()
        self.entries['to_version'] = tk.Entry(main_frame, textvariable=self.vars['to_version'], width=40)
        self.entries['to_version'].grid(row=row, column=1, columnspan=2, padx=10, pady=5)

        row += 1
        tk.Label(main_frame, text="Driver Fields", font=("Arial", 10, "bold")).grid(row=row, column=0, sticky="w", padx=10, pady=5)

        for field in ['status', 'emulation', 'color', 'sound', 'graphic', 'savestate']:
            row += 1
            tk.Label(main_frame, text=f"{field.capitalize()}:").grid(row=row, column=0, sticky="w", padx=10, pady=2)
            var = tk.StringVar()
            entry = tk.Entry(main_frame, textvariable=var, width=40)
            entry.grid(row=row, column=1, columnspan=2, padx=10, pady=2)
            self.vars[field] = var
            self.entries[field] = entry

            # Bind per suggerimento
            entry.bind("<KeyRelease>", lambda e, f=field: self.autocomplete(e, f))

        row += 1
        tk.Button(main_frame, text="Correggi Status", width=15, command=self.run_script).grid(row=row, column=1, padx=10, pady=15)
        tk.Button(main_frame, text="Exit", width=10, command=self.root.quit).grid(row=row, column=2, padx=10, pady=15)

    def autocomplete(self, event, field):
        value = self.vars[field].get().lower()
        options = self.options[field]

        for option in options:
            if option.startswith(value):
                self.vars[field].set(option)
                self.entries[field].icursor(tk.END)
                break

    def browse_folder(self):
        folder = filedialog.askdirectory(title="Seleziona la cartella con i file XML")
        if folder:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder)

    def get_values(self):
        values = {}
        for key in self.vars:
            values[key] = self.vars[key].get().strip().lower()

        try:
            values['from_num'] = int(values.pop('from_version'))
            values['to_num'] = int(values.pop('to_version'))
        except ValueError:
            messagebox.showerror("Errore", "I valori 'da' e 'a' devono essere numeri interi.")
            return None

        if not values['game_name']:
            messagebox.showerror("Errore", "Il campo 'Game/Macchina' è obbligatorio.")
            return None

        return values

    def run_script(self):
        config = self.get_values()
        if not config:
            return

        folder_path = self.folder_entry.get()
        if not folder_path or not os.path.isdir(folder_path):
            messagebox.showerror("Errore", "Seleziona una cartella valida.")
            return

        backup_path = os.path.join(folder_path, "backup")
        os.makedirs(backup_path, exist_ok=True)
        log_file = os.path.join(backup_path, "log_modifiche.txt")

        driver_attrib = {k: v for k, v in config.items() if k not in ['from_num', 'to_num', 'game_name']}

        modified_games = OrderedDict()

        for filename in os.listdir(folder_path):
            if not filename.lower().endswith('.xml'):
                continue

            file_number = extract_number_from_filename(filename)
            if file_number is None or not (config['from_num'] <= file_number <= config['to_num']):
                continue

            file_path = os.path.join(folder_path, filename)
            backup_file = os.path.join(backup_path, filename)

            try:
                tree = ET.parse(file_path)
                root = tree.getroot()

                game_name = config['game_name']
                modified = False

                # Estrai la description dal <header>
                description = get_description_from_header(root)

                # Cerca ricorsivamente <game> o <machine>
                elements_to_check = []
                for elem in root.iter():
                    if elem.tag in ['game', 'machine'] and elem.get('name', '').lower() == game_name.lower():
                        elements_to_check.append(elem)

                if not elements_to_check:
                    continue

                for element in elements_to_check:
                    old_driver = element.find('driver')
                    old_str = prettify_driver(old_driver)

                    if old_driver is not None:
                        old_driver.attrib.update(driver_attrib)
                    else:
                        ET.SubElement(element, 'driver', driver_attrib)

                    new_str = prettify_driver(element.find('driver'))

                    game_key = element.get('name')
                    if game_key not in modified_games:
                        modified_games[game_key] = []

                    modified_games[game_key].append({
                        'before': old_str,
                        'after': new_str,
                        'description': description
                    })

                    modified = True

                if modified:
                    copy2(file_path, backup_file)
                    tree.write(file_path, encoding='utf-8', xml_declaration=True)
                    print(f"Modificato: {filename}")

            except Exception as e:
                print(f"Errore durante l'elaborazione di {filename}: {e}")

        # Scrive il log
        if modified_games:
            with open(log_file, 'w', encoding='utf-8') as f:
                for game in sorted(modified_games.keys()):
                    f.write(f"{game}:\n")
                    for mod in modified_games[game]:
                        f.write(f"{mod['description']}\n")
                        f.write("Prima:\n")
                        f.write(mod['before'])
                        f.write("\nDopo:\n")
                        f.write(mod['after'])
                        f.write("\n\n")
            messagebox.showinfo("Completato", f"Operazione completata!\nLog salvato in: {log_file}")
        else:
            messagebox.showwarning("Nessuna modifica", "Non sono stati trovati file da modificare.")

# --- Avvio app ---
if __name__ == "__main__":
    root = tk.Tk()
    app = XMLUpdaterGUI(root)
    root.mainloop()