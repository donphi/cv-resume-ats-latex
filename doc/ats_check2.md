# ATS-Friendly LaTeX CV — Structural Specification

## Purpose

This document defines the structural constraints for generating an ATS-optimised LaTeX CV. The goal is maximum parsing accuracy across all major Applicant Tracking Systems (Greenhouse, Lever, Workday, iCIMS, Ashby). This version exists purely for machine readability. A designed PDF version with full visual treatment is available via hyperlink within this document.

---

## Source Content

All CV content already exists in the designed CV's component files. The ATS version does **not** require writing new content — it requires **converting the format** of each component from its current styled LaTeX into the plain, ATS-safe structure defined in this spec.

### Component File Location

All source files are in `components/*.tex`. Each file contains one CV section with its own formatting (custom commands, decorative packages, multi-column layouts, etc.). The ATS conversion must:

1. **Read** each `components/*.tex` file
2. **Extract** the raw content (text, dates, job titles, bullet points, skills, etc.)
3. **Reformat** that content into the ATS-safe structure defined below — stripping all custom commands, decorative packages, and non-standard layouts
4. **Assemble** the reformatted sections into a single `main-ats.tex` file (or equivalent) using only the packages and structure permitted by this spec

### Mapping: Component Files → ATS Sections

| Component File | ATS Section Heading | Conversion Notes |
|---|---|---|
| `components/summary.tex` | `PROFESSIONAL SUMMARY` | Strip any custom formatting. Output as plain paragraph text, no bullets. |
| `components/research_experience.tex` | `RESEARCH EXPERIENCE` | Reformat to Title / Institution / Location / Dates + `\itemize` bullets. Strip any custom commands, decorative elements, or multi-column layouts. |
| `components/work_experience.tex` | `WORK EXPERIENCE` | Same format as RESEARCH EXPERIENCE. Preserve reverse chronological order. |
| `components/skills.tex` | `SKILLS` | Convert to `\textbf{Category:}` followed by comma-separated plain text. Remove any progress bars, grids, ratings, or visual skill indicators. Enforce acronym expansion on first use per subheading. |
| `components/education.tex` | `EDUCATION` | Reformat to Degree / Institution / Location / Dates. Strip any decorative elements. |
| `components/publications.tex` | `PUBLICATIONS` | Convert to plain-text citation format. Strip any custom bibliography commands or `biblatex` formatting. |
| `components/certifications.tex` | `CERTIFICATIONS` | Convert to `\textbf{Name}` — Issuer, Year. Strip any decorative elements. |

If a component file does not exist (e.g., `publications.tex` has not been created yet), omit that section from the ATS output entirely. Do not generate placeholder content.

### Critical Conversion Rule

The bot's job is **format conversion only**. The content in `components/*.tex` is the single source of truth. The ATS version must contain **exactly the same information** — same job titles, same dates, same bullet points, same skills — just reformatted into the ATS-safe structure. No content should be added, removed, reworded, or "improved" during conversion unless explicitly instructed.

---

## MUST Include

### Document Class & Core Setup
- `\documentclass[a4paper,11pt]{article}` — standard article class, nothing exotic (also includes a legal size)
- `geometry` package — `25.4mm` (1 inch) margins on all sides
- `fontenc` with `[T1]` — standard text encoding
- `inputenc` with `[utf8]` — if using pdfLaTeX
- `hyperref` — for the clickable link to the designed CV version
- `enumitem` — for clean bullet lists with standard bullet characters
- `titlesec` — optional, only for simple heading size/spacing control

### Font
- One single standard font throughout with `PDFLaTeX` compiler: `Latin Modern`, `Computer Modern`, or as `close` to `iosevka` as possible
- Font size: 10pt–12pt body, no smaller anywhere in the document
- Same font for all text — headings, body, dates, everything

### Section Headings — Use Exactly These Names
```
PROFESSIONAL SUMMARY (or SUMMARY)
RESEARCH EXPERIENCE  (for dissertation, pipeline, or academic project work — parsed identically to WORK EXPERIENCE because it contains "EXPERIENCE")
WORK EXPERIENCE       (not "What I've Built", not "Career History")
SKILLS                (not "Technical Toolkit", not "Competencies")  
EDUCATION             (not "Academic Background")
PUBLICATIONS          (Luddite Loop Pending)
CERTIFICATIONS        (MSc AI and Digital Health Pending)
```

**Section ordering guidance:**
The recommended order above places RESEARCH EXPERIENCE before WORK EXPERIENCE. This is deliberate: for profiles transitioning from non-technical careers into AI/ML roles, the research section contains the densest concentration of relevant keywords (frameworks, tools, methodologies). Placing it early ensures the ATS parser and recruiter keyword searches hit the strongest content first. If your work experience is already ML-heavy, reverse the order.

**RESEARCH EXPERIENCE formatting rule:**
Entries under RESEARCH EXPERIENCE must be formatted identically to WORK EXPERIENCE entries — Title, Institution, Location, Date Range, followed by bullet points. This ensures the ATS parser treats them as experience entries, not free-text blocks.

Example:
```latex
\section{RESEARCH EXPERIENCE}

\textbf{MSc Researcher — AI and Digital Health} \hfill Sep 2024 -- Jan 2026\\
University of Westminster \hfill London, UK
\begin{itemize}[leftmargin=1.5em, itemsep=2pt, parsep=0pt]
  \item Built 47-script, 10-DAG pipeline processing 6,600+ papers through OCR, NLP, and validation layers
  \item Achieved 90\% automated pass rate across multi-engine document extraction
\end{itemize}
```

- Use `\section{}` — standard LaTeX sectioning
- Headings should render as bold, slightly larger text — nothing more
- No custom heading decorations, no lines, no boxes, no icons

### Content Structure
- **Reverse chronological order** within each section
- **Contact block at the very top**: Name, email, phone, location (city + country), LinkedIn URL, GitHub URL — plain text, no table, no columns
- **Job entries**: Job Title, Company Name, Location, Date Range — each on its own line or clearly separated
- **Bullet points**: Use `\begin{itemize}` with standard `\item` — produces standard bullet characters that ATS recognises
- **Skills**: Comma-separated plain text grouped under subheadings, or simple bullet lists — no progress bars, no ratings, no grids
- **Dates**: Consistent format throughout — "Month Year – Month Year" (e.g., "Jan 2024 – Present"). Include month always.
- **Acronym rule:** First use in **every section** = "Full Term (ACRONYM)" — e.g., "Natural Language Processing (NLP)". This applies to body text **and** to the Skills section subheadings. Do not assume the parser carries context across sections. If NLP appears under SKILLS and again under WORK EXPERIENCE, expand it in both places on first use within that section.

### The Designed CV Hyperlink
Include a clearly labelled line near the top of the document, directly below the contact block, also indicating this as the ATS version:

```latex
\noindent\textbf{Full CV:} \url{https://your-link-here.com/cv.pdf}
```

This gives the recruiter/hiring manager direct access to the designed version with full visual treatment. The link should point to a stable URL — a personal site, GitHub Pages hosted PDF, or cloud storage with a permanent link.

Include a brief note:

```latex
\small\textit{This document is optimised for applicant tracking systems. A formatted version is available at the link above.}
```

---

## MUST NOT Include

### Packages to Avoid
- `textpos` — absolute positioning breaks linear text flow
- `tikz` / `pgf` — drawn graphics are invisible to ATS; decorative text in TikZ nodes gets extracted as garbage
- `tcolorbox` — coloured boxes add non-content elements to the text stream
- `multicol` / `paracol` / `flowfram` — multi-column layouts cause interleaved text extraction
- `fancyhdr` — headers/footers are often missed or misattributed by parsers
- `background` — page-level decorations
- `xcolor` (for decorative use) — coloured text may be ignored or misread; if used, only for hyperlinks
- `fontawesome5` / `fontawesome` — icon fonts extract as garbage characters or empty boxes
- `graphicx` (for decorative images) — logos, photos, decorative elements. Exception: only if inserting a QR code as a secondary access method
- `tabularx` / `longtable` (for layout) — tables used for visual layout break parsing. Tables for actual tabular data (e.g., a publications list) are acceptable but should be simple
- `soul` / `ulem` — decorative text effects (strikethrough, underline, letter spacing)
- `setspace` with extreme values — unusual line spacing confuses line-grouping algorithms
- Custom `.sty` files with non-standard commands
- Any package imported by a `components/*.tex` file that is not in the permitted list above — the ATS version uses **only** the packages defined in the Recommended Minimal Preamble section

### Structural Prohibitions
- **No columns** — everything single column, full page width
- **No tables for layout** — never use a table to place content side by side. ATS reads tables cell by cell, often in the wrong order
- **No headers or footers** — many parsers skip them entirely. Your name and page number in a footer may never be read
- **No images** — no photos, no logos, no decorative graphics of any kind
- **No decorative Unicode characters** — no box-drawing characters (─ │ ┌ ╗ etc.), no decorative bullets (▸ ▪ ⬥), no dot patterns (·····). Use only standard bullet from `\item`
- **No coloured text** — all text black on white. Exception: hyperlink blue from `hyperref` is fine
- **No text hidden behind shapes** — no `\colorbox` overlays, no layered elements
- **No nested environments for visual effect** — keep nesting shallow. A section contains items, items contain text. Nothing deeper
- **No custom font sizes scattered throughout** — one body size, one heading size, done
- **No blank lines used as spacing** — use `\vspace{}` sparingly. Blank vertical space in the PDF can cause parsers to split content into separate sections incorrectly
- **No justified text** — use `\raggedright`. Justified text inserts variable word spacing that some parsers misread as multiple spaces or missing characters
- **No `\titlerule` or decorative lines under headings** — horizontal rules rendered via `\titlerule`, `\rule`, or `\hrule` under section headings are decorative elements. While they render as PDF graphic objects (not text) and are unlikely to cause parsing failures, they contradict the principle of zero decoration in the ATS version. The designed CV handles visual hierarchy. This version does not.
- **No `\input{}` or `\include{}`** — the ATS version must be a single self-contained `.tex` file. Do not import the `components/*.tex` files directly. Their content is extracted and reformatted into this file during conversion.

---

## Recommended Minimal Preamble

```latex
\documentclass[a4paper,11pt]{article}

\usepackage[T1]{fontenc}
\usepackage[margin=25.4mm]{geometry}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage[hidelinks]{hyperref}
\usepackage{parskip}

% No paragraph indent, small gap between paragraphs
\setlength{\parindent}{0pt}

% Raggedright globally — prevents variable word spacing
\raggedright

% Removed \titlerule from heading format — zero decoration
\titleformat{\section}{\large\bfseries}{}{0em}{}
\titlespacing{\section}{0pt}{12pt}{6pt}

% No page numbers (they go in footers, which parsers often skip)
\pagestyle{empty}

\begin{document}

% === CONTACT BLOCK ===
\begin{center}
{\LARGE\bfseries Your Name}\\[4pt]
email@example.com \quad +44 XXX XXX XXXX \quad London, UK\\[2pt]
\url{https://linkedin.com/in/donphi} \quad 
\url{https://github.com/donphi}
\end{center}

\smallskip
\noindent\textbf{Full CV:} \url{https://your-domain.com/cv.pdf}\\
{\small\textit{This document is formatted for applicant tracking systems. A designed version with full detail is available at the link above.}}

\bigskip

% === SECTIONS ===
% Content below is extracted and reformatted from components/*.tex
% Do not modify content — format conversion only

\section{PROFESSIONAL SUMMARY}
% Source: components/summary.tex
Two to three sentences. Plain text. No bullet points here.

\section{RESEARCH EXPERIENCE}
% Source: components/research.tex

\textbf{Research Title or Role} \hfill Mon Year -- Mon Year\\
Institution Name \hfill City, Country
\begin{itemize}[leftmargin=1.5em, itemsep=2pt, parsep=0pt]
  \item Achievement with quantified outcome using Named Tool
  \item Another achievement with measurable result
\end{itemize}

\section{WORK EXPERIENCE}
% Source: components/experience.tex

\textbf{Job Title} \hfill Mon Year -- Present\\
Company Name \hfill City, Country
\begin{itemize}[leftmargin=1.5em, itemsep=2pt, parsep=0pt]
  \item Achievement with quantified outcome using Named Tool
  \item Another achievement with measurable result
\end{itemize}

\section{SKILLS}
% Source: components/skills.tex

\textbf{Languages:} Python, Structured Query Language (SQL), R\\
\textbf{Frameworks:} PyTorch, TensorFlow, Hugging Face Transformers\\
\textbf{Infrastructure:} Docker, Kubernetes, Google Cloud Platform (GCP), Amazon Web Services (AWS)\\
\textbf{Domains:} Natural Language Processing (NLP), Computer Vision (CV), Optical Character Recognition (OCR)

\section{EDUCATION}
% Source: components/education.tex

\textbf{Degree Title} \hfill Year -- Year\\
Institution Name \hfill City, Country

\section{PUBLICATIONS}
% Source: components/publications.tex
% Omit this section entirely if components/publications.tex does not exist

Author(s). \textit{Title}. Venue/Journal, Year.

\section{CERTIFICATIONS}
% Source: components/certifications.tex
% Omit this section entirely if components/certifications.tex does not exist

\textbf{Certification Name} — Issuing Body \hfill Year

\end{document}
```

---

## Testing

Before submitting, verify parsing accuracy:

1. **Copy-paste test** — open the PDF, Ctrl+A, Ctrl+C, paste into a plain text editor. If the text reads correctly in order, top to bottom, the ATS will read it correctly.
2. **Online parsers** — upload to a free ATS parser (OpenResume parser, Jobscan, Resume Genius) and check that all sections, dates, skills, and job titles are correctly extracted.
3. **`pdftotext` test** — run `pdftotext your-cv.pdf -` in a terminal. The output should be clean, readable, and in the correct order.

If any test produces garbled, reordered, or missing text, something in the structure needs simplifying.

**Multi-page test:**
If the CV exceeds one page, run the copy-paste test on each page independently. Confirm that no section is split mid-entry across a page break (e.g., job title on page 1, bullets on page 2). ATS parsers handle page breaks but some lose context across them. Use `\newpage` or `\pagebreak` strategically if needed to keep entries whole.

**Content parity test:**
After conversion, diff the text content of the ATS version against the designed version. The information must be identical — same job titles, same dates, same bullet text, same skills. Only the formatting should differ.

---

## Summary

The ATS version is a **data entry document**. Its job is to make your content findable in a recruiter's keyword search. Every structural decision should serve that single goal. The designed version — linked from within this document — is where your visual identity, layout craft, and design thinking live.

Two documents. Two purposes. One set of content. One source of truth: `components/*.tex`.