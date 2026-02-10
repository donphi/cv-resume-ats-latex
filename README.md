# LaTeX CV / Resume Builder — Designed + ATS-Optimised (A4 & US Letter)

A single set of YAML files generates two PDFs: a **designed CV** with monospaced box-drawing typography and an **ATS-friendly resume** optimised for applicant tracking systems. Supports A4 (UK/EU curriculum vitae) and US Letter (American resume). Edit your content once, run one Docker command, get both versions.

- **A4** builds produce files named `yourname-cv.pdf` and `yourname-cv-ats.pdf`
- **US Letter** builds produce `yourname-resume.pdf` and `yourname-resume-ats.pdf`

**Only requirement: Docker and Docker Compose.**

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/donphi/cv.git && cd cv

# 2. Edit your content (the only files you touch)
cp content/contact.yaml.example content/contact.yaml
#    Then open content/contact.yaml and fill in your details.
#    Edit the other content/*.yaml files with your experience, education, etc.

# 3. Build both PDFs
./build.sh

# 4. Open your PDFs
#    Output filenames are based on your name and paper size:
#    e.g. donald-philp-cv.pdf and donald-philp-cv-ats.pdf
```

Build flags:

| Flag | Effect |
|------|--------|
| `./build.sh` | Build both designed + ATS PDFs |
| `./build.sh -d` | Designed CV only |
| `./build.sh -a` | ATS CV only |
| `./build.sh -b` | Force-rebuild Docker images first |
| `./build.sh -c` | Remove all build artifacts |

---

## What Each Folder Does

```
content/          <-- YOUR DATA. The only place you edit.
generated/        <-- Auto-built LaTeX files. Do not hand-edit.
engine/           <-- Layout templates (header, boxes, pageflow). Advanced only.
fonts/            <-- Iosevka typefaces (auto-downloaded on first build) + build parameters.
scripts/          <-- Python generator. Reads content/, writes generated/ + ats_main.tex.
doc/              <-- Deep-dive documentation (grid sizing, ATS requirements).
preamble.tex      <-- Styling hyperparameters (fonts, colours, spacing, grid). Advanced only.
canvas.tex        <-- Page assembly (which boxes go where). Advanced only.
main.tex            <-- Entry point for LuaLaTeX. Do not edit.
```

---

## Editing Your Content (Basic)

All content lives in `content/*.yaml`. Each file has comments explaining the format. Special characters (`&`, `$`, `%`, `#`, `_`, `~`) are auto-escaped for LaTeX -- just type plain text.

### contact.yaml -- your details, paper size, and margin

```yaml
paper_size: "a4"          # "a4" (UK/EU, produces a CV) or "letter" (US, produces a Resume)
margin: 13.5              # page margin in mm — MUST be a sweet spot (see below)
name: "Your Name"
title: "Your Target Job Title"
email: "you@example.com"
phone: "+44 123 456 7890"
linkedin: "linkedin.com/in/you"    # no https:// prefix
github: "github.com/you"           # no https:// prefix
location: "London, UK"
full_cv_url: "https://you.com/cv.pdf"  # shown on ATS version
```

**Margin sweet spots** — the designed CV uses a character grid. The margin must be a "sweet spot" so all four sides are equal. Pick from your paper size's row:

| Paper size | Sweet spot margins (mm) | Default |
|------------|------------------------|---------|
| **A4** (default) | 4.0 · 8.7 · **13.5** · 18.3 · 23.0 · 27.8 | **13.5** |
| Letter | 3.1 · 7.9 · **12.6** · 17.4 · 22.2 · 26.9 | **12.6** |

See `content/contact.yaml` comments or `doc/iosevka_sizing.md` for the full explanation and ASCII diagram.

### summary.yaml -- professional summary

A single paragraph. Use `---` for em-dash, `--` for en-dash.

```yaml
text: >-
  Your professional summary goes here. Plain text, no bullet points.
  The >- syntax folds multiple lines into one paragraph.
```

### work_experience.yaml -- jobs

```yaml
entries:
  - role: "Job Title"
    company: "Company Name"
    dates: "Mar 2023 -- Feb 2024"     # Mon YYYY -- Mon YYYY
    location: "London, UK"
    bullets:
      - "First achievement or responsibility"
      - "Second achievement"
```

### education.yaml -- degrees and courses

```yaml
entries:
  - degree: "MSc Computer Science"
    institution: "University Name"
    dates: "2024 -- 2026"
    location: "London, UK"
    details: "First-class ~78% avg"    # shown as italic text (ATS) or progress bar (designed)
    progress: 78                       # 0-100, optional, designed CV only
```

### skills.yaml -- skill groups

```yaml
groups:
  - category: "Languages"
    items:
      - "Python, Go, Rust"            # each item = one line in designed CV
      - "TypeScript, SQL"
```

### research_experience.yaml -- research roles (optional)

Like work experience but with subsections for project groupings. Omit or leave `entries: []` to skip.

### certifications.yaml -- certifications (optional)

Leave `entries: []` to omit this section entirely. To add certifications:

```yaml
entries:
  - name: "AWS Solutions Architect – Associate"
    issuer: "Amazon Web Services"
    year: "2024"

  - name: "Certified Kubernetes Administrator"
    issuer: "Cloud Native Computing Foundation"
    year: "2023"

  - name: "Google Professional Data Engineer"
    issuer: "Google Cloud"
    year: "2023"
```

### publications.yaml -- papers, patents, articles (optional)

Leave `entries: []` to omit this section entirely. To add publications:

```yaml
entries:
  - authors: "Back, S., Smith, J., & Lee, K."
    title: "Scalable Transformer Architectures for Document Understanding"
    venue: "NeurIPS 2025"
    year: "2025"

  - authors: "Scott, D."
    title: "Patent: Method for Adaptive Layout Generation (US 11,234,567)"
    venue: "United States Patent and Trademark Office"
    year: "2023"
```

### acronyms.yaml -- ATS acronym expansion

First occurrence of each acronym in the ATS PDF is expanded. The designed CV is unaffected.

```yaml
acronyms:
  AI: "Artificial Intelligence"
  ML: "Machine Learning"
```

---

## Customising the Design (Advanced)

The files below control how the CV looks. You should not need to touch them for basic use, but they are fully documented for customisation.

### Paper Size and Margins

Both `paper_size` and `margin` are set in `content/contact.yaml`. The generator writes them into `generated/settings.tex`, which is loaded by `preamble.tex` before `\documentclass`. There is nothing to edit in `preamble.tex` for paper size or margins.

See `doc/iosevka_sizing.md` for the full table of symmetric margin sweet spots and the math behind them.

### Colour Themes -- preamble.tex section 4

Four built-in themes. Uncomment one block, comment the others, rebuild:

- **Cool Blue** (active by default)
- **Warm Orange**
- **Monochrome**
- **Forest Green**

The colour system has 3 tiers:

1. **Palette** (8 hex values) -- the only place hex codes exist. Swap one block to re-theme everything.
2. **Roles** -- maps palette to functional categories (box lines, accents, text). Normally untouched.
3. **Elements** -- every visual element has its own colour name. Override any single one to break it out of its group.

### Column Layout -- preamble.tex section 6

```latex
\newcommand{\LeftBoxWidth}{60}    % left column width in grid columns
\newcommand{\ColumnGap}{6}       % gap between columns
% RightBoxWidth is auto-derived: GridCols - LeftBoxWidth - ColumnGap
```

### Box Types -- canvas.tex

Three box types for placing content on the page:

- `\LeftBox{TITLE}{generated/file.tex}` -- left column box
- `\RightBox{TITLE}{generated/file.tex}` -- right column box
- `\FullBox{TITLE}{generated/file.tex}` -- full-width box

All boxes auto-measure their content height. Stack them with `\LeftBoxGap{\GapBoxToBox}` between.

### Page Breaks and Multi-Page -- canvas.tex

```latex
\CVPageBreak          % start a new page (header repeats automatically)
\LeftBoxInit{0}{\ContentStartY}   % reset left column cursor
\RightBoxInit{\RightColX}{\ContentStartY}  % reset right column cursor
```

### Font Sizing -- preamble.tex section 2

```latex
\newcommand{\GridFontSize}{9}        % base mono font size in pt
\newcommand{\MonoWidthRatio}{0.6}    % character width:height ratio
```

Changing `\GridFontSize` rescales the entire grid. See `doc/iosevka_sizing.md` for the full derivation and grid-density table.

---

## Fonts

Three Iosevka families are used (15 TTF files total, ~150 MB):

| Family | Role | Style |
|--------|------|-------|
| **Iosevka Extended** | Grid font (box borders, structural characters) | Monospace |
| **Iosevka Aile** | Body text (bullets, descriptions) | Proportional sans-serif |
| **Iosevka Etoile** | Display/headings (available, currently unused) | Proportional serif |

**Fonts are downloaded automatically** from the [Iosevka GitHub releases](https://github.com/be5invis/Iosevka/releases) the first time you build. The script `scripts/fetch-fonts.sh` downloads only the 15 files needed, caches them in `fonts/iosevka/`, and skips the download on subsequent builds. No manual font installation required.

The font version is pinned in `scripts/fetch-fonts.sh` (currently v34.1.0). To update, change `IOSEVKA_VERSION`, delete the cached TTFs, and rebuild.

Source: [github.com/be5invis/Iosevka](https://github.com/be5invis/Iosevka) (SIL Open Font License).

Custom build parameters are stored in `fonts/iosevka/parameters/` for reference. These are Iosevka's upstream config files and are not used during LaTeX compilation.

---

## How It Works

```
content/*.yaml                    You edit these
       |
       v
scripts/generate.py               Runs inside Docker
       |
       +---> generated/*.tex       Designed CV components (LaTeX)
       +---> generated/settings.tex   Paper size config
       +---> generated/.build-meta    Dynamic output filenames
       +---> ats_main.tex          ATS CV (self-contained LaTeX)
       |
       v
canvas.tex + preamble.tex         Layout engine
+ engine/*.tex
       |
       v
LuaLaTeX (designed)               Docker container
pdfLaTeX (ATS)                    Docker container
       |
       v
yourname-cv.pdf                   Designed CV
yourname-cv-ats.pdf               ATS-optimised CV
```

The generator reads plain YAML, escapes special characters for LaTeX, and writes two outputs:

1. **Designed CV**: individual `generated/*.tex` files using custom environments (`treelist`, `timeline`, `skilllist`), consumed by `canvas.tex` which places them in boxes on a character-cell grid.
2. **ATS CV**: a single `ats_main.tex` file with plain `\section` / `\itemize` formatting, optimised for applicant tracking system parsers. Acronyms are expanded on first use.

Both outputs are compiled inside Docker containers. No local dependencies beyond Docker.

---

## Requirements

- **Docker** and **Docker Compose** (that's it)
- No Python, no LaTeX, no fonts to install locally
- Works on Linux, macOS, and Windows (WSL2)

---

## Further Documentation

| File | Contents |
|------|----------|
| `doc/iosevka_sizing.md` | Grid derivation, margin sweet spots, font metrics, column layout math |
| `doc/ats_requirements.md` | ATS formatting rules and constraints |
| `doc/ats_check.md` | ATS compliance checklist |
