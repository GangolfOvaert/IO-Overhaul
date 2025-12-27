#!/usr/bin/env python3
"""
Export .sbc <Definition> entries grouped by <Id><TypeId> into one .sbc per TypeId,
then remove the exported <Definition> elements from the original .sbc files.

Usage:
  python3 tools/split_and_prune.py --root . --out ./out_sbc_by_type --backup ./sbc_backups

Options:
  --root    root directory to scan for .sbc files (default: .)
  --out     output directory for per-TypeId .sbc files (default: out_sbc_by_type)
  --backup  directory where original .sbc backups are written (default: backups)
  --force   overwrite existing files in output (default: False)
"""
from pathlib import Path
import argparse
import xml.etree.ElementTree as ET
from collections import defaultdict
from copy import deepcopy
import shutil

# namespace URIs
XSI = "http://www.w3.org/2001/XMLSchema-instance"
XSD = "http://www.w3.org/2001/XMLSchema"

def register_namespaces():
    ET.register_namespace('xsi', XSI)
    ET.register_namespace('xsd', XSD)

def collect_definitions(root_dir: Path):
    groups = defaultdict(list)
    files_with_defs = defaultdict(list)  # path -> list of TypeId found (for pruning)
    for p in root_dir.rglob("*.sbc"):
        try:
            tree = ET.parse(p)
            rt = tree.getroot()
        except Exception as e:
            print(f"skip (parse error) {p}: {e}")
            continue
        cubeblocks = rt.find("CubeBlocks")
        if cubeblocks is None:
            continue
        found = []
        for d in list(cubeblocks.findall("Definition")):
            tid_elem = d.find("Id/TypeId")
            if tid_elem is None or (tid_elem.text is None):
                continue
            typeid = tid_elem.text.strip()
            groups[typeid].append(deepcopy(d))
            found.append(typeid)
        if found:
            files_with_defs[p] = found
    return groups, files_with_defs

def build_definitions_tree(defs_list):
    register_namespaces()
    root = ET.Element("Definitions")
    cube = ET.SubElement(root, "CubeBlocks")
    for d in defs_list:
        cube.append(d)
    ET.SubElement(root, "BlueprintClasses")
    ET.SubElement(root, "BlueprintClassEntries")
    return root

def write_tree_pretty(root_elem: ET.Element, out_path: Path):
    try:
        ET.indent(root_elem, space="  ")
    except Exception:
        pass
    tree = ET.ElementTree(root_elem)
    tree.write(out_path, encoding="utf-8", xml_declaration=True)

def safe_backup(file_path: Path, backup_root: Path):
    rel = file_path.resolve().relative_to(Path.cwd().resolve())
    dest = backup_root / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(file_path, dest)

def prune_originals(files_with_defs: dict, exported_typeids: set, backup_root: Path):
    register_namespaces()
    for p, _ in files_with_defs.items():
        try:
            tree = ET.parse(p)
            rt = tree.getroot()
        except Exception as e:
            print(f"skip (parse error) {p}: {e}")
            continue
        cube = rt.find("CubeBlocks")
        if cube is None:
            continue
        # Backup before modifying
        safe_backup(p, backup_root)
        removed = 0
        for d in list(cube.findall("Definition")):
            tid_elem = d.find("Id/TypeId")
            if tid_elem is None or (tid_elem.text is None):
                continue
            if tid_elem.text.strip() in exported_typeids:
                cube.remove(d)
                removed += 1
        if removed:
            try:
                ET.indent(rt, space="  ")
            except Exception:
                pass
            tree.write(p, encoding="utf-8", xml_declaration=True)
            print(f"Pruned {removed} definitions from {p}")

def sanitize_filename(name: str) -> str:
    keep = "-_.()abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    s = "".join(c if c in keep else "_" for c in name)
    return s.strip("_") or "unknown"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", "-r", default=".", help="root dir to scan for .sbc files")
    ap.add_argument("--out", "-o", default="out_sbc_by_type", help="output directory")
    ap.add_argument("--backup", "-b", default="sbc_backups", help="backup dir for originals")
    ap.add_argument("--force", "-f", action="store_true", help="overwrite existing output files")
    args = ap.parse_args()

    root_dir = Path(args.root).resolve()
    out_dir = Path(args.out).resolve()
    backup_dir = Path(args.backup).resolve()

    # prepare out dir
    out_dir.mkdir(parents=True, exist_ok=True)
    if args.force:
        for p in out_dir.glob("*.sbc"):
            p.unlink()

    groups, files_with_defs = collect_definitions(root_dir)
    if not groups:
        print("No definitions found.")
        return

    # write one file per TypeId
    for typeid, defs in groups.items():
        tree_root = build_definitions_tree(defs)
        fname = sanitize_filename(f"{typeid}.sbc")
        out_path = out_dir / fname
        if out_path.exists() and not args.force:
            print(f"Skipping existing {out_path} (use --force to overwrite)")
            continue
        write_tree_pretty(tree_root, out_path)
        print(f"Wrote {len(defs)} definitions to {out_path}")

    # prune originals (backup first)
    backup_dir.mkdir(parents=True, exist_ok=True)
    exported_typeids = set(groups.keys())
    prune_originals(files_with_defs, exported_typeids, backup_dir)
    print("Done. Backups of modified files are in:", backup_dir)

if __name__ == "__main__":
    main()