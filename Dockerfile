# ──────────────────────────────────────────────────────────────────
#  Designed CV builder (LuaLaTeX)
#  Image : texlive/texlive (official, rebuilt weekly by Island of TeX)
#  Docs  : https://hub.docker.com/r/texlive/texlive
# ──────────────────────────────────────────────────────────────────
FROM texlive/texlive:latest

RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-yaml curl unzip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /data

CMD ["sh", "-c", "sh scripts/fetch-fonts.sh && python3 scripts/generate.py && . generated/.build-meta && latexmk -lualatex -interaction=nonstopmode -jobname=\"${OUTPUT_NAME}-${OUTPUT_TYPE}\" main.tex"]
