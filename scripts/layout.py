#!/usr/bin/env python3
"""
layout.py — Two-pass deterministic page-break engine for the designed CV.

Modes:
    --measure   Generate generated/canvas.tex with all boxes placed
                sequentially (no splits) so pass 1 can measure heights.
    --layout    Read boxheights.dat (written by pass 1 via \\LogBoxHeight),
                compute page breaks, and regenerate generated/canvas.tex
                with proper splits and page breaks.

Inputs (ALL required — no defaults, no assumptions):
    content/contact.yaml   — paper_size, margin
    content/layout.yaml    — section order and column assignments
    preamble.tex           — grid/box master parameters (parsed via regex)
    boxheights.dat         — measured content heights (only for --layout)

Outputs:
    --measure:  generated/canvas.tex (passthrough, no splits)
    --layout:   generated/canvas.tex (with page breaks + splits),
                generated/*-p{N}.tex (split content files)

This script has ZERO default values. Every parameter is read from YAML or
parsed from preamble.tex. If any required value is missing, the script
raises immediately with a clear error message.
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
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
GENERATED_DIR = ROOT / "generated"
PREAMBLE_PATH = ROOT / "preamble.tex"

CONTACT_YAML = CONTENT_DIR / "contact.yaml"
LAYOUT_YAML = CONTENT_DIR / "layout.yaml"
BOXHEIGHTS_PATH = ROOT / "boxheights.dat"
CANVAS_TEX_PATH = GENERATED_DIR / "canvas.tex"

# Page dimensions — keyed by paper_size.
# These are physical paper sizes defined by ISO 216 (A4) and
# ANSI/ASME Y14.1 (Letter). They are lookup values selected by the
# paper_size field in contact.yaml.
PAGE_SIZES: dict[str, tuple[float, float]] = {
    "a4": (210.0, 297.0),
    "letter": (215.9, 279.4),
}

# ---------------------------------------------------------------------------
# Error helpers
# ---------------------------------------------------------------------------

def _die(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def _require(value, name: str, source: str):
    """Raise if value is None or empty string."""
    if value is None or value == "":
        _die(f"required parameter '{name}' not found in {source}")
    return value


# ---------------------------------------------------------------------------
# YAML loaders
# ---------------------------------------------------------------------------

def load_contact() -> dict:
    if not CONTACT_YAML.exists():
        _die(f"{CONTACT_YAML} not found")
    data = yaml.safe_load(CONTACT_YAML.read_text(encoding="utf-8"))
    if not data:
        _die(f"{CONTACT_YAML} is empty")
    _require(data.get("paper_size"), "paper_size", "content/contact.yaml")
    _require(data.get("margin"), "margin", "content/contact.yaml")
    return data


def load_layout() -> list[dict]:
    if not LAYOUT_YAML.exists():
        _die(f"{LAYOUT_YAML} not found")
    data = yaml.safe_load(LAYOUT_YAML.read_text(encoding="utf-8"))
    if not data or "sections" not in data:
        _die(f"{LAYOUT_YAML} must contain a 'sections' list")
    sections = data["sections"]
    if not sections:
        _die(f"{LAYOUT_YAML} 'sections' list is empty")
    for i, sec in enumerate(sections):
        _require(sec.get("title"), f"sections[{i}].title", "content/layout.yaml")
        _require(sec.get("content"), f"sections[{i}].content", "content/layout.yaml")
        col = _require(sec.get("column"), f"sections[{i}].column", "content/layout.yaml")
        if col not in ("left", "right", "full"):
            _die(
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
]


def parse_preamble() -> dict[str, float]:
    """Parse \\newcommand{\\Name}{Value} from preamble.tex."""
    if not PREAMBLE_PATH.exists():
        _die(f"{PREAMBLE_PATH} not found")
    text = PREAMBLE_PATH.read_text(encoding="utf-8")

    pattern = re.compile(r"\\newcommand\{\\(\w+)\}\{([^}]+)\}")

    found: dict[str, str] = {}
    for m in pattern.finditer(text):
        found[m.group(1)] = m.group(2).strip()

    params: dict[str, float] = {}
    for name in REQUIRED_PREAMBLE_PARAMS:
        raw = found.get(name)
        if raw is None:
            _die(f"required parameter '\\{name}' not found in preamble.tex")
        try:
            params[name] = float(raw)
        except ValueError:
            _die(
                f"parameter '\\{name}' in preamble.tex has non-numeric "
                f"value '{raw}'"
            )

    return params


# ---------------------------------------------------------------------------
# Grid math (replicates preamble.tex §2 exactly)
# ---------------------------------------------------------------------------

def compute_grid(contact: dict, params: dict[str, float]) -> dict:
    """Compute grid dimensions from contact.yaml + preamble.tex params."""
    paper_size = contact["paper_size"].lower()
    if paper_size not in PAGE_SIZES:
        _die(
            f"unknown paper_size '{paper_size}' in contact.yaml "
            f"(must be one of: {', '.join(PAGE_SIZES)})"
        )
    page_w, page_h = PAGE_SIZES[paper_size]
    margin = float(contact["margin"])

    font_size = params["GridFontSize"]
    mono_ratio = params["MonoWidthRatio"]
    pt_to_mm = 25.4 / 72.0

    cell_w = font_size * mono_ratio * pt_to_mm
    cell_h = font_size * pt_to_mm

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
    }


def box_rows(content_rows: int, pad_top: float, pad_bot: float) -> int:
    """Total box height: top border + padding + content + padding + bottom border.

    Matches TeX's \\pgfmathtruncatemacro which truncates (floors for positive).
    """
    return int(1 + pad_top + content_rows + pad_bot + 1)


# ---------------------------------------------------------------------------
# boxheights.dat loader
# ---------------------------------------------------------------------------

def load_boxheights() -> dict[str, int]:
    """Load measured content heights from boxheights.dat."""
    if not BOXHEIGHTS_PATH.exists():
        _die(
            f"{BOXHEIGHTS_PATH} not found. "
            "Run the measurement pass (--measure + compile) first."
        )
    heights: dict[str, int] = {}
    for line in BOXHEIGHTS_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("%") or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, val = line.split("=", 1)
        key = key.strip()
        val = val.strip()
        try:
            heights[key] = int(val)
        except ValueError:
            _die(f"invalid height value for '{key}' in boxheights.dat: '{val}'")
    return heights


# ---------------------------------------------------------------------------
# Split-boundary detection
# ---------------------------------------------------------------------------

SPLIT_PATTERNS = [
    re.compile(r"^\\JobSep\s*$"),                          # work_experience
    re.compile(r"^\\vspace\{\\GapTimelineItem"),            # education
    re.compile(r"^\\vspace\{\\GapSkillCat"),                # skills
    re.compile(r"^\\vspace\{\\GapBeforeSubHead"),           # research subsections
    re.compile(r"^\\SubHead\{"),                            # research subsections (alt)
]


def find_split_boundaries(tex_path: Path) -> list[int]:
    """Return line indices (0-based) where a safe split can occur."""
    if not tex_path.exists():
        _die(f"content file not found: {tex_path}")
    lines = tex_path.read_text(encoding="utf-8").splitlines()
    boundaries: list[int] = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        for pat in SPLIT_PATTERNS:
            if pat.match(stripped):
                boundaries.append(i)
                break
    return boundaries


def _find_wrapping_env(lines: list[str]) -> str | None:
    """Detect if the content is wrapped in a single outer environment."""
    begin_pat = re.compile(r"^\s*\\begin\{(\w+)\}\s*$")
    end_pat = re.compile(r"^\s*\\end\{(\w+)\}\s*$")

    # Find the first non-blank, non-comment line
    first_env = None
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("%"):
            continue
        m = begin_pat.match(stripped)
        if m:
            first_env = m.group(1)
        break

    if first_env is None:
        return None

    # Check if the last non-blank line closes this environment
    for line in reversed(lines):
        stripped = line.strip()
        if not stripped or stripped.startswith("%"):
            continue
        m = end_pat.match(stripped)
        if m and m.group(1) == first_env:
            return first_env
        break

    return None


def split_content_file(
    tex_path: Path,
    boundaries: list[int],
    split_after_boundary_idx: int,
) -> tuple[Path, Path]:
    """Split a .tex file at the given boundary into -p1.tex and -p2.tex."""
    lines = tex_path.read_text(encoding="utf-8").splitlines(keepends=True)
    boundary_line = boundaries[split_after_boundary_idx]

    stem = tex_path.stem
    p1_path = GENERATED_DIR / f"{stem}-p1.tex"
    p2_path = GENERATED_DIR / f"{stem}-p2.tex"

    # Detect wrapping environment
    raw_lines = [l.rstrip("\n").rstrip("\r") for l in lines]
    wrapping_env = _find_wrapping_env(raw_lines)

    # Part 1: everything up to (but not including) the boundary line
    p1_lines = list(lines[:boundary_line])
    # Part 2: everything from the boundary line onward
    p2_lines = list(lines[boundary_line:])

    # Strip trailing blank lines from part 1
    while p1_lines and p1_lines[-1].strip() == "":
        p1_lines.pop()

    # Strip leading blank lines and \JobSep from part 2
    while p2_lines and p2_lines[0].strip() in ("", "\\JobSep"):
        p2_lines.pop(0)

    # Handle wrapping environment
    if wrapping_env:
        p1_lines.append(f"\n\\end{{{wrapping_env}}}\n")
        p2_lines.insert(0, f"\\begin{{{wrapping_env}}}\n")

    p1_path.write_text("".join(p1_lines), encoding="utf-8")
    p2_path.write_text("".join(p2_lines), encoding="utf-8")

    return p1_path, p2_path


# ---------------------------------------------------------------------------
# Canvas generation helpers
# ---------------------------------------------------------------------------

CANVAS_HEADER = """\
% !! AUTO-GENERATED by scripts/layout.py — DO NOT EDIT !!
% Source: content/layout.yaml

% ===========================================================================
% CANVAS.TEX — Layout Assembly (auto-generated)
% ===========================================================================

% --- Load engine ---
\\input{engine/header.tex}
\\input{engine/leftbox.tex}
\\input{engine/rightbox.tex}
\\input{engine/fullbox.tex}
\\input{engine/pageflow.tex}

% --- Load contact data ---
\\input{generated/contact.tex}

% --- Store header for repetition ---
\\SetCVHeader
    {\\StoredContactName}
    {\\StoredContactTitle}
    {\\StoredContactEmail}
    {\\StoredContactPhone}
    {\\StoredContactLinkedIn}
    {\\StoredContactLocation}

"""


def _emit_page_header(out: list[str], page: int) -> None:
    """Emit the header section for a page."""
    out.append(f"% {'=' * 76}")
    out.append(f"% PAGE {page}")
    out.append(f"% {'=' * 76}")
    out.append("")
    if page == 1:
        out.append("% --- Header ---")
        out.append(r"\CVHeader{0}{0}")
        out.append(r"    {\StoredName}{\StoredTitle}")
        out.append(r"    {\StoredEmail}{\StoredPhone}")
        out.append(r"    {\StoredLinkedin}{\StoredLocation}")
        out.append("")
    else:
        out.append(r"\CVPageBreak")
        out.append("")


# ---------------------------------------------------------------------------
# MODE 1: --measure — generate passthrough canvas.tex
# ---------------------------------------------------------------------------

def generate_measure_canvas(sections: list[dict]) -> None:
    """Generate a passthrough canvas.tex that places all boxes sequentially.

    This is used for pass 1 so the box templates can measure content heights
    and write them to boxheights.dat via \\LogBoxHeight.
    """
    left_secs = [s for s in sections if s["column"] == "left"]
    right_secs = [s for s in sections if s["column"] == "right"]
    full_secs = [s for s in sections if s["column"] == "full"]

    out: list[str] = [CANVAS_HEADER]

    _emit_page_header(out, 1)

    # Place all boxes on page 1, matching the original canvas structure.
    # The box templates measure content in a \savebox before placement,
    # and \LogBoxHeight writes the measured height to boxheights.dat.
    # Boxes may overflow off the page — that's fine for measurement.

    # Left column
    if left_secs:
        out.append("% --- Left column ---")
        out.append(r"\LeftBoxInit{0}{\ContentStartY}")
        for i, sec in enumerate(left_secs):
            if i > 0:
                out.append(r"\LeftBoxGap{\GapBoxToBox}")
            out.append(f"\\LeftBox{{{sec['title']}}}{{generated/{sec['content']}}}")
        out.append("")

    # Right column
    if right_secs:
        out.append("% --- Right column ---")
        out.append(r"\RightBoxInit{\RightColX}{\ContentStartY}")
        for i, sec in enumerate(right_secs):
            if i > 0:
                out.append(r"\RightBoxGap{\GapBoxToBox}")
            out.append(f"\\RightBox{{{sec['title']}}}{{generated/{sec['content']}}}")
        out.append("")

    # Full-width
    if full_secs:
        out.append("% --- Full-width ---")
        out.append(r"\FullBoxInit{0}{\ContentStartY}")
        for i, sec in enumerate(full_secs):
            if i > 0:
                out.append(r"\FullBoxGap{\GapBoxToBox}")
            out.append(f"\\FullBox{{{sec['title']}}}{{generated/{sec['content']}}}")
        out.append("")

    out.append(r"\endinput")

    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    CANVAS_TEX_PATH.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"  Generated {CANVAS_TEX_PATH.relative_to(ROOT)} (measurement pass)")


# ---------------------------------------------------------------------------
# MODE 2: --layout — compute page breaks and generate final canvas.tex
# ---------------------------------------------------------------------------

def generate_layout_canvas(
    sections: list[dict],
    grid: dict,
    heights: dict[str, int],
) -> None:
    """Compute page layout, split overflowing content, write canvas.tex."""

    # Validate heights
    for sec in sections:
        key = f"generated/{sec['content']}"
        if key not in heights:
            _die(
                f"no height measurement for '{key}' in boxheights.dat. "
                "Re-run the measurement pass."
            )

    left_secs = [s for s in sections if s["column"] == "left"]
    right_secs = [s for s in sections if s["column"] == "right"]
    full_secs = [s for s in sections if s["column"] == "full"]

    gap_box = grid["gap_box"]
    max_y = grid["max_page_y"]
    start_y = grid["content_start_y"]

    class BoxPlacement:
        def __init__(self, title: str, content_path: str, column: str, page: int):
            self.title = title
            self.content_path = content_path
            self.column = column
            self.page = page

    def pad_top(col: str) -> float:
        return grid[f"{col}_pad_top"]

    def pad_bot(col: str) -> float:
        return grid[f"{col}_pad_bot"]

    def layout_column(
        col_sections: list[dict], column: str
    ) -> tuple[list[BoxPlacement], int]:
        placements: list[BoxPlacement] = []
        current_y = start_y
        current_page = 1

        for i, sec in enumerate(col_sections):
            content_key = f"generated/{sec['content']}"
            title = sec["title"]
            c_rows = heights[content_key]
            b_rows = box_rows(c_rows, pad_top(column), pad_bot(column))

            # Gap before this box (except first on this page-column)
            gap_needed = gap_box if (
                i > 0 and placements and placements[-1].page == current_page
            ) else 0
            test_y = current_y + gap_needed

            if test_y + b_rows <= max_y:
                # Fits on current page
                current_y = test_y
                placements.append(BoxPlacement(
                    title, f"generated/{sec['content']}", column, current_page
                ))
                current_y += b_rows
            else:
                # Overflow — try to split
                available_content = int(
                    max_y - test_y - 1 - pad_top(column) - pad_bot(column) - 1
                )

                tex_path = GENERATED_DIR / sec["content"]
                boundaries = find_split_boundaries(tex_path)

                split_done = False
                if available_content >= 3 and boundaries:
                    total_lines = len(
                        tex_path.read_text(encoding="utf-8").splitlines()
                    )
                    best_boundary = None
                    for bi, bline in enumerate(boundaries):
                        fraction = bline / total_lines if total_lines > 0 else 0
                        est_rows = int(math.ceil(c_rows * fraction))
                        est_box = box_rows(est_rows, pad_top(column), pad_bot(column))
                        if test_y + est_box <= max_y:
                            best_boundary = bi
                        else:
                            break

                    if best_boundary is not None:
                        p1_path, p2_path = split_content_file(
                            tex_path, boundaries, best_boundary
                        )
                        print(
                            f"  Split {sec['content']} at boundary {best_boundary} "
                            f"-> {p1_path.name}, {p2_path.name}"
                        )

                        current_y = test_y
                        placements.append(BoxPlacement(
                            title, str(p1_path.relative_to(ROOT)),
                            column, current_page
                        ))

                        # Move to next page
                        current_page += 1
                        current_y = start_y
                        placements.append(BoxPlacement(
                            title + " (cont.)",
                            str(p2_path.relative_to(ROOT)),
                            column, current_page
                        ))
                        # Estimate remainder height
                        total_lines_f = float(total_lines) if total_lines > 0 else 1.0
                        remaining_fraction = 1.0 - (
                            boundaries[best_boundary] / total_lines_f
                        )
                        remaining_rows = max(1, int(math.ceil(
                            c_rows * remaining_fraction
                        )))
                        current_y += box_rows(
                            remaining_rows, pad_top(column), pad_bot(column)
                        )
                        split_done = True

                if not split_done:
                    # Can't split — defer entire box to next page
                    current_page += 1
                    current_y = start_y
                    placements.append(BoxPlacement(
                        title, f"generated/{sec['content']}",
                        column, current_page
                    ))
                    current_y += b_rows

        max_pg = max((p.page for p in placements), default=1)
        return placements, max_pg

    left_pl, left_max = layout_column(left_secs, "left")
    right_pl, right_max = layout_column(right_secs, "right")
    full_pl, full_max = layout_column(full_secs, "full")

    total_pages = max(left_max, right_max, full_max)

    # --- Generate canvas.tex ---
    out: list[str] = [CANVAS_HEADER]

    for page in range(1, total_pages + 1):
        _emit_page_header(out, page)

        page_left = [p for p in left_pl if p.page == page]
        if page_left:
            out.append("% --- Left column ---")
            out.append(r"\LeftBoxInit{0}{\ContentStartY}")
            for i, pl in enumerate(page_left):
                if i > 0:
                    out.append(r"\LeftBoxGap{\GapBoxToBox}")
                out.append(f"\\LeftBox{{{pl.title}}}{{{pl.content_path}}}")
            out.append("")

        page_right = [p for p in right_pl if p.page == page]
        if page_right:
            out.append("% --- Right column ---")
            out.append(r"\RightBoxInit{\RightColX}{\ContentStartY}")
            for i, pl in enumerate(page_right):
                if i > 0:
                    out.append(r"\RightBoxGap{\GapBoxToBox}")
                out.append(f"\\RightBox{{{pl.title}}}{{{pl.content_path}}}")
            out.append("")

        page_full = [p for p in full_pl if p.page == page]
        if page_full:
            out.append("% --- Full-width ---")
            out.append(r"\FullBoxInit{0}{\ContentStartY}")
            for i, pl in enumerate(page_full):
                if i > 0:
                    out.append(r"\FullBoxGap{\GapBoxToBox}")
                out.append(f"\\FullBox{{{pl.title}}}{{{pl.content_path}}}")
            out.append("")

        # Init cursors for columns with no boxes on this page (for reset)
        if not page_left and page > 1:
            out.append(r"\LeftBoxInit{0}{\ContentStartY}")
        if not page_right and page > 1:
            out.append(r"\RightBoxInit{\RightColX}{\ContentStartY}")
        out.append("")

    out.append(r"\endinput")

    CANVAS_TEX_PATH.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"  Generated {CANVAS_TEX_PATH.relative_to(ROOT)} (layout pass)")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in ("--measure", "--layout"):
        print(
            "Usage: layout.py --measure   (generate passthrough canvas)\n"
            "       layout.py --layout    (generate canvas with page breaks)",
            file=sys.stderr,
        )
        sys.exit(1)

    mode = sys.argv[1]

    contact = load_contact()
    sections = load_layout()
    params = parse_preamble()
    grid = compute_grid(contact, params)

    print(
        f"Grid: {grid['grid_cols']} cols × {grid['grid_rows']} rows | "
        f"Content starts at Y={grid['content_start_y']} | "
        f"Max Y={grid['max_page_y']}"
    )

    if mode == "--measure":
        print("Generating measurement canvas...")
        generate_measure_canvas(sections)

    elif mode == "--layout":
        heights = load_boxheights()
        print(f"Loaded heights: {heights}")
        print("Computing page layout...")
        generate_layout_canvas(sections, grid, heights)


if __name__ == "__main__":
    main()
