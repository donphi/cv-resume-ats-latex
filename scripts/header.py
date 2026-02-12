#!/usr/bin/env python3
"""
header.py — Render the CV name as ASCII art for mainframe/crt headers.

Reads:
    content/contact.yaml   — name, header_theme, paper_size, margin
    engine/preamble.tex    — GridFontSize, MonoWidthRatio (via layout.py)

Writes:
    generated/header_name.tex — Pre-rendered TeX \\defs for the ASCII-art name
                                rows, plus pre-computed dash/dot counts for
                                deterministic centering.

For "classic" theme, this script writes a no-op file (exits cleanly).
For "mainframe", it uses the 5-row double-line box-drawing font (FONT_5ROW).
For "crt", it uses the 4-row solid-block font (FONT_4ROW).

This script has ZERO default values. All parameters come from contact.yaml
and preamble.tex. If any required value is missing, the script exits with
a clear error.

Grid computation (page sizes, cell math, grid cols) is imported from
lib/config.py — the single source of truth for those calculations.
Nothing is duplicated.

Font glyphs are imported from font.py — the single source of truth for
both the 5-row and 4-row ASCII-art alphabets. Nothing is duplicated.

The output file defines:
    \\HeaderNameRowA .. \\HeaderNameRowE  — raw Unicode rows (5 for mainframe, 4 for crt)
    \\HeaderNameRows   — number of name rows
    \\HeaderNameWidth  — display width of the rendered name in columns
    \\NameDashTotal, \\NameDashLeft, \\NameDashRight — for row 0 (top border)
    \\NameDotTotal, \\NameDotLeft, \\NameDotRight   — for inner dot rows (1..N)

These are consumed by engine/header_mainframe.tex and engine/header_crt.tex.
The TeX templates do ZERO arithmetic on the name — they use these values directly.
"""

from __future__ import annotations

import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Shared infrastructure — single source of truth
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.config import (  # noqa: E402
    ROOT,
    GENERATED_DIR,
    VALID_HEADER_THEMES,
    die,
    load_contact,
    parse_preamble,
    compute_grid,
)
from font import FONT_5ROW, FONT_4ROW  # noqa: E402

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
OUTPUT_PATH = GENERATED_DIR / "header_name.tex"


# =============================================================================
# Rendering
# =============================================================================

def render_name(name: str, font_dict: dict) -> list[str]:
    """Render a name string using the given font dictionary.

    Returns a list of strings, one per row of the rendered output.
    All rows are guaranteed to be the same length (padded with spaces if needed).
    """
    rows = len(next(iter(font_dict.values())))
    lines: list[str] = []
    for row in range(rows):
        line = "".join(
            font_dict.get(ch, font_dict.get(' ', [' '] * rows))[row]
            for ch in name.upper()
        )
        lines.append(line)

    # Pad all rows to the same width (max row length)
    max_w = max(len(r) for r in lines)
    lines = [r.ljust(max_w) for r in lines]

    return lines


# =============================================================================
# TeX output
# =============================================================================

def generate_header_name_tex(
    name: str,
    theme: str,
    header_width: int,
) -> str:
    """Generate the content of generated/header_name.tex.

    Pre-computes ALL centering arithmetic so the TeX templates do ZERO math
    on the name art. This guarantees deterministic, pixel-perfect alignment.

    Defines:
        \\HeaderNameRowA .. \\HeaderNameRowE  (5 rows for mainframe, 4 for crt)
        \\HeaderNameRows   — number of name rows (5 or 4)
        \\HeaderNameWidth  — display width of the rendered name in columns
        \\NameDashTotal, \\NameDashLeft, \\NameDashRight — for row 0 (top border)
        \\NameDotTotal, \\NameDotLeft, \\NameDotRight   — for inner dot rows
    """
    if theme == "mainframe":
        font = FONT_5ROW
    elif theme == "crt":
        font = FONT_4ROW
    else:
        die(f"header.py called for unsupported theme '{theme}'")
        return ""  # unreachable

    rendered = render_name(name, font)
    num_rows = len(rendered)
    name_width = len(rendered[0])  # all rows same length after padding

    # -------------------------------------------------------------------------
    # Pre-compute centering values (replicates the TeX math exactly)
    # -------------------------------------------------------------------------
    #
    # ROW 0 (top border):
    #   ┌(1) + dashes(left) + ·(1) + space(1) + NAME(W) + space(1) + ·(1) + dashes(right) + ╖(1)
    #   Fixed overhead = 6 chars
    #   dashTotal = headerWidth - 6 - nameWidth
    #
    name_dash_total = header_width - 6 - name_width
    if name_dash_total < 0:
        die(
            f"Name art is too wide ({name_width} cols) for the grid "
            f"({header_width} cols). Shorten the name or use a wider margin."
        )
    name_dash_left = name_dash_total // 2
    name_dash_right = name_dash_total - name_dash_left

    # INNER DOT ROWS (rows 1..N):
    #   │(1) + dots(left) + space(1) + NAME(W) + space(1) + dots(right) + ║(1)
    #   Fixed overhead = 4 chars
    #   dotTotal = headerWidth - 4 - nameWidth
    #
    name_dot_total = header_width - 4 - name_width
    name_dot_left = name_dot_total // 2
    name_dot_right = name_dot_total - name_dot_left

    # -------------------------------------------------------------------------
    # Verification (belt and suspenders)
    # -------------------------------------------------------------------------
    row0_check = 1 + name_dash_left + 1 + 1 + name_width + 1 + 1 + name_dash_right + 1
    rowN_check = 1 + name_dot_left + 1 + name_width + 1 + name_dot_right + 1
    assert row0_check == header_width, (
        f"Row 0 width mismatch: {row0_check} != {header_width}"
    )
    assert rowN_check == header_width, (
        f"Inner row width mismatch: {rowN_check} != {header_width}"
    )

    # -------------------------------------------------------------------------
    # Build output
    # -------------------------------------------------------------------------
    row_labels = "ABCDEFGHIJ"

    lines = [
        "% !! AUTO-GENERATED by scripts/header.py — DO NOT EDIT !!",
        f"% Theme: {theme}, Name: {name}, HeaderWidth: {header_width}",
        "%",
        f"% Name art width: {name_width} cols",
        f"% Row 0 check: 1+{name_dash_left}+1+1+{name_width}+1+1+{name_dash_right}+1 = {row0_check}",
        f"% Row N check: 1+{name_dot_left}+1+{name_width}+1+{name_dot_right}+1 = {rowN_check}",
        "",
        f"\\def\\HeaderNameRows{{{num_rows}}}",
        f"\\def\\HeaderNameWidth{{{name_width}}}",
        "",
        f"\\def\\NameDashTotal{{{name_dash_total}}}",
        f"\\def\\NameDashLeft{{{name_dash_left}}}",
        f"\\def\\NameDashRight{{{name_dash_right}}}",
        "",
        f"\\def\\NameDotTotal{{{name_dot_total}}}",
        f"\\def\\NameDotLeft{{{name_dot_left}}}",
        f"\\def\\NameDotRight{{{name_dot_right}}}",
        "",
    ]

    for i, row in enumerate(rendered):
        label = row_labels[i]
        # Replace every space with ~ (TeX non-breaking space) so each blank
        # cell occupies exactly one grid column. Without this, TeX collapses
        # consecutive/trailing spaces and the row width shrinks.
        tex_row = row.replace(" ", "~")
        lines.append(f"\\def\\HeaderNameRow{label}{{{tex_row}}}")

    lines.append("")
    return "\n".join(lines) + "\n"


# =============================================================================
# Main
# =============================================================================

def main() -> None:
    contact = load_contact()

    name = contact.get("name")
    if not name:
        die("'name' not found in contact.yaml")

    theme_raw = contact.get("header_theme")
    if not theme_raw:
        die("required field 'header_theme' not found in contact.yaml")
    theme = str(theme_raw).lower()

    if theme not in VALID_HEADER_THEMES:
        die(
            f"unknown header_theme '{theme}' in contact.yaml "
            f"(must be one of: {', '.join(VALID_HEADER_THEMES)})"
        )

    if theme == "classic":
        # Classic theme doesn't need ASCII-art name rendering.
        # Write an empty file so \input doesn't fail.
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_PATH.write_text(
            "% header_name.tex — not used for classic theme\n",
            encoding="utf-8",
        )
        print(f"  Generated {OUTPUT_PATH.relative_to(ROOT)} (classic — no-op)")
        return

    # Compute grid columns (= HeaderWidth) using layout.py's grid math
    params = parse_preamble()
    grid = compute_grid(contact, params)
    header_width = grid["grid_cols"]

    content = generate_header_name_tex(name, theme, header_width)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(content, encoding="utf-8")
    print(
        f"  Generated {OUTPUT_PATH.relative_to(ROOT)} "
        f"({theme}, name_width={len(render_name(name, FONT_5ROW if theme == 'mainframe' else FONT_4ROW)[0])}, "
        f"header_width={header_width})"
    )


if __name__ == "__main__":
    main()
