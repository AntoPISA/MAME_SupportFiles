import os
import tkinter as tk
from tkinter import filedialog, messagebox
import openpyxl


def process_excel(option, root):
    """
    Elabora il file Excel in base all'opzione scelta e genera il file .txt formattato.
    """
    # Apri finestra per selezionare il file
    file_path = filedialog.askopenfilename(
        title="Seleziona il file Excel",
        filetypes=[("File Excel", "*.xlsx")]
    )

    if not file_path:
        messagebox.showinfo("Annullato", "Nessun file selezionato.")
        return

    try:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active
        rows = list(sheet.iter_rows(values_only=True))

        if len(rows) == 0:
            messagebox.showwarning("Errore", "Il foglio è vuoto.")
            return

        # Prima riga = intestazioni
        headers = [str(cell).strip().lower() if cell else "" for cell in rows[0]]
        data_rows = rows[1:]

        # Mappatura colonne
        col_map = {}
        for idx, header in enumerate(headers):
            if header:
                col_map[header] = idx

        # Colonne richieste per ogni opzione
        required_cols = []
        if option == 1:
            required_cols = ['new_device', 'numero', 'riga', 'completo']
        elif option == 2:
            required_cols = ['new_machine', 'numero', 'riga', 'completo']
        elif option == 3:
            required_cols = ['new_driver', 'versione', 'completo']

        # Controlla colonne mancanti
        missing = [col for col in required_cols if col not in col_map]
        if missing:
            messagebox.showerror("Errore", f"Colonne mancanti nel file Excel:\n{', '.join(missing)}")
            return

        output_blocks = []

        for row in data_rows:
            try:
                if option == 1:  # Nuovi DEVICE
                    new_device = row[col_map['new_device']] or ""
                    numero = row[col_map['numero']] or ""
                    riga = row[col_map['riga']] or ""
                    completo = row[col_map['completo']] or ""

                    block = f"""{new_device}
$mame
{numero}

{riga}

DRIVER:
xxx

DRIVER STATUS:
Emulation: Good
Color: Good
Sound: Good
Graphics: Good
Save State: Supported

WIP:
{completo}

$end"""
                    output_blocks.append(block)

                elif option == 2:  # Nuove MACCHINE
                    new_machine = row[col_map['new_machine']] or ""
                    numero = row[col_map['numero']] or ""
                    riga = row[col_map['riga']] or ""
                    completo = row[col_map['completo']] or ""

                    block = f"""{new_machine}
$mame
{numero}

{riga}

<No certified information found. If you have info on this machine, please contact us!>

DRIVER:
xxx

DRIVER STATUS:
Emulation: Good
Color: Good
Sound: Good
Graphics: Good
Save State: Supported

SOFTWARE LIST:
-

RESOURCES:
xxx

WIP:
{completo}

ROMSET:
0000000 bytes in 0 files / 000.00Kb packed

$end"""
                    output_blocks.append(block)

                elif option == 3:  # Nuovi DRIVER
                    new_driver = row[col_map['new_driver']] or ""
                    versione = row[col_map['versione']] or ""
                    completo = row[col_map['completo']] or ""

                    block = f"""{new_driver}
$drv
{versione}

xxx

WIP:
{completo}

$end"""
                    output_blocks.append(block)

            except Exception as e:
                messagebox.showwarning("Attenzione", f"Errore nell'elaborare una riga: {e}")
                continue

        # Unisci tutti i blocchi con newline (già includono formattazione)
        final_content = "\n".join(output_blocks)

        # Percorso di output: stesso nome del file Excel, ma .txt
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_dir = os.path.dirname(file_path)
        output_path = os.path.join(output_dir, f"{base_name}.txt")

        # Salva il file di testo
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_content)

        # Conferma
        messagebox.showinfo("Successo", f"File generato con successo:\n\n{output_path}")

    except Exception as e:
        messagebox.showerror("Errore", f"Errore durante l'elaborazione:\n{str(e)}")


def main():
    # Creazione finestra principale
    root = tk.Tk()
    root.title("🔧 Generatore Testi MAME")
    root.geometry("440x280")
    root.resizable(False, False)
    root.configure(bg="#f0f0f0")

    # Titolo
    title_label = tk.Label(
        root,
        text="Seleziona il tipo di elemento da elaborare:",
        font=("Arial", 12, "bold"),
        bg="#f0f0f0",
        fg="#333"
    )
    title_label.pack(pady=15)

    # Pulsanti
    btn_style = {
        'font': ('Arial', 10),
        'width': 30,
        'height': 1,
        'bd': 2,
        'relief': 'raised'
    }

    tk.Button(
        root, text="1. Nuovi Device", bg="#d4edda", fg="black",
        command=lambda: process_excel(1, root), **btn_style
    ).pack(pady=6)

    tk.Button(
        root, text="2. Nuove Macchine", bg="#d1ecf1", fg="black",
        command=lambda: process_excel(2, root), **btn_style
    ).pack(pady=6)

    tk.Button(
        root, text="3. Nuovi Driver", bg="#fff3cd", fg="black",
        command=lambda: process_excel(3, root), **btn_style
    ).pack(pady=6)

    # Bottone Esci
    tk.Button(
        root, text="❌ Exit", bg="#f8d7da", fg="black",
        command=root.destroy, font=("Arial", 10, "bold"),
        width=30, height=1
    ).pack(pady=15)

    # Avvia il loop principale
    root.mainloop()


if __name__ == "__main__":
    main()