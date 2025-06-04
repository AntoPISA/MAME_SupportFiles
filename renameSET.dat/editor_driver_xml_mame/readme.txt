MAME XML Driver Fix v1.0
========================
Antonio Paradossi

### Descrizione:
Questo strumento permette di aggiornare automaticamente i valori dei tag <driver> all'interno dei file XML di MAME, selezionando un range numerico progressivo (es. mame_045_8.1.xml) e un gioco/macchina specifica.

### Funzionalità principali:
- Modifica batch dei campi: status, emulation, color, sound, graphic, savestate
- Backup automatico dei file originali nella cartella "backup"
- Log delle modifiche effettuate
- Interfaccia grafica semplice e intuitiva
- Richiede solo Python 3.x + librerie base (tkinter, xml, PIL)

### Requisiti minimi:
- Sistema operativo: Windows / Linux / macOS
- Python 3.x installato
- Librerie richieste:
  - tkinter (incluso in Python)
  - Pillow
  - lxml (opzionale ma consigliato)

### Come usarlo:
1. Avvia lo script con:
2. Seleziona la cartella contenente i file XML
3. Inserisci:
- Nome breve del gioco/macchina
- Da quale numero file iniziare
- Fino a quale numero proseguire
- Nuovi valori per il driver
4. Premi [Correggi Status] per applicare le modifiche

### Note importanti:
- Il programma cerca i file nel formato `mame_XXX_VERSION.xml`, dove `XXX` è un numero progressivo (es. mame_045_0.21.xml)
- I backup vengono creati prima di ogni modifica
- Il log delle modifiche viene salvato in `backup/log_modifiche.txt`

### Licenza:
MIT License – libero uso e distribuzione, purché si mantenga questa nota.

---

MAME XML Driver Fix v1.0
========================
Antonio Paradossi


### Description:
This tool allows you to automatically update the <driver> tags inside MAME XML files by selecting a numeric range (e.g., mame_045_8.1.xml) and a specific game/machine.

### Main Features:
- Batch edit fields: status, emulation, color, sound, graphic, savestate
- Automatic backup of original files into the "backup" folder
- Modification log
- Simple and intuitive GUI
- Requires only Python 3.x + basic libraries (tkinter, xml, PIL)

### Minimum Requirements:
- Operating System: Windows / Linux / macOS
- Python 3.x installed
- Required libraries:
  - tkinter (included in Python)
  - Pillow
  - lxml (optional but recommended)

### How to Use:
1. Run the script with:
2. Select the folder containing your XML files
3. Enter:
- Short name of the game/machine
- Starting file number
- Ending file number
- New values for the driver
4. Click [Correggi Status] to apply changes

### Important Notes:
- The program looks for files in the format `mame_XXX_VERSION.xml` (e.g., mame_045_0.21.xml)
- Backups are created before any change
- A log is saved in `backup/log_modifiche.txt`

### License:
MIT License – free to use and distribute, as long as this notice is included.
