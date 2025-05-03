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

    except ET.ParseError:
        pass  # Ignora file XML non validi
    except Exception:
        pass  # Ignora altri errori

    return sha1_map

def process_file_pair(primary_path, comparison_path, log_path):
    """Confronta due file XML e genera un log se ci sono differenze."""
    primary_dict = parse_xml(primary_path)
    comparison_dict = parse_xml(comparison_path)

    # Trova gli SHA1 comuni e quelli solo nel primario
    common_sha1s = set(primary_dict.keys()) & set(comparison_dict.keys())
    unique_primary_sha1 = set(primary_dict.keys()) - set(comparison_dict.keys())

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

    # Scrivi il log solo se ci sono differenze
    if log_entries or removed_software:
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
        
        return len(log_entries), len(removed_software)
    
    return 0, 0  # Nessuna differenza trovata

def main():
    # Configurazione interfaccia grafica
    root = tk.Tk()
    root.withdraw()

    try:
        # Selezione cartella primaria
        primary_dir = filedialog.askdirectory(title='Seleziona cartella primaria')
        if not primary_dir:
            print("Nessuna cartella primaria selezionata.")
            return

        # Selezione cartella di confronto
        comparison_dir = filedialog.askdirectory(title='Seleziona cartella di confronto')
        if not comparison_dir:
            print("Nessuna cartella di confronto selezionata.")
            return

        # Creazione della sottocartella LOGs
        logs_dir = os.path.join(comparison_dir, "LOGs")
        os.makedirs(logs_dir, exist_ok=True)

        # Trova tutti i file XML nella cartella primaria
        primary_files = [f for f in os.listdir(primary_dir) if f.lower().endswith('.xml')]
        if not primary_files:
            messagebox.showinfo("Nessun file", "Nessun file XML trovato nella cartella primaria.")
            return

        processed = 0
        created_logs = 0
        total_differences = 0
        total_removals = 0

        # Processa ogni file XML
        for filename in primary_files:
            primary_path = os.path.join(primary_dir, filename)
            comparison_path = os.path.join(comparison_dir, filename)
            
            # Salta se non esiste nella cartella di confronto
            if not os.path.exists(comparison_path):
                continue
            
            processed += 1
            log_filename = f"{os.path.splitext(filename)[0]}-sha1_comparison.log"
            log_path = os.path.join(logs_dir, log_filename)

            # Confronta i file
            diff_count, removal_count = process_file_pair(
                primary_path, comparison_path, log_path
            )

            if diff_count > 0 or removal_count > 0:
                created_logs += 1
                total_differences += diff_count
                total_removals += removal_count

        # Messaggio finale
        if created_logs > 0:
            message = (
                f"Elaborati {processed} file XML\n"
                f"Log creati: {created_logs}\n"
                f"Totale corrispondenze: {total_differences}\n"
                f"Totale software rimossi: {total_removals}\n\n"
                f"I log sono stati salvati in: {logs_dir}"
            )
            messagebox.showinfo("Operazione completata", message)
        else:
            messagebox.showinfo(
                "Nessuna differenza",
                "Nessuna differenza trovata in nessuno dei file elaborati."
            )

    except Exception as e:
        messagebox.showerror("Errore", str(e))

if __name__ == '__main__':
    main()