CHDman_GUI v1.0 - User Instructions

============================================================================

PURPOSE OF THE TOOL

CHDman_GUI is a graphical user interface designed to simplify the use of the chdman command-line utility
included with MAME (Multiple Arcade Machine Emulator). The tool provides an intuitive way to  manage CHD
(Compressed Hunks of Data) files without requiring command-line knowledge.

Key capabilities:
- Generate Info reports containing metadata for all CHD files in a directory tree
- Verify integrity of existing CHD files
- Convert raw disk images or CD images to CHD format
- Extract CHD files back to raw or CD format
- Create new blank CHD hard disk images

============================================================================

DETAILED INSTRUCTIONS

INITIAL SETUP

1.1 First Launch
    Place chdmangui.py and config.ini in the same directory
    Ensure Python 3.8 or higher is installed 
    Run: python chdmangui.py

1.2 Configure Paths
    chdman.exe: Browse to your MAME chdman executable (e.g., C:\MAME\chdman.exe)
    Output: Select the folder where CHD-Info reports will be saved
    Input: Select the folder containing CHD files to process (can be set per session)

1.3 Save Configuration
    Click "Save Config" to store paths and settings in config.ini
    Settings persist across sessions for faster workflow


SELECTING AN OPERATION
Available operations from the dropdown menu:

2.1 Info (Information)
    Extracts and displays metadata from CHD files
    Output includes: File Version, Logical size, Hunk Size, Compression, SHA1 hashes, geometry data
    Most commonly used operation for generating CHD-Info.txt reports

2.2 Verify (Integrity Check)
    Checks CHD files for corruption or errors
    Reports pass/fail status for each file
    Does not generate detailed metadata output

2.3 From CD (CD -> CHD)
    Converts CUE/BIN CD images to CHD format
    Requires input file selection (not folder)
    Output saved to configured Output directory

2.4 From Raw (Raw -> CHD)
    Converts raw disk images (.img, .bin) to CHD format
    Requires CHS geometry parameters (Cylinders, Heads, Sectors)
    Output saved to configured Output directory

2.5 Extract Raw (CHD -> Raw)
    Extracts CHD content back to raw disk image format
    Output saved to configured Output directory

2.6 Extract CD (CHD -> CD)
    Extracts CHD content back to CUE/BIN CD image format
    Output saved to configured Output directory

2.7 Create HD (Create Disk)
    Creates a new blank CHD hard disk image
    Requires CHS geometry and compression settings
    Output saved to configured Output directory


PROCESSING OPTIONS

3.1 CHS Parameters
    Format: Cylinders, Heads, Sectors (e.g., 615,4,17)
    Required for: createhd, fromraw operations
    Default value loaded from config.ini

3.2 Compression Settings
    none: No compression (required for writable CHDs in MAME)
    zlib: Fast compression using Deflate algorithm
    lzma: High compression using LZMA algorithm
    huff: Huffman compression for specific use cases
    Default: none (loaded from config.ini)

3.3 Recursive Processing
    Checkbox: "Include subfolders (alphabetical)"
    When enabled: Processes all .chd files in selected folder and subfolders
    Files and folders processed in alphabetical order
    Empty folders logged as "CHD not dumped" entries in correct alphabetical position


EXECUTING OPERATIONS

4.1 Start Processing
    Select operation from dropdown
    Set Input path (file or folder)
    Click "Execute" button
    Progress bar shows completion percentage
    Log window displays real-time status

4.2 Stop Processing
    Click "Stop" button during execution to halt processing
    Current file completes, then operation terminates
    Progress bar and button states update accordingly

4.3 Monitor Progress
    Log window shows: files processed, successes, warnings, errors
    Color-coded messages: green (success), yellow (warning), red (error)
    Scrollable log with syntax highlighting for readability


SAVING OUTPUT

5.1 Save Log (CHD-Info Report)
    Click "Save Log" button after processing completes
    Enter version number when prompted (e.g., 286 for MAME 0.286)
    File automatically saved as: CHD-Info_[version].txt in Output directory
    No file dialog for location - uses configured Output path

5.2 Output Format
    Header section with tool information and version

5.3 Clear Log
    Click "Clear Log" to reset the log window before new operations
    Recommended for long batch processes to maintain readability


CONFIGURATION FILE (config.ini)

6.1 Structure
    [paths]
    chdman = C:\MAME\chdman.exe
    output = C:\MAME\chd_output
    input = C:\MAME\chd_collection
    [settings]
    chs = 615,4,17
    compression = none

6.2 Manual Editing
    File can be edited with any text editor
    Changes take effect on next application launch
    Use UTF-8 encoding to avoid character issues

6.3 Automatic Updates
    Paths updated via GUI are saved automatically
    Settings changed in interface persist across sessions


TROUBLESHOOTING

7.1 Common Issues
    chdman.exe not found: Verify path in config or use Browse button
    No files processed: Check Input path and recursive checkbox
    Permission errors: Run as administrator or check folder permissions
    Encoding issues: Ensure config.ini saved as UTF-8

7.2 Error Messages
    Log window shows detailed error information
    Check chdman.exe version compatibility with CHD files
    Verify input files are valid CHD, CUE, or raw images

7.3 Performance Tips
    Large directories: Allow time for recursive scanning
    Network drives: May experience slower processing
    Memory usage: Log window limits history for efficiency


FILE NAMING CONVENTIONS

8.1 Output Files
    CHD-Info_[version].txt: Main report file
    config.ini: Application settings
    chdmangui.py: Main application script

8.2 Input Files
    .chd: Compressed Hunks of Data files (MAME format)
    .cue/.bin: CD image files for conversion
    .img/.raw: Raw disk images for conversion


INTEGRATION NOTES

9.1 Compatibility
    Output format matches CHD-Info standard from progettosnaps.net
    Suitable for use with other CHD management tools
    Timestamps use MM/DD/YYYY and HH:MM:SS format

9.2 Batch Processing
    Alphabetical ordering ensures reproducible output
    Empty folder handling maintains consistent report structure
    Progress tracking enables monitoring of long operations

9.3 Automation
    Configuration file enables scripted deployments
    Command-line execution possible with Python
    Log output can be parsed by external tools if needed


SUPPORT AND UPDATES

10.1 Home Page
     https://www.progettosnaps.net/chdinfo/
     Documentation, updates, and community support

10.2 Version Tracking
     Tool version displayed in window title and header
     Report version number entered during Save Log operation
     Maintain version consistency for reproducible results

10.3 Feedback
     Report issues with specific error messages and steps to reproduce
     Include Python version and operating system information
     Suggest feature requests with use case descriptions


© 2026 AntoPISA