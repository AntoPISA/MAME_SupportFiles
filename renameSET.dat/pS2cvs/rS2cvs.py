import re
import tkinter as tk
from tkinter import filedialog

TITLE = "renameSET2cvs v1.05"

# Elenco completo dei campi nell'ordine richiesto
campi = [
    "versione", "versione progressiva", "data",
    "total items", "drivers", "machines", "parents", "clones", "BIOSes", "devices",
    "requires CHDs", "use samples", "audio mono", "audio stereo", "audio multichannel", "no audio",
    "working", "not working", "mechanicals", "not mechanicals",
    "save supported", "save unsupported",
    "horizontal screen", "vertical screen", "raster graphics", "vector graphics", "lcd graphics", "svg graphics", "screenless",
    "total roms", "machines roms", "devices roms", "BIOSes roms", "CHDs", "sample files", "sample packs",
    "good dumps", "no dumps", "bad dumps", "bugs fixed",
    "software list", "software", "active SL", "orphan SL", "active software", "orphan software",
    "software parents", "software clones", "software roms", "software CHD",
    "supported software", "partially supported software", "unsupported software"
]

def estrai_valore(linea):
    """Estrae solo il primo numero e rimuove i punti"""
    match = re.search(r'^\s*([0-9.]+)', linea.strip())
    if match:
        return match.group(1).replace('.', '')
    return ''

def parse_block(block):
    result = {}

    # Estrai versione e numero progressivo
    ver_match = re.search(r'\$(\d+\.\d+)', block[0])
    num_match = re.search(r'#(\d+)', block[0])
    result["versione"] = ver_match.group(1) if ver_match else ''
    result["versione progressiva"] = num_match.group(1) if num_match else ''

    # Data
    data = block[1].split('/')
    if len(data) == 3:
        result["data"] = f"{data[2]}/{data[1]}/{data[0]}"

    # Campi con regex personalizzate
    campi_regex = {
        'machines': r'([0-9.,]+)\s*machines',
        'parents': r'([0-9.,]+)\s*parents',
        'clones': r'([0-9.,]+)\s*clones',
        'devices': r'([0-9.,]+)\s*devices',
    }

    # Altri campi standard
    altri_campi = {
        'total items': r'([0-9.,]+)\s*total items',
        'drivers': r'([0-9.,]+)\s*drivers',
        'BIOSes': r'([0-9.,]+)\s*BIOSes',
        'requires CHDs': r'([0-9.,]+)\s*requires CHDs',
        'use samples': r'([0-9.,]+)\s*use samples',
        'audio mono': r'([0-9.,]+)\s*audio mono',
        'audio stereo': r'([0-9.,]+)\s*audio stereo',
        'audio multichannel': r'([0-9.,]+)\s*audio multichannel',
        'no audio': r'([0-9.,]+)\s*no audio',
        'working': r'([0-9.,]+)\s*working',
        'not working': r'([0-9.,]+)\s*not working',
        'mechanicals': r'([0-9.,]+)\s*mechanicals',
        'not mechanicals': r'([0-9.,]+)\s*not mechanicals',
        'save supported': r'([0-9.,]+)\s*save supported',
        'save unsupported': r'([0-9.,]+)\s*save unsupported',
        'horizontal screen': r'([0-9.,]+)\s*horizontal screen',
        'vertical screen': r'([0-9.,]+)\s*vertical screen',
        'raster graphics': r'([0-9.,]+)\s*raster graphics',
        'vector graphics': r'([0-9.,]+)\s*vector graphics',
        'lcd graphics': r'([0-9.,]+)\s*lcd graphics',
        'svg graphics': r'([0-9.,]+)\s*svg graphics',
        'screenless': r'([0-9.,]+)\s*screenless',
        'total roms': r'([0-9.,]+)\s*total roms',
        'machines roms': r'([0-9.,]+)\s*machines roms',
        'devices roms': r'([0-9.,]+)\s*devices roms',
        'BIOSes roms': r'([0-9.,]+)\s*BIOSes roms',
        'CHDs': r'([0-9.,]+)\s*CHDs',
        'sample files': r'([0-9.,]+)\s*sample files',
        'sample packs': r'([0-9.,]+)\s*sample packs',
        'good dumps': r'([0-9.,]+)\s*good dumps',
        'no dumps': r'([0-9.,]+)\s*no dumps',
        'bad dumps': r'([0-9.,]+)\s*bad dumps',
        'bugs fixed': r'([0-9.,]+)\s*bugs fixed',
        'software list': r'([0-9.,]+)\s*software list',
        'software': r'([0-9.,]+)\s*software',
        'active SL': r'([0-9.,]+)\s*active SL',
        'orphan SL': r'([0-9.,]+)\s*orphan SL',
        'active software': r'([0-9.,]+)\s*active software',
        'orphan software': r'([0-9.,]+)\s*orphan software',
        'software parents': r'([0-9.,]+)\s*software parents',
        'software clones': r'([0-9.,]+)\s*software clones',
        'software roms': r'([0-9.,]+)\s*software roms',
        'software CHD': r'([0-9.,]+)\s*software CHD',
        'supported software': r'([0-9.,]+)\s*supported software',
        'partially supported software': r'([0-9.,]+)\s*partially supported software',
        'unsupported software': r'([0-9.,]+)\s*unsupported software'
    }

    # Estrai i primi 5 campi problematici separatamente
    for key, pattern in campi_regex.items():
        for line in block[2:]:
            entries = [entry.strip() for entry in line.split(',')]
            for entry in entries:
                match = re.search(pattern, entry)
                if match and key not in result:
                    result[key] = match.group(1).replace('.', '')

    # Estrai gli altri campi
    for line in block[2:]:
        entries = [entry.strip() for entry in line.split(',')]
        for entry in entries:
            for key, pattern in altri_campi.items():
                if key in result:
                    continue
                match = re.search(pattern, entry)
                if match:
                    result[key] = match.group(1).replace('.', '')
                    break

    # Compila output nell'ordine richiesto
    output = []
    for campo in campi:
        output.append(result.get(campo, '0'))

    return output

def main():
    print(f"\n=== {TITLE} ===\nSeleziona il file renameSET.dat...")

    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Seleziona il file renameSET.dat", filetypes=[("DAT Files", "*.dat")])

    if not file_path:
        print("Nessun file selezionato. Uscita.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    print("File caricato. Elaborando dati...")

    blocks = []
    current_block = []

    # Separa i blocchi (ogni blocco inizia con $)
    for line in lines:
        if line.startswith('$'):
            if current_block:
                blocks.append(current_block)
            current_block = [line]
        else:
            current_block.append(line)
    if current_block:
        blocks.append(current_block)

    # Processa tutti i blocchi
    all_output = [campi]
    for block in blocks:
        parsed = parse_block(block)
        all_output.append(parsed)

    # Scrive il CSV
    output_path = file_path.rsplit('.', 1)[0] + ".csv"
    with open(output_path, "w", encoding="utf-8-sig") as csv_file:
        for row in all_output:
            csv_file.write(";".join(row) + "\n")

    print(f"Conversione completata! File salvato come:\n{output_path}")

if __name__ == "__main__":
    main()