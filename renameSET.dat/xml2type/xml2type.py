#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
xml2type.py - Estrae e salva 3 tipi diversi di machine da un file XML MAME:
- bios
- device
- mechanical
Supporta anche vecchi file con <game> al posto di <machine>

(C) 2025 AntoPISA www.progettosnaps.net v.1.3
"""

import os
from tkinter import Tk, filedialog
from lxml import etree
from tqdm import tqdm


def select_xml_file():
    """Apre una finestra di dialogo per selezionare il file XML"""
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Seleziona un file XML",
        filetypes=[("XML files", "*.xml")]
    )
    return file_path


def extract_machines_by_attribute(root, attribute, value):
    """Estrae dal nodo radice solo i nodi <machine> o <game> con l'attributo specifico uguale al valore dato"""
    new_root = etree.Element("mame")

    # Copia gli attributi principali del nodo <mame>
    for attr in root.attrib:
        new_root.set(attr, root.get(attr))

    # Prova prima con <machine>
    machines = list(root.findall("machine"))
    if not machines:
        print("⚠️ Nessun nodo <machine> trovato, provo con <game>...")
        machines = list(root.findall("game"))

    filtered = []

    for machine in tqdm(machines, desc=f"Estrazione {attribute}='{value}'", leave=False, ncols=70):
        if machine.get(attribute) == value:
            # Cambia il tag da game a machine se necessario
            if machine.tag != "machine":
                machine.tag = "machine"
            filtered.append(machine)

    for m in filtered:
        new_root.append(m)

    return etree.ElementTree(new_root)


def write_output_file(tree, input_file, suffix):
    """Salva il nuovo file XML aggiungendo un suffisso al nome originale"""
    dir_name = os.path.dirname(input_file)
    base_name = os.path.basename(input_file)
    name, ext = os.path.splitext(base_name)
    output_file = os.path.join(dir_name, f"{name}_{suffix}{ext}")

    with open(output_file, "wb") as f:
        f.write(etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding="utf-8"))

    print(f"✅ File salvato: {output_file}")
    return output_file


def main():
    print("xml2type v1.3 - Estrattore multiplo da XML MAME (supporto <machine> e <game>)")
    input_file = select_xml_file()
    if not input_file:
        print("Nessun file selezionato.")
        return

    print(f"📄 File selezionato: {input_file}")

    try:
        # Carica il file XML in modo sicuro
        with open(input_file, "rb") as f:
            xml_content = f.read().decode("ISO-8859-1")

        parser = etree.XMLParser(remove_blank_text=True, recover=True)
        root = etree.fromstring(xml_content.encode("utf-8"), parser=parser)

        # Estrai e salva per ogni categoria
        categories = [
            {"attr": "isbios", "value": "yes", "suffix": "bios"},
            {"attr": "isdevice", "value": "yes", "suffix": "device"},
            {"attr": "ismechanical", "value": "yes", "suffix": "mechanical"}
        ]

        print("\n🔍 Inizio estrazione dei dati...\n")

        for cat in categories:
            tqdm.write(f"🔧 Elaborando categoria: {cat['suffix'].upper()}")
            filtered_tree = extract_machines_by_attribute(root, cat["attr"], cat["value"])
            output_file = write_output_file(filtered_tree, input_file, cat["suffix"])

        print("\n🎉 Tutti i file sono stati generati correttamente.")

    except Exception as e:
        print(f"\n🚨 Si è verificato un errore durante l'elaborazione: {e}")


if __name__ == "__main__":
    main()