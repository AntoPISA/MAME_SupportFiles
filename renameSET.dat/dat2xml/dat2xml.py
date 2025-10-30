import re
import os
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
import xml.etree.ElementTree as ET
from datetime import datetime


# Elenco completo dei campi statistici
STAT_FIELDS = [
    "total items", "drivers", "machines", "parents", "clones", "BIOSes", "devices",
    "requires CHDs", "use samples", "audio mono", "audio stereo", "audio multichannel", "no audio",
    "working", "not working", "mechanicals", "not mechanicals", "save supported", "save unsupported",
    "horizontal screen", "vertical screen", "raster graphics", "vector graphics", "lcd graphics",
    "svg graphics", "screenless",
    "one player", "two players", "three players", "more than three players",
    "use stick", "use gambling", "use joystick", "use keyboard", "use keypad", "use lightgun",
    "use mahjong", "use mouse", "use buttons only", "use paddle", "use pedal", "use positional",
    "use dial", "use trackball", "use hanafuda",
    "total roms", "machines roms", "devices roms", "BIOSes roms", "CHDs",
    "sample files", "sample packs", "good dumps", "no dumps", "bad dumps", "bugs fixed",
    "software list", "software", "active SL", "orphan SL", "active software", "orphan software",
    "software parents", "software clones", "software roms", "software CHD",
    "supported software", "partially supported software", "unsupported software"
]

def clean_number(s):
    """Converte '233.450' -> '233450' come stringa di cifre"""
    return re.sub(r'[^\d]', '', s) or "0"

def prettify_with_tabs(elem):
    """Ritorna una stringa XML indentata con TAB invece che spazi"""
    from xml.dom import minidom
    rough = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough)
    return reparsed.toprettyxml(indent="\t", encoding='utf-8').decode('utf-8')

class DATToXMLConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("DAT to XML Converter v2.2 (Final)")
        self.root.geometry("850x680")
        self.root.resizable(True, True)

        top_frame = ttk.Frame(root, padding="10")
        top_frame.pack(fill=tk.X)

        self.btn_exit = ttk.Button(top_frame, text="Esci", command=root.destroy)
        self.btn_exit.pack(side=tk.LEFT)

        self.btn_select = ttk.Button(top_frame, text="Seleziona file .dat", command=self.select_file)
        self.btn_select.pack(side=tk.LEFT, padx=(10, 0))

        self.btn_convert = ttk.Button(top_frame, text="Converti in XML", command=self.convert, state=tk.DISABLED)
        self.btn_convert.pack(side=tk.LEFT, padx=(10, 0))

        self.log_enabled_var = tk.BooleanVar(value=True)
        self.log_checkbox = ttk.Checkbutton(top_frame, text="Abilita log dettagliato", variable=self.log_enabled_var)
        self.log_checkbox.pack(side=tk.LEFT, padx=(20, 0))

        self.status = ttk.Label(top_frame, text="Nessun file selezionato", foreground="gray")
        self.status.pack(side=tk.LEFT, padx=(20, 0))

        log_frame = ttk.LabelFrame(root, text="Log", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.log = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.log.pack(fill=tk.BOTH, expand=True)

        self.dat_path = None

    def log_message(self, msg):
        if not self.log_enabled_var.get():
            return
        self.log.config(state=tk.NORMAL)
        self.log.insert(tk.END, msg + "\n")
        self.log.see(tk.END)
        self.log.config(state=tk.DISABLED)
        self.root.update()

    def select_file(self):
        path = filedialog.askopenfilename(
            title="Seleziona il file renameSET.dat",
            filetypes=[("DAT files", "*.dat *.dat.txt"), ("All files", "*.*")]
        )
        if path:
            self.dat_path = path
            self.status.config(text=os.path.basename(path), foreground="black")
            self.btn_convert.config(state=tk.NORMAL)
            self.log_message(f"✅ File selezionato: {path}")

    def convert(self):
        if not self.dat_path:
            return

        try:
            header_data = self.ask_header_info()
            if header_data is None:
                return
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nei metadati: {e}")
            return

        try:
            self.log_message("🔄 Inizio conversione completa...")
            xml_root = self.parse_full_dat(self.dat_path, header_data)
            xml_str = prettify_with_tabs(xml_root)

            xml_path = os.path.splitext(self.dat_path)[0] + ".xml"
            with open(xml_path, "w", encoding="utf-8") as f:
                f.write(xml_str)

            self.log_message(f"✅ Conversione completata!")
            self.log_message(f"📄 File XML salvato: {xml_path}")
            messagebox.showinfo("Successo", f"File XML generato con successo:\n{xml_path}")

        except Exception as e:
            self.log_message(f"❌ Errore: {str(e)}")
            messagebox.showerror("Errore", f"Si è verificato un errore:\n{str(e)}")

    def ask_header_info(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Metadati XML")
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Data (es. Oct 30 2025):").pack(pady=(10, 0))
        date_var = tk.StringVar(value="Oct 30 2025")
        date_entry = ttk.Entry(dialog, textvariable=date_var, width=30)
        date_entry.pack()

        ttk.Label(dialog, text="Versione interna (es. 15.11):").pack(pady=(10, 0))
        version_var = tk.StringVar(value="15.11")
        version_entry = ttk.Entry(dialog, textvariable=version_var, width=30)
        version_entry.pack()

        result = {}

        def on_ok():
            user_date_str = date_var.get().strip()
            internal_version = version_var.get().strip()
            if not user_date_str or not internal_version:
                messagebox.showwarning("Attenzione", "Compila entrambi i campi.")
                return

            # Converti "Oct 30 2025" → "10/30/2025"
            try:
                parsed_date = datetime.strptime(user_date_str, "%b %d %Y")
                numeric_date = parsed_date.strftime("%m/%d/%Y")
            except ValueError:
                try:
                    parsed_date = datetime.strptime(user_date_str, "%B %d %Y")
                    numeric_date = parsed_date.strftime("%m/%d/%Y")
                except ValueError:
                    messagebox.showerror("Errore data", "Formato data non valido.\nUsa: 'Oct 30 2025' o 'October 30 2025'")
                    return

            result['date_desc'] = user_date_str
            result['numeric_date'] = numeric_date
            result['internal_version'] = internal_version
            dialog.destroy()

        def on_cancel():
            dialog.destroy()

        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=15)
        ttk.Button(btn_frame, text="OK", command=on_ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Annulla", command=on_cancel).pack(side=tk.LEFT, padx=5)

        self.root.wait_window(dialog)
        return result if result else None

    def parse_full_dat(self, dat_path, header_data):
        with open(dat_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        first_mame_version = "unknown"
        mame_match = re.search(r'\$(\S+)\s*\[#', content)
        if mame_match:
            first_mame_version = mame_match.group(1)

        root = ET.Element("renameSET")

        header = ET.SubElement(root, "header")
        ET.SubElement(header, "name").text = "renameSET"
        ET.SubElement(header, "description").text = f"renameSET ({header_data['date_desc']})"
        ET.SubElement(header, "version").text = header_data["internal_version"]
        ET.SubElement(header, "date").text = header_data["numeric_date"]  # ✅ Solo numeri: mm/dd/yyyy
        ET.SubElement(header, "author").text = "AntoPISA"
        ET.SubElement(header, "email").text = "progettosnaps@gmail.com"
        ET.SubElement(header, "homepage").text = "http://www.progettosnaps.net/"
        ET.SubElement(header, "url").text = "http://www.progettosnaps.net/renameset"
        ET.SubElement(header, "comment").text = f"Aligned with MAME {first_mame_version}"

        content = re.sub(r'([a-zA-Z])(\d+\s*ren\s*\()', r'\1 \2', content)
        content = re.sub(r'([a-zA-Z])(\d+\s*del\s*\()', r'\1 \2', content)
        lines = [line.rstrip('\n') for line in content.splitlines()]

        version_pattern = re.compile(r'^\$(\S+)\s*\[#(\d+)\]')
        date_pattern = re.compile(r'^(\d{4})/(\d{2})/(\d{2})')
        rename_pattern = re.compile(r'^(\S+)\s*>\s*(\S+)\s*\(mID:\s*(\d+)\)\s*([MD])\s*(\*\*\*)?$')
        delete_pattern = re.compile(r'^(\S+)\s*\(mID:\s*(\d+)\)\s*([MD])\s*(\*\*\*)?$')

        i = 0
        total_lines = len(lines)

        while i < total_lines:
            line = lines[i].strip()
            if not line:
                i += 1
                continue

            ver_match = version_pattern.match(line)
            if not ver_match:
                i += 1
                continue

            version = ver_match.group(1)
            internal_id = ver_match.group(2)
            elem = ET.SubElement(root, "version", version=version, id=internal_id)

            i += 1
            if i < total_lines:
                date_match = date_pattern.match(lines[i].strip())
                if date_match:
                    y, m, d = date_match.groups()
                    elem.set("date", f"{y}-{m}-{d}")
                    i += 1

            block_lines = []
            while i < total_lines and not version_pattern.match(lines[i].strip()):
                block_lines.append(lines[i].strip())
                i += 1

            stat_lines = []
            ren_del_lines = []
            for line in block_lines:
                if not line:
                    continue
                if re.match(r'^\d+[\d.,]*\s+[a-zA-Z]', line):
                    stat_lines.append(line)
                else:
                    ren_del_lines.append(line)

            stats = {field: "0" for field in STAT_FIELDS}
            full_text = " ".join(stat_lines)
            full_text = re.sub(r'\s*\([^)]*\)', '', full_text)
            full_text = re.sub(r',', ' ', full_text)
            full_text = re.sub(r'\s+', ' ', full_text).strip()

            sorted_fields = sorted(STAT_FIELDS, key=lambda x: -len(x))
            for field in sorted_fields:
                pattern = r'([\d.,]+)\s+' + re.escape(field) + r'(?=\s|$)'
                match = re.search(pattern, full_text, re.IGNORECASE)
                if match:
                    value_raw = match.group(1)
                    clean_val = clean_number(value_raw)
                    stats[field] = clean_val
                    full_text = full_text[:match.start()] + " " + full_text[match.end():]

            stats_elem = ET.SubElement(elem, "statistics")
            for field, value in stats.items():
                ET.SubElement(stats_elem, "stat", name=field.replace(" ", "_")).text = value

            ren_section = None
            del_section = None
            for line in ren_del_lines:
                if not line or line == '-' or re.match(r'^\d+\s+(?:ren|del)\s+\(', line):
                    continue
                r_match = rename_pattern.match(line)
                if r_match:
                    if ren_section is None:
                        ren_section = ET.SubElement(elem, "rename_list")
                    old, new, mID, typ, note = r_match.groups()
                    el = ET.SubElement(ren_section, "rename", old=old, new=new, mID=mID, type=typ)
                    if note:
                        el.set("note", "review")
                    continue
                d_match = delete_pattern.match(line)
                if d_match:
                    if del_section is None:
                        del_section = ET.SubElement(elem, "delete_list")
                    name, mID, typ, note = d_match.groups()
                    el = ET.SubElement(del_section, "delete", name=name, mID=mID, type=typ)
                    if note:
                        el.set("note", "review")
                    continue

        return root


if __name__ == "__main__":
    root = tk.Tk()
    app = DATToXMLConverter(root)
    root.mainloop()