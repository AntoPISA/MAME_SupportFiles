MESSINFO Resources & ROMSET Updater 1.0
=======================================

Descrizione in italiano:
------------------------

Questo script Python permette di aggiornare automaticamente il file messinfo.dat utilizzato nel progetto progettosnaps.net.

Lo script opera in due fasi principali:

Fase 1: Aggiornamento Risorse
- Analizza le cartelle delle risorse (snap, titles, icons, cabinets, ecc.) indicate nel file config.ini.
- Per ogni macchina presente nel file dat (identificata da $info=nomebreve), verifica la presenza dei file corrispondenti.
- Aggiorna la sezione "RESOURCES:" con l'elenco delle risorse disponibili, nel seguente ordine:
  Snap, Title, Icon, machine picture (in "Cabinet" collection), Control Panel, Flyer, pdf Manual, Marquee, PCB, Artwork Preview.
- Il testo viene formattato correttamente con "and" prima dell'ultima voce e un punto finale.
- I valori esistenti vengono sostituiti.

Fase 2: Aggiornamento Pacchetti ROM
- Analizza i file .zip contenuti nella cartella "roms" indicata nel config.ini.
- Per ogni macchina, calcola:
  - Dimensione totale in bytes dei file contenuti
  - Numero di file nello zip
  - Dimensione compressa (packed) in Kb o Mb
- Aggiorna la sezione "ROMSET:" con queste informazioni nel formato:
  XXXX bytes in N file(s) / X.XXKb or X.XXMb packed
- Lo script permette due opzioni:
  a. Aggiornamento completo: aggiorna tutti i set di ROM, anche se già presenti.
  b. Aggiunta informazioni mancanti: aggiorna solo le voci senza dati.

Modalita' di esecuzione:
- All'avvio, lo script chiede di selezionare il file messinfo.dat.
- Successivamente, mostra un menu per scegliere:
  - Eseguire solo la Fase 1
  - Eseguire solo la Fase 2
  - Eseguire prima la Fase 1 e poi la Fase 2
- Durante l'elaborazione, viene mostrata una finestra con barra di avanzamento e log dettagliato.

Requisiti:
- Python 3.6 o superiore
- File config.ini nella stessa cartella dello script, con i percorsi corretti

Come usare:
1. Preparare il file config.ini con tutti i percorsi delle cartelle.
2. Eseguire lo script.
3. Selezionare il file messinfo.dat.
4. Scegliere l'opzione desiderata.
5. Attendere il completamento.

--------------------------------------

Description in English:
------------------------

This Python script automatically updates the messinfo.dat file used in the progettosnaps.net project.

The script works in two main phases:

Phase 1: Resources Update
- Analyzes resource folders (snap, titles, icons, cabinets, etc.) specified in the config.ini file.
- For each machine in the dat file (identified by $info=shortname), checks for the presence of corresponding files.
- Updates the "RESOURCES:" section with a list of available resources, in this order:
  Snap, Title, Icon, machine picture (in "Cabinet" collection), Control Panel, Flyer, pdf Manual, Marquee, PCB, Artwork Preview.
- The text is correctly formatted with "and" before the last item and a final period.
- Existing values are replaced.

Phase 2: ROM Set Update
- Analyzes .zip files in the "roms" folder specified in config.ini.
- For each machine, calculates:
  - Total unpacked size in bytes
  - Number of files in the zip
  - Packed size in Kb or Mb
- Updates the "ROMSET:" section with this data in the format:
  XXXX bytes in N file(s) / X.XXKb or X.XXMb packed
- The script offers two options:
  a. Full update: updates all ROM sets, even if already present.
  b. Add missing info: updates only entries without data.

Execution modes:
- At startup, the script asks to select the messinfo.dat file.
- Then, it shows a menu to choose:
  - Run only Phase 1
  - Run only Phase 2
  - Run Phase 1 then Phase 2
- During processing, a window shows progress bar and detailed log.

Requirements:
- Python 3.6 or higher
- config.ini file in the same folder as the script, with correct paths

How to use:
1. Prepare the config.ini file with all folder paths.
2. Run the script.
3. Select the messinfo.dat file.
4. Choose the desired option.
5. Wait for completion.