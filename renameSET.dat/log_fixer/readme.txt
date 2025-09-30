SCRIPT PER AGGIORNAMENTO AUTOMATICO DEI CONTEGGI MAME
-----------------------------------------------------

COSA FA QUESTO SCRIPT
---------------------
Questo script Python automatizza l'aggiornamento dei conteggi statistici nei file di log di MAME (o simili).
Legge ogni blocco del file, estrae i valori corretti dalla sezione "DAT           XML" (sia il valore base che la variazione, es. "(+5)"),
aggiorna le righe statistiche corrispondenti (es. "0 use joystick (+)" diventa "4.529 use joystick (+1)"),
formatta i numeri con il punto delle migliaia (es. 95751 diventa 95.751)
e infine PULISCE il file eliminando tutta la sezione "DAT           XML" e le righe vuote sopra di essa, lasciando solo "---" alla fine di ogni blocco.
Alla fine, il file risulterà pulito, aggiornato e pronto per l'uso.

COME USARE LO SCRIPT
--------------------
1. Assicurati di avere Python 3 installato sul tuo computer.
2. Salva questo script Python ("log_fixer.py") nella stessa cartella del file che vuoi modificare.
3. Esegui lo script con un doppio click o da riga di comando:
      python log_fixer.py
4. Si aprirà una finestra di dialogo: seleziona il file da aggiornare (qualsiasi estensione esso abbia).
5. Lo script genererà un NUOVO file con lo stesso nome, seguito da ".updated" (es. "miofile.updated.txt").
6. Il file originale NON verrà modificato.

NOTA BENE
---------
- Lo script cerca corrispondenze esatte delle descrizioni (es. "use joystick", "one player").
- Aggiorna SOLO le righe statistiche che contengono la chiave trovata nel DAT/XML.
- Rimuove completamente la sezione DAT/XML e le righe vuote precedenti, sostituendole con un semplice "---".
- Formatta automaticamente tutti i numeri >= 1000 con il punto (es. 1.510, 95.751).

SVILUPPATO PER SODDISFARE REQUISITI SPECIFICI DI REPORTISTICA MAME.
Ultimo aggiornamento: 9 settembre 2025

I file da importare devono essere formattati così (esempio):

---
0.115u3 - 30/05/2007 (v2.43 28/08/2025 14:04)
6.675 total items, 920 drivers (+1), 6.641 machines (+6), 3.582 parents (+1), 3.059 clones (+5), 34 BIOSes, 0 devices, 212 requires CHDs, 123 use samples, 3.925 audio mono (+8), 2.394 audio stereo (+2), 12 audio multichannel, 310 no audio (-4)
5.811 working (+6), 830 not working, 0 mechanicals, 6.641 not mechanicals (+6), 913 save supported (+7), 5.728 save unsupported (-1)
4.804 horizontal screen (+1), 1.837 vertical screen (+5), 6.561 raster graphics (+6), 80 vector graphics, 0 lcd graphics, 0 svg graphics, 0 screenless, 0 one player (+), 0 two players (+), 0 three players (+), 0 more than three players (+)
0 use stick (+), 0 use gambling, 0 use joystick (+), 0 use keyboard, 0 use keypad, 0 use lightgun (+), 0 use mahjong, 0 use mouse, 0 use buttons only, 0 use paddle (+), 0 use pedal, 0 use positional, 0 use dial (+), 0 use trackball (+), 0 use hanafuda
99.170 total roms (+82), 99.069 machines roms (+82), 0 devices roms, 101 BIOSes roms, 222 CHDs, 403 sample files, 35 sample packs, 97.887 good dumps (+82), 1.073 no dumps, 432 bad dumps, 1 bug fixed

           DAT           XML
  >        n/d vs      1.065 one player ERROR
  >        n/d vs      4.802 two players ERROR
  >        n/d vs       (+6) two players DIFF. ERROR
  >        n/d vs        123 three players ERROR
  >        n/d vs        535 more than three players ERROR
  >        n/d vs        276 use stick ERROR
  >        n/d vs        136 use lightgun ERROR
  >        n/d vs        237 use paddle ERROR
  >        n/d vs        265 use pedal ERROR
  >        n/d vs        339 use dial ERROR
  >        n/d vs        184 use trackball ERROR
---