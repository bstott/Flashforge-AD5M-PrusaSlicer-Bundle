#!/usr/bin/env python3
r"""
================================================================================
 Flashforge Adventurer 5M - PrusaSlicer WiFi Upload Script
 Version 7.1 - Upload Verification + Result Pause
================================================================================
 Created by: Brian S & Claude Sonnet 4.6 (Anthropic AI)
 Tested and verified on real Flashforge Adventurer 5M hardware.
 Released to the community freely - use, share, and improve!
================================================================================
 Uploads G-code directly to the AD5M over WiFi via TCP port 8899.
 Pops up a dialog to name the file and choose upload or upload+print.

 v7.1 changes:
   - M661 verification after upload confirms file actually landed on printer
   - Console window stays open 5 seconds after result so you can read it
   - Loud FAILED alert if file is not found on printer after upload
   - Fixed spelling: Finalizing (American English)

 POST-PROCESSING SCRIPT LINE (Print Settings -> Output Options):
   C:\Users\YOUR_NAME\AppData\Local\Programs\Python\Python3xx\python.exe "C:\Users\YOUR_NAME\Documents\PrusaSlicer\send_to_ad5m.py";
================================================================================
"""

import socket
import os
import sys
import time
import tkinter as tk

# ============================================================
# PRINTER SETTINGS - UPDATE THESE FOR YOUR PRINTER
# ============================================================
# How to find your printer settings:
#   PRINTER_IP     : Printer touchscreen -> Settings -> Network -> IP Address
#   PRINTER_SERIAL : Printer touchscreen -> Settings -> About -> Serial Number
#   CHECK_CODE     : Printer touchscreen -> Settings -> About -> Check Code
#                    (8 character alphanumeric code)
# ============================================================
PRINTER_IP     = "192.168.1.25"    # <- Your printer IP address
PRINTER_SERIAL = "SNMQKDD9703270"  # <- Your printer serial number
CHECK_CODE     = "7e3e4f50"        # <- Your printer check code (8 chars)
CMD_PORT       = 8899              # <- Do not change
TIMEOUT        = 15                # <- Do not change
CHUNK_SIZE     = 4096              # <- Do not change
RESULT_PAUSE   = 5                 # <- Seconds to keep console open after result
# ============================================================


def send_cmd(sock, command):
    if not command.endswith("\r\n"):
        command += "\r\n"
    sock.sendall(command.encode("utf-8"))
    time.sleep(0.3)
    response = b""
    sock.settimeout(3)
    try:
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk
    except socket.timeout:
        pass
    return response.decode("utf-8", errors="ignore").strip()


def verify_upload(sock, filename):
    """
    Send ~M661 and check if filename appears in the response.
    Returns True if file is confirmed on printer, False otherwise.
    """
    print("  [V]   Verifying upload...")
    time.sleep(0.5)
    response = send_cmd(sock, "~M661")
    # M661 returns paths like /data/filename.gcode
    # Our uploads go to 0:/user/ but printer lists them under /data/
    # Check for the bare filename anywhere in the response
    bare_name = filename.lower()
    response_lower = response.lower()
    if bare_name in response_lower:
        return True
    # Also check without .gcode in case printer strips it
    if bare_name.replace(".gcode", "") in response_lower:
        return True
    return False


def clean_filename(filepath):
    name = os.path.basename(filepath)
    if name.startswith("."):
        name = name[1:]
    if name.endswith(".pp"):
        name = name[:-3]
    if not name.endswith(".gcode"):
        name += ".gcode"
    return name


def sanitize_name(name, suggested):
    name = name.strip() or suggested
    if name.endswith(".gcode"):
        name = name[:-6].strip()
    name = "".join(c for c in name if c.isalnum() or c in "._- ")
    name = name.strip() + ".gcode"
    return name


def pause_before_close(seconds=RESULT_PAUSE):
    """Keep console open so user can read the result."""
    for i in range(seconds, 0, -1):
        print(f"  Closing in {i}s...", end="\r", flush=True)
        time.sleep(1)
    print()


def ask_filename(suggested):
    """
    Pop up dialog with three buttons:
      - Upload to Printer
      - Upload + Print
      - Cancel
    Returns (filename, start_print) or (None, False) if cancelled.
    """
    result = {"name": None, "print": False}

    root = tk.Tk()
    root.title("AD5M - Name Your Print")
    root.resizable(False, False)
    root.attributes("-topmost", True)

    # Center on screen
    width, height = 480, 170
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

    # Label
    tk.Label(
        root,
        text="Name this print on the AD5M touchscreen:",
        font=("Segoe UI", 10),
        pady=10
    ).pack()

    # Entry pre-filled with suggested name
    entry_var = tk.StringVar(value=suggested)
    entry = tk.Entry(root, textvariable=entry_var, font=("Segoe UI", 11), width=42)
    entry.pack(padx=20)
    # Select filename only - not the .gcode extension
    name_only = len(suggested) - 6 if suggested.endswith(".gcode") else len(suggested)
    entry.select_range(0, name_only)
    entry.icursor(name_only)
    entry.focus()

    def on_upload(event=None):
        result["name"] = sanitize_name(entry_var.get(), suggested)
        result["print"] = False
        root.destroy()

    def on_upload_and_print():
        result["name"] = sanitize_name(entry_var.get(), suggested)
        result["print"] = True
        root.destroy()

    def on_cancel(event=None):
        result["name"] = None
        result["print"] = False
        root.destroy()

    # Buttons
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=12)

    tk.Button(
        btn_frame,
        text="  Upload  ",
        command=on_upload,
        font=("Segoe UI", 10),
        bg="#0066CC",
        fg="white",
        relief="flat",
        padx=6
    ).pack(side=tk.LEFT, padx=8)

    tk.Button(
        btn_frame,
        text="  Upload + Print  ",
        command=on_upload_and_print,
        font=("Segoe UI", 10),
        bg="#006600",
        fg="white",
        relief="flat",
        padx=6
    ).pack(side=tk.LEFT, padx=8)

    tk.Button(
        btn_frame,
        text="  Cancel  ",
        command=on_cancel,
        font=("Segoe UI", 10),
        relief="flat",
        padx=6
    ).pack(side=tk.LEFT, padx=8)

    root.bind("<Return>", on_upload)
    root.bind("<Escape>", on_cancel)
    root.protocol("WM_DELETE_WINDOW", on_cancel)
    root.mainloop()

    return result["name"], result["print"]


def upload(filepath, filename, start_print=False):
    filesize = os.path.getsize(filepath)

    print(f"\n{'='*60}")
    print(f"  Flashforge AD5M - WiFi Upload v7.1")
    print(f"  File  : {filename}")
    print(f"  Size  : {filesize:,} bytes")
    print(f"  Print : {'YES - will start after upload' if start_print else 'No'}")
    print(f"{'='*60}")

    try:
        print("  [1/6] Connecting...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)
        sock.connect((PRINTER_IP, CMD_PORT))

        print("  [2/6] Requesting control...")
        send_cmd(sock, "~M601 S1")

        print("  [3/6] Authenticating...")
        send_cmd(sock, f"~M602 S{PRINTER_SERIAL} P{CHECK_CODE}")

        print("  [4/6] Initiating upload...")
        resp = send_cmd(sock, f"~M28 {filesize} 0:/user/{filename}")
        if "error" in resp.lower():
            print(f"  ERROR: Printer rejected upload: {resp}")
            sock.close()
            pause_before_close()
            return False

        print("  [5/6] Uploading...")
        bytes_sent = 0
        start_time = time.time()
        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break
                sock.sendall(chunk)
                bytes_sent += len(chunk)
                pct = bytes_sent / filesize
                bar = "█" * int(pct*35) + "░" * (35 - int(pct*35))
                elapsed = time.time() - start_time
                speed = bytes_sent / elapsed / 1024 if elapsed > 0 else 0
                print(f"\r        [{bar}] {pct*100:.1f}% {speed:.0f} KB/s", end="", flush=True)

        elapsed = time.time() - start_time
        print(f"\n        {bytes_sent:,} bytes in {elapsed:.1f}s ({bytes_sent/elapsed/1024:.0f} KB/s)")

        print("  [6/6] Finalizing...")
        time.sleep(0.5)
        send_cmd(sock, "~M29")

        # Verify the file actually landed on the printer
        verified = verify_upload(sock, filename)

        if not verified:
            print(f"\n{'='*60}")
            print(f"  !! UPLOAD FAILED !!")
            print(f"  {filename} was NOT found on the printer.")
            print(f"  The file did not transfer successfully.")
            print(f"  Check that no other app is connected to the printer.")
            print(f"{'='*60}\n")
            sock.close()
            pause_before_close()
            return False

        # Start print if requested
        if start_print:
            print("  [+] Starting print...")
            time.sleep(1.0)
            send_cmd(sock, f"~M23 0:/user/{filename}")
            time.sleep(0.5)
            send_cmd(sock, "~M24")
            print(f"  [+] Print started!")

        send_cmd(sock, "~M602")
        sock.close()

        print(f"\n{'='*60}")
        print(f"  SUCCESS! {filename} is ready on the printer.")
        if start_print:
            print(f"  Printing has started!")
        print(f"  Upload verified - file confirmed on printer.")
        print(f"{'='*60}\n")
        pause_before_close()
        return True

    except ConnectionRefusedError:
        print(f"\n  ERROR: Connection refused - is printer on WiFi?")
        pause_before_close()
    except socket.timeout:
        print(f"\n  ERROR: Timed out - check IP {PRINTER_IP}")
        pause_before_close()
    except Exception as e:
        print(f"\n  ERROR: {type(e).__name__}: {e}")
        pause_before_close()
    return False


def main():
    # Called with no args - PrusaSlicer validating script on save
    if len(sys.argv) < 2:
        sys.exit(0)

    filepath = sys.argv[1].strip('"')

    if not os.path.exists(filepath):
        print(f"ERROR: File not found: {filepath}")
        sys.exit(1)

    # Get suggested clean filename
    suggested = clean_filename(filepath)

    # Show dialog - waits for user input
    filename, start_print = ask_filename(suggested)

    # User cancelled - abort silently
    if filename is None:
        print("Upload cancelled.")
        sys.exit(0)

    success = upload(filepath, filename, start_print)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
