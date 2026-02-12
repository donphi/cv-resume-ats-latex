#!/usr/bin/env python3
"""
RETRO ASCII 3D FONT LIBRARY
============================
Two complete 3D ASCII font sets (5-row and 4-row) with:
  - Full uppercase alphabet (A-Z)
  - Numbers (0-9)
  - Punctuation & symbols
  - 80s terminal retro extras

Usage:
    from retro_ascii_fonts import render, render4, FONT_5ROW, FONT_4ROW

    render("HELLO WORLD")       # 5-row 3D font
    render4("HELLO WORLD")      # 4-row 3D font
"""

# =============================================================================
# 5-ROW FONT — "mainframe" theme
# Box-drawing + block shadow. Each glyph: 5 rows.
# =============================================================================

FONT_5ROW = {
    'A': [
        "╔═╗ ",
        "║ ║░",
        "╠═╣░",
        "╚ ╚░",
        " ░░░",
    ],
    'B': [
        "╔═╗ ",
        "║ ║░",
        "╠═╣░",
        "╚═╝░",
        " ░░░",
    ],
    'C': [
        "╔═╗ ",
        "║  ░",
        "║  ░",
        "╚═╝░",
        " ░░░",
    ],
    'D': [
        "╔═╗ ",
        "║ ║░",
        "║ ║░",
        "╚═╝░",
        " ░░░",
    ],
    'E': [
        "╔═╗ ",
        "║  ░",
        "╠═ ░",
        "╚═╝░",
        " ░░░",
    ],
    'F': [
        "╔═╗ ",
        "║  ░",
        "╠═ ░",
        "╚ ░░",
        " ░░░",
    ],
    'G': [
        "╔═╗ ",
        "║  ░",
        "║═╣░",
        "╚═╝░",
        " ░░░",
    ],
    'H': [
        "╔ ╔ ",
        "║ ║░",
        "╠═╣░",
        "╚ ╚░",
        " ░░░",
    ],
    'I': [
        "═╦═ ",
        " ║ ░",
        " ║ ░",
        "═╩═░",
        " ░░░",
    ],
    'J': [
        " ═╗ ",
        "  ║░",
        "╗ ║░",
        "╚═╝░",
        " ░░░",
    ],
    'K': [
        "╔ ╔ ",
        "║╔╝░",
        "║╚╗░",
        "╚ ╚░",
        " ░░░",
    ],
    'L': [
        "╔   ",
        "║  ░",
        "║  ░",
        "╚═╝░",
        " ░░░",
    ],
    'M': [
        "╔╗╔╗ ",
        "║╚╝║░",
        "║  ║░",
        "╚  ╚░",
        " ░░░░",
    ],
    'N': [
        "╔╗ ╔ ",
        "║╚╗║░",
        "║ ╚╣░",
        "╚  ╚░",
        " ░░░░",
    ],
    'O': [
        "╔═╗ ",
        "║ ║░",
        "║ ║░",
        "╚═╝░",
        " ░░░",
    ],
    'P': [
        "╔═╗ ",
        "║ ║░",
        "╠═╝░",
        "╚ ░░",
        " ░░░",
    ],
    'Q': [
        "╔═╗ ",
        "║ ║░",
        "║╚╣░",
        "╚═╚░",
        " ░░░",
    ],
    'R': [
        "╔═╗ ",
        "║ ║░",
        "╠═╝░",
        "╚ ╚░",
        " ░░░",
    ],
    'S': [
        "╔═╗ ",
        "║  ░",
        "╚═╗░",
        "╚═╝░",
        " ░░░",
    ],
    'T': [
        "═╦═ ",
        " ║ ░",
        " ║ ░",
        " ╚ ░",
        " ░░░",
    ],
    'U': [
        "╔ ╔ ",
        "║ ║░",
        "║ ║░",
        "╚═╝░",
        " ░░░",
    ],
    'V': [
        "╔ ╔ ",
        "║ ║░",
        "╚╗║░",
        " ╚╝░",
        " ░░░",
    ],
    'W': [
        "╔  ╔ ",
        "║  ║░",
        "║╔╗║░",
        "╚╝╚╝░",
        " ░░░░",
    ],
    'X': [
        "╔ ╔ ",
        "╚╗║░",
        "╔╝║░",
        "╚ ╚░",
        " ░░░",
    ],
    'Y': [
        "╔ ╔ ",
        "╚╗╝░",
        " ║ ░",
        " ╚ ░",
        " ░░░",
    ],
    'Z': [
        "╔═╗ ",
        " ╔╝░",
        "╔╝ ░",
        "╚═╝░",
        " ░░░",
    ],
    '0': [
        "╔═╗ ",
        "║╱║░",
        "║╱║░",
        "╚═╝░",
        " ░░░",
    ],
    '1': [
        "╔╗  ",
        " ║ ░",
        " ║ ░",
        "═╩═░",
        " ░░░",
    ],
    '2': [
        "╔═╗ ",
        "║ ║░",
        "╔═╝░",
        "╚═╝░",
        " ░░░",
    ],
    '3': [
        "╔═╗ ",
        "  ║░",
        " ═╣░",
        "╚═╝░",
        " ░░░",
    ],
    '4': [
        "╔ ╔ ",
        "║ ║░",
        "╚═║░",
        "  ╚░",
        " ░░░",
    ],
    '5': [
        "╔═╗ ",
        "╠═╗░",
        "  ║░",
        "╚═╝░",
        " ░░░",
    ],
    '6': [
        "╔═╗ ",
        "║  ░",
        "║═╗░",
        "╚═╝░",
        " ░░░",
    ],
    '7': [
        "═══╗",
        "  ╔╝",
        " ╔╝░",
        " ╚ ░",
        " ░░░",
    ],
    '8': [
        "╔═╗ ",
        "║ ║░",
        "╠═╣░",
        "╚═╝░",
        " ░░░",
    ],
    '9': [
        "╔═╗ ",
        "║ ║░",
        "╚═║░",
        "╚═╝░",
        " ░░░",
    ],

    # --- SYMBOLS ---
    '&': [
        "╔═╗ ",
        "╠═╝░",
        "║═╗░",
        "╚═╩░",
        " ░░░",
    ],
    '!': [
        " ╔ ",
        " ║░",
        " ░░",
        " ╚░",
        " ░░",
    ],
    '?': [
        "╔═╗ ",
        "╚═║░",
        " ░ ░",
        " ╚ ░",
        " ░░░",
    ],
    '.': [
        "   ",
        "  ░",
        "  ░",
        " ╚░",
        " ░░",
    ],
    ',': [
        "   ",
        "  ░",
        "  ░",
        " ╝░",
        " ░░",
    ],
    ':': [
        "   ",
        " ║░",
        " ░░",
        " ║░",
        " ░░",
    ],
    '-': [
        "   ",
        "  ░",
        "══░",
        " ░░",
        "░░░",
    ],
    '_': [
        "    ",
        "   ░",
        "   ░",
        "═══░",
        " ░░░",
    ],
    '/': [
        "  ╔ ",
        " ╔╝░",
        "╔╝ ░",
        "╚  ░",
        " ░░░",
    ],
    '\\': [
        "╔   ",
        "╚╗ ░",
        " ╚╗░",
        "  ╚░",
        " ░░░",
    ],
    '@': [
        "╔══╗ ",
        "║╔╗║░",
        "║╚═╝░",
        "╚═══░",
        " ░░░░",
    ],
    '#': [
        " ║║  ",
        "═╬╬═░",
        "═╬╬═░",
        " ║║ ░",
        " ░░░░",
    ],
    '$': [
        "╔╬╗ ",
        "╚╬╗░",
        "║║║░",
        "╚╬╝░",
        " ░░░",
    ],
    '%': [
        "╔╱ ░",
        " ╱ ░",
        "╱  ░",
        "╱╚ ░",
        " ░░░",
    ],
    '(': [
        " ╔ ",
        "╔╝░",
        "╚╗░",
        " ╚░",
        " ░░",
    ],
    ')': [
        "╗  ",
        "╚╗░",
        "╔╝░",
        "╝░░",
        "░░░",
    ],
    '[': [
        "╔═ ",
        "║ ░",
        "║ ░",
        "╚═░",
        " ░░",
    ],
    ']': [
        "═╗ ",
        " ║░",
        " ║░",
        "═╝░",
        " ░░",
    ],
    '+': [
        "    ",
        " ║ ░",
        "═╬═░",
        " ║ ░",
        " ░░░",
    ],
    '=': [
        "    ",
        "══ ░",
        "══ ░",
        "   ░",
        " ░░░",
    ],
    '*': [
        "╲║╱ ",
        "═╬═░",
        "╱║╲░",
        "   ░",
        " ░░░",
    ],
    '"': [
        "║║ ",
        "╚╚░",
        "  ░",
        "  ░",
        " ░░",
    ],
    "'": [
        "║ ",
        "╚░",
        " ░",
        " ░",
        " ░",
    ],
    '<': [
        "  ╔ ",
        " ╔╝░",
        " ╚╗░",
        "  ╚░",
        " ░░░",
    ],
    '>': [
        "╔   ",
        "╚╗ ░",
        "╔╝ ░",
        "╚  ░",
        " ░░░",
    ],
    '^': [
        " ╔╗ ",
        "╔╝╚╗",
        "    ░",
        "   ░",
        " ░░░",
    ],
    '~': [
        "     ",
        "╔╗╔ ░",
        "╚╝╚ ░",
        "    ░",
        " ░░░░",
    ],
    '|': [
        " ║ ",
        " ║░",
        " ║░",
        " ║░",
        " ░░",
    ],

    # --- 80s TERMINAL EXTRAS ---

    # >_  cursor/prompt
    'PROMPT': [
        "╔    ",
        "╚╗▓ ░",
        "╔╝▓ ░",
        "╚ ╚ ░",
        " ░░░░",
    ],
    # $   shell prompt
    'SHELL': [
        "╔╦═ ",
        "╚╬╗░",
        "╔╬╝░",
        "╚╩═░",
        " ░░░",
    ],
    # C:\>  DOS prompt
    'DOS': [
        "╔═╗    ╔ ",
        "║  ║╲╚╗░░",
        "║  ║╱╔╝░░",
        "╚═╝ ╚╚ ░░",
        " ░░░░░░░░░",
    ],
    # Blinking cursor block
    'CURSOR': [
        "▓▓ ",
        "▓▓░",
        "▓▓░",
        "▓▓░",
        "░░░",
    ],
    # Underscore cursor
    'UCURSOR': [
        "   ",
        "  ░",
        "  ░",
        "▓▓░",
        "░░░",
    ],
    # Pipe cursor
    'PCURSOR': [
        " ▓ ",
        " ▓░",
        " ▓░",
        " ▓░",
        " ░░",
    ],
    # Arrow prompt >>>
    'ARROW': [
        "╔ ╔ ╔  ",
        "╚╗╚╗╚╗░",
        "╔╝╔╝╔╝░",
        "╚ ╚ ╚ ░",
        " ░░░░░░",
    ],
    # [OK]
    'OK': [
        "╔═╔═╗╔ ╔═╗",
        "║ ║ ║║╔╝ ░",
        "║ ║ ║║╚╗ ░",
        "╚═╚═╝╚ ╚ ░",
        " ░░░░░░░░░░",
    ],
    # [FAIL]
    'FAIL': [
        "╔═╔══╔═╗╔═╔  ═╗",
        "║ ║═ ║═║║ ║   ░",
        "║ ║  ║ ║║ ║  ░░",
        "╚═╚  ╚ ╚╚═╚══░░",
        " ░░░░░░░░░░░░░░░",
    ],
    # ■ block/stop
    'BLOCK': [
        "████ ",
        "████░",
        "████░",
        "████░",
        " ░░░░",
    ],
    # ► play
    'PLAY': [
        "╔╗   ",
        "║╚╗ ░",
        "║╔╝ ░",
        "╚╝  ░",
        " ░░░░",
    ],

    ' ': [
        "  ",
        "  ",
        "  ",
        "  ",
        "  ",
    ],
}


# =============================================================================
# 4-ROW 3D FONT — Compact block shadow style
# Each glyph: 4 rows, fixed width (mostly 4-5 chars wide)
# Shadow: right side ░ and bottom-right corner
# =============================================================================

FONT_4ROW = {
    'A': [
        "▄▀▄ ",
        "█ █░",
        "█▀█░",
        " ░░░",
    ],
    'B': [
        "█▀▄ ",
        "█▄▀░",
        "█▄▀░",
        " ░░░",
    ],
    'C': [
        "▄▀▀ ",
        "█  ░",
        "▀▄▄░",
        " ░░░",
    ],
    'D': [
        "█▀▄ ",
        "█ █░",
        "█▄▀░",
        " ░░░",
    ],
    'E': [
        "█▀▀ ",
        "█▄ ░",
        "█▄▄░",
        " ░░░",
    ],
    'F': [
        "█▀▀ ",
        "█▄ ░",
        "█  ░",
        " ░░░",
    ],
    'G': [
        "▄▀▀ ",
        "█ █░",
        "▀▄█░",
        " ░░░",
    ],
    'H': [
        "█ █ ",
        "█▄█░",
        "█ █░",
        " ░░░",
    ],
    'I': [
        "▀█▀ ",
        " █ ░",
        "▄█▄░",
        " ░░░",
    ],
    'J': [
        "▀▀█ ",
        "  █░",
        "▀▄▀░",
        " ░░░",
    ],
    'K': [
        "█ █ ",
        "█▄▀░",
        "█ █░",
        " ░░░",
    ],
    'L': [
        "█   ",
        "█  ░",
        "█▄▄░",
        " ░░░",
    ],
    'M': [
        "█▄▄█ ",
        "█▀ █░",
        "█  █░",
        " ░░░░",
    ],
    'N': [
        "█▄ █ ",
        "█▀██░",
        "█  █░",
        " ░░░░",
    ],
    'O': [
        "▄▀▄ ",
        "█ █░",
        "▀▄▀░",
        " ░░░",
    ],
    'P': [
        "█▀▄ ",
        "█▄▀░",
        "█  ░",
        " ░░░",
    ],
    'Q': [
        "▄▀▄ ",
        "█ █░",
        "▀▄▀░",
        " ░▀░",
    ],
    'R': [
        "█▀▄ ",
        "█ █░",
        "█▀▄░",
        " ░░░",
    ],
    'S': [
        "▄▀▀ ",
        "▀▄▄░",
        "▄▄▀░",
        " ░░░",
    ],
    'T': [
        "▀█▀ ",
        " █ ░",
        " █ ░",
        " ░░░",
    ],
    'U': [
        "█ █ ",
        "█ █░",
        "█▄█░",
        " ░░░",
    ],
    'V': [
        "█ █ ",
        "█ █░",
        " ▀ ░",
        " ░░░",
    ],
    'W': [
        "█  █ ",
        "█▄▄█░",
        "▀▀ ▀░",
        " ░░░░",
    ],
    'X': [
        "█ █ ",
        " █ ░",
        "█ █░",
        " ░░░",
    ],
    'Y': [
        "█ █ ",
        " █ ░",
        " █ ░",
        " ░░░",
    ],
    'Z': [
        "▀▀█ ",
        " █ ░",
        "█▄▄░",
        " ░░░",
    ],

    # --- NUMBERS ---
    '0': [
        "▄▀▄ ",
        "█ █░",
        "▀▄▀░",
        " ░░░",
    ],
    '1': [
        "▄█  ",
        " █ ░",
        "▄█▄░",
        " ░░░",
    ],
    '2': [
        "▀▀▄ ",
        " ▄▀░",
        "█▄▄░",
        " ░░░",
    ],
    '3': [
        "▀▀▄ ",
        " ▀▄░",
        "▄▄▀░",
        " ░░░",
    ],
    '4': [
        "█ █ ",
        "▀▀█░",
        "  █░",
        " ░░░",
    ],
    '5': [
        "█▀▀ ",
        "▀▀▄░",
        "▄▄▀░",
        " ░░░",
    ],
    '6': [
        "▄▀▀ ",
        "█▀▄░",
        "▀▄▀░",
        " ░░░",
    ],
    '7': [
        "▀▀█ ",
        " ▄▀░",
        " █ ░",
        " ░░░",
    ],
    '8': [
        "▄▀▄ ",
        "▄▀▄░",
        "▀▄▀░",
        " ░░░",
    ],
    '9': [
        "▄▀▄ ",
        "▀▄█░",
        "▄▄▀░",
        " ░░░",
    ],

    # --- SYMBOLS ---
    '&': [
        "▄▀▄ ",
        "█▀▄░",
        "▀▄█░",
        " ░░░",
    ],
    '!': [
        " █ ",
        " ▀░",
        " █░",
        " ░░",
    ],
    '?': [
        "▀▀▄ ",
        " ▄▀░",
        " ▀ ░",
        " ░░░",
    ],
    '.': [
        "   ",
        "  ░",
        " █░",
        " ░░",
    ],
    ',': [
        "   ",
        "  ░",
        " ▄░",
        " ▀░",
    ],
    ':': [
        "   ",
        " █░",
        " █░",
        " ░░",
    ],
    '-': [
        "    ",
        "▀▀░░",
        "  ░░",
        " ░░░",
    ],
    '_': [
        "    ",
        "   ░",
        "▄▄░░",
        " ░░░",
    ],
    '/': [
        "  █ ",
        " █░░",
        "█ ░░",
        " ░░░",
    ],
    '\\': [
        "█   ",
        "▀█ ░",
        " ▀█░",
        " ░░░",
    ],
    '@': [
        "▄▀▀▄ ",
        "█▄█▀░",
        "▀▄▄▄░",
        " ░░░░",
    ],
    '#': [
        "▄█▄█ ",
        "▀█▀█░",
        " █ █░",
        " ░░░░",
    ],
    '$': [
        "▄█▀ ",
        "▀█▄░",
        "▄█▄░",
        " ░░░",
    ],
    '%': [
        "█▄█ ",
        " █ ░",
        "█▄█░",
        " ░░░",
    ],
    '(': [
        " ▄ ",
        "█ ░",
        "▀▄░",
        " ░░",
    ],
    ')': [
        "▄  ",
        " █░",
        "▄▀░",
        " ░░",
    ],
    '[': [
        "█▀ ",
        "█ ░",
        "█▄░",
        " ░░",
    ],
    ']': [
        "▀█ ",
        " █░",
        "▄█░",
        " ░░",
    ],
    '+': [
        " ▄  ",
        "▄█▄░",
        " ▀ ░",
        " ░░░",
    ],
    '=': [
        "▀▀░ ",
        "▀▀░░",
        "  ░░",
        " ░░░",
    ],
    '*': [
        "▄█▄ ",
        " █ ░",
        "   ░",
        " ░░░",
    ],
    '"': [
        "█▀ ",
        "  ░",
        "  ░",
        " ░░",
    ],
    "'": [
        "█ ",
        " ░",
        " ░",
        " ░",
    ],
    '<': [
        " ▄ ",
        "█ ░",
        "▀▄░",
        " ░░",
    ],
    '>': [
        "▄  ",
        " █░",
        "▄▀░",
        " ░░",
    ],
    '^': [
        "▄▀▄ ",
        "   ░",
        "   ░",
        " ░░░",
    ],
    '~': [
        "▄▀▄▄ ",
        "    ░",
        "    ░",
        " ░░░░",
    ],
    '|': [
        " █ ",
        " █░",
        " █░",
        " ░░",
    ],
    '{': [
        " ▄▀",
        "█ ░",
        " ▀▄",
        " ░░",
    ],
    '}': [
        "▀▄ ",
        " █░",
        "▄▀░",
        " ░░",
    ],

    # --- 80s TERMINAL EXTRAS ---

    # >_  prompt
    'PROMPT': [
        "▄ ▄ ",
        " █▓░",
        "▄▀▀░",
        " ░░░",
    ],
    # $ shell
    'SHELL': [
        "▄█▀ ",
        "▀█▄░",
        "▄█▄░",
        " ░░░",
    ],
    # Block cursor
    'CURSOR': [
        "▓▓ ",
        "▓▓░",
        "▓▓░",
        "░░░",
    ],
    # Underscore cursor
    'UCURSOR': [
        "   ",
        "  ░",
        "▓▓░",
        "░░░",
    ],
    # Pipe cursor
    'PCURSOR': [
        "▓ ",
        "▓░",
        "▓░",
        "░░",
    ],
    # >>> arrow prompt
    'ARROW': [
        "▄ ▄ ▄  ",
        " █ █ █░",
        "▄▀▄▀▄▀░",
        " ░░░░░░",
    ],
    # [OK]
    'OK': [
        "▄ ▄▀▄ █▄▀▄ ",
        "█ █ █ █▀▄ ░",
        "▀ ▀▄▀ █ █ ░",
        " ░░░░░░░░░░",
    ],
    # [FAIL]
    'FAIL': [
        "▄ █▀▀ ▄▀▄ █ █  ▄ ",
        "█ █▀  █▀█ █ █  ░░",
        "▀ █   █ █ █ █▄▄░░",
        " ░░░░░░░░░░░░░░░░",
    ],
    # ■ block
    'BLOCK': [
        "███ ",
        "███░",
        "███░",
        " ░░░",
    ],
    # ► play
    'PLAY': [
        "█▄  ",
        "█ █░",
        "█▀ ░",
        " ░░░",
    ],

    ' ': [
        "  ",
        "  ",
        "  ",
        "  ",
    ],
}


# =============================================================================
# RENDER FUNCTIONS
# =============================================================================

def render(text, font_dict=None, spacing=0):
    """
    Render text using the 5-row 3D font.

    Args:
        text:       String to render (uppercase recommended)
        font_dict:  Override font dictionary (default: FONT_5ROW)
        spacing:    Extra columns between glyphs (default: 0)

    Returns:
        Multi-line string of rendered text
    """
    if font_dict is None:
        font_dict = FONT_5ROW
    rows = len(next(iter(font_dict.values())))
    spacer = " " * spacing
    lines = []
    for row in range(rows):
        line = spacer.join(
            font_dict.get(ch, font_dict.get(' ', [' '] * rows))[row]
            for ch in text.upper()
        )
        lines.append(line)
    return '\n'.join(lines)


def render4(text, spacing=0):
    """Render text using the 4-row 3D font."""
    return render(text, font_dict=FONT_4ROW, spacing=spacing)


def render_with_extras(text, extras=None, font_dict=None, spacing=0):
    """
    Render text with named extras inserted.

    Usage:
        render_with_extras("HELLO", extras=['CURSOR'], font_dict=FONT_5ROW)
        # Renders: HELLO▓▓

    Args:
        text:       Main text
        extras:     List of extra glyph names to append (e.g., ['CURSOR', 'PROMPT'])
        font_dict:  Font dict to use (default: FONT_5ROW)
        spacing:    Extra spacing between glyphs
    """
    if font_dict is None:
        font_dict = FONT_5ROW
    if extras is None:
        extras = []
    rows = len(next(iter(font_dict.values())))
    spacer = " " * spacing

    all_glyphs = [ch for ch in text.upper()] + extras
    lines = []
    for row in range(rows):
        line = spacer.join(
            font_dict.get(g, font_dict.get(' ', [' '] * rows))[row]
            for g in all_glyphs
        )
        lines.append(line)
    return '\n'.join(lines)


# =============================================================================
# DEMO
# =============================================================================

if __name__ == "__main__":
    print("=" * 72)
    print("  RETRO ASCII 3D FONT LIBRARY — DEMO")
    print("=" * 72)

    print("\n▬▬▬ 5-ROW 3D FONT ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n")

    print("— Full name:")
    print(render("DONALD PHILP"))
    print()

    print("— Alphabet A-M:")
    print(render("ABCDEFGHIJKLM"))
    print()
    print("— Alphabet N-Z:")
    print(render("NOPQRSTUVWXYZ"))
    print()

    print("— Numbers:")
    print(render("0123456789"))
    print()

    print("— Symbols:")
    print(render("!?&@#$%+-="))
    print()

    print("— Terminal prompt style:")
    print(render_with_extras("SYSTEM READY", extras=['CURSOR']))
    print()

    print("— Shell prompt:")
    print(render_with_extras("", extras=['SHELL', ' '], font_dict=FONT_5ROW))
    print(render("./RUN.SH"))
    print()

    print("— With prompt cursor:")
    print(render_with_extras("LOADING", extras=['PROMPT']))
    print()

    print("— Status messages:")
    print(render_with_extras("", extras=['OK']))
    print()
    print(render_with_extras("", extras=['FAIL']))
    print()


    print("\n▬▬▬ 4-ROW 3D FONT ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n")

    print("— Full name:")
    print(render4("DONALD PHILP"))
    print()

    print("— Alphabet A-M:")
    print(render4("ABCDEFGHIJKLM"))
    print()
    print("— Alphabet N-Z:")
    print(render4("NOPQRSTUVWXYZ"))
    print()

    print("— Numbers:")
    print(render4("0123456789"))
    print()

    print("— Symbols:")
    print(render4("!?&@#$%+-="))
    print()

    print("— Terminal prompt style:")
    print(render_with_extras("HELLO WORLD", extras=['CURSOR'], font_dict=FONT_4ROW))
    print()

    print("— Shell prompt:")
    print(render_with_extras("", extras=['SHELL', ' '], font_dict=FONT_4ROW))
    print(render4("CONNECT 2400"))
    print()

    print("— With prompt cursor:")
    print(render_with_extras("READY", extras=['PROMPT'], font_dict=FONT_4ROW))
    print()

    print("— Play icon:")
    print(render_with_extras("NOW PLAYING", extras=['PLAY'], font_dict=FONT_4ROW))
    print()

    print("=" * 72)
    print("  RETRO ASCII 3D FONT LIBRARY — END DEMO")
    print("=" * 72)