#!/usr/bin/env python3
"""
Extract all SubtypeId values from PhysicalItems_T1..T5.sbc and write them to T1.txt..T5.txt
(default data directory: ./Data). One value per line, unique & sorted.
"""
from pathlib import Path
import xml.etree.ElementTree as ET

DATA_DIR = Path(__file__).resolve().parents[1] / "Data"  # ../Data relative to tools/
FILES = [f"PhysicalItems_T{n}.sbc" for n in range(1, 6)]

def local_tag(elem):
    # strip namespace if present
    tag = elem.tag
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag

def extract_subtypeids(path: Path):
    try:
        tree = ET.parse(path)
    except Exception as e:
        print(f"skip {path}: {e}")
        return []
    root = tree.getroot()
    ids = []
    # find any element whose local name equals subtypeid (case-insensitive)
    for elem in root.iter():
        if local_tag(elem).lower() == "subtypeid":
            if elem.text and elem.text.strip():
                ids.append(elem.text.strip())
    # deduplicate & sort
    return sorted(set(ids))

def main():
    for fname in FILES:
        inpath = DATA_DIR / fname
        outname = f"T{fname.split('_T')[-1].split('.')[0]}.txt"  # PhysicalItems_T1.sbc -> T1.txt
        outpath = DATA_DIR / outname
        if not inpath.exists():
            print(f"missing {inpath} -> skipping")
            continue
        ids = extract_subtypeids(inpath)
        outpath.write_text("\n".join(ids) + ("\n" if ids else ""))
        print(f"Wrote {len(ids)} entries to {outpath}")

if __name__ == "__main__":
    main()