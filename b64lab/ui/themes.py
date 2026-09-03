"""
Dynamic Color Palette and Lane-Switching Theme Engine.
Pure Python standard library implementation.
"""

from dataclasses import dataclass
from typing import Dict
from .ansi import ANSI

@dataclass
class Palette:
    """Color palette definition for terminal UI elements."""
    name: str
    primary: str       # Main border and header color
    secondary: str     # Accents, badges, highlights
    accent: str        # Special focus, hotkeys, status tags
    text: str          # Standard reading text
    dim: str           # Subdued text, metadata, notes
    alert: str         # Errors, warnings, critical indicators
    success: str       # Flags, passing tests, valid decodes
    prompt: str        # Command input prompt style

# 1. 80s IBM / Cyberpunk Warm Amber (Default Master Theme)
PALETTE_AMBER = Palette(
    name="AMBER_CRT",
    primary=ANSI.rgb_fg(255, 176, 0),      # Classic amber phosphor
    secondary=ANSI.rgb_fg(255, 215, 0),    # Bright gold
    accent=ANSI.rgb_fg(255, 140, 0),       # Deep amber-orange
    text=ANSI.rgb_fg(240, 230, 200),       # Off-white warm text
    dim=ANSI.rgb_fg(160, 120, 40),         # Subdued amber
    alert=ANSI.BRIGHT_RED,
    success=ANSI.BRIGHT_GREEN,
    prompt=ANSI.rgb_fg(255, 190, 20),
)

# 2. Defensive / Blue Team Triage Lane (Ice Blue & Cyan)
PALETTE_ICE_BLUE = Palette(
    name="DEFENSIVE_ICE_BLUE",
    primary=ANSI.rgb_fg(0, 229, 255),      # Neon Ice Blue
    secondary=ANSI.rgb_fg(78, 201, 255),   # Soft Cyan
    accent=ANSI.rgb_fg(0, 150, 255),       # Deep Electric Blue
    text=ANSI.rgb_fg(220, 245, 255),       # Crisp light ice text
    dim=ANSI.rgb_fg(60, 110, 140),         # Subdued slate blue
    alert=ANSI.BRIGHT_RED,
    success=ANSI.rgb_fg(0, 255, 180),      # Neon Mint Green
    prompt=ANSI.rgb_fg(0, 229, 255),
)

# 3. Offensive / Red Team Forge Lane (Tactical Crimson Red)
PALETTE_CRIMSON = Palette(
    name="OFFENSIVE_CRIMSON",
    primary=ANSI.rgb_fg(255, 45, 85),      # Tactical Crimson
    secondary=ANSI.rgb_fg(255, 90, 95),    # Coral Red
    accent=ANSI.rgb_fg(200, 20, 40),       # Deep Blood Red
    text=ANSI.rgb_fg(255, 230, 230),       # Light warm white
    dim=ANSI.rgb_fg(150, 60, 60),          # Subdued dark red
    alert=ANSI.rgb_fg(255, 220, 0),        # High-visibility warning yellow
    success=ANSI.BRIGHT_GREEN,
    prompt=ANSI.rgb_fg(255, 50, 50),
)

# 4. Phosphor Green (Matrix / Retro VT220)
PALETTE_PHOSPHOR = Palette(
    name="PHOSPHOR_GREEN",
    primary=ANSI.rgb_fg(57, 255, 20),      # Neon Phosphor
    secondary=ANSI.rgb_fg(46, 204, 113),   # Jade Green
    accent=ANSI.rgb_fg(0, 180, 50),        # Forest Green
    text=ANSI.rgb_fg(220, 255, 220),       # Soft green-white
    dim=ANSI.rgb_fg(50, 120, 50),          # Subdued moss
    alert=ANSI.BRIGHT_RED,
    success=ANSI.BRIGHT_GREEN,
    prompt=ANSI.rgb_fg(57, 255, 20),
)

# 5. Monochrome High Contrast
PALETTE_MONO = Palette(
    name="MONOCHROME",
    primary=ANSI.BRIGHT_WHITE,
    secondary=ANSI.WHITE,
    accent=ANSI.BRIGHT_BLACK,
    text=ANSI.WHITE,
    dim=ANSI.BRIGHT_BLACK,
    alert=ANSI.BRIGHT_WHITE + ANSI.UNDERLINE,
    success=ANSI.BRIGHT_WHITE + ANSI.BOLD,
    prompt=ANSI.BRIGHT_WHITE,
)

AVAILABLE_PALETTES: Dict[str, Palette] = {
    "AMBER": PALETTE_AMBER,
    "ICE_BLUE": PALETTE_ICE_BLUE,
    "CRIMSON": PALETTE_CRIMSON,
    "PHOSPHOR": PALETTE_PHOSPHOR,
    "MONO": PALETTE_MONO,
}

class ThemeManager:
    """Manages dynamic theme changes and simulation lane switching."""

    _base_theme_key: str = "AMBER"
    _active_lane: str = "NEUTRAL"  # "NEUTRAL", "DEFENSIVE", "OFFENSIVE"

    @classmethod
    def get_palette(cls) -> Palette:
        """Returns the active palette based on current simulation lane."""
        if cls._active_lane == "DEFENSIVE":
            return PALETTE_ICE_BLUE
        if cls._active_lane == "OFFENSIVE":
            return PALETTE_CRIMSON
        return AVAILABLE_PALETTES.get(cls._base_theme_key, PALETTE_AMBER)

    @classmethod
    def set_lane(cls, lane: str) -> None:
        """
        Switches the visual lane context:
        - "DEFENSIVE": Changes terminal frame and accents to Ice Blue / Cyan.
        - "OFFENSIVE": Changes terminal frame and accents to Crimson Red.
        - "NEUTRAL": Reverts to the user's selected base theme (Amber CRT).
        """
        cls._active_lane = lane.upper()

    @classmethod
    def set_base_theme(cls, theme_key: str) -> bool:
        """Changes the default neutral theme (AMBER, PHOSPHOR, MONO, etc.)."""
        key = theme_key.upper()
        if key in AVAILABLE_PALETTES:
            cls._base_theme_key = key
            return True
        return False

    @classmethod
    def get_lane(cls) -> str:
        return cls._active_lane

    @classmethod
    def get_base_theme_name(cls) -> str:
        return cls._base_theme_key

Theme = ThemeManager
