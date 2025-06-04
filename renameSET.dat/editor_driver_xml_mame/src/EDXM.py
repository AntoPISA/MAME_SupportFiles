import os
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog

def select_folder():
    """Apre una finestra per selezionare la cartella"""
    root = tk.Tk()
    root.withdraw()  # Nasconde la finestra principale
    folder_selected = filedialog.askdirectory(title="Seleziona la cartella con i file XML")
    return folder_selected

def extract_number(filename):
    """Estrae il numero dal nome del file (es. '010.xml' → 10)"""
    try:
        return int(os.path.splitext(filename)[0])
    except ValueError:
        return None

def main():
    print("=== Correzione driver status in file XML ===")

    # 1. Selezione della cartella
    folder_path = select_folder()
    if not folder_path:
        print("Nessuna cartella selezionata.")
        return

    # 2. Acquisizione delle risposte dall'utente
    game_name = input("1. Game/Macchina da correggere? ").strip()

    from_version = input("2. Da quale numero file? (es. 10) ").strip()
    to_version = input("3. Fino a quale numero file? (es. 15) ").strip()

    try:
        from_num = int(from_version)
        to_num = int(to_version)
    except ValueError:
        print("Errore: I valori per il range devono essere numeri interi.")
        return

    print("\nInserisci i valori per il tag <driver>:")
    status = input("4. status (good/imperfect/preliminary): ").strip().lower()
    emulation = input("5. emulation (good/preliminary): ").strip().lower()
    color = input("6. color (good/imperfect/preliminary): ").strip().lower()
    sound = input("7. sound (good/imperfect/preliminary): ").strip().lower()
    graphic = input("8. graphic (good/imperfect/preliminary): ").strip().lower()
    savestate = input("9. savestate (unsupported/supported): ").strip().lower()

    # Costruisce l'attributo completo del tag driver SENZA fromversion e toversion
    driver_attrib = {
        'status': status,
        'emulation': emulation,
        'color': color,
        'sound': sound,
        'graphic': graphic,
        'savestate': savestate
    }

    # Scandisce tutti i file .xml nella cartella
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.xml'):
            file_number = extract_number(filename)

            # Salta i file non numerici o fuori dal range
            if file_number is None or not (from_num <= file_number <= to_num):
                continue

            file_path = os.path.join(folder_path, filename)

            try:
                tree = ET.parse(file_path)
                root = tree.getroot()

                modified = False

                # Cerca sia <game> che <machine> con il nome specificato
                elements_to_check = []
                elements_to_check.extend(root.findall(f'.//game[@name="{game_name}"]'))
                elements_to_check.extend(root.findall(f'.//machine[@name="{game_name}"]'))

                for element in elements_to_check:
                    # Cerca un eventuale tag <driver>
                    driver = element.find('driver')

                    if driver is not None:
                        # Aggiorna gli attributi esistenti
                        driver.attrib.update(driver_attrib)
                    else:
                        # Crea un nuovo elemento driver se non esiste
                        driver = ET.SubElement(element, 'driver', driver_attrib)

                    modified = True

                if modified:
                    # Sovrascrive il file XML
                    tree.write(file_path, encoding='utf-8', xml_declaration=True)
                    print(f"Modificato: {filename}")
                else:
                    print(f"Nessuna modifica effettuata su: {filename}")

            except ET.ParseError as pe:
                print(f"Errore nel parsing del file {filename}: {pe}")
            except Exception as e:
                print(f"Errore durante l'elaborazione di {filename}: {e}")

    print("\nOperazione completata.")

if __name__ == "__main__":
    main()