#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────
#  build.sh — compile the CV inside Docker and open the PDF
#
#  Usage:
#    ./build.sh          Compile and preview
#    ./build.sh -b       Force-rebuild the Docker image first
#    ./build.sh -c       Remove auxiliary / output files
# ──────────────────────────────────────────────────────────────────
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# ── Flags ────────────────────────────────────────────────────────
REBUILD=false
CLEAN=false

usage() {
  echo "Usage: $0 [-b] [-c]"
  echo "  -b  Force-rebuild the Docker image"
  echo "  -c  Remove auxiliary / output files"
  exit 1
}

while getopts "bch" opt; do
  case $opt in
    b) REBUILD=true ;;
    c) CLEAN=true ;;
    *) usage ;;
  esac
done

# ── Clean mode ───────────────────────────────────────────────────
if $CLEAN; then
  echo "Cleaning build artifacts..."
  rm -f main.{aux,log,out,fls,fdb_latexmk,synctex.gz,pdf}
  echo "Done."
  exit 0
fi

# ── Fonts symlink (preamble.tex expects Path=fonts/) ─────────────
if [ ! -e fonts ]; then
  ln -s font/iosevka/typefaces fonts
  echo "Created symlink: fonts -> font/iosevka/typefaces"
fi

# ── Build image if requested ─────────────────────────────────────
if $REBUILD; then
  docker compose build --no-cache
fi

# ── Compile ──────────────────────────────────────────────────────
export DOCKER_UID="$(id -u)"
export DOCKER_GID="$(id -g)"

echo "Compiling CV with LuaLaTeX..."
docker compose run --rm latex

# ── Preview ──────────────────────────────────────────────────────
PDF="main.pdf"
if [ -f "$PDF" ]; then
  echo "Output: $(pwd)/$PDF"
  # Linux
  if command -v xdg-open &>/dev/null; then
    xdg-open "$PDF" 2>/dev/null &
  # macOS
  elif command -v open &>/dev/null; then
    open "$PDF"
  else
    echo "Open $PDF manually to preview."
  fi
else
  echo "ERROR: Compilation failed — no PDF produced."
  exit 1
fi
