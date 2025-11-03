# MAME Software List Comparison Tool

## Description

This Python script compares XML files containing MAME software lists from two directories (`old` and `new`). It identifies:

*   **File-level changes:** New, removed, and common XML files.
*   **Content-level changes:** Added, removed, renamed, and SHA1-modified software entries within common XML files.
*   It supports two modes of operation:
    *   **Complete Check:** Analyzes all common XML files found in both directories.
    *   **Targeted Check:** Analyzes only the XML files listed in a `diffs.txt` file, speeding up the process when comparing large sets of files.

The script features a graphical user interface (GUI) built with `tkinter` for user interaction, progress visualization, and result display. It treats the XML files as text to robustly parse software names and SHA1 hashes, even from fragmented or irregularly structured XML dumps.

## Features

*   **GUI Interface:** Provides a clear window for launching the comparison, viewing results, saving output, and selecting comparison mode.
*   **Two Comparison Modes:** Allows users to choose between a complete scan or a targeted scan based on `diffs.txt`.
*   **Detailed Output:** Shows file differences, software additions, removals, renames (with a specific format), and SHA1 modifications.
*   **Progress Indication:** Displays a progress bar and status updates during execution.
*   **Result Saving:** Offers an option to save the comparison results to a text file.

---

# Strumento di Confronto Liste Software MAME

## Descrizione

Questo script Python confronta file XML contenenti liste software MAME da due directory (`old` e `new`). Identifica:

*   **Cambiamenti a livello di file:** File XML nuovi, rimossi e comuni.
*   **Cambiamenti a livello di contenuto:** Voci software aggiunte, rimosse, rinominate e con SHA1 modificati all'interno dei file XML comuni.
*   Supporta due modalità di funzionamento:
    *   **Controllo Completo:** Analizza tutti i file XML comuni trovati in entrambe le directory.
    *   **Controllo Mirato:** Analizza solo i file XML elencati in un file `diffs.txt`, velocizzando il processo quando si confrontano grandi insiemi di file.

Lo script presenta un'interfaccia grafica (GUI) realizzata con `tkinter` per l'interazione con l'utente, la visualizzazione dei progressi e dei risultati. Tratta i file XML come testo per estrarre in modo robusto nomi software e hash SHA1, anche da dump XML frammentati o strutturati in modo irregolare.

## Funzionalità

*   **Interfaccia Grafica:** Fornisce una finestra chiara per avviare il confronto, visualizzare i risultati, salvare l'output e selezionare la modalità di confronto.
*   **Due Modalità di Confronto:** Permette all'utente di scegliere tra una scansione completa o una mirata basata su `diffs.txt`.
*   **Output Dettagliato:** Mostra differenze tra file, aggiunte, rimozioni, rinomine (con un formato specifico) e modifiche agli SHA1.
*   **Indicazione dei Progressi:** Visualizza una barra di avanzamento e aggiornamenti di stato durante l'esecuzione.
*   **Salvataggio dei Risultati:** Offre un'opzione per salvare i risultati del confronto in un file di testo.