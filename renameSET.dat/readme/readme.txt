MAME RENAMESET.DAT/INI 
======================
(C) progetto-SNAPS 2009/2024 AntoPISA

renameSET.dat:    0.270
Internal version:  5.37

The package contains:

- allMAMEremoved.txt      : List with all machines/BIOS/devices removed from MAME.
- allMAMErenamed.txt      : List with all machines/BIOS/devices renamed in MAME.
- allMAMEset.txt          : List with all the machines/BIOS/devices added to MAME from the first version; each machine has a unique progressive number (called mameID).
- renameSET.dat           : All data and counts relating to each published MAME, including renamed and deleted machines.
- renameSET.ini           : Like the previous file but in another format, which can be used with the "MAMErenSET" tool to automate updating operations of resources.
- renameSET_269-270.ini   : Like "renameSET.ini" but only includes the last two releases of the MAME.
- renameSET_SL.dat        : Like "renameSET.dat" but related to software lists.

====================================================================================================================================================================

How to read "renameSET.dat"

For each version of MAME released, are provided, in order:

Line 1 : Official version and [progressive numbering].

Line 2 : Release date (yyyy/mm/dd).

Line 3 : Summary of the various items (with any differences highlighted -/+):

         total items   - The total number of all elements that make up MAME: drivers, machines, devices and BIOSes;
         drivers       - Count of all drivers inherent to the machines;
         machines      - Count of all machines (Parents + Clones);
         parents       - Count of all "Parent" machines (including BIOS but excluding Devices);
         clones        - Count of all "Clones" machines (always excluding Devices);
         BIOSes        - Count of all "BIOSes";
         devices       - Count of all "Devices".
         requires CHDs - Count of machines and BIOS using CHDs;
         use Samples   - Count of machines using Samples.

Line 4:  The operating characteristics of machines supported (with any differences highlighted -/+):

         working           - Count of all "Working" machines;
         not working       - Count of "Non Working" machines;
         mechanicals       - Count of "Mechanical" machines;
         not mechanicals   - Count of non "Mechanical" machines;
         save supported    - Count of machines that support "SaveState";
         save unsupported  - Count of machines that do not support the "SaveState";
         horizontal screen - Count of machines that have a horizontal screen;
         vertical screen   - Count of machines that have a vertical screen.

Line 5:  Counting of all types of ROMs supported (with any differences highlighted -/+):

         total roms     - Count of all roms (including BIOSes and devices); subdivided into:
         machines roms   - Count of roms belonging to machines; 
         devices roms    - Count of roms belonging to the devices;
         BIOSes roms     - Count of roms belonging to the BIOSes;
         CHDs           - Count of all CHDs;
         sample files   - Count of all sample files;
         sample packs   - Count of "Sample" packages needed by MAME;
         good dumps     - Count all supported right ROMs;
         no dumps       - Count of roms not dumped yet;
         bad dumps      - Badly dumped roms count;
         bugs fixed     - Count of certified bugs fixed in a single release (all bugs can be found here: https://mametesters.org/).

Line 6 : Summary of the software lists and related software included:

software list    - Count of all lists present;
software         - Count of all registered software;
active SL        - Count of active lists only;
orphan SL        - Count of lists present but not currently supported;
active software  - Count of present and supported software; 
orphan software  - Count "orphan" list software;
software parents - Count of parents of lists;
software clones  - Count of clones of the lists.

Line 7: 

software roms      - Count of all roms in the lists;
software CHD       - Count of all CHDs in the lists;
supported software - Count bootable software;
partially supported software - Count of partially functioning software;
unsupported software - Count unbootable software;

Line 8 : List of renamed machines/devices/bioses.

         List of all machines or devices or bioses renamed between the new version and the previous one. Before the list of renamed or removed items there are summaries:

         total items renamed "ren" (machines/devices/bioses).

The format is as follows:
         
         OldName > NewName

Line 9 : List of removed machines/devices/bioses.

         List of all removed from MAME, between the new version and the previous one. Before the list of there are summaries:

total items removed "del" (machines/devices/bioses)


Home-page: https://www.progettosnaps.net/renameset/
Github   : https://github.com/AntoPISA/MAME_SupportFiles

(C) 2009/2024 AntoPISA