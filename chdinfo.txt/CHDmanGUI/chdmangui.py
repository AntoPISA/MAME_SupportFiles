#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHDman_GUI v.1.0
Graphical interface for MAME chdman command
Developed to manage CHD files in a simple and intuitive way
Internal version 1.19 03/14/2026 22:09
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import subprocess
import os
import configparser
from datetime import datetime
from pathlib import Path
import threading
import queue
import re

class CHDmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CHDman_GUI v1.0 © AntoPISA")
        self.root.geometry("1200x880")
        self.root.minsize(1000, 880)
        self.setup_style()
        self.config_file = "config.ini"
        self.chdman_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.input_path = tk.StringVar()
        self.chs_value = tk.StringVar(value="615,4,17")
        self.compression_var = tk.StringVar(value="none")
        self.output_queue = queue.Queue()
        self.process_thread = None
        self.stop_flag = False
        self.load_config()
        self.create_widgets()
        self.process_output()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Segoe UI', 10))
        style.configure('Header.TLabel', background='#2c3e50', foreground='white', font=('Segoe UI', 14, 'bold'))
        style.configure('TButton', font=('Segoe UI', 10), padding=5)
        style.configure('Accent.TButton', background='#3498db', foreground='white')
        style.configure('Danger.TButton', background='#e74c3c', foreground='white')
        style.configure('TEntry', font=('Segoe UI', 10), padding=5)
        style.configure('TCombobox', font=('Segoe UI', 10))
        style.configure('Treeview', background='white', fieldbackground='white', rowheight=25, font=('Segoe UI', 9))
        style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'), background='#34495e', foreground='white')

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        ttk.Label(header_frame, text="CHDman_GUI v1.0 © AntoPISA www.progettosnaps/chdinfo", style='Header.TLabel', padding=10).pack(fill=tk.X)
        paths_frame = ttk.LabelFrame(main_frame, text="Paths", padding="10")
        paths_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        paths_frame.columnconfigure(1, weight=1)
        ttk.Label(paths_frame, text="chdman.exe:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(paths_frame, textvariable=self.chdman_path, width=60).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Button(paths_frame, text="Browse...", command=self.browse_chdman).grid(row=0, column=2, pady=5)
        ttk.Label(paths_frame, text="Output:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(paths_frame, textvariable=self.output_path, width=60).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Button(paths_frame, text="Browse...", command=self.browse_output).grid(row=1, column=2, pady=5)
        ops_frame = ttk.LabelFrame(main_frame, text="Operations", padding="10")
        ops_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        ops_frame.columnconfigure(1, weight=1)
        ttk.Label(ops_frame, text="Operation:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.operation_var = tk.StringVar(value="Info (Information)")
        operations = [
            ("Info (Information)", "info"),
            ("Verify (Integrity Check)", "verify"),
            ("From CD (CD -> CHD)", "fromcd"),
            ("From Raw (Raw -> CHD)", "fromraw"),
            ("Extract Raw (CHD -> Raw)", "extractraw"),
            ("Extract CD (CHD -> CD)", "extractcd"),
            ("Create HD (Create Disk)", "createhd")
        ]
        op_combo = ttk.Combobox(ops_frame, textvariable=self.operation_var, values=[op[0] for op in operations], state="readonly", width=40)
        op_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        op_combo.bind('<<ComboboxSelected>>', self.on_operation_change)
        self.operation_map = {op[0]: op[1] for op in operations}
        self.chs_frame = ttk.Frame(ops_frame)
        self.chs_frame.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=5)
        ttk.Label(self.chs_frame, text="CHS (C,H,S):").pack(side=tk.LEFT, padx=5)
        ttk.Entry(self.chs_frame, textvariable=self.chs_value, width=20).pack(side=tk.LEFT, padx=5)
        ttk.Label(self.chs_frame, text="Compression:").pack(side=tk.LEFT, padx=(20, 5))
        ttk.Combobox(self.chs_frame, textvariable=self.compression_var, values=["none", "zlib", "lzma", "huff"], state="readonly", width=10).pack(side=tk.LEFT, padx=5)
        input_frame = ttk.LabelFrame(main_frame, text="Input", padding="10")
        input_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        input_frame.columnconfigure(1, weight=1)
        ttk.Label(input_frame, text="File/Folder:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(input_frame, textvariable=self.input_path, width=60).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Button(input_frame, text="Browse...", command=self.browse_input).grid(row=0, column=2, pady=5)
        self.recursive_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(input_frame, text="Include subfolders (alphabetical)", variable=self.recursive_var).grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=5)
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        self.execute_btn = ttk.Button(btn_frame, text="Execute", command=self.execute_command, style='Accent.TButton', width=20)
        self.execute_btn.pack(side=tk.LEFT, padx=5)
        self.stop_btn = ttk.Button(btn_frame, text="Stop", command=self.stop_command, style='Danger.TButton', width=20, state='disabled')
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Save Config", command=self.save_config, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear Log", command=self.clear_log, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Save Log", command=self.save_log, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Exit", command=self.on_closing, style='Danger.TButton', width=15).pack(side=tk.RIGHT, padx=5)
        self.progress_var = tk.DoubleVar()
        ttk.Progressbar(btn_frame, variable=self.progress_var, maximum=100, length=300).pack(side=tk.RIGHT, padx=5)
        log_frame = ttk.LabelFrame(main_frame, text="Log Output", padding="10")
        log_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, width=100, height=20, font=('Consolas', 9), bg='#1e1e1e', fg='#d4d4d4')
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.log_text.tag_configure('info', foreground='#4ec9b0')
        self.log_text.tag_configure('success', foreground='#6a9955')
        self.log_text.tag_configure('error', foreground='#f44747')
        self.log_text.tag_configure('warning', foreground='#dcdcaa')
        self.log_text.tag_configure('header', foreground='#569cd6', font=('Consolas', 9, 'bold'))

    def on_operation_change(self, event):
        operation = self.operation_map.get(self.operation_var.get())
        if operation in ['createhd', 'fromraw']:
            self.chs_frame.grid()
        else:
            self.chs_frame.grid_remove()

    def browse_chdman(self):
        filename = filedialog.askopenfilename(title="Select chdman.exe", filetypes=[("Executable", "*.exe"), ("All files", "*.*")])
        if filename:
            self.chdman_path.set(filename)
            self.save_config()

    def browse_output(self):
        directory = filedialog.askdirectory(title="Select output folder")
        if directory:
            self.output_path.set(directory)
            self.save_config()

    def browse_input(self):
        operation = self.operation_map.get(self.operation_var.get())
        if operation in ['fromcd', 'fromraw']:
            filetypes = [("CD Images", "*.cue *.iso *.bin"), ("Raw Images", "*.raw *.img *.bin"), ("All files", "*.*")]
            filename = filedialog.askopenfilename(title="Select input file", filetypes=filetypes)
            if filename:
                self.input_path.set(filename)
        else:
            filetypes = [("CHD Files", "*.chd"), ("All files", "*.*")]
            filename = filedialog.askopenfilename(title="Select CHD file", filetypes=filetypes)
            if filename:
                self.input_path.set(filename)
            else:
                directory = filedialog.askdirectory(title="Select folder with CHD files")
                if directory:
                    self.input_path.set(directory)

    def load_config(self):
        config = configparser.ConfigParser()
        if os.path.exists(self.config_file):
            config.read(self.config_file)
            if 'paths' in config:
                self.chdman_path.set(config.get('paths', 'chdman', fallback='chdman.exe'))
                self.output_path.set(config.get('paths', 'output', fallback=os.getcwd()))
                self.input_path.set(config.get('paths', 'input', fallback=''))
            if 'settings' in config:
                self.chs_value.set(config.get('settings', 'chs', fallback='615,4,17'))
                self.compression_var.set(config.get('settings', 'compression', fallback='none'))
        else:
            self.chdman_path.set('chdman.exe')
            self.output_path.set(os.getcwd())

    def save_config(self):
        config = configparser.ConfigParser()
        config['paths'] = {'chdman': self.chdman_path.get(), 'output': self.output_path.get(), 'input': self.input_path.get()}
        config['settings'] = {'chs': self.chs_value.get(), 'compression': self.compression_var.get()}
        with open(self.config_file, 'w', encoding='utf-8') as f:
            config.write(f)
        self.log_message("Configuration saved successfully!", 'success')

    def log_message(self, message, tag='info'):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n", tag)
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def clear_log(self):
        self.log_text.delete(1.0, tk.END)
        self.log_message("Log cleared", 'info')

    def save_log(self):
        version_dialog = tk.Toplevel(self.root)
        version_dialog.title("Select Version")
        version_dialog.geometry("300x150")
        version_dialog.transient(self.root)
        version_dialog.grab_set()
        ttk.Label(version_dialog, text="Enter version number:").pack(pady=10)
        version_entry = ttk.Entry(version_dialog, width=20)
        version_entry.pack(pady=5)
        version_entry.insert(0, "000")
        result = {'version': None}
        def on_ok():
            result['version'] = version_entry.get().strip()
            version_dialog.destroy()
        def on_cancel():
            result['version'] = None
            version_dialog.destroy()
        btn_frame = ttk.Frame(version_dialog)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="OK", command=on_ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=on_cancel).pack(side=tk.LEFT, padx=5)
        self.root.wait_window(version_dialog)
        if result['version'] is None:
            return
        version = result['version']
        output_dir = self.output_path.get()
        if not output_dir:
            messagebox.showerror("Error", "Please set the output path first")
            return
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"CHD-Info_{version}.txt")
        try:
            log_content = self.log_text.get(1.0, tk.END)
            lines = log_content.split('\n')
            cleaned = []
            skip_patterns = [
                'Welcome to CHDman_GUI', 'Select an operation', 'Tip: Configure paths',
                'Log cleared', 'Starting operation:', 'Input: ', 'Found ',
                'Configuration saved', 'Operation completed',
                'chdman - MAME Compressed Hunks of Data', 'Success: ',
                'EMPTY FOLDERS REPORT', 'Processing file',
            ]
            for line in lines:
                if re.match(r'^\[\d{2}:\d{2}:\d{2}\]\s*', line):
                    line = re.sub(r'^\[\d{2}:\d{2}:\d{2}\]\s*', '', line)
                line = line.strip()
                if not line:
                    continue
                if any(p in line for p in skip_patterns):
                    continue
                if re.match(r'^File \d+/\d+:', line):
                    continue
                cleaned.append(line)
            separator = '=' * 70
            entries = []
            current_entry = []
            i = 0
            while i < len(cleaned):
                line = cleaned[i]
                if line == separator and i + 1 < len(cleaned) and cleaned[i + 1].startswith('== Date'):
                    if current_entry:
                        while current_entry and current_entry[-1] == separator:
                            current_entry.pop()
                        if current_entry:
                            entries.append(current_entry)
                    current_entry = [line]
                    i += 1
                else:
                    if current_entry:
                        current_entry.append(line)
                    i += 1
            if current_entry:
                while current_entry and current_entry[-1] == separator:
                    current_entry.pop()
                if current_entry:
                    entries.append(current_entry)
            output_lines = []
            output_lines.append(f"# CHD-Info 0.{version}")
            output_lines.append("# File created and maintained by AntoPISA with CHDmanGUI v1.0")
            output_lines.append("# Home-page: https://www.progettosnaps.net/chdinfo/")
            output_lines.append("#")
            output_lines.append("#")
            for idx, entry in enumerate(entries):
                if idx > 0:
                    output_lines.append('')
                for line in entry:
                    output_lines.append(line)
                output_lines.append(separator)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(output_lines))
            self.log_message(f"Log saved to: {output_file}", 'success')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save log: {str(e)}")
            self.log_message(f"Error saving log: {str(e)}", 'error')

    def stop_command(self):
        self.stop_flag = True
        self.log_message("Stopping operation...", 'warning')
        self.stop_btn.config(state='disabled')

    def on_closing(self):
        if self.process_thread and self.process_thread.is_alive():
            if messagebox.askokcancel("Quit", "A process is running. Stop and quit?"):
                self.stop_flag = True
                self.root.destroy()
        else:
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                self.root.destroy()

    def get_chd_files(self, path, recursive=True):
        chd_files = []
        path = Path(path)
        if path.is_file() and path.suffix.lower() == '.chd':
            return [path]
        if path.is_dir():
            if recursive:
                for root, dirs, files in sorted(os.walk(path), key=lambda x: x[0]):
                    dirs.sort()
                    for file in sorted(files):
                        if file.lower().endswith('.chd'):
                            chd_files.append(Path(root) / file)
            else:
                for file in sorted(os.listdir(path)):
                    if file.lower().endswith('.chd'):
                        chd_files.append(path / file)
        return chd_files

    def get_empty_folders(self, path):
        empty_folders = []
        path = Path(path)
        if path.is_dir():
            for root, dirs, files in os.walk(path):
                dirs.sort()
                has_chd = any(f.lower().endswith('.chd') for f in files)
                if not has_chd and root != str(path):
                    folder_name = Path(root).name
                    relative_path = Path(root).relative_to(path)
                    empty_folders.append({'path': str(relative_path), 'name': folder_name, 'full_path': str(root)})
            empty_folders.sort(key=lambda x: x['path'].lower())
        return empty_folders

    def execute_command(self):
        operation = self.operation_map.get(self.operation_var.get())
        chdman = self.chdman_path.get()
        input_path = self.input_path.get()
        output_path = self.output_path.get()
        if not chdman:
            messagebox.showerror("Error", "Please select the chdman.exe path")
            return
        if not input_path:
            messagebox.showerror("Error", "Please select an input file or folder")
            return
        if not os.path.exists(chdman):
            messagebox.showerror("Error", f"chdman.exe not found: {chdman}")
            return
        if not os.path.exists(input_path):
            messagebox.showerror("Error", f"Input path does not exist: {input_path}")
            return
        self.stop_flag = False
        self.execute_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.progress_var.set(0)
        self.process_thread = threading.Thread(target=self.run_command, args=(operation, chdman, input_path, output_path))
        self.process_thread.daemon = True
        self.process_thread.start()

    def run_command(self, operation, chdman, input_path, output_path):
        try:
            self.log_message(f"Starting operation: {operation}", 'header')
            self.log_message(f"Input: {input_path}", 'info')
            chd_files = self.get_chd_files(input_path, self.recursive_var.get())
            empty_folders = []
            if self.recursive_var.get() and os.path.isdir(input_path):
                empty_folders = self.get_empty_folders(input_path)
            items_to_process = []
            for chd_file in chd_files:
                if self.stop_flag: break
                try: rel_path = os.path.relpath(str(chd_file), input_path)
                except: rel_path = str(chd_file)
                items_to_process.append((rel_path.lower(), 'chd', chd_file, None))
            for folder in empty_folders:
                if self.stop_flag: break
                chd_path = f"{folder['path']}\\{folder['name']}.chd"
                items_to_process.append((chd_path.lower(), 'empty', None, folder))
            items_to_process.sort(key=lambda x: x[0])
            total_items = len(items_to_process)
            self.log_message(f"Found {len(chd_files)} CHD files", 'info')
            if empty_folders:
                self.log_message(f"Found {len(empty_folders)} folders without CHD (not dumped)", 'warning')
            if total_items == 0 and operation not in ['createhd', 'fromcd', 'fromraw']:
                self.log_message("No CHD files found!", 'error')
                self.execute_btn.config(state='normal')
                self.stop_btn.config(state='disabled')
                return
            for index, item in enumerate(items_to_process):
                if self.stop_flag:
                    self.log_message("Operation stopped by user.", 'warning')
                    break
                sort_key, item_type, chd_file, folder_info = item
                if item_type == 'chd':
                    self.process_file(operation, chdman, chd_file, output_path, index, total_items)
                else:
                    self.log_undumped_entry(folder_info)
                progress = ((index + 1) / total_items) * 100
                self.progress_var.set(progress)
            if not self.stop_flag:
                self.log_message(f"Operation completed successfully!", 'success')
                self.progress_var.set(100)
        except Exception as e:
            self.log_message(f"Error: {str(e)}", 'error')
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            self.execute_btn.config(state='normal')
            self.stop_btn.config(state='disabled')

    def process_file(self, operation, chdman, chd_file, output_path, index, total):
        filename = chd_file.name
        filepath = str(chd_file)
        self.log_message(f"{'='*70}", 'header')
        self.log_message(f"File {index + 1}/{total}: {filename}", 'header')
        self.log_message(f"{'='*70}", 'header')
        cmd = [chdman, operation, '-i', filepath]
        if operation == 'createhd':
            output_file = os.path.join(output_path, chd_file.stem + '.chd')
            cmd.extend(['-o', output_file, '-chs', self.chs_value.get()])
            if self.compression_var.get() != 'none':
                cmd.extend(['-c', self.compression_var.get()])
            else:
                cmd.extend(['-c', 'none'])
        elif operation == 'fromraw':
            output_file = os.path.join(output_path, chd_file.stem + '.chd')
            cmd.extend(['-o', output_file, '-chs', self.chs_value.get()])
        elif operation == 'fromcd':
            output_file = os.path.join(output_path, chd_file.stem + '.chd')
            cmd.extend(['-o', output_file])
        elif operation in ['extractraw', 'extractcd']:
            output_file = os.path.join(output_path, chd_file.stem + ('.raw' if operation == 'extractraw' else '.cue'))
            cmd.extend(['-o', output_file])
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                self.log_message(f"Success: {filename}", 'success')
                if operation == 'info':
                    self.display_info_output(result.stdout, filepath)
                elif operation == 'verify':
                    self.log_message(f"Verification passed: {filename}", 'success')
            else:
                self.log_message(f"Warning: {result.stderr}", 'warning')
        except subprocess.TimeoutExpired:
            self.log_message(f"Timeout for {filename}", 'warning')
        except Exception as e:
            self.log_message(f"Error: {str(e)}", 'error')

    def log_undumped_entry(self, folder):
        try:
            now = datetime.now()
            date_str = now.strftime("%m/%d/%Y")
            time_str = now.strftime("%H:%M:%S")
            self.log_message(f"{'='*70}", 'header')
            self.log_message(f"== Date {date_str}", 'header')
            self.log_message(f"== Time {time_str}", 'header')
            self.log_message(f"{'='*70}", 'header')
            chd_path = f"{folder['path']}\\{folder['name']}.chd"
            self.log_message(f"Input file:   {chd_path}", 'info')
            self.log_message(f"Note      :   CHD not dumped.", 'warning')
            self.log_message(f"{'='*70}", 'header')
        except Exception as e:
            self.log_message(f"Error logging undumped entry: {str(e)}", 'error')

    def display_info_output(self, output, filepath):
        try:
            now = datetime.now()
            date_str = now.strftime("%m/%d/%Y")
            time_str = now.strftime("%H:%M:%S")
            self.log_message(f"{'='*70}", 'header')
            self.log_message(f"== Date {date_str}", 'header')
            self.log_message(f"== Time {time_str}", 'header')
            self.log_message(f"{'='*70}", 'header')
            try:
                rel_path = os.path.relpath(filepath, self.input_path.get())
            except:
                rel_path = filepath
            self.log_message(f"Input file:   {rel_path}", 'info')
            if output:
                for line in output.split('\n'):
                    if line.strip():
                        if 'chdman - MAME Compressed Hunks of Data' in line:
                            continue
                        if line.strip().startswith('Input file:') and 'File Version' not in line:
                            continue
                        self.log_message(line, 'info')
            self.log_message(f"{'='*70}", 'header')
        except Exception as e:
            self.log_message(f"Error parsing output: {str(e)}", 'error')

    def process_output(self):
        try:
            while True:
                message = self.output_queue.get_nowait()
                self.log_message(message['text'], message['tag'])
        except queue.Empty:
            pass
        self.root.after(100, self.process_output)

def main():
    root = tk.Tk()
    app = CHDmanGUI(root)
    app.log_message("Welcome to CHDman_GUI v.1.0!", 'success')
    app.log_message("Select an operation and start working with CHD files", 'info')
    app.log_message("Tip: Configure paths in config.ini for quick access", 'warning')
    root.mainloop()

if __name__ == "__main__":
    main()