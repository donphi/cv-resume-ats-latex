"""
lib/config.py — Single source of truth for grid math, YAML loading,
                preamble parsing, and error helpers.

Every script in scripts/ imports from here. Nothing is duplicated.

Page dimensions are physical constants defined by ISO 216 (A4) and
ANSI/ASME Y14.1 (Letter). They are lookup values selected by the
paper_size field in contact.yaml. The preamble.tex conditional
(\\ifx\\PageFormat...) uses the same values — this is the Python-side
mirror, kept in ONE place.
"""

from __future__ import annotations

import math
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print(
        "ERROR: PyYAML is required.  Install it with:\n"
        "  pip install pyyaml",
        file=sys.stderr,
    )
    sys.exit(1)


# ---------------------------------------------------------------------------
# Paths (derived from this file's location: scripts/lib/shared.py)
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent.parent          # repo root
CONTENT_DIR = ROOT / "content"
GENERATED_DIR = ROOT / "generated"
PREAMBLE_PATH = ROOT / "engine" / "preamble.tex"
CONTACT_YAML = CONTENT_DIR / "contact.yaml"
LAYOUT_YAML = CONTENT_DIR / "layout.yaml"
BUILD_DIR = ROOT / "build"
BOXHEIGHTS_PATH = BUILD_DIR / "boxheights.dat"
CANVAS_TEX_PATH = GENERATED_DIR / "canvas.tex"


# ---------------------------------------------------------------------------
# Physical paper sizes (ISO 216 / ANSI Y14.1)
# ---------------------------------------------------------------------------
# These are the ONLY place page dimensions exist in Python.
# preamble.tex §1 has the TeX-side mirror (\PageWidthMM / \PageHeightMM).
PAGE_SIZES: dict[str, tuple[float, float]] = {
    "a4": (210.0, 297.0),
    "letter": (215.9, 279.4),
}

# ---------------------------------------------------------------------------
# Valid header themes
# ---------------------------------------------------------------------------
VALID_HEADER_THEMES = ("classic", "mainframe", "crt")

# Header theme → engine file mapping
HEADER_ENGINE_FILES: dict[str, str] = {
    "classic": "engine/header.tex",
    "mainframe": "engine/header_mainframe.tex",
    "crt": "engine/header_crt.tex",
}


# ---------------------------------------------------------------------------
# Error helpers
# ---------------------------------------------------------------------------

def die(msg: str) -> None:
    """Print error and exit."""
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def require(value, name: str, source: str):
    """Raise if value is None or empty string."""
    if value is None or value == "":
        die(f"required parameter '{name}' not found in {source}")
    return value


# ---------------------------------------------------------------------------
# YAML loaders
# ---------------------------------------------------------------------------

def load_contact() -> dict:
    """Load and validate content/contact.yaml."""
    if not CONTACT_YAML.exists():
        die(f"{CONTACT_YAML} not found")
    data = yaml.safe_load(CONTACT_YAML.read_text(encoding="utf-8"))
    if not data:
        die(f"{CONTACT_YAML} is empty")
    require(data.get("paper_size"), "paper_size", "content/contact.yaml")
    require(data.get("margin"), "margin", "content/contact.yaml")
    return data


def load_layout() -> list[dict]:
    """Load and validate content/layout.yaml."""
    if not LAYOUT_YAML.exists():
        die(f"{LAYOUT_YAML} not found")
    data = yaml.safe_load(LAYOUT_YAML.read_text(encoding="utf-8"))
    if not data or "sections" not in data:
        die(f"{LAYOUT_YAML} must contain a 'sections' list")
    sections = data["sections"]
    if not sections:
        die(f"{LAYOUT_YAML} 'sections' list is empty")
    for i, sec in enumerate(sections):
        require(sec.get("title"), f"sections[{i}].title", "content/layout.yaml")
        require(sec.get("content"), f"sections[{i}].content", "content/layout.yaml")
        col = require(sec.get("column"), f"sections[{i}].column", "content/layout.yaml")
        if col not in ("left", "right", "full"):
            die(
                f"sections[{i}].column must be 'left', 'right', or 'full', "
                f"got '{col}' in content/layout.yaml"
            )
    return sections


# ---------------------------------------------------------------------------
# Preamble parser
# ---------------------------------------------------------------------------

REQUIRED_PREAMBLE_PARAMS = [
    "GridFontSize",
    "MonoWidthRatio",
    "ContentWidthScale",
    "HeaderHeight",
    "GapHeaderToContent",
    "GapBoxToBox",
    "LeftBoxWidth",
    "ColumnGap",
    "LeftBoxPadLeft",
    "LeftBoxPadRight",
    "LeftBoxPadTop",
    "LeftBoxPadBot",
    "RightBoxPadLeft",
    "RightBoxPadRight",
    "RightBoxPadTop",
    "RightBoxPadBot",
    "FullBoxPadLeft",
    "FullBoxPadRight",
    "FullBoxPadTop",
    "FullBoxPadBot",
    "MinSplitContentRows",
]


def parse_preamble() -> dict[str, float]:
    r"""Parse \newcommand{\Name}{Value} from preamble.tex."""
    if not PREAMBLE_PATH.exists():
        die(f"{PREAMBLE_PATH} not found")
    text = PREAMBLE_PATH.read_text(encoding="utf-8")

    pattern = re.compile(r"\\newcommand\{\\(\w+)\}\{([^}]+)\}")

    found: dict[str, str] = {}
    for m in pattern.finditer(text):
        found[m.group(1)] = m.group(2).strip()

    params: dict[str, float] = {}
    for name in REQUIRED_PREAMBLE_PARAMS:
        raw = found.get(name)
        if raw is None:
            die(f"required parameter '\\{name}' not found in preamble.tex")
        try:
            params[name] = float(raw)
        except ValueError:
            die(
                f"parameter '\\{name}' in preamble.tex has non-numeric "
                f"value '{raw}'"
            )

    return params


# ---------------------------------------------------------------------------
# Grid math (replicates preamble.tex §2 exactly)
# ---------------------------------------------------------------------------

# 1 pt = 25.4 mm / 72  (standard TeX PostScript point)
PT_TO_MM = 25.4 / 72.0


def compute_grid(contact: dict, params: dict[str, float]) -> dict:
    """Compute grid dimensions from contact.yaml + preamble.tex params."""
    paper_size = contact["paper_size"].lower()
    if paper_size not in PAGE_SIZES:
        die(
            f"unknown paper_size '{paper_size}' in contact.yaml "
            f"(must be one of: {', '.join(PAGE_SIZES)})"
        )
    page_w, page_h = PAGE_SIZES[paper_size]
    margin = float(contact["margin"])

    font_size = params["GridFontSize"]
    mono_ratio = params["MonoWidthRatio"]

    cell_w = font_size * mono_ratio * PT_TO_MM
    cell_h = font_size * PT_TO_MM

    grid_cols = int(math.floor((page_w - 2 * margin) / cell_w))
    grid_rows = int(math.floor((page_h - 2 * margin) / cell_h))

    header_height = int(params["HeaderHeight"])
    gap_header = params["GapHeaderToContent"]
    gap_box = params["GapBoxToBox"]
    content_start_y = header_height + gap_header

    return {
        "grid_cols": grid_cols,
        "grid_rows": grid_rows,
        "header_height": header_height,
        "gap_header": gap_header,
        "gap_box": gap_box,
        "content_start_y": content_start_y,
        "max_page_y": grid_rows,
        # Padding per column type
        "left_pad_top": params["LeftBoxPadTop"],
        "left_pad_bot": params["LeftBoxPadBot"],
        "right_pad_top": params["RightBoxPadTop"],
        "right_pad_bot": params["RightBoxPadBot"],
        "full_pad_top": params["FullBoxPadTop"],
        "full_pad_bot": params["FullBoxPadBot"],
        "min_split_rows": int(params["MinSplitContentRows"]),
    }


def box_rows(content_rows: int, pad_top: float, pad_bot: float) -> int:
    """Total box height: top border + padding + content + padding + bottom border.

    Matches TeX's \\pgfmathtruncatemacro which truncates (floors for positive).
    """
    return int(1 + pad_top + content_rows + pad_bot + 1)
