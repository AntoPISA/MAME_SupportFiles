import os
import traceback
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText
import configparser
import zipfile

# ==============================
# MESSINFO Resources & ROMSET Updater 1.0
# Fase 1: Aggiornamento Risorse
# Fase 2: Aggiornamento ROMSET
# ==============================

RESOURCES = {
    'snap': ('Snap', '.png'),
    'titles': ('Title', '.png'),
    'icons': ('Icon', '.ico'),
    'cabinets': ('machine picture (in "Cabinet" collection)', '.png'),
    'cpanels': ('Control Panel', '.png'),
    'flyers': ('Flyer', '.png'),
    'manuals': ('pdf Manual', '.pdf'),
    'marquees': ('Marquee', '.png'),
    'pcbs': ('PCB', '.png'),
    'artpreview': ('Artwork Preview', '.png')
}

def load_config():
    """Carica i percorsi dal config.ini"""
    config = configparser.ConfigParser()
    config_file = 'config.ini'
    if not os.path.exists(config_file):
        return None, f"File di configurazione '{config_file}' non trovato!"

    try:
        config.read(config_file)
        paths = {}
        for key in RESOURCES.keys():
            if key not in config['Paths']:
                return None, f"Chiave '{key}' mancante in config.ini"
            path = config['Paths'][key]
            abs_path = os.path.abspath(path)
            if not os.path.exists(abs_path):
                return None, f"Percorso non trovato: {abs_path}"
            paths[key] = abs_path

        if 'roms' not in config['Paths']:
            return None, "Chiave 'roms' mancante in config.ini"
        roms_path = os.path.abspath(config['Paths']['roms'])
        if not os.path.exists(roms_path):
            return None, f"Percorso ROMs non trovato: {roms_path}"
        paths['roms'] = roms_path

        return paths, None
    except Exception as e:
        return None, f"Errore nel config.ini: {e}"

def check_resource_exists(base_name, folder_path, extension, log_widget=None):
    """Verifica se esiste il file nella cartella"""
    if not os.path.exists(folder_path):
        if log_widget:
            log_widget.insert(tk.END, f"❌ Cartella non esiste: {folder_path}\n")
            log_widget.see(tk.END)
        return False

    filename = base_name + extension
    filepath = os.path.join(folder_path, filename)

    found = os.path.isfile(filepath)
    if found:
        if log_widget:
            log_widget.insert(tk.END, f"✅ Trovato: {filename}\n")
            log_widget.see(tk.END)
    else:
        if log_widget:
            log_widget.insert(tk.END, f"❌ Non trovato: {filename}\n")
            log_widget.see(tk.END)
    return found

def build_resources_line(base_name, resource_paths, log_widget=None):
    """Costruisce la riga delle risorse disponibili"""
    available = []
    for key, (display_name, ext) in RESOURCES.items():
        if key == 'roms': continue
        folder = resource_paths[key]
        if check_resource_exists(base_name, folder, ext, log_widget):
            available.append(display_name)

    if not available:
        return "No resources available."

    if len(available) == 1:
        return available[0] + "."
    elif len(available) == 2:
        return f"{available[0]} and {available[1]}."
    else:
        return ", ".join(available[:-1]) + f" and {available[-1]}."

def get_romset_info(zip_path, log_widget=None):
    """Calcola informazioni sul pacchetto ROM"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            info_list = z.infolist()
            total_unpacked = sum(f.file_size for f in info_list)
            total_files = len(info_list)
            total_packed = sum(f.compress_size for f in info_list)

            if total_packed >= 1024 * 1024:
                packed_str = f"{total_packed / (1024*1024):.2f}Mb"
            else:
                packed_str = f"{total_packed / 1024:.2f}Kb"

            file_str = "file" if total_files == 1 else "files"
            return f"{total_unpacked} bytes in {total_files} {file_str} / {packed_str} packed"
    except Exception as e:
        if log_widget:
            log_widget.insert(tk.END, f"⚠️ Errore lettura zip {os.path.basename(zip_path)}: {e}\n")
        return None

def update_resources_phase(dat_path, resource_paths):
    """Fase 1: Aggiorna la sezione RESOURCES"""
    try:
        with open(dat_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        messagebox.showerror("Errore", f"Impossibile leggere il file: {e}")
        return False

    total_entries = sum(1 for line in lines if line.strip().startswith('$info='))
    if total_entries == 0:
        messagebox.showwarning("Attenzione", "Nessuna macchina trovata nel file .dat.")
        return False

    progress_window = tk.Toplevel()
    progress_window.title("Fase 1: Aggiornamento Risorse")
    progress_window.geometry("600x300")
    progress_window.transient()
    progress_window.grab_set()

    label = tk.Label(progress_window, text="Aggiornamento Risorse in corso...", font=("Helvetica", 10))
    label.pack(pady=5)

    progress_bar = ttk.Progressbar(progress_window, length=500, mode="determinate")
    progress_bar.pack(pady=5)
    progress_bar["maximum"] = total_entries

    log_text = ScrolledText(progress_window, height=12, width=70)
    log_text.pack(pady=5, padx=10)
    log_text.insert(tk.END, "Avvio Fase 1...\n")
    log_text.see(tk.END)
    progress_window.update()

    updated_lines = []
    i = 0
    in_entry = False
    info_name = None
    processed = 0

    while i < len(lines):
        line = lines[i]
        updated_lines.append(line)
        stripped = line.strip()

        if stripped.startswith('$info='):
            info_name = stripped.split('=', 1)[1].strip()
            in_entry = True

        elif in_entry and stripped.startswith('RESOURCES:'):
            # Salta la riga corrente
            i += 1
            # Aggiungi la nuova riga
            if info_name:
                res_line = build_resources_line(info_name, resource_paths, log_text)
                updated_lines.append(res_line + '\n')
            else:
                updated_lines.append("No resources available.\n")
            processed += 1
            progress_bar["value"] = processed
            progress_window.update()

        elif stripped.startswith('$end'):
            in_entry = False
            info_name = None

        i += 1

    try:
        with open(dat_path, 'w', encoding='utf-8') as f:
            f.writelines(updated_lines)
        log_text.insert(tk.END, "\n✅ Fase 1 completata.\n")
    except Exception as e:
        log_text.insert(tk.END, f"\n❌ Errore salvataggio: {e}\n")
        messagebox.showerror("Errore", f"Salvataggio fallito: {e}")
        return False

    progress_window.update()
    progress_window.destroy()
    return True

def update_romset_phase(dat_path, resource_paths):
    """Fase 2: Aggiorna la sezione ROMSET"""
    roms_folder = resource_paths['roms']

    try:
        with open(dat_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        messagebox.showerror("Errore", f"Impossibile leggere il file: {e}")
        return False

    # Trova tutte le macchine
    machines = []
    i = 0
    while i < len(lines):
        if lines[i].strip().startswith('$info='):
            name = lines[i].strip().split('=', 1)[1].strip()
            machines.append({'name': name, 'index': i})
        i += 1

    # Scelta: aggiornamento completo o solo mancanti
    choice = messagebox.askyesnocancel(
        "Fase 2: Aggiornamento ROMSET",
        "Scegli l'opzione:\n\n"
        "✅ Sì: Aggiornamento COMPLETO (tutte le macchine)\n"
        "❌ No: Aggiungi SOLO informazioni mancanti\n"
        "✖️ Cancella: Annulla"
    )
    if choice is None:
        return False

    full_update = choice

    # Elenco macchine da aggiornare
    to_update = []
    for m in machines:
        zip_path = os.path.join(roms_folder, m['name'] + '.zip')
        if not os.path.exists(zip_path):
            continue

        # Cerca se ROMSET ha già dati
        has_data = False
        j = m['index']
        while j < len(lines) and not lines[j].strip().startswith('$end'):
            if lines[j].strip().startswith('ROMSET:') and j + 1 < len(lines):
                next_line = lines[j+1].strip()
                if 'bytes in' in next_line or 'packed' in next_line:
                    has_data = True
            j += 1

        if full_update or not has_data:
            to_update.append(m['name'])

    if not to_update:
        messagebox.showinfo("Fase 2", "Nessuna voce da aggiornare.")
        return True

    # Finestra avanzamento
    progress_window = tk.Toplevel()
    progress_window.title("Fase 2: Aggiornamento ROMSET")
    progress_window.geometry("600x300")
    progress_window.transient()
    progress_window.grab_set()

    label = tk.Label(progress_window, text="Aggiornamento ROMSET in corso...", font=("Helvetica", 10))
    label.pack(pady=5)

    progress_bar = ttk.Progressbar(progress_window, length=500, mode="determinate")
    progress_bar.pack(pady=5)
    progress_bar["maximum"] = len(to_update)

    log_text = ScrolledText(progress_window, height=12, width=70)
    log_text.pack(pady=5, padx=10)
    log_text.insert(tk.END, "Avvio Fase 2...\n")
    log_text.see(tk.END)
    progress_window.update()

    # Ricrea il file
    updated_lines = []
    i = 0
    current_info = None

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith('$info='):
            current_info = stripped.split('=', 1)[1].strip()

        if current_info and stripped.startswith('ROMSET:'):
            # Aggiungi ROMSET:
            updated_lines.append(line)

            # Calcola i nuovi dati
            zip_path = os.path.join(roms_folder, current_info + '.zip')
            info_str = get_romset_info(zip_path, log_text)
            final_str = info_str if info_str else "0 bytes in 0 files / 0.00Kb packed"

            # Aggiungi la riga aggiornata
            updated_lines.append(final_str + "\n")
            log_text.insert(tk.END, f"📝 {current_info}: {final_str}\n")

            # Salta la riga successiva se contiene dati vecchi
            if i + 1 < len(lines):
                next_line = lines[i+1].strip()
                if next_line and not next_line.startswith('$') and ('bytes in' in next_line or 'packed' in next_line):
                    i += 1  # salta la riga obsoleta

            log_text.see(tk.END)
            progress_window.update()

        else:
            updated_lines.append(line)

        i += 1

    # Salva
    try:
        with open(dat_path, 'w', encoding='utf-8') as f:
            f.writelines(updated_lines)
        log_text.insert(tk.END, "\n✅ Fase 2 completata.\n")
    except Exception as e:
        log_text.insert(tk.END, f"\n❌ Errore salvataggio: {e}\n")
        messagebox.showerror("Errore", f"Salvataggio fallito: {e}")
        return False

    progress_window.update()
    messagebox.showinfo("Fase 2", "Aggiornamento ROMSET completato.")
    progress_window.destroy()
    return True

def main():
    root = tk.Tk()
    root.withdraw()

    # Seleziona il file dat
    dat_path = filedialog.askopenfilename(
        title="Seleziona il file messinfo.dat",
        filetypes=[("DAT files", "*.dat"), ("All files", "*.*")]
    )
    if not dat_path:
        messagebox.showwarning("Attenzione", "Nessun file selezionato.")
        return

    # Carica configurazione
    resource_paths, error = load_config()
    if error:
        messagebox.showerror("Errore Config", error)
        return

    # Scegli la fase
    choice = messagebox.askyesnocancel(
        "Seleziona Fase",
        "Scegli cosa eseguire:\n\n"
        "✅ Sì: Fase 1 → Fase 2\n"
        "❌ No: Solo Fase 2 (ROMSET)\n"
        "✖️ Cancella: Solo Fase 1 (Risorse)"
    )

    if choice is True:
        # Fase 1 + Fase 2
        if update_resources_phase(dat_path, resource_paths):
            update_romset_phase(dat_path, resource_paths)
    elif choice is False:
        # Solo Fase 2
        update_romset_phase(dat_path, resource_paths)
    else:
        # Solo Fase 1
        update_resources_phase(dat_path, resource_paths)

    messagebox.showinfo("Completato", "Operazione terminata.")
    root.destroy()

if __name__ == "__main__":
    main()