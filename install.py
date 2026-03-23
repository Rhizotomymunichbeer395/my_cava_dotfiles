#!/usr/bin/env python3
"""
install.py — Cava Dotfiles
Cross-platform installer for Windows, macOS, and Linux.

Usage:
    python install.py           # install with prompts
    python install.py --force   # overwrite existing config without asking
    python install.py --dry-run # preview actions, make no changes
    python install.py --uninstall # restore backed-up config or remove installed
"""

import argparse
import os
import platform
import shutil
import sys
from datetime import datetime
from pathlib import Path

# ── Colours (gracefully disabled on Windows if not supported) ──────────────

def _supports_colour() -> bool:
    if platform.system() == "Windows":
        try:
            import ctypes
            kernel = ctypes.windll.kernel32
            # Enable VIRTUAL_TERMINAL_PROCESSING
            kernel.SetConsoleMode(kernel.GetStdHandle(-11), 7)
            return True
        except Exception:
            return False
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()

USE_COLOUR = _supports_colour()

def _c(code: str, text: str) -> str:
    if not USE_COLOUR:
        return text
    codes = {
        "green":  "\033[38;2;46;216;162m",
        "aqua":   "\033[38;2;0;225;192m",
        "teal":   "\033[38;2;0;246;216m",
        "yellow": "\033[38;2;255;214;0m",
        "red":    "\033[38;2;255;80;80m",
        "dim":    "\033[2m",
        "bold":   "\033[1m",
        "reset":  "\033[0m",
    }
    return f"{codes.get(code, '')}{text}{codes['reset']}"

def banner():
    lines = [
        "  ╔══════════════════════════════════════════════════╗",
        "  ║     CAVA — VERDANT AQUA EDITION                  ║",
        "  ║     cross-platform dotfiles installer            ║",
        "  ╚══════════════════════════════════════════════════╝",
    ]
    print()
    for line in lines:
        print(_c("aqua", line))
    print()

def info(msg: str):    print(_c("aqua",   f"  ✦  {msg}"))
def ok(msg: str):      print(_c("green",  f"  ✔  {msg}"))
def warn(msg: str):    print(_c("yellow", f"  ⚠  {msg}"))
def err(msg: str):     print(_c("red",    f"  ✘  {msg}"))
def dim(msg: str):     print(_c("dim",    f"     {msg}"))
def section(msg: str): print(f"\n{_c('teal', '  ──')} {_c('bold', msg)}\n")

# ── Platform detection ─────────────────────────────────────────────────────

def get_config_dir() -> Path:
    """Return the OS-appropriate cava config directory."""
    system = platform.system()
    if system == "Windows":
        base = os.environ.get("APPDATA")
        if not base:
            raise RuntimeError("%%APPDATA%% not set — cannot locate config dir.")
        return Path(base) / "cava"
    else:
        # macOS and Linux both use XDG_CONFIG_HOME or ~/.config
        xdg = os.environ.get("XDG_CONFIG_HOME")
        base = Path(xdg) if xdg else Path.home() / ".config"
        return base / "cava"

def detect_cava() -> tuple[bool, str]:
    """Return (found, path_or_hint)."""
    path = shutil.which("cava")
    if path:
        return True, path
    return False, ""

def install_hint():
    """Print OS-specific cava installation instructions."""
    system = platform.system()
    print()
    if system == "Windows":
        dim("Install cava on Windows via scoop:")
        dim("  scoop bucket add extras")
        dim("  scoop install cava")
        dim("")
        dim("Or via the GitHub releases page:")
        dim("  https://github.com/nicowillis/cava/releases")
    elif system == "Darwin":
        dim("Install cava on macOS via Homebrew:")
        dim("  brew install cava")
    else:
        dim("Install cava on Linux:")
        dim("  Ubuntu/Debian : sudo apt install cava")
        dim("  Arch/Manjaro  : sudo pacman -S cava   (or yay -S cava-git)")
        dim("  Fedora        : sudo dnf install cava")
        dim("  Nix           : nix-env -iA nixpkgs.cava")
    print()

# ── Backup helpers ─────────────────────────────────────────────────────────

def backup_path(dest: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return dest.with_suffix(f".bak_{stamp}")

def backup_existing(dest: Path, dry_run: bool) -> Path | None:
    if not dest.exists():
        return None
    bak = backup_path(dest)
    warn(f"Existing config found → backing up to:")
    dim(str(bak))
    if not dry_run:
        shutil.copy2(dest, bak)
    return bak

# ── Core install / uninstall ───────────────────────────────────────────────

def install(force: bool, dry_run: bool):
    banner()

    section("Detecting environment")

    system = platform.system()
    info(f"OS: {system} ({platform.release()})")
    info(f"Python: {sys.version.split()[0]}")

    cava_found, cava_path = detect_cava()
    if cava_found:
        ok(f"cava found: {cava_path}")
    else:
        warn("cava not found in PATH")
        install_hint()
        if not _ask("Continue installing config anyway?", default=True):
            err("Aborted.")
            sys.exit(1)

    try:
        config_dir = get_config_dir()
    except RuntimeError as e:
        err(str(e))
        sys.exit(1)

    dest = config_dir / "config"
    src  = Path(__file__).parent / "config" / "cava" / "config"

    if not src.exists():
        err(f"Source config not found at: {src}")
        err("Make sure you're running install.py from the repo root.")
        sys.exit(1)

    section("Installing config")

    info(f"Source : {src}")
    info(f"Target : {dest}")

    if dry_run:
        warn("Dry-run mode — no files will be written.")

    # Ask to overwrite if needed
    if dest.exists() and not force:
        if not _ask(f"Config already exists at {dest}. Overwrite?", default=False):
            err("Aborted. Use --force to skip this prompt.")
            sys.exit(1)

    # Backup
    bak = backup_existing(dest, dry_run)

    # Create dir
    if not dry_run:
        config_dir.mkdir(parents=True, exist_ok=True)

    # Copy
    if not dry_run:
        shutil.copy2(src, dest)
        ok(f"Config installed to {dest}")
    else:
        ok(f"[dry-run] Would install to {dest}")

    section("Post-install")

    _print_input_hint(system)

    if bak:
        dim(f"Your old config is safe at: {bak}")
        dim("Run `python install.py --uninstall` to restore it.")

    print()
    ok("Done! Run  " + _c("green", "cava") + "  in your terminal and enjoy.")
    print()


def uninstall(dry_run: bool):
    banner()
    section("Uninstalling")

    try:
        config_dir = get_config_dir()
    except RuntimeError as e:
        err(str(e))
        sys.exit(1)

    dest = config_dir / "config"

    if not dest.exists():
        warn("No installed config found — nothing to do.")
        return

    # Find most recent backup
    baks = sorted(config_dir.glob("config.bak_*"), reverse=True)

    if baks:
        bak = baks[0]
        info(f"Restoring backup: {bak}")
        if not dry_run:
            shutil.copy2(bak, dest)
            bak.unlink()
            ok("Backup restored.")
        else:
            ok(f"[dry-run] Would restore {bak} → {dest}")
    else:
        warn("No backup found — removing installed config.")
        if not _ask("Delete the installed config with no restore?", default=False):
            err("Aborted.")
            sys.exit(1)
        if not dry_run:
            dest.unlink()
            ok("Config removed.")
        else:
            ok(f"[dry-run] Would delete {dest}")

    print()


# ── Helpers ────────────────────────────────────────────────────────────────

def _ask(prompt: str, default: bool) -> bool:
    hint = "[Y/n]" if default else "[y/N]"
    try:
        answer = input(f"  {_c('teal', '?')}  {prompt} {_c('dim', hint)} ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print()
        return False
    if not answer:
        return default
    return answer in ("y", "yes")


def _print_input_hint(system: str):
    if system == "Windows":
        ok("Windows detected — input section is already commented out.")
        dim("Cava captures system audio automatically via WASAPI.")
    elif system == "Darwin":
        info("macOS detected — uncomment this in your config if needed:")
        dim("  [input]")
        dim("  method = portaudio")
        dim("  source = auto")
        dim("")
        dim("Also install BlackHole for system-audio capture:")
        dim("  brew install blackhole-2ch")
    else:
        info("Linux detected — uncomment the right input method:")
        dim("  PipeWire (modern) : method = pipewire  + source = auto")
        dim("  PulseAudio        : method = pulse     + source = auto")
        dim("  Bare ALSA         : method = alsa      + source = hw:Loopback,1")


# ── Entry point ────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Cava dotfiles installer — cross-platform.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  python install.py                 install with interactive prompts
  python install.py --force         overwrite existing config silently
  python install.py --dry-run       preview what would happen
  python install.py --uninstall     restore backup / remove config
        """,
    )
    parser.add_argument("--force",     action="store_true", help="Overwrite without prompting")
    parser.add_argument("--dry-run",   action="store_true", help="Preview only — no writes")
    parser.add_argument("--uninstall", action="store_true", help="Restore backup or remove config")
    args = parser.parse_args()

    if args.uninstall:
        uninstall(dry_run=args.dry_run)
    else:
        install(force=args.force, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
    