class CardFrame(tk.Frame):
    """A dark card with a 1-px border — used as a panel container."""

    def __init__(self, parent, **kwargs):
        # A plain Frame with a dark card background and a thin border.
        # Used as a reusable container/panel throughout the UI.
        super().__init__(parent, bg=AppTheme.CARD,
            highlightbackground=AppTheme.BORDER,
            highlightthickness=1, **kwargs)


class SectionHeader(tk.Frame):
    """Numbered section header row (e.g. '① PROCESS QUEUE')."""

    def __init__(self, parent, number: str, title: str):
        super().__init__(parent, bg=AppTheme.CARD)
        # The circled number (e.g. '①') shown in accent blue on the left
        tk.Label(self, text=number, bg=AppTheme.CARD, fg=AppTheme.ACCENT,
            font=("Consolas", 10, "bold")).pack(side="left", padx=(0, 8))
        # The section title (e.g. 'PROCESS QUEUE') shown in muted gray
        tk.Label(self, text=title, bg=AppTheme.CARD, fg=AppTheme.MUTED,
            font=("Consolas", 8, "bold")).pack(side="left")


class HoverButton(tk.Button):
    """Button that swaps foreground/background color on hover."""

    def __init__(self, parent, hover_bg=None, hover_fg=None, **kwargs):
        # Store the normal and hover colors so we can swap between them
        self._normal_bg  = kwargs.get("bg", AppTheme.CARD)
        self._normal_fg  = kwargs.get("fg", AppTheme.MUTED)
        self._hover_bg   = hover_bg or self._normal_bg   # Falls back to normal bg if not given
        self._hover_fg   = hover_fg or AppTheme.ACCENT   # Falls back to accent blue if not given
        super().__init__(parent, relief="flat", cursor="hand2", **kwargs)
        # Bind mouse enter/leave events to trigger the color swap
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, _):
        # Mouse is hovering — switch to hover colors
        self.config(
            bg=self._hover_bg if self._hover_bg != self._normal_bg else self._normal_bg,
            fg=self._hover_fg)

    def _on_leave(self, _):
        # Mouse left — restore the original colors
        self.config(bg=self._normal_bg, fg=self._normal_fg)