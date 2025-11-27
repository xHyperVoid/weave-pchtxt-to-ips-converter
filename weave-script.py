import os
import sys
import struct
import re
import ctypes
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from pathlib import Path

IPS32_MAGIC = b'IPS32'
IPS32_EOF = b'EEOF'

class Theme:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    PURPLE = '\033[38;5;99m'
    BLUE = '\033[38;5;75m'
    GREEN = '\033[38;5;78m'
    YELLOW = '\033[38;5;221m'
    RED = '\033[38;5;203m'
    WHITE = '\033[38;5;255m'
    GREY = '\033[38;5;240m'
    BAR_V = "│"
    BAR_L = "└"
    ARROW = "→"

def enable_colors():
    if os.name == 'nt':
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        sys.stdout.reconfigure(encoding='utf-8')

@dataclass
class FileData:
    nso_id: Optional[str] = None
    mod_name: str = "Unknown Mod"
    offset_shift: int = 0
    patches: List[Tuple[int, bytes]] = field(default_factory=list)
    error_msg: Optional[str] = None

class Converter:
    RE_ID = re.compile(r'^@flag\s+nsobid\s+([a-fA-F0-9]+)|^@nsobid[- ]?([a-fA-F0-9]+)')
    RE_TITLE = re.compile(r'^@title\s+(.+)')
    RE_SHIFT = re.compile(r'^@flag\s+offset_shift\s+(0x[0-9a-fA-F]+|\d+)')

    @staticmethod
    def read_file(path: Path) -> FileData:
        data = FileData()
        try:
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            data.error_msg = f"Could not read file: {e}"
            return data

        active = False
        for line in lines:
            line = line.strip()
            if not line: continue

            if m := Converter.RE_ID.match(line):
                data.nso_id = (m.group(1) or m.group(2)).strip()
                continue
            if m := Converter.RE_TITLE.match(line):
                data.mod_name = m.group(1).strip().strip('"')
                continue
            if m := Converter.RE_SHIFT.match(line):
                base = 16 if '0x' in m.group(1).lower() else 10
                data.offset_shift = int(m.group(1), base)
                continue

            if line.startswith('@enabled'):
                active = True
                continue
            if line.startswith(('@disabled', '@stop')):
                active = False
                if line.startswith('@stop'): break
                continue

            if active:
                if line.startswith(('/', '#', '@')): continue
                parts = line.split(maxsplit=1)
                if len(parts) < 2: continue
                
                try:
                    addr = int(parts[0], 16) + data.offset_shift
                    val_str = parts[1]
                    
                    if val_str.startswith('"') and val_str.endswith('"'):
                        content = val_str[1:-1].replace(r'\n', '\n').replace(r'\0', '\0')
                        payload = content.encode('utf-8')
                    else:
                        payload = bytes.fromhex(val_str.replace(' ', ''))
                    
                    data.patches.append((addr, payload))
                except:
                    continue
        return data

    @staticmethod
    def create_ips(dest: Path, patches: List[Tuple[int, bytes]]):
        with open(dest, 'wb') as f:
            f.write(IPS32_MAGIC)
            for addr, payload in patches:
                f.write(struct.pack('>I', addr))
                f.write(struct.pack('>H', len(payload)))
                f.write(payload)
            f.write(IPS32_EOF)

class App:
    def __init__(self):
        enable_colors()
        self.stats = {'ok': 0, 'skip': 0, 'fail': 0}

    def start(self):
        print(f"\n{Theme.PURPLE}{Theme.BOLD}  WEAVE: PCHTXT TO IPS CONVERTER{Theme.RESET}")
        print(f"{Theme.DIM}  Looking for patch files...{Theme.RESET}\n")
        
        files = []
        for root, _, filenames in os.walk("."):
            for name in filenames:
                if name.lower().endswith(".pchtxt"):
                    files.append(Path(root) / name)

        if not files:
            print(f"  {Theme.YELLOW}No .pchtxt files found here.{Theme.RESET}")
            input("\n  Press Enter to close...")
            return

        for i, path in enumerate(files, 1):
            self.handle_file(path, i, len(files))

        self.show_summary(len(files))
        input(f"  {Theme.DIM}Press Enter to close...{Theme.RESET}")

    def handle_file(self, path: Path, index: int, total: int):
        info = Converter.read_file(path)
        output_file = path.parent / f"{info.nso_id}.ips"
        
        if info.error_msg or not info.nso_id:
            status_color = Theme.RED
            action = "ERROR"
        elif output_file.exists():
            status_color = Theme.YELLOW
            action = "SKIP"
        else:
            status_color = Theme.GREEN
            action = "OK"

        counter = f"{status_color}[{index}/{total}]{Theme.RESET}"
        print(f"  {counter} {Theme.BOLD}{path.name}{Theme.RESET}")

        folder = str(path.parent)
        if not folder.startswith(".") and not os.path.isabs(folder):
             folder = f".\\{folder}"

        print(f"   {Theme.DIM}{Theme.BAR_V} Folder:   {Theme.RESET}{folder}")
        
        if info.nso_id:
            name_display = info.mod_name if info.mod_name != "Unknown Mod" else info.nso_id
            print(f"   {Theme.DIM}{Theme.BAR_V} Mod:      {Theme.RESET}{name_display}")

        if action == "ERROR":
            reason = info.error_msg if info.error_msg else "Missing Game ID"
            print(f"   {Theme.DIM}{Theme.BAR_L}{Theme.RESET} {Theme.RED}Failed: {reason}{Theme.RESET}")
            self.stats['fail'] += 1

        elif action == "SKIP":
            print(f"   {Theme.DIM}{Theme.BAR_L}{Theme.RESET} {Theme.YELLOW}Skipped (File exists){Theme.RESET}")
            self.stats['skip'] += 1

        elif action == "OK":
            try:
                Converter.create_ips(output_file, info.patches)
                print(f"   {Theme.DIM}{Theme.BAR_L}{Theme.RESET} {Theme.GREEN}Created {info.nso_id}.ips{Theme.RESET}")
                self.stats['ok'] += 1
            except Exception as e:
                print(f"   {Theme.DIM}{Theme.BAR_L}{Theme.RESET} {Theme.RED}Save Failed: {e}{Theme.RESET}")
                self.stats['fail'] += 1
        
        print("")

    def show_summary(self, total):
        print(f"  {Theme.DIM}────────────────────────────────────────{Theme.RESET}")
        print(f"  {Theme.BOLD}Finished{Theme.RESET}")
        
        if self.stats['ok'] > 0:
            print(f"  {Theme.GREEN}• Created: {self.stats['ok']}{Theme.RESET}")
        if self.stats['skip'] > 0:
            print(f"  {Theme.YELLOW}• Skipped: {self.stats['skip']}{Theme.RESET}")
        if self.stats['fail'] > 0:
            print(f"  {Theme.RED}• Failed:  {self.stats['fail']}{Theme.RESET}")
        print("")

if __name__ == "__main__":
    App().start()
