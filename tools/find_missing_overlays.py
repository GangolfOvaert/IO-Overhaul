#!/usr/bin/env python3
"""
Scans .sbc files and lists definitions that have 1 or fewer <Icon> tags.
Usage: python3 tools/find_missing_overlays.py
"""
from pathlib import Path
import xml.etree.ElementTree as ET

def main():
    # Scan the Space Engineers installation directory
    root_dir = Path("/home/chris/.local/share/Steam/steamapps/common/SpaceEngineers/Content")
    
    print(f"Scanning {root_dir} for definitions without composite icons...")
    
    missing_overlays = []

    for sbc_path in root_dir.rglob("*.sbc"):
        try:
            tree = ET.parse(sbc_path)
            root = tree.getroot()
        except Exception as e:
            print(f"Skipping {sbc_path.name}: {e}")
            continue

        # Iterate over all elements to find those with an <Id> block
        for elem in root.iter():
            id_node = elem.find("Id")
            if id_node is not None:
                type_id = id_node.find("TypeId")
                subtype_id = id_node.find("SubtypeId")

                # Ensure it's a valid definition
                if type_id is not None and subtype_id is not None:
                    # Count <Icon> tags in the definition element
                    icons = elem.findall("Icon")
                    
                    # If 1 or 0 icons, it has no overlay
                    if len(icons) <= 1:
                        t_text = type_id.text if type_id.text else "Unknown"
                        s_text = subtype_id.text if subtype_id.text else "Unknown"
                        missing_overlays.append(f"[{sbc_path.name}] {t_text}/{s_text}")

    # Output results to tools/result.txt
    out_file = Path(__file__).parent / "result.txt"
    with open(out_file, "w") as f:
        for item in sorted(missing_overlays):
            f.write(item + "\n")
            
    print(f"Found {len(missing_overlays)} items. List saved to {out_file.resolve()}")

if __name__ == "__main__":
    main()