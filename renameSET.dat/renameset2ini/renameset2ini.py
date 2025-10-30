#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox


def remove_bom(line):
    if line.startswith('\ufeff'):
        return line[1:]
    return line


def parse_rename_set_dat(lines):
    output_lines = []

    # === Intestazione: linee 1-14, 20, 21 ===
    header_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 20, 21]
    for n in header_nums:
        if n - 1 < len(lines):
            raw_line = lines[n - 1]
            line = remove_bom(raw_line.rstrip('\r\n'))
            if line.startswith('#'):
                output_lines.append(';;' + line[1:])
            else:
                output_lines.append('; ' + line)
    output_lines.append('')

    i = 0
    while i < len(lines):
        raw_line = lines[i]
        line = remove_bom(raw_line.rstrip('\r\n')).strip()

        # Estrai versione: tutto dopo "$" fino al primo spazio
        version_match = re.match(r'^\$(\S+)', line)
        if version_match and ' [#' in line:
            version = version_match.group(1)
            output_lines.append(f'[{version}]')
            i += 1

            # Data
            date_str = ''
            if i < len(lines):
                cand = remove_bom(lines[i].rstrip('\r\n')).strip()
                if re.fullmatch(r'\d{4}/\d{2}/\d{2}', cand):
                    date_str = cand
                    i += 1

            # Stat_00 fisso
            output_lines.append(
                "Stat_00=Date, total items, drivers, machines, parents, clones, BIOSes, devices, "
                "requires CHDs, use samples, audio mono, audio stereo, audio multichannel, no audio, "
                "working, not working, mechanicals, not mechanicals, save supported, save unsupported, "
                "horizontal screen, vertical screen, raster graphics, vector graphics, lcd graphics, "
                "svg graphics, screenless, one player, two players, three players, more than three players, "
                "use stick, use gambling, use joystick, use keyboard, use keypad, use lightgun, use mahjong, "
                "use mouse, use buttons only, use paddle, use pedal, use positional, use dial, use trackball, "
                "use hanafuda, total roms, machines roms, devices roms, BIOSes roms, CHDs, sample files, "
                "sample packs, good dumps, no dumps, bad dumps, bugs fixed, software list, software, "
                "active SL, orphan SL, active software, orphan software, software parents, software clones, "
                "software roms, software CHD, supported software, partially supported software, "
                "unsupported software, Rename, Delete"
            )
            output_lines.append(f'Stat_01={date_str}')

            stats = []
            ren_entries = []
            del_entries = []

            # Leggi statistiche fino a "X ren" o "X del"
            while i < len(lines):
                current = remove_bom(lines[i].rstrip('\r\n')).strip()
                if current in ('MAME:', 'MAME SL:', '-', '', 'software added/removed:', 'software renamed:', 'software removed:'):
                    i += 1
                    continue
                elif re.match(r'\d+\s+ren\s+\(\d+/\d+/\d+\):', current):
                    break
                elif re.match(r'\d+\s+del\s+\(\d+/\d+/\d+\):', current):
                    break
                elif re.match(r'^\$\d', current):  # nuova versione
                    break
                else:
                    # Estrai ogni campo completo: "3.235 drivers (+7)" → "3.235 (+7)"
                    parts = current.split(',')
                    for part in parts:
                        part = part.strip()
                        if not part:
                            continue
                        match = re.match(r'^([\d\.,]+(?:\s*\([^)]+\))?)', part)
                        if match:
                            val = match.group(1).replace(',', '.')
                            stats.append(val)
                    i += 1

            # Leggi rename
            ren_count = 0
            if i < len(lines) and re.match(r'\d+\s+ren\s+\(\d+/\d+/\d+\):', remove_bom(lines[i].rstrip('\r\n')).strip()):
                ren_count = int(lines[i].split()[0])
                i += 1
                count = 0
                while count < ren_count and i < len(lines):
                    entry = remove_bom(lines[i].rstrip('\r\n')).strip()
                    if entry in ('', '-',) or re.match(r'\d+\s+del', entry) or entry.startswith('$'):
                        i += 1
                        continue
                    match = re.match(r'^(\S+)\s+>\s+(\S+)', entry)
                    if match:
                        ren_entries.append(f"{match.group(1)}   > {match.group(2)}")
                    else:
                        clean = entry.split(' (mID:')[0].strip()
                        ren_entries.append(clean)
                    count += 1
                    i += 1

            # Leggi delete
            del_count = 0
            if i < len(lines) and re.match(r'\d+\s+del\s+\(\d+/\d+/\d+\):', remove_bom(lines[i].rstrip('\r\n')).strip()):
                del_count = int(lines[i].split()[0])
                i += 1
                count = 0
                while count < del_count and i < len(lines):
                    entry = remove_bom(lines[i].rstrip('\r\n')).strip()
                    if entry in ('', '-',) or entry.startswith('$'):
                        i += 1
                        continue
                    clean = entry.split(' (mID:')[0].strip()
                    del_entries.append(clean)
                    count += 1
                    i += 1

            # Aggiungi conteggi alla fine delle statistiche
            stats.append(str(len(ren_entries)))
            stats.append(str(len(del_entries)))

            # Scrivi Stat_02, Stat_03, ...
            for idx, val in enumerate(stats, start=2):
                output_lines.append(f'Stat_{idx:02d}={val}')

            # Riga vuota dopo Stat_XX
            output_lines.append('')

            # Scrivi Ren
            for j, r in enumerate(ren_entries, 1):
                output_lines.append(f'Ren_{j:03d}={r}')

            # Riga vuota tra Ren e Del (solo se entrambi presenti)
            if ren_entries and del_entries:
                output_lines.append('')

            # Scrivi Del
            for j, d in enumerate(del_entries, 1):
                output_lines.append(f'Del_{j:03d}={d}')

            # Riga vuota finale tra versioni
            output_lines.append('')

        else:
            i += 1

    return output_lines


def main():
    root = tk.Tk()
    root.withdraw()

    dat_path = filedialog.askopenfilename(
        title="Seleziona il file renameSET.dat",
        filetypes=[("DAT files", "*.dat"), ("All files", "*.*")]
    )
    if not dat_path:
        return

    try:
        with open(dat_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        ini_lines = parse_rename_set_dat(lines)

        ini_path = os.path.splitext(dat_path)[0] + '.ini'
        with open(ini_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(ini_lines))

        messagebox.showinfo("Successo", f"File INI creato:\n{ini_path}")

    except Exception as e:
        messagebox.showerror("Errore", f"Errore:\n{str(e)}")


if __name__ == '__main__':
    main()