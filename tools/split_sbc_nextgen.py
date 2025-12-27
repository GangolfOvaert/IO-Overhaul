#!/usr/bin/env python3
"""
Collect air-related CubeBlock definitions from the vanilla Content and
write them into Data/CubeBlocks/air.sbc in this mod.
"""
from pathlib import Path
import xml.etree.ElementTree as ET
from copy import deepcopy

CONTENT_DIR = Path("/home/chris/.local/share/Steam/steamapps/common/SpaceEngineers/Content")
OUTPUT_PATH = Path(__file__).parents[1] / "Data" / "CubeBlocks" / "air.sbc"

TARGET_TYPEIDS = {
    "AirVent",
    "AirtightHangarDoor",
    "AirtightSlideDoor",
    "OxygenTank",
    "OxygenGenerator",
    "OxygenFarm",
    "Parachute",
}

def local(tag: str) -> str:
    return tag.split("}", 1)[1] if "}" in tag else tag

def wants(type_id: str, subtype_id: str) -> bool:
    if type_id in TARGET_TYPEIDS:
        return True
    if type_id == "CubeBlock" and subtype_id.startswith("AirDuct"):
        return True
    if type_id == "InteriorLight" and "AirDuct" in subtype_id:
        return True
    return False

def collect():
    picked = []
    for sbc in CONTENT_DIR.rglob("*.sbc"):
        try:
            tree = ET.parse(sbc)
            root = tree.getroot()
        except Exception:
            continue
        cube = root.find("CubeBlocks")
        if cube is None:
            continue
        for d in cube.findall("Definition"):
            id_node = d.find("Id")
            if id_node is None:
                continue
            tid = (id_node.findtext("TypeId") or "").strip()
            sid = (id_node.findtext("SubtypeId") or "").strip()
            if not sid:
                continue
            if wants(tid, sid):
                picked.append(deepcopy(d))
    return picked

def write_output(defs):
    # build minimal Definitions doc
    root = ET.Element("Definitions", {"xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"})
    cube = ET.SubElement(root, "CubeBlocks")
    for d in defs:
        cube.append(d)
    ET.SubElement(root, "BlueprintClasses")
    ET.SubElement(root, "BlueprintClassEntries")
    try:
        ET.indent(root, space="  ")
    except Exception:
        pass
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    tree = ET.ElementTree(root)
    tree.write(OUTPUT_PATH, encoding="utf-8", xml_declaration=True)

def main():
    defs = collect()
    if not defs:
        print("No air-related definitions found.")
        return
    write_output(defs)
    print(f"Wrote {len(defs)} definitions to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()