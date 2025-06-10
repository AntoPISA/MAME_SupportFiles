README - renameSET2cvs v1.05
============================
Questo script converte i dati presenti nel file "renameSET.dat" in un formato CSV apribile con Excel, con i campi separati da punto e virgola (;).

---

COSA FA QUESTO SCRIPT:
-------------------------
Estrae i dati numerici dal file renameSET.dat (es. 48.166 total items)
Rimuove le differenze tra parentesi (es. (+14), (-3/+68))
Elimina i punti nei numeri (es. 356.566 → 356566) per renderli compatibili con Excel
Converte la data nel formato italiano (aaaa/mm/gg → gg/mm/aaaa)
Gestisce correttamente i campi simili (es. "software", "active software", ecc.)
Crea un file .csv con tutti i valori nell'ordine richiesto

---

FORMATO DEL FILE DI OUTPUT:
-----------------------------
Il file .csv risultante contiene tutti i seguenti campi nell'ordine specifico:

versione;versione progressiva;data;total items;drivers;machines;parents;clones;BIOSes;devices;requires CHDs;use samples;audio mono;audio stereo;audio multichannel;no audio;working;not working;mechanicals;not mechanicals;save supported;save unsupported;horizontal screen;vertical screen;raster graphics;vector graphics;lcd graphics;svg graphics;screenless;total roms;machines roms;devices roms;BIOSes roms;CHDs;sample files;sample packs;good dumps;no dumps;bad dumps;bugs fixed;software list;software;active SL;orphan SL;active software;orphan software;software parents;software clones;software roms;software CHD;supported software;partially supported software;unsupported software

---

COME USARE LO SCRIPT:
------------------------
1. Posiziona il file renameSET.dat nella stessa cartella dello script.
2. Avvia lo script con Python:
   python rS2cvs.py
3. Seleziona il file renameSET.dat usando la finestra di dialogo.
4. Il programma genera automaticamente un file .csv con lo stesso nome del file .dat.

---

REQUISITI:
-------------
- Python 3.x
- Librerie installate: nessuna esterna necessaria (usa solo librerie standard)

---

LICENZA:
-----------
Questo script e' fornito "cosi come'", senza garanzie esplicite o implicite.  
Puoi modificarlo e utilizzarlo liberamente.

---

README - renameSET2cvs v1.05
============================
This script converts data from the "renameSET.dat" file into a CSV format compatible with Excel, using semicolons (;) as field separators.

---

WHAT THIS SCRIPT DOES:
-------------------------
Extracts numeric values from "renameSET.dat" (e.g., 48.166 total items)
Removes differences in parentheses (e.g., (+14), (-3/+68))
Strips dots from numbers (e.g., 356.566 → 356566) for Excel compatibility
Converts date to Italian format (yyyy/mm/dd → dd/mm/yyyy)
Correctly handles similar fields (e.g., "software", "active software", etc.)
Generates a .csv file with all values in the correct order

---

OUTPUT FILE FORMAT:
----------------------
The resulting .csv file contains all the following fields in the exact order:

versione;versione progressiva;data;total items;drivers;machines;parents;clones;BIOSes;devices;requires CHDs;use samples;audio mono;audio stereo;audio multichannel;no audio;working;not working;mechanicals;not mechanicals;save supported;save unsupported;horizontal screen;vertical screen;raster graphics;vector graphics;lcd graphics;svg graphics;screenless;total roms;machines roms;devices roms;BIOSes roms;CHDs;sample files;sample packs;good dumps;no dumps;bad dumps;bugs fixed;software list;software;active SL;orphan SL;active software;orphan software;software parents;software clones;software roms;software CHD;supported software;partially supported software;unsupported software

---

HOW TO USE:
---------------
1. Place your renameSET.dat file in the same folder as the script.
2. Run the script using Python:
   python rS2cvs.py
3. Select the renameSET.dat file via the file dialog.
4. The program will automatically generate a .csv file with the same name.

---

REQUIREMENTS:
----------------
- Python 3.x
- No external libraries required (uses only built-in modules)

---

LICENSE:
------------
This script is provided "as is", without warranty of any kind.
You can freely modify and use it.