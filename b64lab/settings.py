"""
Settings and Palette Customizer for B64Lab.
Pure Python standard library implementation.
"""

from .ui.components import UIComponents
from .ui.themes import Theme, AVAILABLE_PALETTES
from .ui.ansi import ANSI

class SettingsMenu:
    """Configures visual themes, terminal dimensions, and display preferences."""

    @classmethod
    def run(cls) -> None:
        while True:
            current_theme = Theme.get_base_theme_name()
            UIComponents.header(
                f"SETTINGS & PALETTE CUSTOMIZER  [ACTIVE THEME: {current_theme}]",
                "Select aesthetic themes, color temperature, and display formats"
            )

            print("  [1] 80s IBM / Cyberpunk Warm Amber (Default Retro CRT)")
            print("  [2] Phosphor Green (Matrix / VT220 Terminal)")
            print("  [3] Neon Ice Blue (Defensive SOC Console)")
            print("  [4] Tactical Crimson Red (Offensive Warfare Deck)")
            print("  [5] High-Contrast Monochrome (Pure White / Black)")
            print("  [0] Return to Main Menu\n")

            choice = UIComponents.prompt("Select theme option (0-5)")
            if choice == "0":
                break
            elif choice == "1":
                Theme.set_base_theme("AMBER")
                print("\n  [+] Applied 80s IBM / Cyberpunk Warm Amber.")
            elif choice == "2":
                Theme.set_base_theme("PHOSPHOR")
                print("\n  [+] Applied Phosphor Green theme.")
            elif choice == "3":
                Theme.set_base_theme("ICE_BLUE")
                print("\n  [+] Applied Neon Ice Blue theme.")
            elif choice == "4":
                Theme.set_base_theme("CRIMSON")
                print("\n  [+] Applied Tactical Crimson Red theme.")
            elif choice == "5":
                Theme.set_base_theme("MONO")
                print("\n  [+] Applied High-Contrast Monochrome theme.")
