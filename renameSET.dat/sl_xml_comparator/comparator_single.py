import xml.etree.ElementTree as ET
from collections import defaultdict
import tkinter as tk
from tkinter import filedialog, messagebox
import os

    # (C) AntoPISA www.progettosnaps.net v1.0

def parse_xml(file_path):
    """Analizza un file XML e mappa gli SHA1 ai nomi dei software."""
    sha1_map = defaultdict(set)
    stats = {'total_software': 0, 'roms_with_sha1': 0}

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        for software in root.findall('software'):
            stats['total_software'] += 1
            software_name = software.get('name')
            if not software_name:
                continue

            for part in software.findall('part'):
                for dataarea in part.findall('dataarea'):
                    for rom in dataarea.findall('rom'):
                        sha1 = rom.get('sha1', '').strip().lower()
                        if sha1 and len(sha1) == 40 and all(c in '0123456789abcdef' for c in sha1):
                            sha1_map[sha1].add(software_name)
                            stats['roms_with_sha1'] += 1

        print(f"\nStatistiche per {os.path.basename(file_path)}:")
        print(f"Software analizzati: {stats['total_software']}")
        print(f"ROM con SHA1 valido: {stats['roms_with_sha1']}")

    except ET.ParseError as e:
        raise RuntimeError(f"Errore nell'analisi del file XML: {e}")
    except Exception as e:
        raise RuntimeError(f"Errore imprevisto: {e}")

    return sha1_map

def main():
    # Configurazione interfaccia grafica
    root = tk.Tk()
    root.withdraw()

    try:
        # Selezione file primario
        primary_path = filedialog.askopenfilename(
            title='Seleziona file XML Primario',
            filetypes=[('File XML', '*.xml')]
        )
        if not primary_path:
            print("Nessun file primario selezionato.")
            return

        # Selezione file di confronto
        comparison_path = filedialog.askopenfilename(
            title='Seleziona file XML di Confronto',
            filetypes=[('File XML', '*.xml')]
        )
        if not comparison_path:
            print("Nessun file di confronto selezionato.")
            return

        # Analisi dei file XML
        print("\nAnalisi file primario...")
        primary_dict = parse_xml(primary_path)

        print("\nAnalisi file di confronto...")
        comparison_dict = parse_xml(comparison_path)

        # Trova gli SHA1 comuni e quelli solo nel primario
        common_sha1s = set(primary_dict.keys()) & set(comparison_dict.keys())
        unique_primary_sha1 = set(primary_dict.keys()) - set(comparison_dict.keys())

        print("\nRisultati dell'analisi:")
        print(f"SHA1 comuni: {len(common_sha1s)}")
        print(f"SHA1 solo nel primario: {len(unique_primary_sha1)}")

        if not common_sha1s and not unique_primary_sha1:
            messagebox.showwarning(
                "Nessun risultato",
                "Non sono stati trovati SHA1 comuni né software esclusivi del file primario."
            )
            return

        # Creazione del file di log
        log_dir = os.path.dirname(primary_path)
        primary_basename = os.path.splitext(os.path.basename(primary_path))[0]
        log_filename = f"{primary_basename}-sha1_comparison.log"
        log_path = os.path.join(log_dir, log_filename)

        # Raccogli le differenze tra file
        log_entries = []
        
        for sha1 in sorted(common_sha1s):
            primary_names = sorted(primary_dict[sha1])
            comparison_names = sorted(comparison_dict[sha1])
            
            for p_name in primary_names:
                for c_name in comparison_names:
                    if p_name != c_name:
                        log_entries.append({
                            'primary': p_name,
                            'comparison': c_name,
                            'sha1': sha1
                        })

        # Ordina per nome software primario
        log_entries.sort(key=lambda x: x['primary'])

        # Raccogli i software rimossi
        removed_software = []
        for sha1 in unique_primary_sha1:
            for software_name in primary_dict[sha1]:
                removed_software.append({
                    'name': software_name,
                    'sha1': sha1
                })

        # Ordina i software rimossi per nome
        removed_software.sort(key=lambda x: x['name'])

        # Scrivi tutto nel log
        with open(log_path, 'w', encoding='utf-8') as log_file:
            # Scrivi le differenze tra file
            if log_entries:
                log_file.write("Corrispondenze con software diversi\n")
                log_file.write("-" * 40 + "\n")
                for entry in log_entries:
                    log_file.write(
                        f"{entry['primary']} > {entry['comparison']} (SHA1: {entry['sha1']})\n"
                    )
            
            # Scrivi i software rimossi
            if removed_software:
                if log_entries:
                    log_file.write("\n")
                
                log_file.write("Software rimossi\n")
                log_file.write("-" * 40 + "\n")
                for entry in removed_software:
                    log_file.write(f"{entry['name']} (SHA1: {entry['sha1']})\n")

        # Messaggio finale
        message = ""
        if log_entries:
            message += f"Totale corrispondenze: {len(log_entries)}\n"
        if removed_software:
            message += f"Totale software rimossi: {len(removed_software)}\n"
        
        if not message:
            messagebox.showinfo(
                "Nessuna differenza",
                "Tutti gli SHA1 comuni appartengono a software con lo stesso nome e non ci sono software rimossi."
            )
        else:
            messagebox.showinfo(
                "Operazione completata",
                f"Log salvato in: {log_filename}\n\n" + message.strip()
            )

    except Exception as e:
        messagebox.showerror("Errore", str(e))
        print(f"Errore dettagliato: {e}")

if __name__ == '__main__':
    main()