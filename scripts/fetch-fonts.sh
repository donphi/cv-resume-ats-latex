#!/bin/sh
# ──────────────────────────────────────────────────────────────────
#  fetch-fonts.sh — download Iosevka TTF fonts from GitHub releases
#
#  Called automatically inside the Docker container before compilation.
#  Skips download if fonts already exist (e.g. from a previous build
#  or a local copy).
#
#  Requires: curl, unzip  (installed in the Dockerfile)
# ──────────────────────────────────────────────────────────────────
set -eu

IOSEVKA_VERSION="34.1.0"
FONT_DIR="fonts/iosevka"
BASE_URL="https://github.com/be5invis/Iosevka/releases/download/v${IOSEVKA_VERSION}"

# ── Files we need from each zip ──────────────────────────────────
# PkgTTF-Iosevka  (base monospace family)
IOSEVKA_FILES="Iosevka-Extended.ttf Iosevka-ExtendedBold.ttf Iosevka-ExtendedItalic.ttf Iosevka-ExtendedBoldItalic.ttf Iosevka-BoldItalic.ttf"
# PkgTTF-IosevkaAile  (proportional sans-serif)
AILE_FILES="IosevkaAile-Regular.ttf IosevkaAile-Bold.ttf IosevkaAile-Italic.ttf IosevkaAile-BoldItalic.ttf IosevkaAile-SemiBold.ttf"
# PkgTTF-IosevkaEtoile  (proportional serif)
ETOILE_FILES="IosevkaEtoile-Regular.ttf IosevkaEtoile-Bold.ttf IosevkaEtoile-Italic.ttf IosevkaEtoile-BoldItalic.ttf IosevkaEtoile-SemiBold.ttf"

# ── Check if fonts already exist ─────────────────────────────────
all_present=true
for f in $IOSEVKA_FILES $AILE_FILES $ETOILE_FILES; do
    if [ ! -f "${FONT_DIR}/${f}" ]; then
        all_present=false
        break
    fi
done

if [ "$all_present" = true ]; then
    echo "Fonts already present in ${FONT_DIR}/ — skipping download."
    exit 0
fi

echo "Downloading Iosevka v${IOSEVKA_VERSION} fonts..."
mkdir -p "$FONT_DIR"
TMPDIR=$(mktemp -d)

# ── Download and extract each family ─────────────────────────────
fetch_family() {
    zip_name="$1"
    shift
    files="$*"

    url="${BASE_URL}/${zip_name}"
    zip_path="${TMPDIR}/${zip_name}"

    echo "  Fetching ${zip_name}..."
    curl -fsSL -o "$zip_path" "$url"

    # Extract only the files we need (-j = junk paths, flatten)
    for f in $files; do
        unzip -joq "$zip_path" "*/${f}" -d "$FONT_DIR" 2>/dev/null || \
        unzip -joq "$zip_path" "${f}" -d "$FONT_DIR" 2>/dev/null || \
        echo "    WARNING: ${f} not found in ${zip_name}"
    done

    rm -f "$zip_path"
}

fetch_family "PkgTTF-Iosevka-${IOSEVKA_VERSION}.zip"       $IOSEVKA_FILES
fetch_family "PkgTTF-IosevkaAile-${IOSEVKA_VERSION}.zip"   $AILE_FILES
fetch_family "PkgTTF-IosevkaEtoile-${IOSEVKA_VERSION}.zip" $ETOILE_FILES

rm -rf "$TMPDIR"

# ── Verify ───────────────────────────────────────────────────────
missing=0
for f in $IOSEVKA_FILES $AILE_FILES $ETOILE_FILES; do
    if [ ! -f "${FONT_DIR}/${f}" ]; then
        echo "ERROR: missing ${FONT_DIR}/${f}"
        missing=$((missing + 1))
    fi
done

if [ "$missing" -gt 0 ]; then
    echo "FATAL: ${missing} font file(s) missing after download."
    exit 1
fi

echo "All 15 font files downloaded to ${FONT_DIR}/."
