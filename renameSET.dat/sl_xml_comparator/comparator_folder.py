import xml.etree.ElementTree as ET
from collections import defaultdict
import tkinter as tk
from tkinter import filedialog, messagebox
import os

    # (C) AntoPISA www.progettosnaps.net v1.01

def parse_xml(file_path):
    """Analizza un file XML e mappa gli SHA1 ai nomi dei software."""
    sha1_map = defaultdict(set)
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        for software in root.findall('software'):
            software_name = software.get('name')
            if not software_name:
                continue

            for part in software.findall('part'):
                for dataarea in part.findall('dataarea'):
                    for rom in dataarea.findall('rom'):
                        sha1 = rom.get('sha1', '').strip().lower()
                        if sha1 and len(sha1) == 40 and all(c in '0123456789abcdef' for c in sha1):
                            sha1_map[sha1].add(software_name)
    except ET.ParseError:
        pass  # Ignora file XML non validi
    return sha1_map

def process_file_pair(primary_path, comparison_path, log_path, filename_base):
    """Confronta due file XML e genera un log se ci sono differenze nel formato richiesto."""
    primary_dict = parse_xml(primary_path)
    comparison_dict = parse_xml(comparison_path)

    # Trova gli SHA1 comuni con software diversi
    common_sha1s = set(primary_dict.keys()) & set(comparison_dict.keys())
    # Trova gli SHA1 unici nel primario (software rimossi)
    unique_primary_sha1 = set(primary_dict.keys()) - set(comparison_dict.keys())
    
    log_entries = []
    
    # Aggiungi le differenze tra file
    for sha1 in sorted(common_sha1s):
        primary_names = sorted(primary_dict[sha1])
        comparison_names = sorted(comparison_dict[sha1])
        
        for p_name in primary_names:
            for c_name in comparison_names:
                if p_name != c_name:
                    log_entries.append({
                        'type': 'diff',
                        'primary': p_name,
                        'comparison': c_name,
                        'sha1': sha1
                    })
    
    # Aggiungi i software rimossi
    for sha1 in sorted(unique_primary_sha1):
        for software_name in primary_dict[sha1]:
            log_entries.append({
                'type': 'removed',
                'primary': software_name,
                'comparison': '',  # Non utilizzato ma necessario per struttura
                'sha1': sha1
            })

    # Ordina per nome software primario
    log_entries.sort(key=lambda x: x['primary'])

    # Scrivi il log solo se ci sono differenze
    if log_entries:
        with open(log_path, 'w', encoding='utf-8') as log_file:
            # Prepara il nome della lista (filename senza estensione)
            list_name = filename_base[:24].ljust(24)  # Colonne 1-24
            
            for entry in log_entries:
                # Colonna 25: "|", Colonna 26: spazio
                # Colonne 27-44: Software primario (max 18 caratteri)
                primary = entry['primary'][:18].ljust(18)
                
                if entry['type'] == 'diff':
                    # Colonna 45: ">", Colonna 46: spazio
                    # Colonne 47-64: Software di confronto (max 18 caratteri)
                    comparison = entry['comparison'][:18].ljust(18)
                else:
                    # Software rimosso: mostra "REMOVED" nella colonna 47-64
                    comparison = 'REMOVED'.ljust(18)
                
                # Crea la riga formattata
                line = f"{list_name}| {primary}> {comparison} SHA1: {entry['sha1']}"
                # Garantisce che il formato sia corretto con slicing
                line = (
                    line[:24] + "| " + 
                    line[24+2:24+2+18] + "> " + 
                    line[24+2+18+2:24+2+18+2+18] + 
                    " SHA1: " + entry['sha1']
                )
                log_file.write(line + '\n')
        
        # Conta i tipi di differenza
        diff_count = sum(1 for e in log_entries if e['type'] == 'diff')
        removed_count = sum(1 for e in log_entries if e['type'] == 'removed')
        return diff_count, removed_count
    
    return 0, 0  # Nessuna differenza trovata

def merge_logs(logs_dir, comparison_dir):
    """Unisce tutti i log nella cartella LOGs in un unico file."""
    log_files = [f for f in os.listdir(logs_dir) if f.lower().endswith('.log')]
    
    if not log_files:
        return 0
    
    # Crea il nome del file combinato
    comparison_name = os.path.basename(os.path.normpath(comparison_dir))
    merged_log = os.path.join(logs_dir, f"{comparison_name}_sha1_comparison.log")
    
    # Unisce i file
    with open(merged_log, 'w', encoding='utf-8') as outfile:
        for filename in sorted(log_files):
            if filename == os.path.basename(merged_log):
                continue  # Salta il file combinato se esiste già
                
            file_path = os.path.join(logs_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as infile:
                outfile.write(f"--- Inizio log: {filename} ---\n")
                outfile.write(infile.read())
                outfile.write(f"\n--- Fine log: {filename} ---\n\n")
    
    return len(log_files)

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
            filename_base = os.path.splitext(filename)[0]
            log_filename = f"{filename_base}-sha1_comparison.log"
            log_path = os.path.join(logs_dir, log_filename)

            # Confronta i file
            result = process_file_pair(
                primary_path, comparison_path, log_path, filename_base
            )
            
            if result[0] + result[1] > 0:
                created_logs += 1
                total_differences += result[0]
                total_removals += result[1]

        # Chiedi se unire i log
        merge = False
        if created_logs > 0:
            merge = messagebox.askyesno(
                "Unisci log",
                "Vuoi unire tutti i file generati in un unico file log?\n"
                "YES = Unisci - NO = Termina senza unire"
            )

        # Messaggio finale
        if created_logs > 0:
            message = (
                f"Elaborati {processed} file XML\n"
                f"Log creati: {created_logs}\n"
                f"Totale corrispondenze: {total_differences}\n"
                f"Totale software rimossi: {total_removals}\n\n"
                f"I log sono stati salvati in: {logs_dir}"
            )
            
            if merge:
                merged_count = merge_logs(logs_dir, comparison_dir)
                message += f"\n\nFile log unificato creato: {os.path.basename(os.path.normpath(comparison_dir))}_sha1_comparison.log"
                message += f"\nLog uniti: {merged_count}"
                
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