# ──────────────────────────────────────────────────────────────────
#  Designed CV builder (LuaLaTeX) — two-pass build with auto layout
#  Image : texlive/texlive (official, rebuilt weekly by Island of TeX)
#  Docs  : https://hub.docker.com/r/texlive/texlive
#
#  Pipeline:
#    1. fetch-fonts.sh          — download Iosevka fonts if missing
#    2. generate.py             — YAML → generated/*.tex (content)
#    3. layout.py --measure     — passthrough canvas (no splits)
#    4. latexmk main.tex        — pass 1: measure box heights
#    5. layout.py --layout      — compute page breaks, split canvas
#    6. latexmk main.tex        — pass 2: final PDF → root
#
#  All intermediate files (.aux, .log, .fls, etc.) go into build/.
#  Only the final PDF is copied to the project root.
# ──────────────────────────────────────────────────────────────────
FROM texlive/texlive:latest

RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-yaml curl unzip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /data

CMD ["sh", "-c", "\
    sh scripts/fetch-fonts.sh \
    && python3 scripts/generate.py \
    && mkdir -p build \
    && (rm -f generated/*-p[0-9]*.tex 2>/dev/null; rm -f build/boxheights.dat; true) \
    && python3 scripts/layout.py --measure \
    && . generated/.build-meta \
    && latexmk -lualatex -auxdir=build -outdir=build -interaction=nonstopmode -jobname=\"${OUTPUT_NAME}-${OUTPUT_TYPE}\" main.tex \
    && python3 scripts/layout.py --layout \
    && rm -f build/\"${OUTPUT_NAME}-${OUTPUT_TYPE}.aux\" build/\"${OUTPUT_NAME}-${OUTPUT_TYPE}.fls\" build/\"${OUTPUT_NAME}-${OUTPUT_TYPE}.fdb_latexmk\" \
    && latexmk -lualatex -auxdir=build -outdir=build -interaction=nonstopmode -jobname=\"${OUTPUT_NAME}-${OUTPUT_TYPE}\" main.tex \
    && cp build/\"${OUTPUT_NAME}-${OUTPUT_TYPE}.pdf\" . \
"]
