# ATS-Friendly LaTeX CV — Structural Specification

## Purpose

This document defines the structural constraints for generating an ATS-optimised LaTeX CV. The goal is maximum parsing accuracy across all major Applicant Tracking Systems (Greenhouse, Lever, Workday, iCIMS, Ashby). This version exists purely for machine readability. A designed PDF version with full visual treatment is available via hyperlink within this document.

---

## MUST Include

### Document Class & Core Setup
- `\documentclass[a4paper,11pt]{article}` — standard article class, nothing exotic (also includes a legal size)
- `geometry` package — (12mm) margins on all sides, no more, no less
- `fontenc` with `[T1]` — standard text encoding
- `inputenc` with `[utf8]` — if using pdfLaTeX
- `hyperref` — for the clickable link to the designed CV version
- `enumitem` — for clean bullet lists with standard bullet characters
- `titlesec` — optional, only for simple heading size/spacing control

### Font
- One single standard font throughout: `Latin Modern`, `Computer Modern`, or if using LuaLaTeX/XeLaTeX, as `close` to `iosevka` as possible
- Font size: 10pt–12pt body, no smaller anywhere in the document
- Same font for all text — headings, body, dates, everything

### Section Headings — Use Exactly These Names
```
PROFESSIONAL SUMMARY  (or SUMMARY)
WORK EXPERIENCE       (not "What I've Built", not "Career History")
SKILLS                (not "Technical Toolkit", not "Competencies")  
EDUCATION             (not "Academic Background")
PUBLICATIONS          (if applicable)
CERTIFICATIONS        (if applicable)
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
- **Acronyms**: First use = "Full Term (ACRONYM)" — e.g., "Natural Language Processing (NLP)"

### The Designed CV Hyperlink
Include a clearly labelled line near the top of the document, directly below the contact block:

```latex
\noindent\textbf{Full CV:} \url{https://your-link-here.com/cv.pdf}
```

This gives the recruiter/hiring manager direct access to the designed version with full visual treatment. The link should point to a stable URL — a personal site, GitHub Pages hosted PDF, or cloud storage with a permanent link.

Optionally, include a brief note:

```latex
\small\textit{This document is optimised for applicant tracking systems. 
A formatted version is available at the link above.}
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

% Simple heading format — bold, slightly larger, minimal spacing
\titleformat{\section}{\large\bfseries}{}{0em}{}[\titlerule]
\titlespacing{\section}{0pt}{12pt}{6pt}

% No page numbers (they go in footers, which parsers often skip)
\pagestyle{empty}

\begin{document}

% === CONTACT BLOCK ===
\begin{center}
{\LARGE\bfseries Your Name}\\[4pt]
email@example.com \quad +44 XXX XXX XXXX \quad London, UK\\[2pt]
\url{https://linkedin.com/in/yourprofile} \quad 
\url{https://github.com/yourhandle}
\end{center}

\smallskip
\noindent\textbf{Full CV:} \url{https://your-domain.com/cv.pdf}\\
{\small\textit{This document is formatted for applicant tracking systems. 
A designed version with full detail is available at the link above.}}

\bigskip

% === SECTIONS ===
\section{PROFESSIONAL SUMMARY}
Two to three sentences. Plain text. No bullet points here.

\section{WORK EXPERIENCE}

\textbf{Job Title} \hfill Mon Year -- Present\\
Company Name \hfill City, Country
\begin{itemize}[leftmargin=1.5em, itemsep=2pt, parsep=0pt]
  \item Achievement with quantified outcome using Named Tool
  \item Another achievement with measurable result
\end{itemize}

\section{SKILLS}

\textbf{Languages:} Python, SQL, R\\
\textbf{Frameworks:} PyTorch, TensorFlow, Hugging Face Transformers\\
\textbf{Infrastructure:} Docker, Kubernetes, GCP, AWS\\
\textbf{Domains:} Natural Language Processing (NLP), Computer Vision (CV)

\section{EDUCATION}

\textbf{Degree Title} \hfill Year -- Year\\
Institution Name \hfill City, Country

\end{document}
```

---

## Testing

Before submitting, verify parsing accuracy:

1. **Copy-paste test** — open the PDF, Ctrl+A, Ctrl+C, paste into a plain text editor. If the text reads correctly in order, top to bottom, the ATS will read it correctly.
2. **Online parsers** — upload to a free ATS parser (OpenResume parser, Jobscan, Resume Genius) and check that all sections, dates, skills, and job titles are correctly extracted.
3. **`pdftotext` test** — run `pdftotext your-cv.pdf -` in a terminal. The output should be clean, readable, and in the correct order.

If any test produces garbled, reordered, or missing text, something in the structure needs simplifying.

---

## Summary

The ATS version is a **data entry document**. Its job is to make your content findable in a recruiter's keyword search. Every structural decision should serve that single goal. The designed version — linked from within this document — is where your visual identity, layout craft, and design thinking live.

Two documents. Two purposes. One set of content.