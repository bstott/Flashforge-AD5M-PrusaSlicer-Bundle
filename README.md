# Flashforge Adventurer 5M - Complete PrusaSlicer Bundle

![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)
![PrusaSlicer](https://img.shields.io/badge/PrusaSlicer-2.9.4%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-green)

![Flashforge AD5M in PrusaSlicer](PrusaSlicer-AD5M.PNG)

**Created by: Brian S & Claude Sonnet 4.6 (Anthropic AI)**
*Tested and verified on real Flashforge Adventurer 5M hardware.*
*Released to the community freely — use, share, and improve!*

---

## What Is This?

A complete, fully working PrusaSlicer setup for the Flashforge Adventurer 5M.
Slice and WiFi-upload directly to your AD5M from PrusaSlicer — **no USB stick required!**

All known issues with bed origin, thumbnails, purge line, and G-code compatibility have been corrected and verified on a real printer. Supports Windows and Linux.

---

## What's Included

| File | Description |
|------|-------------|
| `Flashforge_Adventurer_5M_PrusaSlicer_v2.5.ini` | Complete PrusaSlicer config bundle |
| `send_to_ad5m.py` | WiFi upload Python script v7.4 |
| `send_to_ad5m.cfg` | Printer configuration file (IP address) |
| `compile_linux.sh` | Linux binary compiler script |
| `AD5M_Bed_Texture_Official.png` | Bed texture with official Flashforge branding |
| `AD5M_Printer_Model.stl` | Official Flashforge bed plate model |
| `LICENSE` | CC BY-NC 4.0 |
| `README.txt` | Plain text installation guide |

---

## What's In The Config Bundle

### Printer Profile
- Bed Shape: 220x220mm centered origin (-110 to +110)
- Bed Type: Stock Textured PEI Build Plate
- Thumbnails: 140x110 PNG (displays correctly on touchscreen)
- Purge line: centered front of bed X=-50 to X=+50 at Y=-100
- G-code flavor: Marlin compatible
- WiFi upload post-processing baked into all print profiles

### Print Profiles (3)
- **0.10mm DETAIL** — Fine detail, slower speed
- **0.20mm QUALITY** — Best balance of quality and speed *(recommended)*
- **0.30mm DRAFT** — Fast prototyping

### Filament Profiles (8)
- Generic PLA
- Generic PETG
- Generic TPU 95A *(direct drive optimized)*
- Generic ABS *(open frame notes included)*
- Generic PLA Silk *(corrected temperatures)*
- Generic HS PLA *(High Speed)*
- Generic PLA-CF *(0.6mm hardened nozzle required)*
- Generic Pro PCTG

---

## Requirements

| Requirement | Notes |
|-------------|-------|
| PrusaSlicer 2.9.4 or later | Earlier versions untested |
| Flashforge Adventurer 5M on WiFi | IP address required |
| Windows 10/11 | Python 3.x required — see Windows install |
| Linux | No Python needed — compile binary once with included script |

> **Note for existing users:** If you have a working setup you do not need to change anything.
> Your current script and PrusaSlicer configuration continue to work exactly as before.
> v2.5 adds Linux support and a config file option for easier IP configuration.
> Existing Windows users who want the new features can simply replace `send_to_ad5m.py`
> and place `send_to_ad5m.cfg` alongside it with your printer IP.

---

## Windows Installation

### STEP 1 — Install Python
- Download Python 3.x from [python.org](https://www.python.org/downloads/)
- Click **Customize installation**
- Ensure **tcl/tk and IDLE** is checked *(required for upload dialog)*
- Ensure **Add Python to PATH** is checked
- Note your install path: `C:\Users\YOUR_NAME\AppData\Local\Programs\Python\Python3xx\`

### STEP 2 — Configure the Upload Script
Copy `send_to_ad5m.py` and `send_to_ad5m.cfg` to the same folder:
`C:\Users\YOUR_NAME\Documents\PrusaSlicer\`

**Option A — Edit the config file** *(recommended — no script editing needed)*:
Open `send_to_ad5m.cfg` in Notepad and set your printer IP:
```ini
[printer]
ip = 192.168.1.xxx
```

**Option B — Edit the script directly**:
Open `send_to_ad5m.py` in Notepad and set `PRINTER_IP`:
```python
PRINTER_IP = "192.168.1.xxx"
```

Find your printer IP: touchscreen → Settings → Network → IP Address

### STEP 3 — Import the Config Bundle
- Open PrusaSlicer
- Go to: **File → Import → Import Config Bundle**
- Select: `Flashforge_Adventurer_5M_PrusaSlicer_v2.5.ini`
- Click OK on any warnings
- Flashforge AD5M printer and all profiles now appear in PrusaSlicer

### STEP 4 — Set Up Bed Texture *(optional but recommended)*
- Go to: **Printers Settings → General → Bed Shape → Set**
- Under **Texture** → select `AD5M_Bed_Texture_Official.png`
- Under **Model** → select `AD5M_Printer_Model.stl`
- Click OK

### STEP 5 — Add Post-Processing Script to Each Print Profile
- Select a print profile from the **Print Settings** dropdown
- Go to: **Print Settings → Output Options → Post-processing scripts**
- Add this line using YOUR paths:

```
C:\Users\YOUR_NAME\AppData\Local\Programs\Python\Python3xx\python.exe "C:\Users\YOUR_NAME\Documents\PrusaSlicer\send_to_ad5m.py";
```

- Click the **Save icon** (floppy disk) next to the print profile name
- Repeat for all three print profiles

---

## Linux Installation

> Linux requires a standalone binary because PrusaSlicer on Linux uses its own
> internal Python which does not support tkinter. Compile once — no Python needed after that.

### STEP 1 — Configure the Upload Script
Copy `send_to_ad5m.py`, `send_to_ad5m.cfg`, and `compile_linux.sh` to a working folder
*(example: `~/Documents/PrusaSlicer/`)*

Open `send_to_ad5m.cfg` and set your printer IP:
```ini
[printer]
ip = 192.168.1.xxx
```

Find your printer IP: touchscreen → Settings → Network → IP Address

### STEP 2 — Compile the Binary
```bash
chmod +x compile_linux.sh
./compile_linux.sh
```

The script checks dependencies, installs PyInstaller if needed, and compiles
`send_to_ad5m.py` into a standalone binary `send_to_ad5m` in the current folder.

### STEP 3 — Place Files in Final Location
Copy the binary `send_to_ad5m (binary)` and `send_to_ad5m.cfg` to your chosen location:
`/home/YOUR_USERNAME/Documents/PrusaSlicer/`

**Both files must always be in the same folder.**

### STEP 4 — Import the Config Bundle
Same as Windows STEP 3 above.

### STEP 5 — Set Up Bed Texture *(optional)*
Same as Windows STEP 4 above.

### STEP 6 — Add Post-Processing Script to Each Print Profile
- Go to: **Print Settings → Output Options → Post-processing scripts**
- Add the full path to the binary `send_to_ad5m (binary)`:

```
/home/YOUR_USERNAME/Documents/PrusaSlicer/send_to_ad5m
```

- Click the **Save icon** next to the print profile name
- Repeat for all three print profiles

---

## Test a Full Slice and Upload

- Import any STL into PrusaSlicer
- Select **Flashforge Adventurer 5M** as printer
- Select **0.20mm QUALITY - AD5M** as print profile
- Click **Slice**
- Click **Export G-code**
- PrusaSlicer save dialog opens — save your local .gcode file
- Upload dialog opens automatically with three buttons:

| Button | Action |
|--------|--------|
| **Upload** | Transfers file to printer. Start print from touchscreen. |
| **Upload + Print** | Transfers file then starts printing immediately. |
| **Cancel** | Aborts without sending anything. |

- Dialog pre-fills with your actual save filename automatically
- Console shows upload progress and verification:

```
============================================================
  Flashforge AD5M - WiFi Upload v7.4
============================================================
  Filename from PrusaSlicer: MyPart_PLA.gcode
  [1/6] Connecting...
  [2/6] Requesting control...
  [3/6] Authenticating...
  [4/6] Initiating upload...
  [5/6] Uploading... [█████████████████████░░░░░░░] 72% 4521 KB/s
  [6/6] Finalizing...
  [V]   Verifying upload...

  SUCCESS! MyPart_PLA.gcode is ready on the printer.
  Upload verified - file confirmed on printer.
============================================================
  Closing in 5s...
```

> **Upload + Print:** Printer must be **idle**. If a print is already running
> the script will report a connection error. This is expected firmware behavior.

---

## How the WiFi Upload Works

The script communicates with the AD5M over TCP port 8899:

**Upload:**
1. Connects to printer IP on port 8899
2. Requests printer control (~M601)
3. Authenticates (~M602)
4. Initiates file transfer (~M28)
5. Streams G-code data in 4KB chunks
6. Finalizes transfer (~M29)
7. Verifies file on printer (~M661)
8. Releases printer control (~M602)

**Upload + Print (additional steps):**
9. Selects the uploaded file (~M23)
10. Starts the print (~M24)

> Only the printer IP address is required. Serial number and check code are not
> required on firmware 2.1 and later. If your firmware requires them see Troubleshooting.

---

## Known Issues and Notes

- **ABS** prints well open frame for smaller parts. Larger parts are more susceptible to warping and layer splitting — an enclosure helps. Good ventilation recommended.
- **PLA-CF** requires a hardened nozzle (0.6mm minimum). Do NOT use with the stock 0.4mm brass nozzle.
- **PCTG** bonds very strongly to bare PEI. Always apply PVA glue stick to the bed before printing PCTG.

---

## Troubleshooting

**Post-processing script fails with Error Code 2 (Windows):**

Most likely cause: tkinter not installed or missing from Python.

Verify tkinter is working — open Command Prompt and type:
```
python -m tkinter
```
A small test window should appear. If nothing appears — tkinter is missing.

Fix: Run Python installer → **Modify** → check **tcl/tk and IDLE** → complete installation.

**Upload fails / connection refused:**
- Is printer powered on and connected to WiFi?
- Ping your printer: `ping 192.168.1.xxx` *(replace with your IP)*
- Check printer is not currently printing
- Check no other app is connected on port 8899

**Upload reports SUCCESS but verification fails:**
- Another app is holding the TCP session
- Close any other printer control apps and try again

**Script crashes with "getaddrinfo failed" or times out:**
- IP address is still a placeholder — not set correctly
- Check `send_to_ad5m.cfg` or `PRINTER_IP` in the script

**Older firmware requires serial and check code:**

Some older AD5M firmware versions require authentication.
If upload fails after confirming IP is correct:

Find your credentials on the printer touchscreen:
- Serial Number: touchscreen → Settings → About → Serial Number
- Check Code: touchscreen → Settings → About → Check Code *(8 character alphanumeric)*

Uncomment and add them to `send_to_ad5m.cfg`:
```ini
[printer]
ip = 192.168.1.xxx
serial = XXXXXXXXXXXX
check_code = xxxxxxxx
```

**Script not running after slice (Windows):**
- Verify Python path in post-processing script field is correct
- Verify script is saved in each print profile with the floppy disk icon

**Binary not found (Linux):**
- Verify binary and `send_to_ad5m.cfg` are in the same folder
- Verify binary is executable: `chmod +x send_to_ad5m`
- Verify full path is correct in PrusaSlicer post-processing field

---

## License

This work is licensed under the
[Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/)

You are free to share and adapt this work for non-commercial purposes
with appropriate attribution to **Brian S & Claude Sonnet 4.6 (Anthropic AI)**.

---

## Credits

Developed through extensive testing and troubleshooting on a real Flashforge Adventurer 5M printer.

Bed texture designed to accurately represent the actual AD5M print bed including official Flashforge branding, safety markings, and grid overlay.

WiFi upload protocol based on Flashforge network communication and community documentation.

*Give back. Share freely. Help others.* 🙏

---

## Version History

| Version | Changes |
|---------|---------|
| v2.5 | Added Linux support via compile_linux.sh, config file (send_to_ad5m.cfg) for IP configuration, existing Windows users unaffected, updated README with Windows and Linux sections, troubleshooting expanded |
| v2.4 | send_to_ad5m.py updated to v7.2 — uses SLIC3R_PP_OUTPUT_NAME to get real filename from PrusaSlicer. Dialog pre-fills with actual save name. |
| v2.3 | send_to_ad5m.py updated to v7.1 — M661 upload verification, FAILED alert, 5 second result pause, American English spelling. |
| v2.2 | send_to_ad5m.py updated to v7.0 — Upload+Print button, filename highlight fix, double-extension fix. |
| v2.1 | Fixed Windows path backslashes, removed personal credentials, official Flashforge bed model, compressed bed texture, CC BY-NC 4.0 license. |
| v2.0 | Corrected bed origin (centered), fixed thumbnails (140x110), corrected purge line, Silk PLA temperatures corrected, rename dialog added. |
| v1.0 | Initial release. |
