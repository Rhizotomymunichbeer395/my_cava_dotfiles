# 🌿 Cava — Verdant Aqua

> **god-tier terminal audio visualizer config** · deep-V EQ · unique patterns per genre · cross-platform

![Demo](demo/demo.gif)

A hand-tuned [cava](https://github.com/karlstav/cava) configuration built for maximum visual drama. Every genre produces a visually distinct pattern — EDM erupts with towering bass walls and crackling treble spikes, jazz breathes with warm low columns and delicate wisps, classical sweeps luminous mid-range arches. No two songs look the same.

```
  ██▁   ▁██       ▁██▁   ▁██▁      ▁███▁
 █████▁▁████▁   ▁███████████████▁▁██████▁
█████████████▁▁████████████████████████████
```

---

## Palette — Verdant Aqua

| Stop | Hex | Role |
|------|-----|------|
| 1 | `#071109` | Bar roots — near-black forest floor |
| 2 | `#0D4025` | Sub-bass — deep undergrowth |
| 3 | `#1A9C6B` | Bass — rich forest-to-teal |
| 4 | `#2ED8A2` | Midrange — vivid emerald |
| 5 | `#00E1C0` | High-mids — pure aquamarine |
| 6 | `#00F6D8` | Presence — bright cyan-aqua |
| 7 | `#50FFF0` | Air — electric seafoam |
| 8 | `#AAFFF0` | Peaks — crystalline near-white aqua |

Background: `#0B1A14` — dark forest floor, zero bleed.

---

## What makes it unique

**Deep-V EQ curve** — the single biggest driver of visual variety. Sub-bass bands are boosted to 2.8×, the mid-range is scooped to 0.2×, and the air band fires at 2.9×. This creates a visual canyon in the center so bass and treble columns fire completely independently. Every genre literally looks different:

| Genre | Visual pattern |
|-------|---------------|
| EDM / Trap | Massive bass towers at center, crackling treble spikes at edges |
| Rock | Kick punches up center, guitar presence sits mid-low |
| Jazz | Warm low columns, delicate treble wisps at the flanks |
| Classical | Sweeping mid-range architecture, gentle luminous peaks |
| Lo-fi | Slow rolling hills, almost no treble activity |

**`noise_reduction = 40`** — fast and reactive. Every drum hit, pluck, and stab snaps to a distinct visual event instead of blurring into the previous frame.

**`reverse = 1` + stereo** — treble lives at the outer edges, bass in the center. Kick drums produce a W-shaped crown that collapses back down; hi-hat rolls fire bright spikes at both flanks simultaneously.

**`waves = 1` + `monstercat = 1`** — bar tops flow into soft organic curves instead of hard block steps.

---

## Installation

Requires **Python 3.8+** — no external dependencies.

```bash
# Clone
git clone https://github.com/programmersd21/my_cava_dotfiles.git
cd my_cava_dotfiles

# Install (interactive — backs up existing config automatically)
python install.py

# Or force-overwrite silently
python install.py --force

# Preview what would happen without touching anything
python install.py --dry-run

# Restore your old config
python install.py --uninstall
```

### What the installer does

| OS | Config location |
|----|----------------|
| Windows | `%APPDATA%\cava\config` |
| macOS | `~/.config/cava/config` (or `$XDG_CONFIG_HOME/cava/config`) |
| Linux | `~/.config/cava/config` (or `$XDG_CONFIG_HOME/cava/config`) |

- Detects your OS automatically
- Backs up any existing config with a timestamp before overwriting
- Checks whether `cava` is in your PATH and prints install instructions if not
- Prints OS-specific audio input guidance after installing

---

## Installing cava

<details>
<summary><b>Windows</b></summary>

```powershell
# Via Scoop (recommended)
scoop bucket add extras
scoop install cava
```

Or download a pre-built binary from the [GitHub releases](https://github.com/nicowillis/cava/releases) page.

Cava on Windows captures system audio automatically via WASAPI loopback — no audio configuration needed.

</details>

<details>
<summary><b>macOS</b></summary>

```bash
brew install cava
```

To capture system audio (not just microphone), install [BlackHole](https://github.com/ExistentialAudio/BlackHole):

```bash
brew install blackhole-2ch
```

Then set your Mac's output to BlackHole, and set cava's input to `portaudio`. The installer will remind you.

</details>

<details>
<summary><b>Linux</b></summary>

```bash
# Ubuntu / Debian
sudo apt install cava

# Arch / Manjaro
sudo pacman -S cava
# or from AUR: yay -S cava-git

# Fedora
sudo dnf install cava

# Nix
nix-env -iA nixpkgs.cava
```

After installing, uncomment the correct input method in the config:

```ini
[input]
method = pipewire   # modern systems
; method = pulse    # PulseAudio
; method = alsa     # bare ALSA
source = auto
```

</details>

---

## Terminal recommendations

For the best visual experience:

| Setting | Recommendation |
|---------|---------------|
| **Background** | `#0B1A14` — match the config background exactly |
| **Font** | Iosevka, Maple Mono, or any Nerd Font — soft block glyph geometry reads closest to rounded bars |
| **Font size** | 8–10pt — more rows = taller bars = more gradient visible |
| **Terminal** | Windows Terminal, kitty, WezTerm, Alacritty — all support `synchronized_sync` |

---

## Config structure

```
my_cava_dotfiles/
├── config/
│   └── cava/
│       └── config          ← the actual cava config
├── themes/
│   └── verdant_aqua.md     ← palette reference card
├── demo/
│   └── demo.gif            ← the demo of the dotfile
├── install.py              ← cross-platform installer
├── README.md
├── LICENSE
└── .github/
    └── ISSUE_TEMPLATE/
        └── bug_report.md
```

---

## Customisation

The config is heavily commented — every value explains what it does and why. Key things to tweak:

```ini
sensitivity = 150    # raise for quiet sources, lower for loud systems
noise_reduction = 40 # lower = snappier, higher = smoother/more fluid
framerate = 120      # match your monitor's refresh rate
```

To change the palette, edit the `gradient_color_1` through `gradient_color_8` values. Any hex colours work.

---

## License

MIT — do whatever you want with it.

---

<p align="center">
  made with 🌿 for people who care about their terminal
</p>
