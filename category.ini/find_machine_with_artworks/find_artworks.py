import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog
import os
import sys
from datetime import datetime
import re

def main():
    # Crea una finestra Tkinter nascosta per la dialog di selezione file
    root = tk.Tk()
    root.withdraw()
    
    # Apri la finestra di dialogo per selezionare il file XML
    file_path = filedialog.askopenfilename(
        title="Seleziona il file XML di MAME",
        filetypes=[("XML files", "*.xml"), ("All files", "*.*")]
    )
    
    # Se nessun file è stato selezionato, esci
    if not file_path:
        print("Nessun file selezionato. Uscita dal programma.")
        return
    
    try:
        # Analizza il file XML
        print("Analisi del file XML in corso...")
        tree = ET.parse(file_path)
        root_xml = tree.getroot()
        
        # Trova tutte le macchine con requiresartwork="yes" nel tag driver
        machines_with_artwork = []
        
        # Cerca i tag <machine> e controlla il tag <driver> al loro interno
        for machine in root_xml.findall('machine'):
            # Cerca il tag <driver> all'interno di <machine>
            driver = machine.find('driver')
            if driver is not None and driver.get('requiresartwork') == 'yes':
                machine_name = machine.get('name', 'Nome non disponibile')
                machines_with_artwork.append(machine_name)
        
        # Conta le macchine trovate
        count = len(machines_with_artwork)
        
        # Estrai il numero di versione dal nome del file
        # Cerca un pattern come "mame_717_0.278.xml" o "mame0.278.xml" o "mame_278.xml"
        filename = os.path.basename(file_path)
        version = "xxx"  # valore di default
        
        # Pattern per cercare numeri dopo il punto o underscore
        patterns = [
            r'[_\.]0\.(\d{3})',  # cerca _0.278 o .0.278
            r'[_\.](\d{3})[^\.]*$',  # cerca _278 alla fine
            r'(\d{3})'  # cerca qualsiasi sequenza di 3 cifre
        ]
        
        for pattern in patterns:
            match = re.search(pattern, filename)
            if match:
                version = match.group(1)
                break
        
        # Prepara il contenuto del file ini con l'intestazione richiesta
        # Ottieni la data corrente per l'intestazione
        current_date = datetime.now().strftime("%d-%b-%y")
        
        output_content = """[FOLDER_SETTINGS]
RootFolderIcon mame
SubFolderIcon folder

;; ARTWORKNECESSARY.ini 0.{} / {} / MAME 0.{} ;;
;; List of MAME machines that need Artwork ;;

[ROOT_FOLDER]
""".format(version, current_date, version)
        
        # Aggiungi i nomi delle macchine, uno per riga
        output_content += '\n'.join(machines_with_artwork)
        
        # Determina il nome del file ini (sempre artwork_necessary.ini)
        directory = os.path.dirname(os.path.abspath(sys.argv[0]))  # Directory dello script
        output_filename = "artwork_necessary.ini"
        output_path = os.path.join(directory, output_filename)
        
        # Scrivi il file ini
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output_content)
        
        # Mostra i risultati
        print(f"\nAnalisi completata!")
        print(f"Numero di macchine trovate: {count}")
        print(f"Versione MAME rilevata: {version}")
        print(f"File ini creato: {output_path}")
        print("(File formattato come ini con intestazione)")
        
        # Mostra le prime 10 macchine come esempio
        if machines_with_artwork:
            print(f"\nPrime 10 macchine trovate:")
            for i, machine in enumerate(machines_with_artwork[:10], 1):
                print(f"  {machine}")
            if count > 10:
                print(f"  ... e altre {count - 10} macchine")
        
    except ET.ParseError as e:
        print(f"Errore durante l'analisi del file XML: {e}")
    except FileNotFoundError:
        print(f"File non trovato: {file_path}")
    except Exception as e:
        print(f"Si è verificato un errore: {e}")
        import traceback
        traceback.print_exc()
    
    # Mantieni la finestra aperta (opzionale)
    input("\nPremi INVIO per chiudere...")

if __name__ == "__main__":
    main()