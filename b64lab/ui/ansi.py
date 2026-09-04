"""
ANSI Escape Sequence Engine and Windows Terminal Initializer.
Pure Python standard library. Zero external dependencies.
"""

import os
import sys
import re
from typing import Tuple

# Regex to strip ANSI escape codes for accurate visual length calculation
ANSI_REGEX = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

def strip_ansi(text: str) -> str:
    """Removes all ANSI escape codes to calculate visible string length."""
    return ANSI_REGEX.sub("", text)

def visible_len(text: str) -> int:
    """Calculates visible character count ignoring ANSI styles."""
    return len(strip_ansi(text))

class ANSI:
    """Raw ANSI escape sequence constants and helpers."""
    
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    REVERSE = "\033[7m"
    
    # 4-bit standard foregrounds
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Bright foregrounds
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    # Screen control
    CLEAR_SCREEN = "\033[2J\033[H"
    CLEAR_LINE = "\033[2K\r"
    CURSOR_HIDE = "\033[?25l"
    CURSOR_SHOW = "\033[?25h"

    @staticmethod
    def rgb_fg(r: int, g: int, b: int) -> str:
        """24-bit TrueColor foreground escape sequence."""
        return f"\033[38;2;{r};{g};{b}m"

    @staticmethod
    def rgb_bg(r: int, g: int, b: int) -> str:
        """24-bit TrueColor background escape sequence."""
        return f"\033[48;2;{r};{g};{b}m"


class Terminal:
    """Terminal hardware controller and state initializer."""

    _initialized: bool = False

    @classmethod
    def initialize(cls) -> None:
        """Enables Virtual Terminal Processing on Windows consoles."""
        if cls._initialized:
            return

        # Ensure cross-platform UTF-8 terminal output on Windows
        if hasattr(sys.stdout, "reconfigure"):
            try:
                sys.stdout.reconfigure(encoding="utf-8", errors="replace")
                sys.stderr.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass

        if sys.platform == "win32":
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                # STD_OUTPUT_HANDLE = -11
                handle = kernel32.GetStdHandle(-11)
                mode = ctypes.c_ulong()
                kernel32.GetConsoleMode(handle, ctypes.byref(mode))
                # ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
                mode.value |= 0x0004
                kernel32.SetConsoleMode(handle, mode)
            except Exception:
                pass
                
        cls._initialized = True

    @staticmethod
    def get_size(default_width: int = 80, default_height: int = 24) -> Tuple[int, int]:
        """Returns the current (width, height) of the terminal window."""
        try:
            size = os.get_terminal_size()
            return max(32, size.columns), max(10, size.lines)
        except (OSError, ValueError):
            return default_width, default_height

    @staticmethod
    def get_width(default: int = 80) -> int:
        """Returns the current visible column width of the terminal window."""
        try:
            size = os.get_terminal_size()
            return max(32, size.columns)
        except (OSError, ValueError):
            return default

    @staticmethod
    def clear() -> None:
        """Clears the terminal screen smoothly."""
        sys.stdout.write(ANSI.CLEAR_SCREEN)
        sys.stdout.flush()
