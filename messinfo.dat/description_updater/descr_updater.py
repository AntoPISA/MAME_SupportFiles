import tkinter as tk
from tkinter import filedialog
import os

def leggi_descrizioni(file_path):
    descrizioni = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or not line.startswith('|'):
                continue
            content = line[1:].strip()
            if ' | ' in content:
                nome, descr = content.split(' | ', 1)
                descrizioni[nome.strip()] = descr.strip()
    return descrizioni

def elabora_file_dat(file_path, descrizioni, output_path):
    macchina_corrente = None
    sostituito = False

    with open(file_path, 'r', encoding='utf-8') as infile, \
         open(output_path, 'w', encoding='utf-8') as outfile:

        for num_linea, linea in enumerate(infile, 1):
            linea_stripped = linea.rstrip('\r\n')  # rimuove solo i newline finali

            # Rileva inizio blocco
            if linea_stripped.startswith('$info='):
                macchina_corrente = linea_stripped[6:].strip()
                sostituito = False  # reset per ogni nuovo blocco

            # Se siamo in un blocco e non abbiamo ancora sostituito...
            if macchina_corrente and not sostituito:
                if '<No certified information found. If you have info on this machine, please contact us!>' in linea_stripped:
                    # Verifica che sia l'intera riga (o quasi)
                    if linea_stripped.strip() == '<No certified information found. If you have info on this machine, please contact us!>':
                        # Sostituisci con la descrizione corretta, mantenendo gli spazi iniziali
                        indent = linea[:len(linea) - len(linea.lstrip())]  # spazi/tab iniziali
                        nuova_descrizione = descrizioni.get(macchina_corrente)
                        if nuova_descrizione:
                            outfile.write(indent + nuova_descrizione + '\n')
                            sostituito = True
                            continue

            # Altrimenti, scrivi la riga originale
            outfile.write(linea)

    print(f"✅ File elaborato: {output_path}")

def main():
    root = tk.Tk()
    root.withdraw()

    file_dat = filedialog.askopenfilename(
        title="Seleziona il file messinfo.dat",
        filetypes=[("DAT files", "*.dat"), ("All files", "*.*")]
    )
    if not file_dat:
        print("❌ Nessun file DAT selezionato.")
        return

    file_desc = filedialog.askopenfilename(
        title="Seleziona il file con le descrizioni",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if not file_desc:
        print("❌ Nessun file descrizioni selezionato.")
        return

    try:
        descrizioni = leggi_descrizioni(file_desc)
        print(f"✅ Caricate {len(descrizioni)} descrizioni.")

        nome_output = file_dat
        if nome_output.endswith('.dat'):
            nome_output = nome_output[:-4] + '_descrupdated.dat'
        else:
            nome_output += '_descrupdated'

        elabora_file_dat(file_dat, descrizioni, nome_output)

    except Exception as e:
        print(f"💥 Errore: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()