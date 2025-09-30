import re
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def format_number_with_dot(n):
    """Formatta un numero intero con punto come separatore delle migliaia."""
    return f"{n:,}".replace(",", ".")

def parse_dat_xml_block(dat_xml_lines):
    """Estrae valori base e variazioni dalla sezione DAT/XML.
    Gestisce:
      - ">        n/d vs        446 raster graphics ERROR"
      - ">        442 vs        446 raster graphics ERROR"
      - ">        n/d vs      (+15) raster graphics DIFF. ERROR"
      - ">      (+11) vs      (+15) raster graphics DIFF. ERROR"
    """
    updates = {}
    i = 0
    while i < len(dat_xml_lines):
        line = dat_xml_lines[i]
        # Rimuovi prefisso '> ... vs' (sia "n/d" che numeri o variazioni)
        clean = re.sub(r'^\s*>\s+(?:n/d|\d+\.?\d*|\([\+\-]?\d+(?:\/\+\d+)?\))\s+vs\s+', '', line.strip())

        # 1. Cerca valore base: "446 raster graphics ERROR"
        base_match = re.match(r'^([\d\.]+)\s+(.+?)\s+ERROR$', clean)
        if base_match:
            value_str = base_match.group(1).replace('.', '')
            try:
                value = int(value_str)
                key = base_match.group(2).strip()
                diff_str = None

                # Cerca variazione DIFF nella riga successiva
                if i + 1 < len(dat_xml_lines):
                    next_line = dat_xml_lines[i + 1]
                    next_clean = re.sub(r'^\s*>\s+(?:n/d|\d+\.?\d*|\([\+\-]?\d+(?:\/\+\d+)?\))\s+vs\s+', '', next_line.strip())
                    diff_match = re.match(r'^(\([\+\-]?\d+(?:\/\+\d+)?\))\s+(.+?)\s+DIFF\.\s+ERROR$', next_clean)
                    if diff_match and diff_match.group(2).strip() == key:
                        diff_str = diff_match.group(1)
                        i += 1  # Salta la riga DIFF

                updates[key] = (value, diff_str)
            except ValueError:
                pass

        # 2. Cerca riga DIFF. ERROR SENZA riga base precedente
        else:
            diff_only_match = re.match(r'^(\([\+\-]?\d+(?:\/\+\d+)?\))\s+(.+?)\s+DIFF\.\s+ERROR$', clean)
            if diff_only_match:
                diff_str = diff_only_match.group(1)
                key = diff_only_match.group(2).strip()
                updates[key] = (None, diff_str)

        i += 1
    return updates

def update_stat_line(line, key_to_update):
    """Aggiorna i valori nella riga statistica."""
    parts = line.split(',')
    updated_parts = []

    for part in parts:
        updated_part = part
        for key, (new_value, diff_str) in key_to_update.items():
            pattern = r'(\d+)\s+(' + re.escape(key) + r')(\s*\([^\)]*\))?'
            match = re.search(pattern, part)
            if match:
                start, end = match.span()
                before = part[:start]
                after_key = part[end:]

                formatted_value = format_number_with_dot(new_value) if new_value is not None else match.group(1)
                new_segment = f"{formatted_value} {key}"
                if diff_str:
                    new_segment += f" {diff_str}"

                updated_part = before + new_segment + after_key
                break
        updated_parts.append(updated_part)

    return ','.join(updated_parts)

def process_file(input_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Dividi i blocchi usando '\n---\n' come separatore
    raw_blocks = content.strip().split('\n---\n')
    output_blocks = []

    for block in raw_blocks:
        lines = block.split('\n')
        dat_xml_index = -1

        # Trova la riga che contiene "DAT           XML"
        for i, line in enumerate(lines):
            if "DAT           XML" in line:
                dat_xml_index = i
                break

        if dat_xml_index == -1:
            output_blocks.append(block)
            continue

        # Estrai le righe DAT/XML (quelle che iniziano con '>')
        dat_xml_lines = []
        i = dat_xml_index + 1
        while i < len(lines) and lines[i].strip().startswith('>'):
            dat_xml_lines.append(lines[i])
            i += 1

        # Estrai aggiornamenti
        key_to_update = parse_dat_xml_block(dat_xml_lines)

        # Applica aggiornamenti alle righe PRIMA di "DAT XML"
        stat_lines = lines[:dat_xml_index]  # Esclude la riga "DAT XML" e tutto ciò che segue
        updated_stat_lines = []
        for line in stat_lines:
            updated_line = update_stat_line(line, key_to_update)
            updated_stat_lines.append(updated_line)

        # ✅ RIMUOVI RIGHE VUOTE FINALI
        while updated_stat_lines and updated_stat_lines[-1].strip() == "":
            updated_stat_lines.pop()

        # Unisci le righe senza newline finale extra
        new_block = '\n'.join(updated_stat_lines)
        output_blocks.append(new_block)

    # Unisci i blocchi con '\n---\n' — questo aggiunge il separatore SOLO tra i blocchi
    full_content = '\n---\n'.join(output_blocks)

    # Scrivi output
    base, ext = os.path.splitext(input_path)
    output_path = base + ".updated" + ext
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_content)

    return output_path

def main():
    root = tk.Tk()
    root.withdraw()
    root.update()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = filedialog.askopenfilename(
        title="Seleziona il file da modificare",
        initialdir=script_dir,
        filetypes=[("Tutti i file", "*.*")]
    )

    if not input_file:
        print("❌ Nessun file selezionato.")
        return

    try:
        output_file = process_file(input_file)
        messagebox.showinfo("✅ Completato", f"File aggiornato e pulito salvato come:\n{output_file}")
        print(f"✅ File processato: {output_file}")
    except Exception as e:
        messagebox.showerror("❌ Errore", f"Si è verificato un errore:\n{str(e)}")
        print(f"❌ Errore: {e}")

if __name__ == "__main__":
    main()