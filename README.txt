================================================================================
 Flashforge Adventurer 5M - Complete PrusaSlicer Profile Bundle
 Version 2.4 - Community Release
================================================================================
 Created by: Brian & Claude Sonnet 4.6 (Anthropic AI)
 Released to the community freely - use, share, and improve!
================================================================================

WHAT IS THIS?
-------------
A complete, fully working PrusaSlicer setup for the Flashforge Adventurer 5M.
This bundle includes everything you need to slice and WiFi-upload directly
to your AD5M from PrusaSlicer - no USB stick required!

Everything has been tested and verified on a real AD5M printer.
All known issues with bed origin, thumbnails, purge line, and G-code
compatibility have been corrected.

WHAT'S INCLUDED?
----------------
  1. Flashforge_Adventurer_5M_PrusaSlicer_v2.1.ini  - Complete config bundle
  2. send_to_ad5m.py                               - WiFi upload Python script v7.2
  3. AD5M_Bed_Texture_Official.png                 - Custom bed texture
  4. AD5M_Printer_Model.stl                        - Official Flashforge bed model
  5. README.txt                                    - This file

WHAT'S IN THE CONFIG BUNDLE?
-----------------------------
  Printer Profile:
    - Bed Shape: 220x220mm, centered origin (-110 to +110 both axes)
    - Bed Type: Stock Textured PEI Build Plate
    - Thumbnails: 140x110 PNG (displays correctly on touchscreen)
    - Purge line: centered front of bed, centered coordinates
    - G-code flavor: Marlin compatible
    - All machine limits configured for AD5M hardware
    - WiFi upload post-processing baked in to all print profiles

  Print Profiles (3):
    - 0.10mm DETAIL  - Fine detail, slower speed
    - 0.20mm QUALITY - Best balance of quality and speed (recommended)
    - 0.30mm DRAFT   - Fast prototyping

  Filament Profiles (8):
    - Generic PLA         - Standard PLA
    - Generic PETG        - PETG
    - Generic TPU 95A     - Flexible TPU (direct drive optimized)
    - Generic ABS         - ABS (open frame notes included)
    - Generic PLA Silk    - Silk/Shiny PLA (corrected temperatures)
    - Generic HS PLA      - High Speed PLA
    - Generic PLA-CF      - Carbon Fiber PLA (0.6mm hardened nozzle required)
    - Generic Pro PCTG    - PCTG copolyester

REQUIREMENTS
------------
  - PrusaSlicer 2.9.4 or later
  - Python 3.x (for WiFi upload script)
    Download: https://www.python.org/downloads/
  - Flashforge Adventurer 5M on WiFi network
  - tkinter (included with standard Python installation)

INSTALLATION - STEP BY STEP
----------------------------

STEP 1 - Install Python (if not already installed)
  - Download Python 3.x from https://www.python.org/downloads/
  - During install CHECK "Add Python to PATH"
  - Note your install path (default: C:\Users\YOUR_NAME\AppData\Local\Programs\Python\Python3xx\)

STEP 2 - Copy the WiFi upload script
  - Copy send_to_ad5m.py to:
    C:\Users\YOUR_NAME\Documents\PrusaSlicer\send_to_ad5m.py
  - Open send_to_ad5m.py in Notepad
  - Edit the PRINTER SETTINGS section at the top:

    PRINTER_IP     = "192.168.1.xxx"    <- Your printer's IP address
    PRINTER_SERIAL = "XXXXXXXXXXXX"     <- Your printer's serial number
    CHECK_CODE     = "xxxxxxxx"         <- Your printer's check code

  HOW TO FIND YOUR PRINTER SETTINGS:
    - IP Address:     Printer touchscreen -> Settings -> Network -> IP Address
    - Serial Number:  Printer touchscreen -> Settings -> About -> Serial Number
    - Check Code:     Printer touchscreen -> Settings -> About -> Check Code
                      (8 character alphanumeric code)

STEP 3 - Import the config bundle into PrusaSlicer
  - Open PrusaSlicer
  - Go to: File -> Import -> Import Config Bundle
  - Select: Flashforge_Adventurer_5M_PrusaSlicer_v2.1.ini
  - Click OK on any warnings about substituted values
  - Your Flashforge AD5M printer and all profiles will now appear in PrusaSlicer

STEP 4 - Set up the bed texture (optional but recommended)
  - In PrusaSlicer go to: Printers Settings -> General -> Bed Shape -> Set
  - Under Texture click the folder icon
  - Browse to and select: AD5M_Bed_Texture_Official.png
  - Under Model click the folder icon
  - Browse to and select: AD5M_Printer_Model.stl
  - Click OK

STEP 5 - Add the post-processing script path to each print profile
  The config bundle includes three print profiles (DETAIL, QUALITY, DRAFT).
  You need to add YOUR Python path and script location to each one.

  In PrusaSlicer:
  - Select the print profile from the Print Settings dropdown
    (look for: 0.10mm DETAIL - AD5M, 0.20mm QUALITY - AD5M, 0.30mm DRAFT - AD5M)
  - Go to: Print Settings -> Output Options -> Post-processing scripts
  - Add the following line using YOUR Python path and script location:

    C:\Users\YOUR_NAME\AppData\Local\Programs\Python\Python3xx\python.exe "C:\Users\YOUR_NAME\Documents\PrusaSlicer\send_to_ad5m.py";

  - Click the Save icon (floppy disk) next to the print profile name to save
  - Repeat for each of the three print profiles

STEP 6 - Test a full slice and upload
  - Import any STL model into PrusaSlicer
  - Select Flashforge Adventurer 5M as your printer
  - Select a print profile (0.20mm QUALITY - AD5M recommended for first test)
  - Click Slice
  - Click Export G-code
  - PrusaSlicer opens a SAVE dialog — save your .gcode file to your computer
    with whatever name you choose. This is your local copy.
  - After saving — the upload dialog opens automatically with three options:

      [ Upload ]  [ Upload + Print ]  [ Cancel ]

    Upload         — transfers the file to printer storage only.
                     Start the print manually from the touchscreen.
    Upload + Print — transfers the file then immediately starts printing.
                     No touchscreen interaction needed.
    Cancel         — aborts without sending anything.

  - The dialog pre-fills with your actual save filename automatically.
    No more cryptic temp names — what you saved is what you see.
    Edit the name if desired or accept as-is.
    Note: .gcode extension is added automatically — no need to type it.
  - A console window will show upload progress and verification:
    Filename from PrusaSlicer: MyPart_PLA.gcode
    [1/6] Connecting...
    [2/6] Requesting control...
    [3/6] Authenticating...
    [4/6] Initiating upload...
    [5/6] Uploading... [████████████████████░░░░░░░░░] 65% 4521 KB/s
    [6/6] Finalizing...
    [V]   Verifying upload...
    SUCCESS! MyPart_PLA.gcode is ready on the printer.
    Upload verified - file confirmed on printer.
    Closing in 5s...
  - Find your file on the printer touchscreen - ready to print!

  IMPORTANT - Upload + Print:
    The printer must be IDLE to use Upload + Print.
    If a print is already running, the script will report a connection error.
    This is expected firmware behavior — the AD5M refuses new TCP connections
    during an active print.

HOW THE WIFI UPLOAD WORKS
--------------------------
The script communicates with the AD5M over TCP port 8899 using the
Flashforge proprietary protocol:

  Upload:
    1. Connects to printer IP on port 8899
    2. Requests printer control (~M601)
    3. Authenticates with serial and check code (~M602)
    4. Initiates file transfer (~M28)
    5. Streams G-code data in 4KB chunks
    6. Finalizes transfer (~M29)
    7. Verifies file on printer (~M661)
    8. Releases printer control (~M602)

  Upload + Print (additional steps after upload):
    9.  Selects the uploaded file (~M23)
    10. Starts the print (~M24)

KNOWN ISSUES AND NOTES
-----------------------
  - ABS can be printed successfully on the AD5M without an enclosure.
    Smaller parts print well open frame. Larger parts are more susceptible
    to warping and layer splitting due to temperature gradients. An enclosure
    will improve results on larger ABS prints. Good ventilation is always
    recommended when printing ABS.

  - PLA-CF requires a hardened nozzle (0.6mm minimum).
    Do NOT use carbon fiber filaments with the stock 0.4mm brass nozzle.

  - PCTG bonds very strongly to bare PEI. Always apply PVA glue stick
    to the bed before printing PCTG.

TROUBLESHOOTING
---------------
  Upload fails / connection refused:
    - Is printer powered on and connected to WiFi?
    - Ping your printer IP to verify network connectivity:
      Open Command Prompt and type: ping 192.168.1.xxx
      (replace with your printer's IP address)
    - Verify IP address in script matches printer network settings
    - Check printer is not currently printing (required for Upload + Print)
    - Verify port 8899 is accessible on your network
    - Check no other app is connected to the printer on port 8899

  Upload reports SUCCESS but verification fails (!! UPLOAD FAILED !!):
    - Another app is connected to the printer and holding the TCP session
    - Only one TCP connection to port 8899 is allowed at a time
    - Close any other printer control apps and try again

  Script crashes with "getaddrinfo failed":
    - The PRINTER_IP in send_to_ad5m.py is blank or set to a hostname.
    - Open the script in Notepad and verify PRINTER_IP is a valid IP address
      (example: "192.168.1.25") not a hostname or placeholder.

  Wrong serial/check code error:
    - Double check serial and check code on printer touchscreen
    - Printer touchscreen -> Settings -> About

  Script not running after slice:
    - Verify Python path in post-processing script field is correct
    - Check Python is installed and working
    - Verify post-processing script path is correct in each print profile

CREDITS
-------
  Developed through extensive testing and troubleshooting on a real
  Flashforge Adventurer 5M printer.

  Bed texture designed to accurately represent the actual AD5M print
  bed including official Flashforge branding, safety markings, and
  grid overlay.

  WiFi upload protocol based on Flashforge network communication
  and community documentation.

  Special thanks to the Flashforge AD5M community for sharing
  printer protocol information.

  Give back. Share freely. Help others. 🙏

================================================================================
 Version History:
   v2.4 - March 2026
          send_to_ad5m.py updated to v7.2
          Uses SLIC3R_PP_OUTPUT_NAME environment variable to get real filename
          Dialog pre-fills with the actual filename the user saved in PrusaSlicer
          No more dot-prefix temp filename workaround
          Workflow is now exactly: Slice -> Save -> Upload -> Print
          clean_filename() kept as fallback if environment variable not available

   v2.3 - March 2026
          send_to_ad5m.py updated to v7.1
          M661 upload verification — confirms file actually landed on printer
          Loud FAILED alert if file not found on printer after upload
          5 second result pause — console stays open so you can read outcome
          American English spelling throughout (Finalizing, behavior, etc.)
          New troubleshooting entry: verification failure / conflicting TCP session

   v2.2 - March 2026
          send_to_ad5m.py updated to v7.0
          Added Upload + Print button — slices and starts print in one click
          Upload + Print uses ~M23 (select) + ~M24 (start) after upload
          Dialog now highlights filename only, not the .gcode extension
          Double-extension bug fixed (.gcode not appended if already present)
          README updated with Upload + Print instructions and troubleshooting
          New troubleshooting entry: getaddrinfo failed / blank IP address

   v2.1 - February 2026
          Fixed Windows path backslashes throughout README and script
          Removed all personal credentials - replaced with YOUR_NAME placeholders
          Silk PLA temperatures corrected (reduced from 235/230 to 220/215)

   v2.0 - February 2026
          Corrected bed origin to centered coordinates (-110 to +110)
          Fixed "Print File Out of Range" firmware error
          Fixed thumbnails to 140x110 PNG single size (blank touchscreen fix)
          Corrected purge line coordinates for centered origin
          Fixed host_type to octoprint for PrusaSlicer 2.9.4 compatibility
          Added rename dialog to WiFi upload script
          Personal credentials removed for community release
          Official Flashforge bed plate STL included
          ABS open-frame printing notes revised

   v1.0 - Initial release
================================================================================
