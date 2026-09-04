"""
Hand-Crafted Terminal UI Components, Boxes, Banners, and Tables.
Zero external dependencies. Pure ANSI and Unicode box-drawing.
"""

import os
import sys
import re
from typing import List, Optional, Tuple, Any
from .ansi import ANSI, Terminal, visible_len, strip_ansi
from .themes import Theme, Palette

class UIComponents:
    """Renders robust, nostalgic terminal UI elements."""

    DEFAULT_WIDTH = 80
    MIN_WIDTH = 40

    @classmethod
    def get_width(cls, requested_width: Optional[int] = None) -> int:
        """Calculates responsive component width constrained by terminal dimensions."""
        try:
            real_cols = os.get_terminal_size().columns
            term_width = max(cls.MIN_WIDTH, real_cols)
            if requested_width is not None:
                return max(cls.MIN_WIDTH, min(term_width, requested_width))
            return max(cls.MIN_WIDTH, min(term_width, cls.DEFAULT_WIDTH))
        except (OSError, ValueError):
            if requested_width is not None:
                return max(cls.MIN_WIDTH, requested_width)
            return cls.DEFAULT_WIDTH

    @classmethod
    def wrap_text(cls, line: str, max_width: int) -> List[str]:
        """
        Wraps a single text line (with optional ANSI escape codes and indentation)
        so that no line exceeds max_width visible characters.
        """
        if not line:
            return [""]
        if visible_len(line) <= max_width:
            return [line]
            
        raw_indent_match = re.match(r'^(\s*)', strip_ansi(line))
        indent = raw_indent_match.group(1) if raw_indent_match else ""
        indent_len = len(indent)
        if indent_len >= max_width:
            indent = ""
            indent_len = 0
            
        from .ansi import ANSI_REGEX
        token_pattern = re.compile(r'(\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])|\S+|\s+)')
        tokens = token_pattern.findall(line)
        
        lines: List[str] = []
        current_tokens: List[str] = []
        current_vis = 0
        active_style = ""
        
        for tok in tokens:
            if ANSI_REGEX.match(tok):
                current_tokens.append(tok)
                if tok in ('\033[0m', '\x1b[0m', '\033[m', '\x1b[m'):
                    active_style = ""
                else:
                    active_style += tok
                continue
                
            is_space = tok.isspace()
            t_len = len(tok)
            
            if is_space:
                if current_vis + t_len <= max_width:
                    current_tokens.append(tok)
                    current_vis += t_len
                else:
                    # Omit trailing whitespace at line break
                    pass
            else: # Word
                if current_vis + t_len <= max_width:
                    current_tokens.append(tok)
                    current_vis += t_len
                else:
                    if current_vis > indent_len:
                        if active_style:
                            current_tokens.append('\033[0m')
                        lines.append("".join(current_tokens))
                        current_tokens = [active_style, indent] if indent else ([active_style] if active_style else [])
                        current_vis = indent_len
                        
                    avail = max(1, max_width - indent_len)
                    w_tok = tok
                    while len(w_tok) > avail:
                        chunk = w_tok[:avail]
                        current_tokens.append(chunk)
                        if active_style:
                            current_tokens.append('\033[0m')
                        lines.append("".join(current_tokens))
                        current_tokens = [active_style, indent] if indent else ([active_style] if active_style else [])
                        current_vis = indent_len
                        w_tok = w_tok[avail:]
                        
                    if w_tok:
                        current_tokens.append(w_tok)
                        current_vis += len(w_tok)
                        
        if current_tokens:
            lines.append("".join(current_tokens))
            
        return lines

    @classmethod
    def banner(cls, lane_label: Optional[str] = None) -> str:
        """
        Renders the signature B64Lab nostalgic ASCII logo with dynamic lane badge.
        Adapts responsively: full 80-col banner on standard screens, compact on narrow (<80 cols).
        """
        palette = Theme.get_palette()
        p = palette.primary
        s = palette.secondary
        a = palette.accent
        d = palette.dim
        t = palette.text
        r = ANSI.RESET

        lane = lane_label or Theme.get_lane()
        if lane == "DEFENSIVE":
            badge_text = "[ DEFENSIVE TRIAGE ]"
            badge_color = palette.primary
        elif lane == "OFFENSIVE":
            badge_text = "[ OFFENSIVE FORGE ]"
            badge_color = palette.primary
        else:
            badge_text = "[ ZERO-DEPENDENCY ]"
            badge_color = palette.secondary

        term_w = cls.get_width()
        if term_w < 80:
            # Responsive compact banner for narrow screens
            badge = lane_label or Theme.get_lane()
            title = " B64LAB :: CYBER LAB "
            rem = max(2, term_w - len(title) - 3)
            top = f"{p}┌─{s}{ANSI.BOLD}{title}{r}{p}{'─' * rem}┐{r}"
            
            mid1_vis = len(badge) + 2 + 2 + 16
            mid1_pad = " " * max(0, term_w - mid1_vis - 6)
            mid1 = f"{p}│{r}  {badge_color}[{badge}]{r}  {d}v1.0.0 (SEC-STD){r}{mid1_pad}  {p}│{r}"
            
            mid2_txt = "Zero-Dependency Base64 & Bitwise Engine"
            if len(mid2_txt) > term_w - 6:
                mid2_txt = mid2_txt[:term_w - 9] + "..."
            mid2_pad = " " * max(0, term_w - len(mid2_txt) - 6)
            mid2 = f"{p}│{r}  {t}{mid2_txt}{r}{mid2_pad}  {p}│{r}"
            
            bot = f"{p}└{'─' * (term_w - 2)}┘{r}"
            return "\n".join([top, mid1, mid2, bot])

        # Standard 80-column retro ASCII art banner
        logo = [
            "██████╗  ██████╗ ██╗  ██╗ ██╗       █████╗  ██████╗ ",
            "██╔══██╗██╔════╝ ██║  ██║ ██║      ██╔══██╗ ██╔══██╗",
            "██████╔╝███████╗ ███████║ ██║      ███████║ ██████╔╝",
            "██╔══██╗██╔═══██╗╚════██║ ██║      ██╔══██║ ██╔══██╗",
            "██████╔╝╚██████╔╝     ██║ ███████╗ ██║  ██║ ██████╔╝",
            "╚═════╝  ╚═════╝      ╚═╝ ╚══════╝ ╚═╝  ╚═╝ ╚═════╝ ",
        ]

        pad_b = " " * (23 - len(badge_text))
        right_items = [
            " " * 23,
            f"{badge_color}{badge_text}{r}" + pad_b,
            f"{d}[ RFC 4648 SPEC ]{r}" + (" " * (23 - 17)),
            f"{d}[ BITWISE & CTF ]{r}" + (" " * (23 - 17)),
            f"{d}[ FORENSIC LAB ]{r}" + (" " * (23 - 16)),
            f"{a}v1.0.0 (SEC-STD){r}" + (" " * (23 - 16)),
        ]

        lines = [f"{p}╔" + ("═" * 78) + f"╗{r}"]
        for i in range(6):
            lines.append(f"{p}║{r} {s}{logo[i]}{r} {right_items[i]} {p}║{r}")
        lines.append(f"{p}╚" + ("═" * 78) + f"╝{r}")
        return "\n".join(lines)

    @classmethod
    def header(cls, title: str, subtitle: Optional[str] = None, width: Optional[int] = None) -> None:
        """Prints a standardized section header responsive to terminal width."""
        palette = Theme.get_palette()
        p = palette.primary
        d = palette.dim
        r = ANSI.RESET

        box_w = cls.get_width(width)
        title_vis = visible_len(title)
        if title_vis > box_w - 10:
            fill_len = 2
        else:
            fill_len = max(2, box_w - title_vis - 7)
        print(f"\n{p}───[ {ANSI.BOLD}{title.upper()}{r}{p} ]" + ("─" * fill_len) + f"{r}")
        if subtitle:
            sub_lines = cls.wrap_text(subtitle, box_w - 6)
            for sline in sub_lines:
                print(f"    {d}{sline}{r}")
        print()

    @classmethod
    def box(
        cls,
        content_lines: List[str],
        title: Optional[str] = None,
        style: str = "double",
        width: Optional[int] = None,
    ) -> None:
        """
        Draws an aligned box around lines of text, automatically handling ANSI codes
        and word-wrapping long lines to fit the terminal width without breaking borders.
        Styles: 'double', 'single', 'rounded'.
        """
        palette = Theme.get_palette()
        p = palette.primary
        t = palette.text
        r = ANSI.RESET

        box_width = cls.get_width(width)
        inner_width = max(10, box_width - 6)

        if style == "double":
            tl, tr, bl, br, h, v = "╔", "╗", "╚", "╝", "═", "║"
        elif style == "rounded":
            tl, tr, bl, br, h, v = "╭", "╮", "╰", "╯", "─", "│"
        else:
            tl, tr, bl, br, h, v = "┌", "┐", "└", "┘", "─", "│"

        # Top border
        if title:
            max_title_content = max(1, box_width - 11)
            if visible_len(title) > box_width - 8:
                title_trimmed = title[:max_title_content] + "..."
            else:
                title_trimmed = title
            title_str = f" {title_trimmed} "
            title_vis = visible_len(title_str)
            remaining_h = max(2, box_width - title_vis - 4)
            top_line = f"{p}{tl}{h}{h}{palette.secondary}{ANSI.BOLD}{title_str}{r}{p}{h * remaining_h}{tr}{r}"
        else:
            top_line = f"{p}{tl}{h * (box_width - 2)}{tr}{r}"

        print(top_line)

        # Body: wrap all lines to inner_width
        for raw_line in content_lines:
            wrapped_lines = cls.wrap_text(raw_line, inner_width)
            for line in wrapped_lines:
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
        max_width: Optional[int] = None,
    ) -> None:
        """Renders an ASCII table with styled borders, alignment, and responsive column scaling."""
        palette = Theme.get_palette()
        p = palette.primary
        s = palette.secondary
        t = palette.text
        r = ANSI.RESET

        target_max_w = cls.get_width(max_width)
        num_cols = len(headers)
        overhead = num_cols + 1 # 1 border per column boundary
        avail_width = max(num_cols * 5, target_max_w - overhead)

        # Calculate natural column widths if not provided
        if not col_widths:
            col_widths = []
            for col_idx in range(num_cols):
                max_w = visible_len(headers[col_idx])
                for row in rows:
                    if col_idx < len(row):
                        max_w = max(max_w, visible_len(str(row[col_idx])))
                col_widths.append(max_w + 2)

        # Responsive downscaling if columns exceed available terminal width
        widths = list(col_widths)
        if sum(widths) > avail_width:
            while sum(widths) > avail_width:
                max_val = max(widths)
                if max_val <= 6:
                    break
                idx = widths.index(max_val)
                widths[idx] -= 1
        col_widths = widths

        # Header top
        header_cells = []
        for h, w in zip(headers, col_widths):
            h_str = h[:w - 4] + "..." if visible_len(h) > w - 1 else h
            pad = " " * max(0, w - 1 - visible_len(h_str))
            header_cells.append(f" {s}{ANSI.BOLD}{h_str}{r}{pad}")
        print(f"{p}┌" + "┬".join("─" * w for w in col_widths) + f"┐{r}")
        print(f"{p}│{r}" + f"{p}│{r}".join(header_cells) + f"{p}│{r}")
        print(f"{p}├" + "┼".join("─" * w for w in col_widths) + f"┤{r}")

        # Data rows
        for row in rows:
            cells = []
            for col_idx, w in enumerate(col_widths):
                val = str(row[col_idx]) if col_idx < len(row) else ""
                v_len = visible_len(val)
                if v_len > w - 1:
                    val = val[:max(1, w - 4)] + "..."
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
