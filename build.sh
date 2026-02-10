#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────
#  build.sh — compile the CV inside Docker and open the PDF(s)
#
#  Usage:
#    ./build.sh          Build both designed + ATS PDFs
#    ./build.sh -d       Designed CV only (LuaLaTeX)
#    ./build.sh -a       ATS CV only (generate + pdfLaTeX)
#    ./build.sh -b       Force-rebuild Docker image(s) first
#    ./build.sh -c       Remove auxiliary / output files
# ──────────────────────────────────────────────────────────────────
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# ── Flags ────────────────────────────────────────────────────────
REBUILD=false
CLEAN=false
BUILD_DESIGNED=true
BUILD_ATS=true

usage() {
  echo "Usage: $0 [-b] [-c] [-d] [-a]"
  echo "  -b  Force-rebuild the Docker image(s)"
  echo "  -c  Remove auxiliary / output files"
  echo "  -d  Build designed CV only"
  echo "  -a  Build ATS CV only"
  exit 1
}

while getopts "bcdah" opt; do
  case $opt in
    b) REBUILD=true ;;
    c) CLEAN=true ;;
    d) BUILD_DESIGNED=true; BUILD_ATS=false ;;
    a) BUILD_ATS=true; BUILD_DESIGNED=false ;;
    *) usage ;;
  esac
done

# ── Clean mode ───────────────────────────────────────────────────
if $CLEAN; then
  echo "Cleaning build artifacts..."
  rm -f main.{aux,log,out,fls,fdb_latexmk,synctex.gz,pdf}
  rm -f ats_cv.{aux,log,out,fls,fdb_latexmk,synctex.gz,pdf}
  rm -f ats_main.{aux,log,out,fls,fdb_latexmk,synctex.gz,tex}
  echo "Done."
  exit 0
fi

# ── Fonts symlink (preamble.tex expects Path=fonts/) ─────────────
if [ ! -e fonts ]; then
  ln -s font/iosevka/typefaces fonts
  echo "Created symlink: fonts -> font/iosevka/typefaces"
fi

# ── Set UID/GID for Docker ───────────────────────────────────────
export DOCKER_UID="$(id -u)"
export DOCKER_GID="$(id -g)"

# ── Build images if requested ────────────────────────────────────
if $REBUILD; then
  if $BUILD_DESIGNED; then
    docker compose build --no-cache
  fi
  if $BUILD_ATS; then
    docker compose -f docker-compose.ats.yml build --no-cache
  fi
fi

# ── Compile designed CV ──────────────────────────────────────────
if $BUILD_DESIGNED; then
  echo "Compiling designed CV with LuaLaTeX..."
  docker compose run --rm latex
  PDF_DESIGNED="main.pdf"
  if [ -f "$PDF_DESIGNED" ]; then
    echo "Output: $(pwd)/$PDF_DESIGNED"
  else
    echo "ERROR: Designed CV compilation failed — no PDF produced."
    exit 1
  fi
fi

# ── Generate + compile ATS CV ────────────────────────────────────
if $BUILD_ATS; then
  echo "Generating ATS LaTeX from text files..."
  python3 scripts/generate_ats.py

  echo "Compiling ATS CV with pdfLaTeX..."
  docker compose -f docker-compose.ats.yml run --rm latex-ats
  PDF_ATS="ats_cv.pdf"
  if [ -f "$PDF_ATS" ]; then
    echo "Output: $(pwd)/$PDF_ATS"
  else
    echo "ERROR: ATS CV compilation failed — no PDF produced."
    exit 1
  fi
fi

# ── Preview ──────────────────────────────────────────────────────
open_pdf() {
  if command -v xdg-open &>/dev/null; then
    xdg-open "$1" 2>/dev/null &
  elif command -v open &>/dev/null; then
    open "$1"
  else
    echo "Open $1 manually to preview."
  fi
}

if $BUILD_DESIGNED && [ -f "main.pdf" ]; then
  open_pdf "main.pdf"
fi
if $BUILD_ATS && [ -f "ats_cv.pdf" ]; then
  open_pdf "ats_cv.pdf"
fi
