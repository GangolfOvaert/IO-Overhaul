#!/usr/bin/env python3
"""
Scan Space Engineers Content for Blocks, Components, and Physical Items,
and list their SubtypeIds into tools/report.txt.

- Blocks: any <Definition> under <CubeBlocks>
- Components: Id/TypeId == Component
- Physical Items: Id/TypeId in ALLOWED_PHYSICAL
"""
from pathlib import Path
import xml.etree.ElementTree as ET
from collections import defaultdict

CONTENT_DIR = Path("/home/chris/.local/share/Steam/steamapps/common/SpaceEngineers/Content")
REPORT_PATH = Path(__file__).parent / "report.txt"

ALLOWED_PHYSICAL = {
    "PhysicalItem", "PhysicalObject",
    "Ore", "Ingot",
    "AmmoMagazine",
    "ConsumableItem",
    "Tool",
    "GasContainerObject", "OxygenContainerObject",
    "Datapad",
    "Package",
}

def local(tag: str) -> str:
    return tag.split("}", 1)[1] if "}" in tag else tag

def collect():
    blocks = set()
    components = set()
    physicals = set()
    file_count = 0

    for sbc_path in CONTENT_DIR.rglob("*.sbc"):
        file_count += 1
        try:
            tree = ET.parse(sbc_path)
            root = tree.getroot()
        except Exception as e:
            print(f"Skipping {sbc_path}: {e}")
            continue

        # Blocks: Definitions under CubeBlocks
        cb = root.find("CubeBlocks")
        if cb is not None:
            for d in cb.findall("Definition"):
                id_node = d.find("Id")
                if id_node is not None:
                    tid = id_node.findtext("TypeId", "").strip()
                    sid = id_node.findtext("SubtypeId", "").strip()
                    if sid:
                        blocks.add(f"{tid or 'Block'}/{sid}")

        # Components & Physical items: scan all Id nodes
        for id_node in root.iter():
            if local(id_node.tag) != "Id":
                continue
            tid = id_node.findtext("TypeId", "").strip()
            sid = id_node.findtext("SubtypeId", "").strip()
            if not sid:
                continue
            if tid == "Component":
                components.add(f"{tid}/{sid}")
            elif tid in ALLOWED_PHYSICAL:
                physicals.add(f"{tid}/{sid}")

    return file_count, blocks, components, physicals

def main():
    print(f"Scanning {CONTENT_DIR} ...")
    files, blocks, comps, phys = collect()

    lines = []
    lines.append(f"# Files scanned: {files}")
    lines.append("")
    lines.append("[Blocks]")
    lines.extend(sorted(blocks))
    lines.append("")
    lines.append("[Components]")
    lines.extend(sorted(comps))
    lines.append("")
    lines.append("[PhysicalItems]")
    lines.extend(sorted(phys))

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote report to {REPORT_PATH.resolve()}")
    print(f"Blocks: {len(blocks)}, Components: {len(comps)}, Physical items: {len(phys)}")

if __name__ == "__main__":
    main()