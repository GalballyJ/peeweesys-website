# Ghidra Setup & Symbol Import Guide — Porsche 986 Boxster S 3.2L ME7.2 (`y966ohc.ori`)

## 1. Binary & Processor Configuration
- **Target binary:** `y966ohc.ori` (524,288 bytes / 512 KB, Bosch SW `1037357109`, HW `0261204790`, Porsche `986 618 657 01`)
- **Language / Processor:** `C166:LE:16:default` (Siemens C167CR, Little Endian)
- **Flash Base Address:** `0x800000` (maps `0x000000..0x07FFFF` -> `0x800000..0x87FFFF`)

## 2. Memory Map & DPP Registers
Before running analysis or importing symbols, add the two RAM regions in **Window -> Memory Map**:
1. **Internal RAM / XRAM:** `0x00F600` - `0x00FFDF` (length `0x09E0`, Read/Write/Volatile)
2. **External SRAM:** `0x380000` - `0x387FFF` (length `0x8000`, Read/Write/Volatile)

Set the C167 Data Page Pointers (DPPs) in **Register Manager** (or at reset/main) to match the `y966ohc.ori` boot setup (`0x80BCE4..0x80BCF0`):
- `DPP0 = 0x204` (`0x810000..0x813FFF` — calibration flash page 0)
- `DPP1 = 0x205` (`0x814000..0x817FFF` — calibration flash page 1)
- `DPP2 = 0x0E0` (`0x380000..0x383FFF` — external SRAM)
- `DPP3 = 0x003` (`0x00C000..0x00FFFF` — internal RAM / SFRs)

## 3. Importing Symbols (317 Total)
| Category | Count | Address Domain |
| :--- | :---: | :--- |
| Verified C167 Functions | 31 | `0x800000..0x87FFFF` |
| Verified KWP Tables | 3 | `0x81CD6A..0x81DCD8` |
| `VERIFIED_TUNER` Calibration Maps | 82 | `0x810000..0x81FFFF` |
| `VERIFIED_TUNER` Calibration Axes | 101 | `0x810000..0x81FFFF` |
| Confirmed RAM Variables (Primary) | 86 | `0x00F600..0x00FFDF`, `0x380000..0x387FFF` |
| Confirmed RAM Mirror Addresses | 14 | `0x380000..0x387FFF` |

### Option A — Full Script (Recommended: functions + labels + comments)
1. Copy `me72_y966ohc_ImportSymbols.py` into your Ghidra scripts directory (e.g. `~/ghidra_scripts/`).
2. Open **Window -> Script Manager**, click **Refresh**, and run `Porsche.ME72 -> me72_y966ohc_ImportSymbols.py`.

### Option B — Built-in `ImportSymbolsScript.py`
1. Open **Window -> Script Manager** and run Ghidra's built-in `ImportSymbolsScript.py`.
2. Select `me72_y966ohc_symbols.txt` when prompted.
