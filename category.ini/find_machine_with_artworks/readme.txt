MAME Artwork Necessary Extractor v1.0
=====================================

Questo script Python analizza un file XML di MAME ed estrae tutte le macchine che richiedono artwork,
creando un file INI formattato correttamente per l'utilizzo con frontend come MAMEUI o altri frontends.

Funzionalità:
-------------
- Interfaccia grafica per la selezione del file XML di MAME
- Analisi automatica delle macchine con attributo requiresartwork="yes"
- Creazione di un file INI con intestazione completa e formattazione corretta
- Estrazione automatica del numero di versione dal nome del file XML
- Generazione della data corrente nell'intestazione

Utilizzo:
---------
1. Eseguire lo script Python
2. Selezionare il file XML di MAME quando richiesto
3. Il file "artwork_necessary.ini" verrà creato nella stessa directory dello script

Formato output:
---------------
Il file generato avrà il seguente formato:
[FOLDER_SETTINGS]
RootFolderIcon mame
SubFolderIcon folder

;; ARTWORKNECESSARY.ini 0.xxx / DD-MMM-YY / MAME 0.xxx ;;
;; List of MAME machines that need Artwork ;;

[ROOT_FOLDER]
nome_macchina_1
nome_macchina_2
...

Requisiti:
----------
- Python 3.x
- Librerie standard di Python (xml, tkinter, os, sys, datetime, re)

Note:
-----
- Il file XML di MAME deve contenere i tag <machine> con <driver requiresartwork="yes"/>
- Lo script estrae automaticamente il numero di versione dal nome del file XML
- Il file di output viene sempre salvato come "artwork_necessary.ini"


MAME Artwork Necessary Extractor v1.0
=====================================

This Python script analyzes a MAME XML file and extracts all machines that require artwork,
creating a properly formatted INI file for use with frontends like MAMEUI or other frontends.

Features:
---------
- Graphical interface for selecting the MAME XML file
- Automatic analysis of machines with requiresartwork="yes" attribute
- Creation of INI file with complete header and proper formatting
- Automatic extraction of version number from XML filename
- Generation of current date in header

Usage:
------
1. Run the Python script
2. Select the MAME XML file when prompted
3. The "artwork_necessary.ini" file will be created in the same directory as the script

Output format:
--------------
The generated file will have the following format:
[FOLDER_SETTINGS]
RootFolderIcon mame
SubFolderIcon folder

;; ARTWORKNECESSARY.ini 0.xxx / DD-MMM-YY / MAME 0.xxx ;;
;; List of MAME machines that need Artwork ;;

[ROOT_FOLDER]
machine_name_1
machine_name_2
...

Requirements:
-------------
- Python 3.x
- Python standard libraries (xml, tkinter, os, sys, datetime, re)

Notes:
------
- The MAME XML file must contain <machine> tags with <driver requiresartwork="yes"/>
- The script automatically extracts the version number from the XML filename
- The output file is always saved as "artwork_necessary.ini"