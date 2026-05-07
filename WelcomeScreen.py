class WelcomeScreen(tk.Frame):
    """Splash / landing screen shown on app start."""

    # Each member is paired with a process ID so they get a matching color dot
    MEMBERS = [
        ("P1", "Zabala, Kylle Luis L."),
        ("P2", "Rodrigo, Ahron Daniel A."),
        ("P3", "Resuelo, Hanna Gabrielle N."),
    ]

    def __init__(self, parent, on_launch):
        super().__init__(parent, bg=AppTheme.BG)
        self._on_launch = on_launch  # Callback fired when the user clicks "Launch Simulator"
        self._build()

    def _build(self):
        # Build the welcome screen top to bottom:
        # course label → app title → subtitle → members card → launch button

        # Course label at the top
        tk.Label(self, text="OPERATING SYSTEMS  ·  LAB PROJECT",
            bg=AppTheme.BG, fg=AppTheme.ACCENT,
            font=("Consolas", 9, "bold")).pack(pady=(56, 0))

        # Main app title
        tk.Label(self, text="CPU Scheduler Simulator",
            bg=AppTheme.BG, fg="#ffffff",
            font=AppTheme.FONT_LARGE).pack(pady=(8, 2))

        # Subtitle describing the algorithm and feature
        tk.Label(self,
            text="First Come First Serve  ·  Dynamic Memory Allocation",
            bg=AppTheme.BG, fg=AppTheme.ACCENT,
            font=("Consolas", 11)).pack(pady=(0, 32))

        self._build_members_card()

        # Launch button — clicking it calls on_launch to switch to the simulator
        btn = HoverButton(self,
            text="▶  LAUNCH SIMULATOR",
            bg=AppTheme.ACCENT, fg="#0d1117",
            font=("Consolas", 11, "bold"),
            padx=40, pady=14,
            hover_bg="#79b8ff", hover_fg="#0d1117",
            command=self._on_launch)
        btn.pack(pady=44)

    def _build_members_card(self):
        # Builds the bordered card listing each project member with their color dot.
        card = tk.Frame(self, bg=AppTheme.CARD,
            highlightbackground=AppTheme.BORDER, highlightthickness=1,
            padx=56, pady=24)
        card.pack()

        tk.Label(card, text="— PROJECT MEMBERS —",
            bg=AppTheme.CARD, fg=AppTheme.MUTED,
            font=("Consolas", 8, "bold")).pack(pady=(0, 14))

        # One row per member: colored dot on the left, name on the right
        for pid, name in self.MEMBERS:
            row = tk.Frame(card, bg=AppTheme.CARD)
            row.pack(anchor="w", pady=5)
            # Small canvas used to draw the colored dot matching their process color
            cv = tk.Canvas(row, width=12, height=12,
                bg=AppTheme.CARD, highlightthickness=0)
            cv.pack(side="left", padx=(0, 8))
            cv.create_oval(1, 1, 12, 12,
                fill=AppTheme.PROC_COLORS[pid], outline="")
            tk.Label(row, text=name, bg=AppTheme.CARD, fg=AppTheme.TEXT,
                font=AppTheme.FONT_MONO).pack(side="left")