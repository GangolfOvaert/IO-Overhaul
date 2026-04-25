# SpaceEngineersMod – Industry Progression

A tiered industrial progression mod for Space Engineers. Replaces Industrial Overhaul's production system with a custom multi-tier crafting chain, starting with primitive iron-based Tier 1 components and progressing through increasingly advanced materials.

---

## Dependencies

| Dependency | Required | Notes |
|---|---|---|
| Space Engineers | Yes | Base game |
| Industrial Overhaul (Steam ID: 2344068716) | Yes | Models and icons are reused; IO production blocks are disabled |
| Apex Survival DLC | Optional | Enables reskinned Survival Kit variants |

---

## Project Structure

```
SpaceEngineersMod/
├── Data/
│   ├── Tier1/                  # Tier 1 blocks, blueprints, components
│   ├── Tier2/                  # Tier 2 ore definitions and refining recipes
│   ├── Blueprints/             # IO blueprint overrides
│   ├── PhysicalItems/          # IO item overrides
│   ├── Overrides/              # Blocks disabled from Industrial Overhaul
│   ├── BlockVariantGroups_Refineries.sbc
│   └── ...                     # Vanilla overrides and shared definitions
├── Icons/                      # Tier icons (t1.dds – t6.dds)
├── metadata.mod                # Mod metadata
├── modinfo.sbmi                # Workshop metadata
└── README.md
```

---

## Progression Overview

| Tier | Status | Ores | Refining Time |
|---|---|---|---|
| Tier 1 | Complete | Iron, Nickel, Silicon, Magnesium, Stone | 750s |
| Tier 2 | In Progress | Cobalt, Silver, Aluminium, Copper, Carbon | 1500s |
| Tier 3–6 | Planned | – | – |

Icons for Tiers 1–6 exist (`Icons/t1.dds` – `Icons/t6.dds`). Blueprint class slots and refinery variant group placeholders are already prepared for future tiers.

---

## Ore Purity System

Every ore type exists in three purity variants. Input is always 1,000 ore per batch; only the yield differs.

| Purity | Yield | T1 Refining Time | T2 Refining Time |
|---|---|---|---|
| Impure | 250 (25%) | 750s | 1500s |
| Normal | 600 (60%) | 750s | 1500s |
| Pure | 800 (80%) | 750s | 1500s |

---

## Tier 1

### Ores

| Ore | SubtypeId |
|---|---|
| Stone | Stone |
| Iron | Iron |
| Nickel | Nickel |
| Silicon | Silicon |
| Magnesium | Magnesium |

### Stone Processing

Stone is handled as a special multi-output recipe in the T1 Refinery.

| Input | Output | Time |
|---|---|---|
| 100,000 Stone | 50,000 Gravel + 3,000 Iron Ingot + 3,000 Nickel Ingot + 3,000 Silicon Ingot | 15,000s |

### Components

Defined in `Data/Tier1/Components_T1_Component.sbc`.

| Component | SubtypeId | Description |
|---|---|---|
| Iron Plate | IronPlate | Basic flat metal sheet |
| Iron Rod | IronRod | Solid metal bar |
| Iron Bolt | IronBolt | Fastener |
| Iron Tube | IronTube | Small hollow cylinder |
| Iron Pipe | IronPipe | Large hollow cylinder |
| Magnesium Pressed Plate | MagnesiumPressedPlate | Lightweight structural plate |
| Simple Bearing | SimpleBearing | Basic rotational component |
| Iron Frame (S) | IronFrameS | Small structural frame |
| Iron Frame (L) | IronFrameL | Large structural frame |
| Iron Frame (XL) | IronFrameXL | Extra-large structural frame |
| Ice Energy Cell | T1_EnergyCell | Primitive energy storage; fuel for T1 Reactor |

### Component Crafting Recipes

Defined in `Data/Tier1/Blueprints_T1_Components.sbc`.

| Result | Input | Time |
|---|---|---|
| 1 Iron Rod | 1 Iron Ingot | 5s |
| 1 Iron Plate | 1 Iron Ingot | 10s |
| 2 Iron Bolts | 1 Iron Rod | 10s |
| 1 Iron Tube | 4 Iron Rods | 10s |
| 1 Iron Pipe | 2 Iron Rods | 15s |
| 1 Magnesium Pressed Plate | 10 Magnesium Ingots | 15s |
| 1 Simple Bearing | 8 Iron Rods + 1 Iron Tube | 20s |
| 1 Iron Frame (S) | 12 Iron Rods + 24 Iron Bolts | 20s |
| 1 Iron Frame (L) | 24 Iron Rods + 16 Iron Bolts + 2 Iron Plates | 30s |
| 1 Iron Frame (XL) | 48 Iron Rods + 32 Iron Bolts + 4 Iron Plates | 50s |
| 1 Energy Cell | 100 Ice | 60s |
| 1 Energy Cell | – (atmospheric extraction) | 1200s |

### Production Blocks

#### Survival Kit

Entry-point block. Handles emergency respawn and primitive crafting. Available in large/small grid and Apex DLC reskin variants.

| Property | Value |
|---|---|
| Size | 1×1×1 (Large) / 4×3×3 (Small) |
| Power | 0.2 MW |
| Assembly Speed | 0.15 |
| Blueprint Classes | T1SurvivalKitIngots, T1SurvivalKitComponents |
| Construction (Large) | 30 Steel Plate, 2 Construction, 3 Medical, 4 Motor, 1 Display, 5 Computer |

#### Assembling Bench

Manual crafting workbench. Slowest throughput but can craft all T1 items. Built from vanilla components; no T1 components required.

| Property | Value |
|---|---|
| Size | 1×1×1 (Large) |
| Power | 0 MW |
| Assembly Speed | 0.25 |
| Blueprint Class | T1Bench |
| Construction | 20 Steel Plate, 10 Large Tube, 15 Construction |

#### Metal Extruder

Specialized block for forming rods, tubes, and pipes.

| Property | Value |
|---|---|
| Size | 2×1×1 (Large) |
| Power | 0.5 MW |
| Assembly Speed | 0.75 |
| Blueprint Class | T1Extruder |
| Critical Component | Simple Bearing |
| Construction | 80 Iron Plate, 30 Iron Rod, 40 Iron Bolt, 15 Iron Tube, 6 Simple Bearing, 4 Iron Frame (S) |

#### Hydraulic Press

Specialized block for forming plates and screws.

| Property | Value |
|---|---|
| Size | 2×3×3 (Large) |
| Power | 0.5 MW |
| Assembly Speed | 0.75 |
| Blueprint Class | T1Stamp |
| Critical Component | Simple Bearing |
| Construction | 100 Iron Plate, 40 Iron Rod, 60 Iron Bolt, 10 Iron Pipe, 8 Simple Bearing, 4 Iron Frame (L) |

#### Fabricator

General-purpose assembler for composite parts.

| Property | Value |
|---|---|
| Size | 1×1×1 (Large) |
| Power | 0.5 MW |
| Assembly Speed | 0.75 |
| Blueprint Class | T1Fabricator |
| Critical Component | Simple Bearing |
| Construction | 50 Iron Plate, 20 Iron Rod, 30 Iron Bolt, 10 Iron Tube, 5 Iron Pipe, 4 Simple Bearing, 2 Iron Frame (S) |

#### Tier 1 Refinery

Processes T1 ores into ingots. Built from vanilla components (not T1 components).

| Property | Value |
|---|---|
| Size | 2×4×2 (Large) |
| Power | 3 MW |
| Refine Speed | 2× |
| Blueprint Class | T1Refining |
| Critical Component | Computer |
| Construction | 300 Steel Plate, 40 Construction, 20 Large Tube, 20 Metal Grid, 16 Motor, 25 Electromagnet, 50 Heating Element, 20 Computer |

#### T1 Small Reactor

Primitive power source. Burns T1 Energy Cells instead of uranium.

| Property | Value |
|---|---|
| Size | 1×1×1 (Large) |
| Max Power Output | 1.5 MW |
| Fuel | T1_EnergyCell |
| Critical Component | Iron Frame (S) |
| Construction | 40 Iron Plate, 20 Iron Rod, 8 Iron Tube, 20 Iron Bolt, 4 Simple Bearing, 2 Iron Frame (S) |

### Blocks (from Industrial Overhaul)

| Category | Block | SubtypeId |
|---|---|---|
| Energy | Wind Turbine T1 | LargeBlockWindTurbinet1 |
| Energy | Large Wind Turbine T1 | LargeWindTurbine |
| Energy | Alkaline Battery (Large) | LargeBlockAlkalineBatteryBlock |
| Energy | Small Alkaline Battery | SmallBlockSmallAlkalineBatteryBlock |
| Refining | Smelter T1 | Blast Furnace |
| Refining | Rock Crusher T1 | RockCrusher |
| Refining | Ore Purifier T1 | OrePurifier |
| Refining | Refinery T1 | LargeRefineryt1 |
| Refining | Incinerator | Incinerator |
| Production | Cement Kiln | CementKiln |
| Mobility | Speeder Cockpit | SpeederCockpit |
| Mobility | Speeder Cockpit Compact | SpeederCockpitCompact |
| Mobility | Buggy Cockpit | BuggyCockpit |
| Mobility | Rover Cockpit | RoverCockpit |
| Storage | Oxygen Tank Small | OxygenTankSmall |
| Infrastructure | Air Duct 1 | AirDuct1 |
| Infrastructure | Air Duct 2 | AirDuct2 |
| Infrastructure | Air Duct Light | AirDuctLight |
| Infrastructure | Air Duct Corner | AirDuctCorner |
| Infrastructure | Air Duct T | AirDuctT |
| Infrastructure | Air Duct X | AirDuctX |
| Infrastructure | Air Duct Ramp | AirDuctRamp |
| Infrastructure | Air Duct Grate | AirDuctGrate |

### Blocks (from Vanilla Game)

| Category | Block | SubtypeId |
|---|---|---|
| Armor | Light Armor (all variants) | See CubeBlocks_T1_LightArmor.sbc |
| Blast Doors | Blast Door Center (Large) | ArmorCenter |
| Blast Doors | Blast Door Corner (Large) | ArmorCorner |
| Blast Doors | Blast Door Inv Corner (Large) | ArmorInvCorner |
| Blast Doors | Blast Door Side (Large) | ArmorSide |
| Blast Doors | Blast Door Center (Small) | SmallArmorCenter |
| Blast Doors | Blast Door Corner (Small) | SmallArmorCorner |
| Blast Doors | Blast Door Inv Corner (Small) | SmallArmorInvCorner |
| Blast Doors | Blast Door Side (Small) | SmallArmorSide |
| Windows | All 58 window variants | See CubeBlocks_T1_Windows.sbc |
| Interiors | Passage | (Passage TypeId) |
| Interiors | Passage Straight | Passage2 |
| Interiors | Passage Wall | Passage2Wall |
| Interiors | Stairs | LargeStairs |
| Interiors | Ramp | LargeRamp |
| Interiors | Steel Catwalk (4 variants) | LargeSteelCatwalk, 2Sides, Corner, Plate |
| Interiors | Cover Wall (Full, Half, Half Mirrored) | LargeCoverWall, LargeCoverWallHalf, LargeCoverWallHalfMirrored |
| Interiors | Interior Wall | LargeBlockInteriorWall |
| Interiors | Interior Pillar | LargeInteriorPillar |
| Interiors | Passenger Seat (Large) | PassengerSeatLarge |
| Interiors | Passenger Seat (Small) | PassengerSeatSmallNew, PassengerSeatSmallOffset |
| Interiors | Ladder (Large) | (Ladder2 TypeId) |
| Interiors | Ladder Shaft | LadderShaft |
| Interiors | Ladder (Small) | LadderSmall |
| Lights | Reflector Light (Large) | LargeBlockFrontLight |
| Lights | Reflector Light (Small) | SmallBlockFrontLight |
| Lights | Interior Light (Large) | SmallLight |
| Lights | Interior Light (Small) | SmallBlockSmallLight |
| Lights | Corner Light (Large) | LargeBlockLight_1corner, LargeBlockLight_2corner |
| Lights | Corner Light (Small) | SmallBlockLight_1corner, SmallBlockLight_2corner |
| Utility | Landing Gear (Large) | LargeBlockLandingGear |
| Utility | Landing Gear (Small) | SmallBlockLandingGear |
| Utility | Magnetic Plate (Large) | LargeBlockSmallMagneticPlate |
| Utility | Magnetic Plate (Small) | SmallBlockSmallMagneticPlate |
| Mechanical | Piston Top (Large) | LargePistonTop |
| Mechanical | Piston Top (Small) | SmallPistonTop |
| Mechanical | Rotor Part (Large) | LargeRotor |
| Mechanical | Rotor Part (Small) | SmallRotor |
| Mechanical | Hinge Head (Large) | LargeHingeHead |
| Mechanical | Hinge Head Medium (Small) | MediumHingeHead |
| Mechanical | Hinge Head Small (Small) | SmallHingeHead |
| Wheels | Metal Wheel Suspension 3x3 | MetalWheelSuspension3x3 |
| Wheels | Metal Wheel 3x3 | MetalWheel3x3 |

---

## Tier 2

### Production Blocks

| Block | SubtypeId | Power | Blueprint Classes | Crafts |
|---|---|---|---|---|
| Tier 2 Refinery | LargeRefineryT2 | 6 MW | T2Refining | T2 ores → ingots; RefineSpeed 4× |
| Tier 2 Assembler | T2_Assembler | 1.5 MW | T1AssemblingBench, T2AssemblingBench | All T1 + T2 components (general) |
| Cement Kiln | CementKiln | 3 MW | CementKilnComponents | Concrete (IO block) |
| Furnace | T2_Furnace | 2 MW | T2Furnace | Glass, CarbonBlock |
| Electronics Fabricator | T2_ElectronicsFabricator | 1 MW | T2ElectronicsFabricator | SiliciumWafer, SimplePCB, ComputerChip, BasicComputer, Display, Sensors, MedicalComponents, T2_PowerCell |
| T2 Hydraulic Press | T2_HydraulicPress | 1 MW | T1Stamp, T2Stamp | T1 plates + CobaltPlate, AluminumPlate |
| T2 Metal Extruder | T2_MetalExtruder | 1 MW | T1Extruder, T2Extruder | T1 tubes & rods + CopperWire, AluminumRod |
| T2 Fabricator | T2_Fabricator | 1 MW | T1Fabricator, T2Fabricator | T1 composite parts + ComputerChip, T2_ThrustComponent, AluminumFrameS/L/XL |

### Atmospheric Vehicles & Mobility

| Block | SubtypeId | Power | Notes |
|---|---|---|---|
| Battery Block (Large) | LargeBlockBatteryBlock | — | Rechargeable; 12 MW / 3 MWh; overrides vanilla; `AluminumFrameL` + `AluminumPlate` critical |
| Battery Block (Small) | SmallBlockBatteryBlock | — | Rechargeable; 1 MW / 0.2 MWh; overrides vanilla; `AluminumFrameS` + `AluminumPlate` critical |
| O2/H2 Generator (Large) | OxygenGenerator | 0.5 MW | Ice → O2 + H2; overrides vanilla |
| O2/H2 Generator (Small) | OxygenGeneratorSmall | 0.15 MW | Ice → O2 + H2; overrides vanilla |
| Gyroscope (Large grid) | LargeBlockGyro | 0.01 MW | Overrides vanilla; `BasicComputer` critical |
| Gyroscope (Small grid) | SmallBlockGyro | 0.002 MW | Overrides vanilla; `BasicComputer` critical |
| Large Atmos Thruster (Large grid) | LargeBlockLargeAtmosphericThrust | 16.8 MW | Overrides vanilla |
| Small Atmos Thruster (Large grid) | LargeBlockSmallAtmosphericThrust | 2.4 MW | Overrides vanilla |
| Large Atmos Thruster (Small grid) | SmallBlockLargeAtmosphericThrust | 2.4 MW | Overrides vanilla |
| Small Atmos Thruster (Small grid) | SmallBlockSmallAtmosphericThrust | 0.6 MW | Overrides vanilla |
| Large Flat Atmos Thruster (Large grid) | LargeBlockLargeFlatAtmosphericThrust | 6.7 MW | IO flat variant; overrides IO |
| Large Flat Atmos Thruster D (Large grid) | LargeBlockLargeFlatAtmosphericThrustDShape | 6.7 MW | IO flat D-shape; overrides IO |
| Small Flat Atmos Thruster (Large grid) | LargeBlockSmallFlatAtmosphericThrust | 0.8 MW | IO flat variant; overrides IO |
| Small Flat Atmos Thruster D (Large grid) | LargeBlockSmallFlatAtmosphericThrustDShape | 0.8 MW | IO flat D-shape; overrides IO |
| Large Flat Atmos Thruster (Small grid) | SmallBlockLargeFlatAtmosphericThrust | 1.0 MW | IO flat variant; overrides IO |
| Large Flat Atmos Thruster D (Small grid) | SmallBlockLargeFlatAtmosphericThrustDShape | 1.0 MW | IO flat D-shape; overrides IO |
| Small Flat Atmos Thruster (Small grid) | SmallBlockSmallFlatAtmosphericThrust | 0.2 MW | IO flat variant; overrides IO |
| Small Flat Atmos Thruster D (Small grid) | SmallBlockSmallFlatAtmosphericThrustDShape | 0.2 MW | IO flat D-shape; overrides IO |
| Large Atmos Thruster Sci-Fi (Large grid) | LargeBlockLargeAtmosphericThrustSciFi | 16.8 MW | DLC: SparksOfTheFuture |
| Small Atmos Thruster Sci-Fi (Large grid) | LargeBlockSmallAtmosphericThrustSciFi | 2.4 MW | DLC: SparksOfTheFuture |
| Large Atmos Thruster Sci-Fi (Small grid) | SmallBlockLargeAtmosphericThrustSciFi | 2.4 MW | DLC: SparksOfTheFuture |
| Small Atmos Thruster Sci-Fi (Small grid) | SmallBlockSmallAtmosphericThrustSciFi | 0.6 MW | DLC: SparksOfTheFuture |

All atmospheric thrusters require `T2_ThrustComponent` (critical). All batteries require `T2_PowerCell` (critical). Gyroscopes require `BasicComputer` (critical).

### Ores

| Ore | SubtypeId |
|---|---|
| Cobalt | Cobalt |
| Silver | Silver |
| Aluminium | Aluminium |
| Copper | Copper |
| Carbon | Carbon |

Each ore has Impure, Normal, and Pure variants following the same purity system as Tier 1. Refining time is 1,500s per batch of 1,000 ore. Recipes are defined in `Data/Tier2/Blueprints_T2_Refining.sbc`.

### Components

Defined in `Data/Tier2/Components_T2_Component.sbc`. Recipes in `Data/Tier2/Blueprints_T2_Components.sbc`.

| Component | SubtypeId | Inputs | Time |
|---|---|---|---|
| Glass | Glass | 2 Silicon Ingot | 10s |
| Silicium Wafer | SiliciumWafer | 1 Silicon Ingot | 8s |
| Carbon Block | CarbonBlock | 2 Carbon Ingot | 10s |
| Simple PCB | SimplePCB | 2 Silicon Ingot + 1 CopperWire | 12s |
| Copper Wire | CopperWire | 1 Copper Ingot | 8s |
| Computer Chip | ComputerChip | 1 SiliciumWafer + 1 CarbonBlock + 1 CopperWire | 15s |
| Basic Computer | BasicComputer | 2 CopperWire + 1 SimplePCB + 1 ComputerChip | 25s |
| Display | Display | 1 BasicComputer + 2 CopperWire + 2 Silicon Ingot | 30s |
| Sensors | Sensors | 1 BasicComputer + 2 CopperWire + 2 Silicon Ingot | 30s |
| Medical Components | MedicalComponents | 1 Sensors + 1 BasicComputer + 2 CopperWire + 2 IronPlate + 2 IronPipe | 45s |
| Cobalt Plate | CobaltPlate | 1 Iron Ingot + 1 Cobalt Ingot | 15s |
| T2 Power Cell | T2_PowerCell | 2 Cobalt Ingot + 1 SiliciumWafer + 2 CopperWire | 20s |
| Thrust Component | T2_ThrustComponent | 2 CobaltPlate + 1 BasicComputer + 2 CopperWire | 25s |
| Aluminum Plate | AluminumPlate | 1 Aluminium Ingot | 10s |
| Aluminum Rod | AluminumRod | 1 Aluminium Ingot | 5s |
| Aluminum Frame (S) | AluminumFrameS | 12 AluminumRod + 24 IronBolt | 20s |
| Aluminum Frame (L) | AluminumFrameL | 24 AluminumRod + 16 IronBolt + 2 AluminumPlate | 30s |
| Aluminum Frame (XL) | AluminumFrameXL | 48 AluminumRod + 32 IronBolt + 4 AluminumPlate | 50s |

> **Note:** Silver ingots have no component recipes yet — they are available as refinery outputs but currently unused.

---

## Blueprint Class Inheritance

T2 (and higher tier) production machines inherit all recipes from lower tiers by referencing multiple blueprint classes on the block definition. Each class appears as a separate tab in the production UI.

**Pattern:** A T2 block references both the T1 and T2 class in its `<BlueprintClasses>`:

```xml
<BlueprintClasses>
    <Class>T1Stamp</Class>      <!-- T1 recipes tab (inherited) -->
    <Class>T2Stamp</Class>      <!-- T2 recipes tab -->
</BlueprintClasses>
```

The T1 class entries stay in `BlueprintClasses_T1.sbc`, and the T2 class entries stay in `BlueprintClasses_T2.sbc`. No duplication needed — the game resolves each class from whichever file defines its entries.

**Current T2 inheritance:**

| T2 Block | T1 Class (inherited) | T2 Class | T1 Recipes Gained |
|---|---|---|---|
| T2 Hydraulic Press | T1Stamp | T2Stamp | IronPlate, MagnesiumPressedPlate, IronBolt, NickelBall |
| T2 Metal Extruder | T1Extruder | T2Extruder | IronRod, IronTube, IronPipe |
| T2 Fabricator | T1Fabricator | T2Fabricator | SimpleBearing, IronFrameS, IronFrameL, IronFrameXL |
| T2 Assembler | T1AssemblingBench | T2AssemblingBench | All 12 T1 components |

Blocks with no T1 equivalent (Furnace, Electronics Fabricator) only reference their T2 class.

**Scaling to higher tiers:** A T3 Hydraulic Press would reference `T1Stamp`, `T2Stamp`, and `T3Stamp` — three tabs, one per tier. This pattern continues through T6.

---

## Aluminum Armor

Defined in `Data/Tier2/CubeBlocks_T2_Aluminum_Armor.sbc`. 46 block variants (23 large grid, 23 small grid) using IO models.

Lighter than T1 Light Armor but less durable. Uses aluminium-based components instead of iron/steel.

### Component Requirements

| Grid | First Component (critical) | Filler | Filler Count |
|---|---|---|---|
| Large | AluminumFrameL (1) | AluminumPlate | Varies by shape |
| Small | AluminumFrameS (1) | AluminumPlate | 1 |

### Aluminum Component Chain

| Component | SubtypeId | Inputs | Machine | Time |
|---|---|---|---|---|
| Aluminum Plate | AluminumPlate | 1 Aluminium Ingot | T2 Hydraulic Press | 10s |
| Aluminum Rod | AluminumRod | 1 Aluminium Ingot | T2 Metal Extruder | 5s |
| Aluminum Frame (S) | AluminumFrameS | 12 AluminumRod + 24 IronBolt | T2 Fabricator | 20s |
| Aluminum Frame (L) | AluminumFrameL | 24 AluminumRod + 16 IronBolt + 2 AluminumPlate | T2 Fabricator | 30s |
| Aluminum Frame (XL) | AluminumFrameXL | 48 AluminumRod + 32 IronBolt + 4 AluminumPlate | T2 Fabricator | 50s |

AluminumFrameXL is defined for future use (3×3+ footprint blocks at higher tiers); no current armor block requires it.

---

## Industrial Overhaul Integration

This mod disables specific Industrial Overhaul blocks via override definitions and reuses IO models and icons for several T1 production blocks (Hydraulic Press, Metal Extruder, Assembling Bench) to avoid bundling duplicate assets.

Disabled blocks are defined in:
- `Data/Overrides/CubeBlocks_IO_Disabled.sbc`
- `Data/Overrides/CubeBlocks_SurvivalKit_Disabled.sbc`
