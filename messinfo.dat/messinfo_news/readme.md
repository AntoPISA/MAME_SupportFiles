========================================
               README - MESSINFO NEW ITEMS
========================================

ITALIANO

Questo script Python genera automaticamente file di testo formattati per nuovi elementi aggiunti a MAME (device, macchine, driver) a partire da un foglio Excel (.xlsx).

Funzionalita principali:
- Carica un file Excel contenente i dati dei nuovi elementi.
- Genera un file di testo con struttura predefinita.
- Salva il file .txt nella stessa cartella del file Excel, con lo stesso nome.

Opzioni disponibili:
1. Nuovi Device: crea il file per nuovi device.
2. Nuove Macchine: crea il file per nuove macchine.
3. Nuovi Driver: crea il file per nuovi driver.

Formato richiesto del file Excel:
- La prima riga deve contenere le intestazioni delle colonne.
- Le colonne devono corrispondere ai nomi richiesti per ogni opzione.

Colonne richieste:
- Opzione 1 (Device): new_device, numero, riga, completo
- Opzione 2 (Macchine): new_machine, numero, riga, completo
- Opzione 3 (Driver): new_driver, versione, completo

I dati nelle celle verranno inseriti nei rispettivi campi del file di testo.
Ogni blocco termina con una riga vuota seguita da "$end".

Istruzioni per l'uso:
1. Assicurati di avere Python installato (versione 3.6 o superiore).
2. Installa le librerie necessarie:
   pip install openpyxl tkinter
3. Esegui lo script: python nome_script.py
4. Scegli l'opzione desiderata dal menu.
5. Seleziona il file Excel quando richiesto.
6. Il file .txt verra creato automaticamente.

Nota: lo script non si chiude dopo l'uso. Puoi elaborare piu file consecutivamente. Usa il pulsante "Exit" per uscire.

----------------------------------------

ENGLISH

This Python script automatically generates formatted text files for new MAME elements (devices, machines, drivers) from an Excel spreadsheet (.xlsx).

Main features:
- Loads an Excel file containing data about new elements.
- Generates a text file with a predefined structure.
- Saves the .txt file in the same folder as the Excel file, using the same name.

Available options:
1. New Devices: creates output for new devices.
2. New Machines: creates output for new machines.
3. New Drivers: creates output for new drivers.

Required Excel file format:
- The first row must contain column headers.
- Column names must match the expected ones for each option.

Required columns:
- Option 1 (Devices): new_device, numero, riga, completo
- Option 2 (Machines): new_machine, numero, riga, completo
- Option 3 (Drivers): new_driver, versione, completo

Cell data will be inserted into the corresponding fields in the text file.
Each block ends with a blank line followed by "$end".

Usage instructions:
1. Make sure Python is installed (version 3.6 or higher).
2. Install required libraries:
   pip install openpyxl tkinter
3. Run the script: python script_name.py
4. Choose the desired option from the menu.
5. Select the Excel file when prompted.
6. The .txt file will be created automatically.

Note: the script remains open after each operation. You can process multiple files in sequence. Use the "Exit" button to close the program.