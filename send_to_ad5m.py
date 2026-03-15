#!/usr/bin/env python3
r"""
================================================================================
 Flashforge Adventurer 5M - PrusaSlicer WiFi Upload Script
 Version 6.0 - Rename Dialog Before Upload
================================================================================
 Created by: Brian & Claude Sonnet 4.6 (Anthropic AI)
 Tested and verified on real Flashforge Adventurer 5M hardware.
 Released to the community freely - use, share, and improve!
================================================================================
 Uploads G-code directly to the AD5M over WiFi via TCP port 8899.
 Pops up a rename dialog before uploading so you can give the file
 a meaningful name on the printer touchscreen.

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
PRINTER_IP     = "192.168.1.xxx"   # <- Your printer IP address
PRINTER_SERIAL = "XXXXXXXXXXXX"    # <- Your printer serial number
CHECK_CODE     = "xxxxxxxx"        # <- Your printer check code (8 chars)
CMD_PORT       = 8899              # <- Do not change
TIMEOUT        = 15                # <- Do not change
CHUNK_SIZE     = 4096              # <- Do not change
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


def clean_filename(filepath):
    name = os.path.basename(filepath)
    if name.startswith("."):
        name = name[1:]
    if name.endswith(".pp"):
        name = name[:-3]
    if not name.endswith(".gcode"):
        name += ".gcode"
    return name


def ask_filename(suggested):
    """
    Pop up a clean dialog showing the suggested filename.
    User can accept, rename, or cancel to abort upload.
    Returns chosen filename or None if cancelled.
    """
    result = {"name": None}

    root = tk.Tk()
    root.title("AD5M - Name Your Print")
    root.resizable(False, False)
    root.attributes("-topmost", True)

    # Center on screen
    width, height = 440, 165
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
    entry = tk.Entry(root, textvariable=entry_var, font=("Segoe UI", 11), width=40)
    entry.pack(padx=20)
    # Select filename only - not the .gcode extension
    name_only = len(suggested) - 6 if suggested.endswith(".gcode") else len(suggested)
    entry.select_range(0, name_only)
    entry.icursor(name_only)
    entry.focus()

    def on_upload(event=None):
        name = entry_var.get().strip() or suggested
        # Strip extension to clean then re-add
        if name.endswith(".gcode"):
            name = name[:-6].strip()
        # Sanitize for printer filesystem
        name = "".join(c for c in name if c.isalnum() or c in "._- ")
        name = name.strip() + ".gcode"
        result["name"] = name
        root.destroy()

    def on_cancel(event=None):
        result["name"] = None
        root.destroy()

    # Buttons
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=12)

    tk.Button(
        btn_frame,
        text="  Upload to Printer  ",
        command=on_upload,
        font=("Segoe UI", 10),
        bg="#0066CC",
        fg="white",
        relief="flat",
        padx=6
    ).pack(side=tk.LEFT, padx=12)

    tk.Button(
        btn_frame,
        text="  Cancel  ",
        command=on_cancel,
        font=("Segoe UI", 10),
        relief="flat",
        padx=6
    ).pack(side=tk.LEFT, padx=12)

    root.bind("<Return>", on_upload)
    root.bind("<Escape>", on_cancel)
    root.protocol("WM_DELETE_WINDOW", on_cancel)
    root.mainloop()

    return result["name"]


def upload(filepath, filename):
    filesize = os.path.getsize(filepath)

    print(f"\n{'='*60}")
    print(f"  Flashforge AD5M - WiFi Upload v6.0")
    print(f"  File : {filename}")
    print(f"  Size : {filesize:,} bytes")
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

        print("  [6/6] Finalising...")
        time.sleep(0.5)
        send_cmd(sock, "~M29")
        send_cmd(sock, "~M602")
        sock.close()

        print(f"\n  SUCCESS! {filename} is ready on the printer.")
        print(f"{'='*60}\n")
        return True

    except ConnectionRefusedError:
        print(f"\n  ERROR: Connection refused - is printer on WiFi?")
    except socket.timeout:
        print(f"\n  ERROR: Timed out - check IP {PRINTER_IP}")
    except Exception as e:
        print(f"\n  ERROR: {type(e).__name__}: {e}")
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

    # Show rename dialog - waits for user input
    filename = ask_filename(suggested)

    # User cancelled - abort silently
    if filename is None:
        print("Upload cancelled.")
        sys.exit(0)

    success = upload(filepath, filename)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
