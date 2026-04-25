# NextGen Mod – Context Template for New Sessions

This file gives a new AI session the essential context to continue work on the NextGen Space Engineers mod without reading the entire codebase from scratch. Read this alongside `README.md`.

---

## What This Mod Does

Replaces Space Engineers' default progression with a **multi-tier industrial chain** (T1–T6). Players start with primitive iron-based T1 components and unlock increasingly advanced materials and machines at each tier. Requires Industrial Overhaul (IO) mod as a dependency for models and icons.

---

## File Architecture

```
SpaceEngineersMod/Data/
├── Tier1/                          # All T1 definitions
│   ├── Components_T1_Component.sbc     # T1 component items
│   ├── Blueprints_T1_Components.sbc    # T1 component recipes
│   ├── BlueprintClasses_T1.sbc         # T1 blueprint class + entry definitions
│   ├── PhysicalItems_T1_Ores*.sbc      # T1 ore variants (normal/impure/pure)
│   ├── PhysicalItems_T1_Ingots.sbc     # T1 ingot items
│   ├── Blueprints_T1_Refining.sbc      # T1 ore → ingot recipes
│   └── CubeBlocks_T1_*.sbc             # T1 block overrides (one file per category)
│
├── Tier2/                          # All T2 definitions (same structure as T1)
│   ├── Components_T2_Component.sbc
│   ├── Blueprints_T2_Components.sbc
│   ├── BlueprintClasses_T2.sbc
│   ├── PhysicalItems_T2_Ores*.sbc
│   ├── PhysicalItems_T2_Ingots.sbc
│   ├── Blueprints_T2_Refining.sbc
│   ├── CubeBlocks_T2_Assembler.sbc         # T2 general assembler
│   ├── CubeBlocks_T2_Assembler_Production.sbc  # Furnace, ElecFab, Press, Extruder, Fabricator
│   ├── CubeBlocks_T2_Refinery.sbc
│   ├── CubeBlocks_T2_Battery.sbc
│   ├── CubeBlocks_T2_Gyroscope.sbc
│   ├── CubeBlocks_T2_Thrusters.sbc
│   └── CubeBlocks_T2_OxygenGenerator.sbc
│
├── Overrides/
│   ├── CubeBlocks_IO_Disabled.sbc      # IO production blocks disabled (we replace them)
│   └── CubeBlocks_SurvivalKit_Disabled.sbc
│
├── Blueprints/                     # IO blueprint overrides (passthrough)
├── PhysicalItems/                  # IO item overrides (passthrough)
├── BlockCategories_IndustryNG.sbc  # In-game G-menu category entries
└── BlockVariantGroups.sbc          # Refinery variant group
```

**Rule:** When adding a new tier, mirror the Tier1/Tier2 structure exactly. Each tier needs: Components, Blueprints, BlueprintClasses, PhysicalItems (ores + ingots), Blueprints_Refining, and CubeBlocks files.

---

## Core Mechanics

### 1. Component System

Each tier defines its own components in `Components_T<N>_Component.sbc`. Components are `<TypeId>Component</TypeId>` items with a SubtypeId. Use `<IconSymbol>T1</IconSymbol>` (or T2, etc.) to show the tier badge in-game.

**IronFrame sizing rule — critical:**
- `IronFrameS` → small grid blocks OR small large-grid blocks
- `IronFrameL` → standard large grid blocks
- `IronFrameXL` → large grid blocks that are 3×3 footprint or bigger
- IronFrame (matching size) must **always be the first component** in a block's `<Components>` list.

### 2. Blueprint Classes (Production UI Tabs)

A `BlueprintClass` defines one tab shown inside a production block's UI. Defined in `BlueprintClasses_T<N>.sbc` with two sections:

- `<BlueprintClasses>` — declares the class (name, icon, display name)
- `<BlueprintClassEntries>` — maps blueprint SubtypeIds to classes

A production block references which tabs to show via `<BlueprintClasses>` in the block definition:

```xml
<BlueprintClasses>
    <Class>T1Stamp</Class>
    <Class>T2Stamp</Class>
</BlueprintClasses>
```

**Inheritance rule:** T2 blocks reference both the T1 and T2 class. This gives them two tabs — one with T1 recipes, one with T2 recipes. T1 entries stay in `BlueprintClasses_T1.sbc`; T2 entries stay in `BlueprintClasses_T2.sbc`. No duplication. For T3, add a third `<Class>T3Stamp</Class>` reference on the block.

### 3. Block Overrides

A `.sbc` file with the same `SubtypeId` as a vanilla or IO block **replaces** that block's definition. This is how T2 batteries, thrusters, and O2 generators work — they reuse vanilla SubtypeIds but have updated component requirements.

### 4. G-Menu Categories

All new blocks must be added to `BlockCategories_IndustryNG.sbc` to appear in the in-game toolbar. Format:

```xml
<string>TypeId/SubtypeId</string>
```

Common TypeIds: `Assembler`, `Refinery`, `BatteryBlock`, `Reactor`, `WindTurbine`, `SurvivalKit`, `OxygenGenerator`, `Thrust`.

---

## T1 Components (complete list)

| SubtypeId | Description | Machine |
|---|---|---|
| IronPlate | Flat sheet | Hydraulic Press |
| IronRod | Solid bar | Metal Extruder |
| IronBolt | Fastener | Hydraulic Press |
| IronTube | Small hollow cylinder | Metal Extruder |
| IronPipe | Large hollow cylinder | Metal Extruder |
| MagnesiumPressedPlate | Lightweight structural plate | Hydraulic Press |
| NickelBall | Rounded nickel bearing blank | Hydraulic Press |
| SimpleBearing | Rotational part | Fabricator |
| IronFrameS | Small structural frame | Fabricator |
| IronFrameL | Large structural frame | Fabricator |
| IronFrameXL | Extra-large structural frame | Fabricator |
| Concrete | Cement block | Assembling Bench / Cement Kiln |
| T1_EnergyCell | Primitive energy storage | Assembling Bench |

## T2 Components (complete list)

| SubtypeId | Description | Machine |
|---|---|---|
| Glass | Transparent panel | Furnace |
| SiliciumWafer | Pure silicon slice | Electronics Fabricator |
| CarbonBlock | Fused carbon material | Furnace |
| SimplePCB | Basic circuit board (+ 1 CopperWire) | Electronics Fabricator |
| CopperWire | Drawn copper conductor | Metal Extruder / Electronics Fabricator |
| ComputerChip | Integrated circuit (+ 1 CopperWire) | Electronics Fabricator |
| BasicComputer | Assembled computing unit | Electronics Fabricator |
| Display | Screen assembly | Electronics Fabricator |
| Sensors | Sensor array | Electronics Fabricator |
| MedicalComponents | Medical sub-assembly | Electronics Fabricator |
| CobaltPlate | Dense alloy plate | Hydraulic Press |
| T2_PowerCell | Rechargeable cobalt cell (+ 2 CopperWire) | Electronics Fabricator |
| T2_ThrustComponent | Impeller/fan assembly | Fabricator |
| AluminumPlate | Lightweight structural sheet | Hydraulic Press |
| AluminumRod | Lightweight solid bar | Metal Extruder |
| AluminumFrameS | Small aluminium structural frame | Fabricator |
| AluminumFrameL | Large aluminium structural frame | Fabricator |
| AluminumFrameXL | XL aluminium structural frame | Fabricator |

**Never use in T1:** CopperWire, ComputerChip, BasicComputer, Display, Sensors, MedicalComponents, CobaltPlate, T2_PowerCell, T2_ThrustComponent, AluminumPlate, AluminumRod, AluminumFrameS, AluminumFrameL, AluminumFrameXL.

---

## T2 Production Blocks & Blueprint Classes

| Block | SubtypeId | TypeId | T1 Class (tab) | T2 Class (tab) | T2 Recipes |
|---|---|---|---|---|---|
| T2 Refinery | LargeRefineryT2 | Refinery | — | T2Refining | T2 ores → ingots |
| T2 Assembler | T2_Assembler | Assembler | T1AssemblingBench | T2AssemblingBench | All T2 components |
| Furnace | T2_Furnace | Assembler | — | T2Furnace | Glass, CarbonBlock |
| Electronics Fabricator | T2_ElectronicsFabricator | Assembler | — | T2ElectronicsFabricator | CopperWire, Electronics, PowerCell |
| T2 Hydraulic Press | T2_HydraulicPress | Assembler | T1Stamp | T2Stamp | CobaltPlate, AluminumPlate |
| T2 Metal Extruder | T2_MetalExtruder | Assembler | T1Extruder | T2Extruder | CopperWire, AluminumRod |
| T2 Fabricator | T2_Fabricator | Assembler | T1Fabricator | T2Fabricator | ComputerChip, ThrustComponent, AluminumFrameS/L/XL |
| Battery Block (Large) | LargeBlockBatteryBlock | BatteryBlock | — | — | Overrides vanilla; 12 MW / 3 MWh; `AluminumFrameL` first; `T2_PowerCell` critical |
| Battery Block (Small) | SmallBlockBatteryBlock | BatteryBlock | — | — | Overrides vanilla; 1 MW / 0.2 MWh; `AluminumFrameS` first; `T2_PowerCell` critical |
| Gyroscope (Large) | LargeBlockGyro | Gyro | — | — | Overrides vanilla; `BasicComputer` critical; `AluminumFrameL` first |
| Gyroscope (Small) | SmallBlockGyro | Gyro | — | — | Overrides vanilla; `BasicComputer` critical; `AluminumFrameS` first |

---

## What Does NOT Belong in T1

- `CopperWire` — T2 only (Metal Extruder)
- `advMotor` — T2 only
- `Computer`, `Display`, `Fabric`, `Electromagnet`, `HeatingElement`, `Ceramic` — removed from all T1 block recipes
- Wheel suspensions, tires, RealWheels — T2 (only `MetalWheel3x3` and its suspension are T1)

---

## Naming Conventions

| Thing | Convention | Example |
|---|---|---|
| T1 block SubtypeIds | `T1_<Name>` | `T1_HydraulicPress` |
| T2 block SubtypeIds | `T2_<Name>` | `T2_HydraulicPress` |
| T1 component SubtypeIds | PascalCase, no prefix | `IronPlate`, `SimpleBearing` |
| T2 component SubtypeIds | PascalCase, `T2_` only for new T2-specific items | `CobaltPlate`, `T2_PowerCell` |
| T1 blueprint SubtypeIds | `T1_<Result>` | `T1_IronPlate` |
| T2 blueprint SubtypeIds | `T2_<Result>` | `T2_CobaltPlate` |
| Blueprint class SubtypeIds | `T<N><Function>` | `T2Stamp`, `T1Fabricator` |
| Block category file entries | `TypeId/SubtypeId` | `Assembler/T2_Furnace` |

---

## Pending / In-Progress Work

- **IronMesh** — new T1 component (woven metal mesh); needs: component definition, blueprint recipe, BlueprintClass entry, used in MetalWheel3x3 construction
- **T3 tier** — not started; `Data/Tier3/` exists but only has Heavy Armor placeholder
- **Silver** — T2 ingot exists, no component recipes yet
- **T1 AssemblingBench** — stops at T1; no T2 or higher equivalent (by design)
