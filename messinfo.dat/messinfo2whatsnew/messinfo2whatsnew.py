import tkinter as tk
from tkinter import filedialog
import re

def print_progress(progress):
    bar_length = 40
    block = int(round(bar_length * progress))
    text = f"\rElaborando... [{('#' * block).ljust(bar_length)}] {int(progress * 100)}%"
    print(text, end='', flush=True)

def main():
    root = tk.Tk()
    root.withdraw()

    input_file = filedialog.askopenfilename(title="Seleziona il file messinfo.dat", filetypes=[("DAT files", "*.dat")])
    if not input_file:
        print("\nNessun file selezionato.")
        return

    mame_version = input("Inserisci la versione MAME da cercare (es. 0.277): ").strip()
    if not mame_version:
        print("\nNessuna versione inserita.")
        return

    wip_entry_re = re.compile(rf"^- {re.escape(mame_version)}: (.+)$")
    exclude_suffixes = ("device.", "system.", "driver.")

    output_lines = []

    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    total_lines = len(lines)
    current_machine = None
    i = 0

    print_progress(0)

    while i < len(lines):
        line = lines[i].strip()

        # Rileva il nome della macchina
        if line.startswith("$info="):
            current_machine = line.split("=", 1)[1].strip()

        # Cerca il blocco WIP
        elif line.startswith("WIP:"):
            i += 1
            while i < len(lines):
                wip_line = lines[i].strip()
                if wip_line == "":
                    break
                match = wip_entry_re.match(wip_line)
                if match:
                    description = match.group(1)
                    if not any(description.lower().endswith(suffix) for suffix in exclude_suffixes):
                        if current_machine:
                            output_lines.append(f"- {current_machine}: {description}")
                i += 1
            continue  # Salta l'i += 1 fuori

        i += 1

        if i % 1000 == 0 or i == len(lines):
            print_progress(i / total_lines)

    print("\nFatto!")

    # Salva l'output su file
    version_suffix = mame_version.split('.')[-1]
    output_file = f"output_{version_suffix}.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))

    print(f"Output salvato in '{output_file}'")
    print(f"Trovate {len(output_lines)} corrispondenze per la versione '{mame_version}'.")
    if len(output_lines) == 0:
        print("Attenzione: nessuna voce trovata. Verifica che la versione sia presente nel file.")

if __name__ == "__main__":
    main()