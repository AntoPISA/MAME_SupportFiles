#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import re
from pathlib import Path

def parse_software_from_xml(filepath):
    """Estrae software con name e sha1 da file XML."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        software_dict = {}

        # Regex per trovare blocchi <software name="..."> ... </software> (anche se interrotti)
        # Cerca <software name="..." seguito da tutto fino al prossimo <software o </softwarelist
        software_pattern = r'<software\s+name="([^"]+)"[^>]*>.*?(?=<software|</softwarelist|\Z)'
        for match in re.finditer(software_pattern, content, re.DOTALL):
            software_name = match.group(1)
            software_block = match.group(0)

            # Cerca tutti i tag <rom> o <disk> con attributo sha1
            sha1_pattern = r'sha1="([a-fA-F0-9]{40})"'
            sha1_matches = re.findall(sha1_pattern, software_block)

            if sha1_matches:
                software_dict[software_name] = {
                    'sha1_set': set(sha1_matches),
                    'sha1_list': sha1_matches  # Se serve mantenere l'ordine o i duplicati
                }

        return software_dict
    except Exception as e:
        print(f"[ERRORE] Parsing {filepath}: {e}")
        return {}

def get_xml_files_from_dir(directory):
    """Restituisce set di file XML."""
    return {f for f in os.listdir(directory) if f.lower().endswith('.xml')}

def find_renamed_software(old_sw, new_sw):
    """Trova software rinominati: stessi SHA1, nomi diversi.
    Restituisce lista di tuple (old_name, new_name)"""
    renamed = []
    matched_new = set()
    for old_name in old_sw:
        for new_name in new_sw:
            if new_name in matched_new:
                continue
            if old_name != new_name:
                # Verifica che i set SHA1 siano uguali
                if old_sw[old_name]['sha1_set'] == new_sw[new_name]['sha1_set']:
                    renamed.append((old_name, new_name))
                    matched_new.add(new_name)
                    break
    return renamed

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("MAME SL Comparision v1.0")
        self.root.geometry("900x700")

        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Bottone per avviare il confronto
        self.btn_run = ttk.Button(main_frame, text="Esegui Confronto", command=self.start_comparison)
        self.btn_run.pack(side=tk.LEFT, padx=5)

        # Bottone per uscire
        btn_exit = ttk.Button(main_frame, text="Esci", command=self.root.destroy)
        btn_exit.pack(side=tk.RIGHT, padx=5)

        # Barra di progresso (inizialmente nascosta)
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(pady=5, fill=tk.X)
        self.progress.pack_forget()

        # Etichetta di stato
        self.status_label = ttk.Label(main_frame, text="", foreground="blue")
        self.status_label.pack(pady=5)

        # Frame per i risultati
        self.result_frame = ttk.Frame(main_frame)
        self.result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Area testo con scrollbar
        self.text_area = scrolledtext.ScrolledText(self.result_frame, wrap=tk.WORD, width=100, height=30)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # Pulsante salva risultati
        btn_save = ttk.Button(main_frame, text="Salva Risultati", command=self.save_results)
        btn_save.pack(pady=5)

    def start_comparison(self):
        # Chiedi all'utente il tipo di confronto
        choice = self.ask_comparison_type()
        if choice is None:
            return # L'utente ha annullato

        self.btn_run.config(state=tk.DISABLED)
        self.progress.pack()
        self.progress.start()
        self.status_label.config(text="Elaborazione in corso...")

        # Avvia il confronto in un thread separato
        thread = threading.Thread(target=self.run_comparison_in_thread, args=(choice,))
        thread.start()

    def ask_comparison_type(self):
        """Chiede all'utente se eseguire un controllo completo o mirato."""
        # Crea una finestra di dialogo temporanea
        dialog = tk.Toplevel(self.root)
        dialog.title("Tipo di Confronto")
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()  # Blocca input sulla finestra principale

        tk.Label(dialog, text="Scegli il tipo di confronto:", font=("Arial", 12)).pack(pady=10)

        selected_option = tk.StringVar(value="complete") # Default: completo

        rb_complete = ttk.Radiobutton(dialog, text="Controllo Completo (tutti i file comuni)", variable=selected_option, value="complete")
        rb_complete.pack(anchor="w", padx=20, pady=5)

        rb_targeted = ttk.Radiobutton(dialog, text="Controllo Mirato (solo file in 'diffs.txt')", variable=selected_option, value="targeted")
        rb_targeted.pack(anchor="w", padx=20, pady=5)

        result = {"value": None}

        def on_ok():
            result["value"] = selected_option.get()
            dialog.destroy()

        btn_ok = ttk.Button(dialog, text="OK", command=on_ok)
        btn_ok.pack(pady=15)

        self.root.wait_window(dialog) # Attendi la chiusura della finestra

        return result["value"]

    def run_comparison_in_thread(self, comparison_type):
        old_dir = 'old'
        new_dir = 'new'
        diffs_file = 'diffs.txt'

        if not os.path.isdir(old_dir) or not os.path.isdir(new_dir):
            self.show_error("Cartelle 'old' e 'new' non trovate.")
            return

        # Pulisci area risultati
        self.text_area.delete(1.0, tk.END)

        # FASE 1: Confronto file
        self.append_text("=" * 70 + "\n")
        self.append_text("FASE 1: CONFRONTO FILE\n")
        self.append_text("=" * 70 + "\n")

        old_files = get_xml_files_from_dir(old_dir)
        new_files = get_xml_files_from_dir(new_dir)

        new_only = new_files - old_files
        removed = old_files - new_files
        common_all = old_files & new_files

        self.append_text(f"File in '{old_dir}': {len(old_files)}\n")
        self.append_text(f"File in '{new_dir}': {len(new_files)}\n")

        if new_only:
            self.append_text(f"NUOVI ({len(new_only)}):\n")
            for f in sorted(new_only):
                self.append_text(f" + {f}\n")
            self.append_text("\n")

        if removed:
            self.append_text(f"RIMOSSI ({len(removed)}):\n")
            for f in sorted(removed):
                self.append_text(f" - {f}\n")
            self.append_text("\n")

        self.append_text(f"File comuni: {len(common_all)}\n")

        # --- Logica per selezionare i file da analizzare ---
        if comparison_type == "targeted":
            # Leggi i file da diffs.txt
            if not os.path.exists(diffs_file):
                self.show_error(f"File '{diffs_file}' non trovato per il confronto mirato.")
                return
            with open(diffs_file, 'r', encoding='utf-8') as f:
                target_files = {line.strip() for line in f if line.strip()}
            # Assicurati che abbiano estensione .xml
            target_files = {f if f.endswith('.xml') else f + '.xml' for f in target_files}
            # Interseca con i file comuni
            files_to_analyze = common_all & target_files
            self.append_text(f"File da analizzare (da '{diffs_file}'): {len(files_to_analyze)}\n")
        else: # comparison_type == "complete"
            files_to_analyze = common_all
            self.append_text("File da analizzare (tutti i comuni): tutti\n")

        self.append_text(f"File effettivamente analizzati: {len(files_to_analyze)}\n")
        self.append_text("-" * 70 + "\n")

        # FASE 2: Analisi contenuti
        self.append_text("FASE 2: ANALISI CONTENUTI\n")
        self.append_text("-" * 70 + "\n")

        for idx, filename in enumerate(sorted(files_to_analyze), 1):
            self.update_status(f"Elaborando {idx}/{len(files_to_analyze)}: {filename}")

            old_path = os.path.join(old_dir, filename)
            new_path = os.path.join(new_dir, filename)

            old_sw = parse_software_from_xml(old_path)
            new_sw = parse_software_from_xml(new_path)

            if not old_sw and not new_sw:
                self.append_text(f"[{filename}] Nessun software trovato in entrambi i file.\n")
                continue
            if not old_sw:
                self.append_text(f"[{filename}] Nessun software trovato in '{old_dir}'.\n")
                continue
            if not new_sw:
                self.append_text(f"[{filename}] Nessun software trovato in '{new_dir}'.\n")
                continue

            old_names = set(old_sw.keys())
            new_names = set(new_sw.keys())

            added = new_names - old_names
            removed_sw = old_names - new_names
            common_sw = old_names & new_names

            # Trova rinominati
            renamed = find_renamed_software(old_sw, new_sw)
            renamed_old = {old for old, new in renamed}
            renamed_new = {new for old, new in renamed}

            # Rimuovi dai set di aggiunti/rimossi
            added = added - renamed_new
            removed_sw = removed_sw - renamed_old

            has_changes = bool(added or removed_sw or renamed or any(
                old_sw[name]['sha1_set'] != new_sw[name]['sha1_set']
                for name in common_sw if name in old_sw and name in new_sw
            ))

            if has_changes:
                self.append_text(f"[{filename}]\n\n") # Aggiunto \n\n dopo il nome del file
                if added:
                    self.append_text(f" Aggiunti ({len(added)}):\n")
                    for name in sorted(added):
                        self.append_text(f" + {name}\n")
                    self.append_text("\n") # Aggiunto \n dopo la sezione Aggiunti
                if removed_sw:
                    self.append_text(f" Rimossi ({len(removed_sw)}):\n")
                    for name in sorted(removed_sw):
                        self.append_text(f" - {name}\n")
                    self.append_text("\n") # Aggiunto \n dopo la sezione Rimossi

                if renamed:
                    self.append_text(f" Rinominati ({len(renamed)}):\n")
                    base_name = Path(filename).stem # Ottieni il nome del file senza estensione
                    for old_name, new_name in sorted(renamed):
                        # Formattazione richiesta per i rinominati
                        self.append_text(f" {base_name:<20} | {old_name:<15} > {new_name}\n")
                    self.append_text("\n") # Aggiunto \n dopo la sezione Rinominati

                modified = []
                for name in common_sw:
                    if name in old_sw and name in new_sw:
                        if old_sw[name]['sha1_set'] != new_sw[name]['sha1_set']:
                            modified.append(name)
                if modified:
                    self.append_text(f" SHA1 modificati ({len(modified)}):\n")
                    for name in sorted(modified):
                        self.append_text(f" '{name}' (SHA1 diversi)\n")
                self.append_text("\n")
            else:
                self.append_text(f"[{filename}] Nessuna differenza significativa trovata.\n\n")

        # Completamento
        self.update_status("Confronto completato!")
        self.progress.stop()
        self.progress.pack_forget()
        self.btn_run.config(state=tk.NORMAL)

    def append_text(self, text):
        """Aggiunge testo all'area risultati (da thread)."""
        self.root.after(0, lambda: self.text_area.insert(tk.END, text))
        # Scrolla in fondo automaticamente
        self.root.after(0, lambda: self.text_area.see(tk.END))

    def update_status(self, text):
        """Aggiorna etichetta stato (da thread)."""
        self.root.after(0, lambda: self.status_label.config(text=text))

    def show_error(self, message):
        """Mostra errore in finestra di dialogo e riabilita pulsante."""
        self.root.after(0, lambda: messagebox.showerror("Errore", message))
        self.root.after(0, lambda: self.btn_run.config(state=tk.NORMAL))
        self.root.after(0, lambda: self.progress.stop())
        self.root.after(0, lambda: self.progress.pack_forget())
        self.root.after(0, lambda: self.status_label.config(text=""))

    def save_results(self):
        """Salva i risultati in un file di testo."""
        content = self.text_area.get(1.0, tk.END)
        filepath = "confronto_risultati.txt"
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            messagebox.showinfo("Salvataggio", f"Risultati salvati in '{filepath}'")
        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile salvare: {e}")

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == '__main__':
    main()