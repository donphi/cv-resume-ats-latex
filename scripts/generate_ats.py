#!/usr/bin/env python3
"""
generate_ats.py — Build an ATS-optimised LaTeX CV from semantic text files.

Reads:
    components/contact.tex          — shared contact details
    components/acronym.tex          — acronym expansion library
    components/text/summary.tex     — professional summary
    components/text/research_experience.tex
    components/text/work_experience.tex
    components/text/skills.tex
    components/text/education.tex
    components/text/publications.tex
    components/text/certifications.tex

Writes:
    ats_main.tex  — single self-contained file, pdfLaTeX-safe

No external dependencies — stdlib only.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths (relative to project root)
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
CONTACT_FILE = ROOT / "components" / "contact.tex"
ACRONYM_FILE = ROOT / "components" / "acronym.tex"
TEXT_DIR = ROOT / "components" / "text"
OUTPUT_FILE = ROOT / "ats_main.tex"

# ---------------------------------------------------------------------------
# Regex helpers
# ---------------------------------------------------------------------------

# Match a brace-delimited argument allowing one level of nesting:
#   {stuff {nested} more}
_ARG = r"\{((?:[^{}]|\{[^{}]*\})*)\}"
_ARG_NC = r"\{(?:[^{}]|\{[^{}]*\})*\}"  # non-capturing version


def _extract_args(text: str, command: str, n_args: int) -> list[tuple[str, ...]]:
    """Return list of tuples, one per occurrence of \\command{a1}{a2}...{aN}."""
    pattern = re.escape(command) + r"\s*" + r"\s*".join([_ARG] * n_args)
    return re.findall(pattern, text, re.DOTALL)


def _strip_comments(text: str) -> str:
    """Remove LaTeX comment lines (lines starting with %)."""
    return "\n".join(
        line for line in text.splitlines()
        if not line.lstrip().startswith("%")
    )


def _has_content(path: Path) -> bool:
    """Return True if file exists and has non-comment, non-whitespace content."""
    if not path.exists():
        return False
    content = _strip_comments(path.read_text(encoding="utf-8"))
    return bool(content.strip())


# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------

def parse_contact(path: Path) -> dict[str, str]:
    """Parse components/contact.tex → dict of field→value."""
    text = path.read_text(encoding="utf-8")
    fields = {}
    for field in (
        "ContactName", "ContactTitle", "ContactEmail", "ContactPhone",
        "ContactLinkedIn", "ContactGitHub", "ContactLocation", "ContactFullCV",
    ):
        match = re.search(re.escape("\\" + field) + r"\s*" + _ARG, text)
        if match:
            fields[field] = match.group(1).strip()
    return fields


def parse_acronyms(path: Path) -> dict[str, str]:
    """Parse components/acronym.tex → dict of short→full."""
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    return dict(_extract_args(text, r"\Acronym", 2))


def expand_acronyms(text: str, acronyms: dict[str, str], seen: set[str]) -> str:
    """Expand first use of each acronym in *text*, mutating *seen* in place.

    All matches are found in the **original** text first, then applied in a
    single pass.  This prevents cascading expansions (e.g. FAISS expanding
    to "Facebook AI Similarity Search (FAISS)" and then AI being re-expanded
    inside that string).

    Longer acronyms are matched first to avoid partial-match collisions
    (e.g. "CI/CD" before "CI").  Overlapping matches are discarded.
    """
    # Phase 1: find all first occurrences in the ORIGINAL text
    expansions: list[tuple[int, int, str]] = []  # (start, end, replacement)
    for short in sorted(acronyms, key=len, reverse=True):
        if short in seen:
            continue
        full = acronyms[short]
        escaped = re.escape(short)
        pattern = r"(?<![A-Za-z/])" + escaped + r"(?![A-Za-z/])"
        match = re.search(pattern, text)
        if match:
            # Check this position doesn't overlap with an already-claimed span
            overlaps = any(
                not (match.end() <= s or match.start() >= e)
                for s, e, _ in expansions
            )
            if not overlaps:
                replacement = f"{full} ({short})"
                expansions.append((match.start(), match.end(), replacement))
                seen.add(short)

    # Phase 2: apply all replacements right-to-left (preserves positions)
    expansions.sort(key=lambda x: x[0], reverse=True)
    for start, end, replacement in expansions:
        text = text[:start] + replacement + text[end:]
    return text


# ---------------------------------------------------------------------------
# Section renderers
# ---------------------------------------------------------------------------

def render_summary(path: Path, acronyms: dict[str, str]) -> str:
    """Render PROFESSIONAL SUMMARY section."""
    if not _has_content(path):
        return ""
    text = _strip_comments(path.read_text(encoding="utf-8")).strip()
    seen: set[str] = set()
    text = expand_acronyms(text, acronyms, seen)
    return (
        "\\section{PROFESSIONAL SUMMARY}\n"
        f"{text}\n"
    )


def _parse_experience_entries(text: str) -> list[dict]:
    """Parse an experience text file into structured entries.

    Returns a list of dicts, each with keys:
        title, org, dates, location,
        description (str | None),
        subsections: list of (heading | None, [bullet_texts])
    """
    text = _strip_comments(text)
    entries: list[dict] = []
    # Split on \Entry — keep the command so we can re-parse
    parts = re.split(r"(?=\\Entry\s*\{)", text)
    for part in parts:
        part = part.strip()
        if not part.startswith("\\Entry"):
            continue
        # Extract the 4 Entry args
        entry_match = re.match(
            r"\\Entry\s*" + r"\s*".join([_ARG] * 4),
            part,
            re.DOTALL,
        )
        if not entry_match:
            continue
        title, org, dates, location = (g.strip() for g in entry_match.groups())
        rest = part[entry_match.end():]

        # Optional description
        desc_match = re.search(r"\\Description\s*" + _ARG, rest, re.DOTALL)
        description = desc_match.group(1).strip() if desc_match else None

        # Collect subsections and their bullets
        # Split rest into chunks at \SubSection boundaries
        subsections: list[tuple[str | None, list[str]]] = []
        # Find all subsection positions
        subsec_iter = list(re.finditer(r"\\SubSection\s*" + _ARG, rest, re.DOTALL))
        if subsec_iter:
            # Content before first \SubSection (may have bullets without heading)
            pre = rest[:subsec_iter[0].start()]
            pre_bullets = _extract_bullets(pre)
            if pre_bullets:
                subsections.append((None, pre_bullets))
            # Each \SubSection
            for i, m in enumerate(subsec_iter):
                heading = m.group(1).strip()
                start = m.end()
                end = subsec_iter[i + 1].start() if i + 1 < len(subsec_iter) else len(rest)
                chunk = rest[start:end]
                bullets = _extract_bullets(chunk)
                subsections.append((heading, bullets))
        else:
            # No subsections — just bullets
            bullets = _extract_bullets(rest)
            if bullets:
                subsections.append((None, bullets))

        entries.append({
            "title": title,
            "org": org,
            "dates": dates,
            "location": location,
            "description": description,
            "subsections": subsections,
        })
    return entries


def _extract_bullets(text: str) -> list[str]:
    """Extract all \\Bullet{} and \\BulletLast{} texts from a chunk."""
    return [m.group(1).strip() for m in re.finditer(
        r"\\(?:Bullet|BulletLast)\s*" + _ARG, text, re.DOTALL
    )]


def render_experience(
    path: Path,
    section_name: str,
    acronyms: dict[str, str],
    flatten_subsections: bool = False,
) -> str:
    """Render a WORK EXPERIENCE or RESEARCH EXPERIENCE section."""
    if not _has_content(path):
        return ""
    text = path.read_text(encoding="utf-8")
    entries = _parse_experience_entries(text)
    if not entries:
        return ""

    seen: set[str] = set()
    lines = [f"\\section{{{section_name}}}\n"]

    for i, entry in enumerate(entries):
        title = expand_acronyms(entry["title"], acronyms, seen)
        org = expand_acronyms(entry["org"], acronyms, seen)
        dates = entry["dates"]
        location = entry["location"]

        lines.append(f"\\textbf{{{title}}} \\hfill {dates}\\\\")
        lines.append(f"{org} \\hfill {location}")

        # Optional description (research entries)
        if entry["description"]:
            desc = expand_acronyms(entry["description"], acronyms, seen)
            lines.append(f"\n{desc}\n")

        # Collect all bullets (flatten subsections for ATS)
        all_bullets: list[str] = []
        for heading, bullets in entry["subsections"]:
            if heading and flatten_subsections and bullets:
                # Prepend subsection heading as bold label on first bullet
                first = f"\\textbf{{{expand_acronyms(heading, acronyms, seen)}:}} {expand_acronyms(bullets[0], acronyms, seen)}"
                all_bullets.append(first)
                for b in bullets[1:]:
                    all_bullets.append(expand_acronyms(b, acronyms, seen))
            else:
                for b in bullets:
                    all_bullets.append(expand_acronyms(b, acronyms, seen))

        if all_bullets:
            lines.append("\\begin{itemize}[leftmargin=1.5em, itemsep=2pt, parsep=0pt]")
            for b in all_bullets:
                lines.append(f"  \\item {b}")
            lines.append("\\end{itemize}")

        # Add spacing between entries (except after the last)
        if i < len(entries) - 1:
            lines.append("")

    return "\n".join(lines) + "\n"


def render_skills(path: Path, acronyms: dict[str, str]) -> str:
    """Render SKILLS section."""
    if not _has_content(path):
        return ""
    text = _strip_comments(path.read_text(encoding="utf-8"))
    groups = _extract_args(text, r"\SkillGroup", 2)
    if not groups:
        return ""

    seen: set[str] = set()
    lines = ["\\section{SKILLS}\n"]
    rendered: list[str] = []
    for category, items in groups:
        cat = expand_acronyms(category.strip(), acronyms, seen)
        itm = expand_acronyms(items.strip(), acronyms, seen)
        rendered.append(f"\\textbf{{{cat}:}} {itm}")
    lines.append("\\\\\\relax\n".join(rendered))
    return "\n".join(lines) + "\n"


def render_education(path: Path, acronyms: dict[str, str]) -> str:
    """Render EDUCATION section."""
    if not _has_content(path):
        return ""
    text = _strip_comments(path.read_text(encoding="utf-8"))
    entries = _extract_args(text, r"\EduEntry", 5)
    if not entries:
        return ""

    seen: set[str] = set()
    lines = ["\\section{EDUCATION}\n"]
    for i, (degree, institution, dates, location, details) in enumerate(entries):
        degree = expand_acronyms(degree.strip(), acronyms, seen)
        institution = expand_acronyms(institution.strip(), acronyms, seen)
        dates = dates.strip()
        location = location.strip()
        details = details.strip()

        line1 = f"\\textbf{{{degree}}} \\hfill {dates}"
        if location:
            line2 = f"{institution} \\hfill {location}"
        else:
            line2 = institution
        lines.append(f"{line1}\\\\")
        lines.append(line2)
        if details:
            lines.append(f"\\\\\n\\textit{{{details}}}")

        if i < len(entries) - 1:
            lines.append("\n\\medskip\n")

    return "\n".join(lines) + "\n"


def render_publications(path: Path, acronyms: dict[str, str]) -> str:
    """Render PUBLICATIONS section (omitted if empty)."""
    if not _has_content(path):
        return ""
    text = _strip_comments(path.read_text(encoding="utf-8"))
    pubs = _extract_args(text, r"\Publication", 4)
    if not pubs:
        return ""

    seen: set[str] = set()
    lines = ["\\section{PUBLICATIONS}\n"]
    for authors, title, venue, year in pubs:
        entry = f"{authors.strip()}. \\textit{{{title.strip()}}}. {venue.strip()}, {year.strip()}."
        entry = expand_acronyms(entry, acronyms, seen)
        lines.append(entry)
        lines.append("")
    return "\n".join(lines) + "\n"


def render_certifications(path: Path, acronyms: dict[str, str]) -> str:
    """Render CERTIFICATIONS section (omitted if empty)."""
    if not _has_content(path):
        return ""
    text = _strip_comments(path.read_text(encoding="utf-8"))
    certs = _extract_args(text, r"\Certification", 3)
    if not certs:
        return ""

    seen: set[str] = set()
    lines = ["\\section{CERTIFICATIONS}\n"]
    for name, issuer, year in certs:
        entry = f"\\textbf{{{name.strip()}}} --- {issuer.strip()} \\hfill {year.strip()}"
        entry = expand_acronyms(entry, acronyms, seen)
        lines.append(entry)
        lines.append("")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Preamble & document assembly
# ---------------------------------------------------------------------------

PREAMBLE = r"""\documentclass[a4paper,11pt]{article}

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

% Section heading format — zero decoration
\titleformat{\section}{\large\bfseries}{}{0em}{}
\titlespacing{\section}{0pt}{12pt}{6pt}

% No page numbers (they go in footers, which parsers often skip)
\pagestyle{empty}

\begin{document}
"""

POSTAMBLE = r"""
\end{document}
"""


def build_contact_block(contact: dict[str, str]) -> str:
    """Build the centred contact block + Full CV hyperlink."""
    name = contact.get("ContactName", "Your Name")
    email = contact.get("ContactEmail", "")
    phone = contact.get("ContactPhone", "")
    location = contact.get("ContactLocation", "")
    linkedin = contact.get("ContactLinkedIn", "")
    github = contact.get("ContactGitHub", "")
    full_cv = contact.get("ContactFullCV", "")

    lines = [
        "% === CONTACT BLOCK ===",
        "\\begin{center}",
        f"{{\\LARGE\\bfseries {name}}}\\\\[4pt]",
        f"{email} \\quad {phone} \\quad {location}\\\\[2pt]",
    ]
    urls: list[str] = []
    if linkedin:
        urls.append(f"\\url{{https://{linkedin}}}")
    if github:
        urls.append(f"\\url{{https://{github}}}")
    if urls:
        lines.append(" \\quad ".join(urls))
    lines.append("\\end{center}")
    lines.append("")

    if full_cv:
        lines.append("\\smallskip")
        lines.append(f"\\noindent\\textbf{{Full CV:}} \\url{{{full_cv}}}\\\\")
        lines.append(
            "{\\small\\textit{This document is formatted for applicant tracking "
            "systems. A designed version with full detail is available at the "
            "link above.}}"
        )
        lines.append("")
    lines.append("\\bigskip")
    return "\n".join(lines)


def main() -> None:
    """Entry point: parse all sources and write ats_main.tex."""
    # Parse shared data
    if not CONTACT_FILE.exists():
        print(f"ERROR: {CONTACT_FILE} not found", file=sys.stderr)
        sys.exit(1)
    contact = parse_contact(CONTACT_FILE)
    acronyms = parse_acronyms(ACRONYM_FILE)

    # Build sections
    sections: list[str] = []

    sections.append(render_summary(
        TEXT_DIR / "summary.tex", acronyms))

    sections.append(render_experience(
        TEXT_DIR / "research_experience.tex",
        "RESEARCH EXPERIENCE",
        acronyms,
        flatten_subsections=True,
    ))

    sections.append(render_experience(
        TEXT_DIR / "work_experience.tex",
        "WORK EXPERIENCE",
        acronyms,
        flatten_subsections=False,
    ))

    sections.append(render_skills(
        TEXT_DIR / "skills.tex", acronyms))

    sections.append(render_education(
        TEXT_DIR / "education.tex", acronyms))

    sections.append(render_publications(
        TEXT_DIR / "publications.tex", acronyms))

    sections.append(render_certifications(
        TEXT_DIR / "certifications.tex", acronyms))

    # Filter out empty sections
    sections = [s for s in sections if s.strip()]

    # Assemble document
    doc = PREAMBLE
    doc += build_contact_block(contact)
    doc += "\n"
    doc += "\n".join(sections)
    doc += POSTAMBLE

    OUTPUT_FILE.write_text(doc, encoding="utf-8")
    print(f"Generated {OUTPUT_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
