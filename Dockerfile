# ──────────────────────────────────────────────────────────────────
#  LuaLaTeX builder
#  Image : texlive/texlive (official, rebuilt weekly by Island of TeX)
#  Docs  : https://hub.docker.com/r/texlive/texlive
# ──────────────────────────────────────────────────────────────────
FROM texlive/texlive:latest

WORKDIR /data

CMD ["latexmk", "-lualatex", "-interaction=nonstopmode", "main.tex"]
