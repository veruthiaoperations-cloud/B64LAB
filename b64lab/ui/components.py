"""
Hand-Crafted Terminal UI Components, Boxes, Banners, and Tables.
Zero external dependencies. Pure ANSI and Unicode box-drawing.
"""

import sys
from typing import List, Optional, Tuple, Any
from .ansi import ANSI, Terminal, visible_len, strip_ansi
from .themes import Theme, Palette

class UIComponents:
    """Renders robust, nostalgic terminal UI elements."""

    DEFAULT_WIDTH = 80

    @classmethod
    def banner(cls, lane_label: Optional[str] = None) -> str:
        """
        Renders the signature B64Lab nostalgic ASCII logo with dynamic lane badge.
        """
        palette = Theme.get_palette()
        p = palette.primary
        s = palette.secondary
        a = palette.accent
        d = palette.dim
        r = ANSI.RESET

        lane = lane_label or Theme.get_lane()
        if lane == "DEFENSIVE":
            lane_badge = f"{palette.primary}[ DEFENSIVE / BLUE TEAM TRIAGE ]{r}"
        elif lane == "OFFENSIVE":
            lane_badge = f"{palette.primary}[ OFFENSIVE / RED TEAM SIMULATOR ]{r}"
        else:
            lane_badge = f"{palette.secondary}[ ZERO-DEPENDENCY LAB ENVIRONMENT ]{r}"

        lines = [
            f"{p}╔══════════════════════════════════════════════════════════════════════════════╗{r}",
            f"{p}║{r}  {s}██████╗  ██████╗ ██╗  ██╗██╗      █████╗ ██████╗{r}                            {p}║{r}",
            f"{p}║{r}  {s}██╔══██╗██╔════╝ ██║  ██║██║     ██╔══██╗██╔══██╗{r}   {lane_badge.ljust(43)} {p}║{r}",
            f"{p}║{r}  {s}██████╔╝███████╗ ███████║██║     ███████║██████╔╝{r}   {d}[ RFC 4648 SPEC ENGINE ]{r}     {p}║{r}",
            f"{p}║{r}  {s}██╔══██╗██╔═══██╗╚════██║██║     ██╔══██║██╔══██╗{r}   {d}[ BITWISE ACADEMY & CTF]{r}     {p}║{r}",
            f"{p}║{r}  {s}██████╔╝╚██████╔╝     ██║███████╗██║  ██║██████╔╝{r}                           {p}║{r}",
            f"{p}║{r}  {s}╚═════╝  ╚═════╝      ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝{r}    {a}v1.0.0 (SEC-STD-EDITION){r} {p}║{r}",
            f"{p}╚══════════════════════════════════════════════════════════════════════════════╝{r}",
        ]
        return "\n".join(lines)

    @classmethod
    def header(cls, title: str, subtitle: Optional[str] = None, width: int = DEFAULT_WIDTH) -> None:
        """Prints a standardized section header."""
        palette = Theme.get_palette()
        p = palette.primary
        t = palette.text
        d = palette.dim
        r = ANSI.RESET

        print(f"\n{p}───[ {ANSI.BOLD}{title.upper()}{r}{p} ]" + "─" * max(2, width - len(title) - 8) + f"{r}")
        if subtitle:
            print(f"    {d}{subtitle}{r}")
        print()

    @classmethod
    def box(
        cls,
        content_lines: List[str],
        title: Optional[str] = None,
        style: str = "double",
        width: int = DEFAULT_WIDTH,
    ) -> None:
        """
        Draws an aligned box around lines of text, automatically handling ANSI codes.
        Styles: 'double', 'single', 'rounded'.
        """
        palette = Theme.get_palette()
        p = palette.primary
        t = palette.text
        r = ANSI.RESET

        # Calculate actual width dynamically to prevent borders from breaking
        max_line_len = max((visible_len(l) for l in content_lines), default=0)
        title_len = visible_len(title) if title else 0
        box_width = max(width, max_line_len + 6, title_len + 8)

        if style == "double":
            tl, tr, bl, br, h, v = "╔", "╗", "╚", "╝", "═", "║"
        elif style == "rounded":
            tl, tr, bl, br, h, v = "╭", "╮", "╰", "╯", "─", "│"
        else:
            tl, tr, bl, br, h, v = "┌", "┐", "└", "┘", "─", "│"

        # Top border
        if title:
            title_str = f" {title} "
            title_vis = visible_len(title_str)
            remaining_h = max(2, box_width - 2 - title_vis - 2)
            top_line = f"{p}{tl}{h}{palette.secondary}{ANSI.BOLD}{title_str}{r}{p}{h * remaining_h}{tr}{r}"
        else:
            top_line = f"{p}{tl}{h * (box_width - 2)}{tr}{r}"

        print(top_line)

        # Body
        inner_width = box_width - 4
        for line in content_lines:
            vis = visible_len(line)
            pad_len = max(0, inner_width - vis)
            print(f"{p}{v}{r}  {t}{line}{r}{' ' * pad_len}  {p}{v}{r}")

        # Bottom border
        print(f"{p}{bl}{h * (box_width - 2)}{br}{r}")

    @classmethod
    def table(
        cls,
        headers: List[str],
        rows: List[List[Any]],
        col_widths: Optional[List[int]] = None,
    ) -> None:
        """Renders an ASCII table with styled borders and alignment."""
        palette = Theme.get_palette()
        p = palette.primary
        s = palette.secondary
        t = palette.text
        d = palette.dim
        r = ANSI.RESET

        # Calculate column widths if not provided
        if not col_widths:
            col_widths = []
            for col_idx in range(len(headers)):
                max_w = visible_len(headers[col_idx])
                for row in rows:
                    if col_idx < len(row):
                        max_w = max(max_w, visible_len(str(row[col_idx])))
                col_widths.append(max_w + 2)

        total_width = sum(col_widths) + len(col_widths) + 1

        # Header top
        header_cells = []
        for h, w in zip(headers, col_widths):
            header_cells.append(f" {s}{ANSI.BOLD}{h.ljust(w - 1)}{r}")
        print(f"{p}┌" + "┬".join("─" * w for w in col_widths) + f"┐{r}")
        print(f"{p}│{r}" + f"{p}│{r}".join(header_cells) + f"{p}│{r}")
        print(f"{p}├" + "┼".join("─" * w for w in col_widths) + f"┤{r}")

        # Data rows
        for row in rows:
            cells = []
            for col_idx, w in enumerate(col_widths):
                val = str(row[col_idx]) if col_idx < len(row) else ""
                v_len = visible_len(val)
                padding = " " * max(0, w - 1 - v_len)
                cells.append(f" {t}{val}{r}{padding}")
            print(f"{p}│{r}" + f"{p}│{r}".join(cells) + f"{p}│{r}")

        # Bottom
        print(f"{p}└" + "┴".join("─" * w for w in col_widths) + f"┘{r}")

    @classmethod
    def badge(cls, text: str, kind: str = "INFO") -> str:
        """Formats an inline cybersecurity badge."""
        palette = Theme.get_palette()
        r = ANSI.RESET
        if kind == "ALERT" or kind == "CRITICAL":
            return f"{ANSI.rgb_bg(180, 20, 20)}{ANSI.BRIGHT_WHITE} {text} {r}"
        if kind == "SUCCESS":
            return f"{ANSI.rgb_bg(20, 140, 40)}{ANSI.BRIGHT_WHITE} {text} {r}"
        if kind == "DEFENSIVE":
            return f"{ANSI.rgb_bg(0, 100, 140)}{ANSI.BRIGHT_WHITE} {text} {r}"
        if kind == "OFFENSIVE":
            return f"{ANSI.rgb_bg(140, 20, 40)}{ANSI.BRIGHT_WHITE} {text} {r}"
        return f"{palette.primary}[{text}]{r}"

    @classmethod
    def prompt(cls, message: str = "Select option") -> str:
        """Displays an interactive user prompt with active palette styling."""
        palette = Theme.get_palette()
        p = palette.prompt
        r = ANSI.RESET
        try:
            val = input(f"{p}[b64lab]{r} {message}: ")
            return val.strip()
        except (KeyboardInterrupt, EOFError):
            print("\n")
            return "0"

    @classmethod
    def pause(cls, msg: str = "Press [ENTER] to continue...") -> None:
        """Pauses execution until user presses Enter."""
        palette = Theme.get_palette()
        d = palette.dim
        r = ANSI.RESET
        try:
            input(f"\n  {d}{msg}{r}")
        except (KeyboardInterrupt, EOFError):
            pass
