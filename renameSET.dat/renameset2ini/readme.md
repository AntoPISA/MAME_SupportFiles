renameSET2ini v1.0

Questo script converte un file renameSET.dat (prodotto da AntoPISA) in un file .ini strutturato,
utile per l'analisi o l'integrazione in altri strumenti.

Requisiti:
- Python 3.x
- Moduli standard: os, re, tkinter

Utilizzo:
1. Eseguire lo script renameset2ini.py.
2. Selezionare il file renameSET.dat tramite la finestra di dialogo.
3. Lo script generera' un file .ini nella stessa cartella, con lo stesso nome base.

Formato output:
- L'intestazione del file .dat viene convertita sostituendo '#' con ';;'.
- Ogni versione MAME (es. $0.281) diventa una sezione [0.281].
- Le statistiche vengono scritte come Stat_01, Stat_02, ..., Stat_72.
- I rename vengono elencati come Ren_001, Ren_002, ecc.
- Le rimozioni vengono elencate come Del_001, Del_002, ecc.

Note:
- Lo script gestisce correttamente versioni MAME con meno dati (non genera errori).
- Le righe vuote o non riconosciute vengono ignorate.
- Il formato dell'output e' conforme alle specifiche fornite dall'utente.

Autore: AntoPISA (ProgettoSNAPS)
Licenza: Uso personale / non commerciale

--------------------------------------------------------------------------------------------------

This script converts a renameSET.dat file (produced by AntoPISA) into a structured .ini file,
useful for analysis or integration into other tools.

Requirements:
- Python 3.x
- Standard modules: os, re, tkinter

Usage:
1. Run the renameset2ini.py script.
2. Select the renameSET.dat file via the dialog box.
3. The script will generate an .ini file in the same folder, with the same base name.

Output format:
- The header of the .dat file is converted by replacing '#' with ';;'.
- Each MAME version (e.g., $0.281) becomes a section [0.281].
- Statistics are written as Stat_01, Stat_02, ..., Stat_72.
- Renames are listed as Ren_001, Ren_002, etc.
- Removals are listed as Del_001, Del_002, etc.

Notes:
- The script correctly handles MAME versions with less data (does not generate errors).
- Empty or unrecognized lines are ignored.
- The output format complies with the specifications provided by the user.

Author: AntoPISA (ProgettoSNAPS)
License: Personal/non-commercial use

