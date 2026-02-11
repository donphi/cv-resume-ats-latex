#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────
#  build.sh — compile the CV / Resume inside Docker and open the PDF(s)
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
  rm -f *.aux *.log *.out *.fls *.fdb_latexmk *.synctex.gz *.pdf
  rm -f main_ats.tex boxheights.dat
  rm -f generated/.build-meta generated/settings.tex generated/canvas.tex
  rm -f generated/*-p[0-9]*.tex 2>/dev/null || true
  echo "Done."
  exit 0
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
  echo "Building designed CV (generate + LuaLaTeX)..."
  docker compose run --rm latex
  # Read dynamic output name from build metadata
  if [ -f "generated/.build-meta" ]; then
    source generated/.build-meta
    PDF_DESIGNED="${OUTPUT_NAME}-${OUTPUT_TYPE}.pdf"
  else
    PDF_DESIGNED="cv.pdf"
  fi
  if [ -f "$PDF_DESIGNED" ]; then
    echo "Output: $(pwd)/$PDF_DESIGNED"
  else
    echo "ERROR: Designed CV compilation failed — no PDF produced."
    exit 1
  fi
fi

# ── Compile ATS CV ───────────────────────────────────────────────
if $BUILD_ATS; then
  echo "Building ATS CV (generate + pdfLaTeX)..."
  docker compose -f docker-compose.ats.yml run --rm latex-ats
  if [ -f "generated/.build-meta" ]; then
    source generated/.build-meta
    PDF_ATS="${OUTPUT_NAME}-${OUTPUT_TYPE}-ats.pdf"
  else
    PDF_ATS="cv-ats.pdf"
  fi
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

if $BUILD_DESIGNED && [ -n "${PDF_DESIGNED:-}" ] && [ -f "${PDF_DESIGNED:-}" ]; then
  open_pdf "$PDF_DESIGNED"
fi
if $BUILD_ATS && [ -n "${PDF_ATS:-}" ] && [ -f "${PDF_ATS:-}" ]; then
  open_pdf "$PDF_ATS"
fi
