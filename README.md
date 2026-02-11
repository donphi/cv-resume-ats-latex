# LaTeX CV / Resume Builder — Designed + ATS-Optimised (A4 & US Letter)

One set of YAML files. Two PDFs. Zero LaTeX knowledge required.

A **designed CV / Resume** with monospaced box-drawing typography and an **ATS-friendly CV / Resume** built for applicant tracking systems — both generated from the same content, both compiled inside Docker. Supports A4 (UK/EU curriculum vitae) and US Letter (American resume).

**Only requirement: [Docker](https://www.docker.com/) and Docker Compose.**

---

## What You Get

<!-- SCREENSHOT: Full-page side-by-side of both PDFs.
     Capture: Open fred-durst-cv.pdf and fred-durst-cv-ats.pdf side by side.
     Zoom to fit both full pages in one screenshot.
     Save as: doc/images/both-cvs-side-by-side.png
     Dimensions: ~1400px wide recommended. -->
![Designed CV and ATS Resume side by side](doc/images/both-cvs-side-by-side.png)

*Left: the designed CV with box-drawing grid layout. Right: the ATS-optimised version — clean, parseable, no formatting tricks.*

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/donphi/cv.git && cd cv

# 2. Edit your content (the only files you touch)
cp content/contact.yaml.example content/contact.yaml
#    Then fill in content/contact.yaml and the other content/*.yaml files.

# 3. Build both PDFs
./build.sh

# That's it. Your PDFs appear in the project root:
#   fred-durst-cv.pdf        (designed)
#   fred-durst-cv-ats.pdf    (ATS-optimised)
```

### Build Flags

| Flag | What it does |
|------|--------------|
| `./build.sh` | Build both designed + ATS PDFs |
| `./build.sh -d` | Designed CV only |
| `./build.sh -a` | ATS CV only |
| `./build.sh -b` | Force-rebuild Docker images first |
| `./build.sh -c` | Remove all build artifacts |

### Output Files

| Paper Size | Designed | ATS-Optimised |
|------------|----------|---------------|
| **A4** (UK/EU) | `yourname-cv.pdf` | `yourname-cv-ats.pdf` |
| **US Letter** | `yourname-resume.pdf` | `yourname-resume-ats.pdf` |

> 💡 Fonts are downloaded automatically on first build (~15 seconds). Subsequent builds skip the download.

---

## The Example: Fred Durst's CV

The repo ships with a complete example CV for **Fred Durst** — Senior Nookie Engineer, frontman of Limp Bizkit, film director, and certified backwards-red-cap operator. Every YAML file is filled in so you can build immediately and see exactly what the output looks like before editing your own content.

### The Designed CV

<!-- SCREENSHOT: Full page 1 of the designed CV.
     Capture: Open fred-durst-cv.pdf, page 1, zoom to fit width.
     Save as: doc/images/designed-page1.png -->
![Designed CV — Page 1](doc/images/designed-page1.png)

The designed version uses a **character-cell grid** — every element is placed on an exact monospaced grid, giving the layout a technical, engineered feel. The left column holds work experience and research; the right column holds education, skills, and contact details.

### Header Detail

<!-- SCREENSHOT: Zoomed crop of the header area (name, title, contact bar).
     Capture: Zoom to ~200% on the top of page 1, crop just the header
     section showing the name "Fred Durst", title, and contact line.
     Save as: doc/images/detail-header.png -->
![Header detail](doc/images/detail-header.png)

*The header is built from `content/contact.yaml`. Name, title, email, phone, LinkedIn, GitHub, and location — all pulled from one file.*

### Work Experience Detail

<!-- SCREENSHOT: Zoomed crop of one work experience entry.
     Capture: Zoom to ~200% on the "Lead Vocalist & Chief Nookie Officer"
     entry showing the role, company, dates, and bullet points.
     Save as: doc/images/detail-work-experience.png -->
![Work experience detail](doc/images/detail-work-experience.png)

*Each role shows the title, company, date range, and bullet points. The box-drawing borders and section headers are all generated — you just write plain text in `content/work_experience.yaml`.*

### Skills & Education Detail

<!-- SCREENSHOT: Zoomed crop of the right column showing skills and education.
     Capture: Zoom to ~200% on the right column, crop to show the skills
     grid and at least one education entry with a progress bar.
     Save as: doc/images/detail-skills-education.png -->
![Skills and education detail](doc/images/detail-skills-education.png)

*Skills are grouped by category. Education entries can include an optional progress bar (the "Certified Red Cap Specialist" at 100% is a personal favourite).*

### The ATS Version

<!-- SCREENSHOT: Full page 1 of the ATS CV.
     Capture: Open fred-durst-cv-ats.pdf, page 1, zoom to fit width.
     Save as: doc/images/ats-page1.png -->
![ATS CV — Page 1](doc/images/ats-page1.png)

*The ATS version strips all visual formatting. Plain sections, plain bullets, standard fonts. Acronyms are expanded on first use (e.g. "Artists and Repertoire (A&R)"). This is what the robot reads.*

### Certifications & Publications

<!-- SCREENSHOT: Zoomed crop of the certifications and publications sections
     from either the designed or ATS version (whichever looks better).
     Capture: Zoom to ~200%, crop to show the certifications list
     (RIAA Diamond, MTV VMA, etc.) and publications list.
     Save as: doc/images/detail-certs-pubs.png -->
![Certifications and publications](doc/images/detail-certs-pubs.png)

*Both sections are optional — leave `entries: []` in the YAML to omit them entirely. Fred's RIAA Diamond certification and backwards-cap aerodynamics patent are included for demonstration purposes.*

---

## Project Structure

```
📦 cv-resume-ats-latex/
│
├── 📁 content/ ·································· ✏️ YOUR CV TEXT GOES HERE
│   │
│   │   Each file below maps to one section of your CV.
│   │   Edit these YAML files with your own information —
│   │   the build system handles all LaTeX formatting.
│   │
│   ├── contact.yaml ····························· Name, email, phone, links, paper size
│   ├── summary.yaml ····························· Professional summary paragraph
│   ├── work_experience.yaml ····················· Jobs: role, company, dates, bullets
│   ├── education.yaml ··························· Degrees, institutions, dates
│   ├── skills.yaml ······························ Skill categories and items
│   ├── research_experience.yaml ················· Research roles (optional)
│   ├── certifications.yaml ······················ Certifications (optional)
│   ├── publications.yaml ························ Papers, patents, albums (optional)
│   ├── acronyms.yaml ···························· ATS acronym expansions
│   └── layout.yaml ······························ Section order and column placement
│
├── 📁 engine/ ··································· 🔧 Layout templates (advanced users)
│   ├── preamble.tex ····························· Styling: fonts, colours, spacing, grid
│   ├── canvas.tex ······························· Auto-generated redirect — do not edit
│   ├── header.tex ······························· Header template
│   ├── leftbox.tex ······························ Left column box template
│   ├── rightbox.tex ····························· Right column box template
│   ├── fullbox.tex ······························ Full-width box template
│   └── pageflow.tex ····························· Page break + header repeat logic
│
├── 📁 generated/ ································ 🤖 Auto-built .tex files — do not edit
├── 📁 build/ ···································· 🗑️ LaTeX intermediate files — gitignored
├── 📁 fonts/ ···································· 🔤 Iosevka typefaces (auto-downloaded)
├── 📁 scripts/ ·································· ⚙️ Python generator, layout engine
├── 📁 doc/ ······································ 📖 Deep-dive docs (grid sizing, ATS)
│
├── main.tex ····································· Entry point for designed CV
├── main_ats.tex ································· Entry point for ATS CV (auto-generated)
├── build.sh ····································· Build script
├── Dockerfile ··································· Designed CV builder
├── Dockerfile.ats ······························· ATS CV builder
├── docker-compose.yml
├── docker-compose.ats.yml
└── README.md
```

---

## Editing Your Content

All content lives in `content/*.yaml`. Each file has inline comments explaining the format.

> 💡 You can use `&`, `$`, `%`, `#`, `_`, `~` directly in your YAML: the build system escapes them for LaTeX.

Section placement is controlled by `content/layout.yaml` — see [Section Order and Columns](#section-order-and-columns--contentlayoutyaml) below.

---

### 📄 contact.yaml — Your Details, Paper Size, and Margin

```yaml
# content/contact.yaml

paper_size: "a4"          # "a4" (UK/EU → CV) or "letter" (US → Resume)
margin: 13.5              # page margin in mm — pick a sweet spot (see below)
name: "Fred Durst"
title: "Senior Nookie Engineer"
email: "fred.durst@limpbizkit.com"
phone: "+1 904 555 1998"
linkedin: "linkedin.com/in/freddurst"
github: "github.com/freddurst"
location: "Jacksonville, FL"
full_cv_url: "https://freddurst.com/cv.pdf"
```

#### Margin Sweet Spots

The designed CV uses a character grid. The margin must be a "sweet spot" so all four sides are equal:

| Paper size | Sweet spot margins (mm) | Default |
|------------|-------------------------|---------|
| **A4** (default) | 4.0 · 8.7 · **13.5** · 18.3 · 23.0 · 27.8 | **13.5** |
| **Letter** | 3.1 · 7.9 · **12.6** · 17.4 · 22.2 · 26.9 | **12.6** |

> 📖 See `content/contact.yaml` for the full ASCII diagram explaining how the grid works, or `doc/iosevka_sizing.md` for the deep derivation.

---

### 📄 summary.yaml — Professional Summary

```yaml
# content/summary.yaml

text: >-
  Visionary frontman, director, and audio systems architect with 10+ years
  leading high-throughput live performance pipelines processing 20,000+
  concurrent audience nodes per venue. I keep rollin', rollin', rollin'.
```

---

### 📄 work_experience.yaml — Jobs

```yaml
# content/work_experience.yaml

entries:
  - role: "Lead Vocalist & Chief Nookie Officer"
    company: "Limp Bizkit"
    dates: "Aug 1994 -- Present"
    location: "Jacksonville, FL"
    bullets:
      - "Scaled live performance infrastructure to 400,000-node distributed audiences"
      - "Negotiated and closed a $30M record deal with Interscope/Flip Records"
```

---

### 📄 education.yaml — Degrees and Courses

```yaml
# content/education.yaml

entries:
  - degree: "Certified Red Cap Specialist"
    institution: "New Era Institute of Headwear Sciences"
    dates: "1997"
    location: "Buffalo, NY"
    details: "Backwards orientation, 100% consistency"
    progress: 100    # optional progress bar (0-100), designed CV only
```

---

### 📄 skills.yaml — Skill Groups

```yaml
# content/skills.yaml

groups:
  - category: "Headwear"
    items:
      - "Red cap (backwards, 100% uptime)"
      - "Fitted, snapback, trucker variants"
      - "All-weather deployment certified"
```

---

### 📄 research_experience.yaml — Research Roles (Optional)

Like work experience but with subsections for project groupings. Omit or leave `entries: []` to skip.

---

### 📄 certifications.yaml — Certifications (Optional)

Leave `entries: []` to omit. To add:

```yaml
# content/certifications.yaml

entries:
  - name: "RIAA Diamond Certification — Significant Other"
    issuer: "Recording Industry Association of America"
    year: "2001"

  - name: "Backwards Red Cap Operator Licence (Level 5)"
    issuer: "New Era Cap Company"
    year: "1997"
```

---

### 📄 publications.yaml — Albums, Papers, Patents (Optional)

Leave `entries: []` to omit. To add:

```yaml
# content/publications.yaml

entries:
  - authors: "Durst, F., Borland, W., Rivers, W., Otto, J., & Lethal, DJ"
    title: "Significant Other"
    venue: "Flip/Interscope Records (7x Platinum)"
    year: "1999"

  - authors: "Durst, F."
    title: "Patent: Method for Backwards Cap Aerodynamic Optimisation (US 6,969,420)"
    venue: "United States Patent and Trademark Office"
    year: "2002"
```

---

### 📄 acronyms.yaml — ATS Acronym Expansion

First occurrence of each acronym in the ATS PDF is expanded. The designed CV is unaffected.

```yaml
# content/acronyms.yaml

acronyms:
  A&R: "Artists and Repertoire"
  RIAA: "Recording Industry Association of America"
  MTV: "Music Television"
  DJ: "Disc Jockey"
  BPM: "Beats Per Minute"
```

---

## Customising the Design (Advanced)

You should not need to touch these for basic use, but they are fully documented.

---

### Paper Size and Margins

Both are set in `content/contact.yaml`. The generator writes them into `generated/settings.tex`, which `engine/preamble.tex` loads before `\documentclass`. Nothing to edit in `engine/preamble.tex`.

---

### 🎨 Colour Themes — engine/preamble.tex section 4

Four built-in themes. Uncomment one block, comment the others, rebuild:

| Theme | Description |
|-------|-------------|
| **Cool Blue** | Default theme |
| **Warm Orange** | Warmer accent tones |
| **Monochrome** | Black and white |
| **Forest Green** | Nature-inspired |

#### Colour System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  TIER 1: Palette ··········· 8 hex values — the only place      │
│                              hex codes exist. Swap one block    │
│                              to re-theme everything.            │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  TIER 2: Roles ············· Maps palette to functional         │
│                              categories (box lines, accents,    │
│                              text). Normally untouched.         │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  TIER 3: Elements ·········· Every visual element has its       │
│                              own colour name. Override any      │
│                              single one to break it out.        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### 📐 Column Layout — engine/preamble.tex section 6

```latex
\newcommand{\LeftBoxWidth}{60}    % left column width in grid columns
\newcommand{\ColumnGap}{6}        % gap between columns
% RightBoxWidth is auto-derived: GridCols - LeftBoxWidth - ColumnGap
```

---

### 📄 Section Order and Columns — content/layout.yaml

> ⚠️ **This is the file you edit to control which sections appear, in what order, and in which column.** Do not edit `engine/canvas.tex` — it is auto-generated on every build and your changes will be overwritten.

```yaml
# content/layout.yaml

sections:
  - title: "SUMMARY"
    content: "summary.tex"
    column: "left"

  - title: "RESEARCH EXPERIENCE"
    content: "research_experience.tex"
    column: "left"

  - title: "WORK EXPERIENCE"
    content: "work_experience.tex"
    column: "left"

  - title: "TECHNICAL SKILLS"
    content: "skills.tex"
    column: "right"

  - title: "EDUCATION"
    content: "education.tex"
    column: "right"
```

| Field | Description |
|-------|-------------|
| `title` | The heading shown in the box border (e.g. `"SUMMARY"`) |
| `content` | The generated `.tex` filename (relative to `generated/`) |
| `column` | `"left"`, `"right"`, or `"full"` |

Sections within the same column are placed top-to-bottom in the order listed. Add, remove, or reorder entries here and rebuild — the layout engine handles page breaks automatically.

---

### 🔄 Automatic Page Breaks

Page breaks are computed automatically. The build pipeline runs a **two-pass compile**:

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  PASS 1 ······················ LuaLaTeX measures the exact      │
│                                height of every content box      │
│                                                                 │
│                                      │                          │
│                                      ▼                          │
│                                                                 │
│  LAYOUT ENGINE ··············· scripts/layout.py reads those    │
│                                heights, computes where page     │
│                                breaks fall, and splits any      │
│                                overflowing section at a clean   │
│                                boundary (between job entries,   │
│                                skill categories, education      │
│                                items, or research subsections)  │
│                                                                 │
│                                      │                          │
│                                      ▼                          │
│                                                                 │
│  PASS 2 ······················ LuaLaTeX compiles the final      │
│                                PDF with the computed layout     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

You never need to manually insert page breaks or split content files. If your content grows or shrinks, just rebuild and the layout adjusts.

> ⛔ **`engine/canvas.tex` is off limits.** It is a one-line redirect to `generated/canvas.tex`, which is regenerated on every build. Any manual edits will be silently overwritten.

---

### 🔤 Font Sizing — engine/preamble.tex section 2

```latex
\newcommand{\GridFontSize}{9}        % base mono font size in pt
\newcommand{\MonoWidthRatio}{0.6}    % character width:height ratio
```

Changing `\GridFontSize` in `engine/preamble.tex` rescales the entire grid.

> 📖 See `doc/iosevka_sizing.md` for the derivation.

---

## Fonts

Three [Iosevka](https://github.com/be5invis/Iosevka) families are used (15 TTF files, ~150 MB):

| Family | Role | Style |
|--------|------|-------|
| **Iosevka Extended** | Grid font (box borders, structural characters) | Monospace |
| **Iosevka Aile** | Body text (bullets, descriptions) | Proportional sans-serif |
| **Iosevka Etoile** | Display/headings (available, currently unused) | Proportional serif |

> 💡 **Fonts are downloaded automatically** from the [Iosevka GitHub releases](https://github.com/be5invis/Iosevka/releases) the first time you build. The script `scripts/fetch-fonts.sh` downloads only the 15 files needed, caches them in `fonts/iosevka/`, and skips the download on subsequent builds. No manual font installation required.

The font version is pinned in `scripts/fetch-fonts.sh` (currently v34.1.0). To update, change `IOSEVKA_VERSION`, delete the cached TTFs, and rebuild.

Custom build parameters are stored in `fonts/iosevka/parameters/` for reference (Iosevka's upstream config files, not used during LaTeX compilation).

---

## How It Works

```

┌─────────────────────────────────────────────────────────────────┐
│                      ✏️ you edit these                          │
│                       ─────────────────                         │
│                content/*.yaml  +  layout.yaml                   │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │   scripts/generate.py  │
                    │      YAML → LaTeX      │
                    └────────────┬───────────┘
                                 │
                                 │  outputs:
                                 │  ├── generated/*.tex ······ designed CV components
                                 │  ├── generated/settings.tex · paper size + margin
                                 │  ├── generated/.build-meta ·· dynamic output filenames
                                 │  └── main_ats.tex ·········· ATS CV (self-contained)
                                 │
                ┌────────────────┴────────────────┐
                │                                 │
                ▼                                 ▼
     ┌─────────────────────┐           ┌─────────────────────┐
     │    DESIGNED CV      │           │       ATS CV        │
     │                     │           │                     │
     │  layout.py --measure│           │      latexmk        │
     │         │           │           │    main_ats.tex     │
     │         ▼           │           │         │           │
     │  LuaLaTeX (pass 1)  │           │         ▼           │
     │  measure box heights│           │ yourname-cv-ats.pdf │
     │  → build/boxheights │           └─────────────────────┘
     │         │           │           
     │         ▼           │           
     │  layout.py --layout │
     │  compute page breaks│
     │  split overflows    │
     │         │           │
     │         ▼           │
     │  LuaLaTeX (pass 2)  │
     │    final compile    │
     │         │           │
     │         ▼           │
     │   yourname-cv.pdf   │
     └─────────────────────┘
```

The generator reads plain YAML, escapes special characters for LaTeX, and writes two outputs:

1. **Designed CV**: individual `generated/*.tex` files using custom environments (`treelist`, `timeline`, `skilllist`). The layout engine (`scripts/layout.py`) measures each section's height, computes page breaks, and generates `generated/canvas.tex` which places them in boxes on a character-cell grid with automatic page breaks.

2. **ATS CV**: a single `main_ats.tex` file with plain `\section` / `\itemize` formatting, optimised for applicant tracking system parsers. Acronyms are expanded on first use.

Both outputs are compiled inside Docker containers. No local dependencies beyond Docker.

---

## Requirements

| Requirement | Notes |
|-------------|-------|
| **Docker** | Required |
| **Docker Compose** | Required |
| Python | ❌ Not needed locally |
| LaTeX | ❌ Not needed locally |
| Fonts | ❌ Not needed locally |

✅ Works on Linux, macOS, and Windows (WSL2)

---

## Further Documentation

| File | Contents |
|------|----------|
| 📖 `doc/iosevka_sizing.md` | Grid derivation, margin sweet spots, font metrics, column layout math |
| 📖 `doc/ats_requirements.md` | ATS formatting rules and constraints |
| 📖 `doc/ats_check.md` | ATS compliance checklist |

---

## License

Iosevka fonts: [SIL Open Font License](https://github.com/be5invis/Iosevka/blob/main/LICENSE.md). Everything else: do whatever you want with it. Keep rollin'.