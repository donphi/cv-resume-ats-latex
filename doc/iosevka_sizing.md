# Iosevka Grid Sizing Calculation

How the CV's character-cell grid is derived from the Iosevka font parameters
and the master config in `preamble.tex`.

---

## 1. Source Files

| File | Role |
|------|------|
| `font/iosevka/parameters/parameters.toml` | Master font metrics: UPM, leading, cap height, spacing mode |
| `font/iosevka/parameters/shape-width.toml` | Width grades: maps variant names to advance-width values |
| `font/iosevka/parameters/variants.toml` | Character shape variants (does not affect grid sizing) |
| `preamble.tex` (§1–§2) | Page size, margins, grid engine |
| `preamble.tex` (§6) | Box geometry: column widths, gaps, padding |

---

## 2. The UPM System (Units Per Em)

Iosevka is designed on a **1000 UPM** grid. All internal dimensions are expressed in
these units relative to 1 em (the font size). Key values from `parameters.toml`:

```
leading    = 1250    # recommended line height = 1250/1000 = 1.25 em
cap        = 735     # cap height    = 735/1000 = 0.735 em
ascender   = 735     # ascender      = 735/1000 = 0.735 em
xHeight    = 520     # x-height      = 520/1000 = 0.520 em
#descender = -215    # descender     = 215/1000 = 0.215 em (below baseline)
```

The total glyph extent is ascender + |descender| = 735 + 215 = **950 UPM** (0.95 em).
The remaining 50 UPM is internal leading distributed around the glyphs.

The font's recommended line spacing is `leading / 1000 = 1.25 em`, which adds
300 UPM of inter-line space above the 950 glyph extent.

---

## 3. Width Grades (shape-width.toml)

Iosevka is a **monospace** family. Every character in a given variant has the same
advance width, defined by the `width` field in `shape-width.toml`. The width is
expressed in UPM (out of 1000):

| Grade | Section Key | Width (UPM) | Width Ratio | Variant Name |
|-------|-------------|-------------|-------------|--------------|
| 3 | `blend.416` | 416 | 0.416 | Condensed |
| 4 | `blend.456` | 456 | 0.456 | Semi-Condensed |
| **5** | **`blend.500`** | **500** | **0.500** | **Normal (default)** |
| 6 | `blend.547` | 547 | 0.547 | Semi-Extended |
| **7** | **`blend.600`** | **600** | **0.600** | **Extended** |
| 8 | `blend.657` | 657 | 0.657 | — |
| 9 | `blend.720` | 720 | 0.720 | — |

The **width ratio** is simply `width / 1000`. It tells you how wide each character
is relative to the em-square height. For Grade 7 ("Extended"):

```
width_ratio = 600 / 1000 = 0.6
```

This means each character is **0.6 em wide** and **1.0 em tall**.

---

## 4. Master Parameters (preamble.tex §1–§2)

These are the only values a user needs to change to resize the entire layout:

| Parameter | Default | Purpose |
|-----------|---------|---------|
| `\PageFormat` | `a4` | Paper size: `a4` (210x297mm) or `letter` (215.9x279.4mm) |
| `\PageMarginMM` | `13.5` | **Minimum** desired margin (mm) — actual margins will be snapped to grid |
| `\GridFontSize` | `9` | Base monospace font size (pt) |
| `\MonoWidthRatio` | `0.6` | Width-to-height ratio of the mono font (Grade 7 = Extended) |
| `\ContentWidthScale` | `0.82` | Scaling factor for proportional content inside mono borders |

### Symmetric Sweet Spots (A4, 9 pt, MonoWidthRatio 0.6)

`\PageMarginMM` is a **minimum**. The system snaps it outward so the drawable
area is an exact multiple of the cell size. At most values the horizontal and
vertical snapped margins will differ slightly, but at specific **sweet spots**
they become near-identical (Δ ≈ 0.002 mm).

**Why sweet spots exist.** The cell aspect ratio equals `MonoWidthRatio` (0.6),
which means every 5 columns spans exactly the same physical distance as 3 rows:

```
5 × CellWidth  = 5 × 1.905 = 9.525 mm
3 × CellHeight = 3 × 3.175 = 9.525 mm
```

So the horizontal and vertical margins shrink/grow in lockstep at intervals of
5 cols / 3 rows. At each such step the H and V margins are nearly equal,
producing a balanced, symmetric layout.

**How to read the table.** The "Safe min" column is the value to put in
`\PageMarginMM` (rounded down to 1 decimal to stay safely below the grid
boundary). The actual snapped margins will be the MarginH / MarginV values.

| Grid | MarginH (mm) | MarginV (mm) | |H−V| (mm) | Safe min | Page % |
|------|-------------|-------------|------------|----------|--------|
| 106 × 91 | 4.035 | 4.037 | 0.002 | 4.0 | 1.6% |
| 101 × 88 | 8.798 | 8.800 | 0.002 | 8.7 | 3.5% |
| **96 × 85** | **13.560** | **13.562** | **0.002** | **13.5** | **5.4%** |
| 91 × 82 | 18.323 | 18.325 | 0.002 | 18.3 | 7.2% |
| 86 × 79 | 23.085 | 23.088 | 0.002 | 23.0 | 9.1% |
| 81 × 76 | 27.848 | 27.850 | 0.002 | 27.8 | 11.0% |
| 76 × 73 | 32.610 | 32.613 | 0.002 | 32.6 | 12.9% |
| 71 × 70 | 37.373 | 37.375 | 0.002 | 37.3 | 14.7% |
| 66 × 67 | 42.135 | 42.138 | 0.002 | 42.1 | 16.6% |
| 61 × 64 | 46.898 | 46.900 | 0.002 | 46.8 | 18.5% |
| 56 × 61 | 51.660 | 51.663 | 0.002 | 51.6 | 20.4% |

The default **96 × 85** (min = 13.5) is highlighted. It gives ~13.56 mm
symmetric margins — a comfortable, professional margin that maximises the
grid area (96 columns, 85 rows) while keeping the document well-framed.

**Non-sweet-spot values still work** — the grid will always be correctly
snapped. The margins just won't be symmetric. For example, `\PageMarginMM{15}`
gives 94 × 84 with MarginH = 15.465 mm vs MarginV = 15.150 mm (a 0.315 mm
difference — imperceptible, but not mathematically elegant).

**Why separate H/V margins aren't needed.** At a sweet spot the H/V difference
is 0.002 mm (thinner than a human hair). Adding a second margin parameter would
add complexity for no visible benefit.

### Column Gap (X-Gap) Sweet Spots

The `\ColumnGap` is always an integer number of grid columns, so it is
inherently on-grid. But some values produce more **harmonious column splits**
than others.

The margin sweet-spot pattern repeats every **5 columns** (see above). For
the column gap to respect this pattern, the remaining columns after the gap
(`GridCols − ColumnGap`) should be divisible by 5. This allows both
`\LeftBoxWidth` and `\RightBoxWidth` to sit on 5-column boundaries.

With GridCols = 96:

| ColumnGap | Remaining | ÷5 | ÷10 | Example splits (Left / Right) | Notes |
|-----------|-----------|----|----|-------------------------------|-------|
| 1 | 95 | ✓ | — | 50/45, 55/40, 45/50, 60/35 | Narrowest gap (1 character) |
| **6** | **90** | **✓** | **✓** | **50/40, 45/45, 60/30, 55/35** | **Recommended — widest range of clean splits** |
| 11 | 85 | ✓ | — | 50/35, 45/40, 55/30, 40/45 | Wide gap (11 characters) |

All other gap values (2–5, 7–10, 12–15) leave a remainder that is **not**
divisible by 5, so neither box width can sit on a 5-column boundary unless
the other compensates with an off-pattern width.

**Gap 6 is optimal** because 90 is divisible by 2, 3, 5, 6, 9, and 10 — the
richest set of factors of any option. This means nearly any desired column
ratio (equal, golden, 2:1, 3:2, etc.) can be expressed with clean integer
widths on 5-column boundaries.

**Practical splits with Gap 6:**

| Left | Right | Ratio | Character |
|------|-------|-------|-----------|
| 45 | 45 | 1:1 | Equal columns |
| 50 | 40 | 5:4 | Slightly wider left |
| 55 | 35 | 11:7 | Dominant left |
| **60** | **30** | **2:1** | **Two-thirds / one-third (default)** |

### Vertical Gap (Y-Gap) Sweet Spots

Vertical gaps use `\vspace{N\TPVertModule}` where `N` is a multiplier of one
grid row. Unlike `\ColumnGap`, vertical gaps can be **fractional** (e.g. 0.5
rows). They are always grid-compliant because `\TPVertModule` is the exact
height of one cell.

```
1 grid row = CellHeight = 3.175 mm
```

| Gap (rows) | mm | Use case | Current parameter |
|-----------|--------|----------|-------------------|
| 0.1 | 0.318 | Tight nudge after subheading | `\GapAfterSubHead` |
| 0.25 | 0.794 | Fine spacing | — |
| 0.5 | 1.588 | Standard section spacing | `\GapBeforeSubHead`, `\GapAfterDesc`, `\GapJobToJob` |
| 0.75 | 2.381 | Three-quarter row | — |
| 1.0 | 3.175 | Between stacked boxes | `\GapBoxToBox` |
| 1.5 | 4.763 | Generous section break | — |
| 2.0 | 6.350 | Double row gap | — |
| 3.0 | 9.525 | Large section break | — |

**Stick to multiples of 0.25 rows** for visual consistency. The mm values will
always have decimals (since CellHeight = 3.175 mm = 127/40 mm), but this is
handled transparently by LaTeX — no rounding error accumulates.

---

## 5. Grid Derivation Chain (Margin-Authority Model)

The derivation follows the **Margin-Authority** principle: the user specifies a
*minimum* margin, and the system snaps it outward so that the drawable area is an
exact integer multiple of the cell size. This guarantees column 0 is precisely at
the left margin and column `GridCols-1` is precisely at the right margin.

### 5.1 Page Dimensions

```
PageWidthMM  = 210   (A4) or 215.9 (Letter)    — from \PageFormat
PageHeightMM = 297   (A4) or 279.4 (Letter)    — from \PageFormat
```

### 5.2 Point-to-Millimetre Conversion

A TeX PostScript point is defined as 1/72 of an inch:

```
PtToMM = 25.4 mm / 72 = 0.35277̄ mm per pt
```

This is stored in `\PtToMM` (via `\fpeval{25.4 / 72}`) so no magic number
appears in the cell-size formulas.

### 5.3 Cell Size (Step 1 in preamble.tex)

```
CellWidth  = GridFontSize * MonoWidthRatio * PtToMM
           = 9 * 0.6 * (25.4/72)
           = 9 * 0.6 * 0.35277̄
           = 1.905 mm

CellHeight = GridFontSize * PtToMM
           = 9 * (25.4/72)
           = 9 * 0.35277̄
           = 3.175 mm
```

Each monospace character occupies a cell that is **1.905 mm wide** and **3.175 mm tall**.

### 5.4 Grid Dimensions (Step 2)

How many whole cells fit inside the minimum margin on each axis?

```
GridCols = floor((PageWidthMM  - 2 * PageMarginMM) / CellWidth)
         = floor((210 - 2 × 13.5) / 1.905)
         = floor(183 / 1.905)
         = 96

GridRows = floor((PageHeightMM - 2 * PageMarginMM) / CellHeight)
         = floor((297 - 2 × 13.5) / 3.175)
         = floor(270 / 3.175)
         = 85
```

**The CV grid is 96 columns × 85 rows** (at default A4 / 13.5 mm / 9 pt settings).

### 5.5 Exact Drawable Area (Step 3)

The drawable area is the grid multiplied by the cell size — *not* the page minus
margins. This guarantees zero fractional-cell waste:

```
DrawableWidth  = GridCols * CellWidth  = 96 × 1.905 = 182.880 mm
DrawableHeight = GridRows * CellHeight = 85 × 3.175 = 269.875 mm
```

### 5.6 Snapped Margins (Step 4)

The leftover space after the exact drawable area is split evenly between both
sides. The result is always ≥ the requested minimum:

```
MarginH = (PageWidthMM  - DrawableWidth)  / 2
        = (210 - 182.880) / 2
        = 13.560 mm   (>= 13.5 ✓)

MarginV = (PageHeightMM - DrawableHeight) / 2
        = (297 - 269.875) / 2
        = 13.563 mm   (>= 13.5 ✓)
```

Because 13.5 sits on a **symmetric sweet spot** (see §4), the horizontal and
vertical margins are near-identical: |H − V| = 0.002 mm. The grid fills the
page symmetrically on all four sides.

### 5.7 Geometry & textpos (Step 5)

```latex
\geometry{left=\MarginH mm, right=\MarginH mm, top=\MarginV mm, bottom=\MarginV mm}
\textblockorigin{\MarginH mm}{\MarginV mm}
```

The `textpos` origin is set to the snapped margin, so `(0, 0)` in grid
coordinates is the top-left corner of the drawable area.

---

## 6. Layout Derivation (preamble.tex §6)

Once the grid dimensions are known, the two-column layout is derived.
The key invariant is:

```
LeftBoxWidth + ColumnGap + RightBoxWidth = GridCols   (always)
```

This means the left box is pinned to the left margin, the right box is pinned
to the right margin, and the gap sits between them.

| Parameter | Value | Derivation |
|-----------|-------|------------|
| `\HeaderWidth` | 96 | `= \GridCols` (margin to margin) |
| `\HeaderHeight` | 6 | Master parameter |
| `\ContentStartY` | 7 | `= \HeaderHeight + 1` |
| `\LeftBoxWidth` | 60 | Master parameter |
| `\ColumnGap` | 6 | Master parameter (sweet spot — see §4) |
| `\RightBoxWidth` | 30 | `= \GridCols - \LeftBoxWidth - \ColumnGap` |
| `\RightColX` | 66 | `= \LeftBoxWidth + \ColumnGap` |

Content widths (for proportional font minipages):

```
LeftContentWidth  = (LeftBoxWidth  - PadLeft - PadRight) * ContentWidthScale
                  = (60 - 2 - 1) * 0.82 = 46.74 grid cols

RightContentWidth = (RightBoxWidth - PadLeft - PadRight) * ContentWidthScale
                  = (30 - 2 - 1) * 0.82 = 22.14 grid cols
```

---

## 7. How the Three Fonts Use the Grid

### 7.1 Mono (Iosevka Extended) — The Grid Font

```latex
\mono = \ttfamily at \GridFontSize pt with baselineskip = \GridFontSize pt
```

- Font size = baselineskip = 9pt (zero extra leading)
- One character = exactly one grid cell
- Box-drawing characters (│ ─ ┌ └ ╘ ═ ╖ etc.) connect seamlessly across cells
- **This font defines the grid. Everything else adapts to it.**

### 7.2 Aile (Iosevka Aile) — Body Text Font

```latex
\aile = \rmfamily (proportional sans-serif)
baselineskip = ContentLeading * TPVertModule = 1.2 * (one grid row)
```

- Proportional: characters have varying widths
- Does NOT align character-by-character to the grid
- Baselineskip is 1.2 grid rows, giving readable line spacing
- Content areas are scaled by `\ContentWidthScale = 0.82` to account for
  the proportional font being ~18% wider per character on average

### 7.3 Etoile (Iosevka Etoile) — Display/Heading Font

```latex
\etoile = \sffamily (proportional serif)
```

- Available for headings or display use
- Same proportional behaviour as Aile
- Currently wired up but unused in the templates

---

## 8. Leading and Line Spacing

The font's `parameters.toml` recommends `leading = 1250` (1.25 em line height).
The grid uses three different leading values depending on context:

| Context | Baselineskip | Grid Rows Per Line | Purpose |
|---------|-------------|-------------------|---------|
| Mono (borders) | 1.0 em (9pt) | 1.0 | Box-drawing chars connect vertically |
| Left body text | 1.2 * grid row | 1.2 | Readable prose, slightly tighter than font default |
| Right body text | 1.2 * grid row | 1.2 | Same as left |

The `\ContentLeading = 1.2` value in `preamble.tex` is slightly less than the
font's recommended 1.25. This was chosen to keep body text compact while
remaining readable. Proportional text "floats" on its own baseline grid
(every 1.2 rows) rather than snapping to integer grid rows.

---

## 9. Typeface File Inventory

Files in `font/iosevka/typefaces/`:

### Mono (grid-aligned, structural)
| File | Used As | Role |
|------|---------|------|
| `Iosevka-Extended.ttf` | UprightFont | Box borders, decorative chars |
| `Iosevka-ExtendedBold.ttf` | BoldFont, BoldItalicFont | Bold structural chars |
| `Iosevka-ExtendedItalic.ttf` | ItalicFont | Italic structural chars |
| `Iosevka-ExtendedBoldItalic.ttf` | — | Available but not loaded |
| `Iosevka-BoldItalic.ttf` | — | Non-Extended; unused |

### Aile (proportional sans-serif, body text)
| File | Used As |
|------|---------|
| `IosevkaAile-Regular.ttf` | UprightFont |
| `IosevkaAile-Bold.ttf` | BoldFont |
| `IosevkaAile-Italic.ttf` | ItalicFont |
| `IosevkaAile-BoldItalic.ttf` | BoldItalicFont |
| `IosevkaAile-SemiBold.ttf` | — (available) |

### Etoile (proportional serif, display)
| File | Used As |
|------|---------|
| `IosevkaEtoile-Regular.ttf` | UprightFont |
| `IosevkaEtoile-Bold.ttf` | BoldFont |
| `IosevkaEtoile-Italic.ttf` | ItalicFont |
| `IosevkaEtoile-BoldItalic.ttf` | BoldItalicFont |
| `IosevkaEtoile-SemiBold.ttf` | — (available) |

---

## 10. Quick Reference: Changing Grid Density

To adjust the grid, change `\GridFontSize` in `preamble.tex`. Everything else
recomputes automatically.

| Font Size (pt) | Cell Width (mm) | Cell Height (mm) | Cols | Rows |
|---------------|-----------------|-------------------|------|------|
| 8.0 | 1.693 | 2.822 | 108 | 95 |
| 8.5 | 1.799 | 2.999 | 101 | 90 |
| **9.0** | **1.905** | **3.175** | **96** | **85** |
| 9.5 | 2.011 | 3.351 | 91 | 80 |
| 10.0 | 2.117 | 3.528 | 86 | 76 |

All values use `\MonoWidthRatio = 0.6`, `\PageMarginMM = 13.5` (A4).
Actual margins are snapped to the nearest symmetric sweet spot.
Column/row counts are always exact integers.

---

## 11. Full Parameter Map

### Master Parameters (user edits these)

| Parameter | Section | Default | Controls |
|-----------|---------|---------|----------|
| `\PageFormat` | §1 | `a4` | Paper size (a4 or letter) |
| `\PageMarginMM` | §1 | `13.5` | **Minimum** desired margin (mm) — use a sweet-spot value (see §4) |
| `\GridFontSize` | §2 | `9` | Base mono font size (pt) |
| `\MonoWidthRatio` | §2 | `0.6` | Mono character width-to-height ratio |
| `\ContentWidthScale` | §2 | `0.82` | Proportional-to-mono width scaling |
| `\HeaderHeight` | §6 | `6` | Header rows |
| `\HeaderContactSep` | §6 | `3` | Dot-gaps between contact items |
| `\LeftBoxWidth` | §6 | `60` | Left column width (grid cols) |
| `\ColumnGap` | §6 | `6` | Gap between columns (grid cols, sweet spot) |
| `\Left/RightBoxPad*` | §6 | `1–2` | Box padding (cols/rows) |
| `\ContentLeading` | §5 | `1.2` | Body text line height (grid rows) |
| `\ContentNudge*` | §5 | `2pt` | Content micro-adjustments |
| `\ContentBleed*` | §5 | `3pt` | White bleed over dot texture |

### Derived Values (computed automatically — do not edit)

| Parameter | Derivation |
|-----------|------------|
| `\PageWidthMM` / `\PageHeightMM` | From `\PageFormat` |
| `\CellWidth` / `\CellHeight` | Font size × ratio × pt-to-mm (Step 1) |
| `\GridCols` / `\GridRows` | floor((page − 2 × min margin) / cell) (Step 2) |
| `\DrawableWidth` / `\DrawableHeight` | grid × cell — exact, zero waste (Step 3) |
| `\MarginH` / `\MarginV` | (page − drawable) / 2 — snapped, ≥ minimum (Step 4) |
| `\HeaderWidth` | = `\GridCols` |
| `\ContentStartY` | = `\HeaderHeight + 1` |
| `\RightBoxWidth` | = `\GridCols - \LeftBoxWidth - \ColumnGap` |
| `\RightColX` | = `\LeftBoxWidth + \ColumnGap` |
| `\Left/RightContentWidth` | (box − padding) × `\ContentWidthScale` |
