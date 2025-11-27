# WEAVE: PCHTXT TO IPS CONVERTER

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

**A Simple Pchtxt to IPS Converter for Nintendo Switch**

**Weave** is a simple CLI tool designed to compile `.pchtxt` patch files into the `IPS32` binary format required by the Nintendo Switch modding environment (Atmosphère).

It replaces manual conversion with a rapid, batch-capable workflow that handles directory recursion, incremental builds, and cross-platform compatibility without requiring external dependencies.

---

## Features

* **Batch Processing:** Recursively scans directory trees to compile entire mod collections in a single pass.
* **Incremental Builds:** Intelligent skipping of files that have already been compiled to maximize speed.
* **IPS32 Compliance:** Generates standard 32-bit addressed IPS files compatible with Switch NSO binaries (supports >16MB files).
* **Zero Dependencies:** Written in pure Python. No `pip install` or virtual environment required.

---

## Installation

### Prerequisites
* **Python 3.8** or higher must be installed and added to your system PATH.
    * [Download Python](https://www.python.org/downloads/)

### Setup
1.  Click **<> Code** and select **Download ZIP** (or clone the repository).
2.  Extract `weave-script.py` and `WEAVE.bat` into the root folder where you keep your Switch mods.

---

## Usage

### Windows

**Method 1: The Launcher (Recommended)**
Double-click **`WEAVE.bat`**. The tool will initialize the terminal environment, set the correct text encoding, and immediately process the current directory and all subdirectories.

**Method 2: Drag & Drop**
You can drag a specific folder containing mods and drop it directly onto **`WEAVE.bat`**. The script will launch and process only the dropped directory.

**Method 3: Command Line**
Open PowerShell or Command Prompt in the folder and run:
```bash
python weave-script.py
```

### Linux & macOS

Weave is fully compatible with Unix-based systems. The `.bat` launcher is not required.

1.  Open your Terminal.
2.  Navigate to the folder containing the script:
    ```bash
    cd /path/to/your/mods
    ```
3.  Run the script using Python 3:
    ```bash
    python3 weave-script.py
    ```

**Optional: Make Executable**
You can mark the script as executable to run it directly:

```bash
chmod +x weave-script.py
./weave-script.py
```

-----

## Directory Structure & Batch Processing

Weave uses a recursive scanner, meaning it will find and convert `.pchtxt` files regardless of where they are located in the folder hierarchy.

**Recommendation:**
For the best experience, organize your input files using the standard Atmosphère structure (`Game Name/TitleID/exefs/`). This allows Weave to generate the `.ips` files directly alongside them, making the result ready to copy-paste to your SD card.

**Example Hierarchy:**

```text
/Switch Mods Collection/
│
├── WEAVE.bat               <-- Place script at the root
├── weave-script.py
│
├── /The Legend of Zelda/   <-- Game Name (For your organization)
│   └── /0100F2C0115B6000/  <-- Title ID
│       └── /exefs/
│           ├── 60FPS.pchtxt          <-- Source File
│           └── 0100F2C0115B6000.ips  <-- Generated File
│
└── /Mario Odyssey/
    └── /0100000000010000/
        └── /exefs/
            ├── EcoMode.pchtxt
            └── 0100000000010000.ips
```

-----
-----

## "Where do I get mods/patches?"

If you downloaded this tool without actually having any patches to convert, I honestly don't know what to tell you.

  * **[Fl4sh9174's Switch-Ultrawide-Mods](https://github.com/Fl4sh9174/Switch-Ultrawide-Mods)** Has an amazing collection for 60FPS and ultrawide patches.
  * **For everything else:** **[link](https://letmegooglethat.com/?q=XXXX+switch+game+pchtxt)**
-----

## Supported Syntax

Weave implements a strict parser for the Pchtxt standard. Files must contain a valid Build ID to be processed.

| Tag | Description |
| :--- | :--- |
| `@nsobid <id>` | Specifies the Build ID. This determines the output filename. |
| `@flag nsobid <id>` | Modern syntax for specifying Build ID. |
| `@flag offset_shift <val>` | **Required.** Shifts addresses (typically `0x100`) to account for NSO headers. |
| `@title <name>` | Optional. Specifies a mod name for the console log. |
| `@enabled` | Starts a block of active patches. |
| `@stop` | Stops parsing the file immediately. |

-----

## Credits

Logic and specifications are derived from the following open-source research:

  * **[Archleaders'PchtxtToIps](https://github.com/ArchLeaders/PchtxtToIps)** – Original C\# implementation logic.
  * **[CrustySean's PCHTXT2IPS](https://github.com/CrustySean/PCHTXT2IPS)** – C++ toolchain and IPS32 format documentation.
  * **[3096's IPSwitch](https://github.com/3096/ipswitch)** – `ipswitch` runtime patching standards.

-----

> **Disclaimer:** This software is provided for educational and homebrew management purposes only.
