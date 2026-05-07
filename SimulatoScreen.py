class SimulatorScreen(tk.Frame):
    """
    The main 4-panel simulator view.
    Owns the 4 panels and orchestrates the animation chain.
    """

    def __init__(self, parent, on_back):
        super().__init__(parent, bg=AppTheme.BG)
        self._on_back   = on_back        # Callback to return to the Welcome screen
        self._results   = []             # Stores scheduled process results after FCFS runs
        self._scheduler = FCFSScheduler() # The pure scheduling algorithm — no UI dependency

        # Panel references — all set to None until _build() creates them
        self._queue_panel  = None   # ① Process input table
        self._memory_panel = None   # ② Memory map bar
        self._gantt_panel  = None   # ③ Gantt chart
        self._stats_panel  = None   # ④ Statistics table + averages

        self._build()

    # ── Build ────────────────────────────────────────────────────────────────

    def _build(self):
        # Build the fixed header bar first, then the scrollable content below it
        self._build_header()
        self._build_scrollable_body()

    def _build_header(self):
        # Fixed top bar showing the app title, subtitle, and a Back button
        hdr = tk.Frame(self, bg=AppTheme.SURFACE,
            highlightbackground=AppTheme.BORDER, highlightthickness=1)
        hdr.pack(fill="x")

        tk.Label(hdr, text="CPU Scheduler Simulator",
            bg=AppTheme.SURFACE, fg="#fff",
            font=AppTheme.FONT_TITLE).pack(side="left", padx=20, pady=12)
        tk.Label(hdr, text="FCFS  ·  Dynamic Memory Allocation",
            bg=AppTheme.SURFACE, fg=AppTheme.ACCENT,
            font=("Consolas", 9)).pack(side="left", pady=12)

        # Back button on the right — calls on_back to return to the Welcome screen
        HoverButton(hdr, text="← Back",
            bg=AppTheme.SURFACE, fg=AppTheme.MUTED,
            font=("Consolas", 9),
            padx=14, pady=8,
            hover_fg=AppTheme.ACCENT,
            command=self._on_back).pack(side="right", padx=20, pady=10)

    def _build_scrollable_body(self):
        # Wraps the main content in a Canvas + Scrollbar so the page can scroll
        # vertically if the window is too short to show everything at once.
        outer = tk.Canvas(self, bg=AppTheme.BG, highlightthickness=0)
        sb    = ttk.Scrollbar(self, orient="vertical", command=outer.yview)
        outer.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        outer.pack(fill="both", expand=True)

        # The actual content lives inside this Frame, placed inside the Canvas
        main = tk.Frame(outer, bg=AppTheme.BG)
        outer.create_window((0, 0), window=main, anchor="nw")

        # Update the scroll region whenever the content frame changes size
        main.bind("<Configure>", lambda e:
            outer.configure(scrollregion=outer.bbox("all")))

        # Enable mouse-wheel scrolling on all platforms
        outer.bind_all("<MouseWheel>", lambda e:
            outer.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        self._build_panels(main)

    def _build_panels(self, container):
        # Layout:
        #   TOP ROW    → ① Process Queue (left, wider) | ② Memory Map (right)
        #   BOTTOM ROW → ③ Gantt Chart + ④ Statistics (full width)

        # ── Top row ──
        top_row = tk.Frame(container, bg=AppTheme.BG)
        top_row.pack(fill="x", padx=24, pady=(20, 0))

        # Left column: Process Queue — expands to fill available width
        input_col = tk.Frame(top_row, bg=AppTheme.BG)
        input_col.pack(side="left", fill="both", expand=True, padx=(0, 16))

        # Right column: Memory Map — fixed width, anchored to the top
        mem_col = tk.Frame(top_row, bg=AppTheme.BG)
        mem_col.pack(side="left", fill="y", anchor="n")

        # ── Bottom row ──
        bottom_col = tk.Frame(container, bg=AppTheme.BG)
        bottom_col.pack(fill="x", padx=24, pady=(16, 24))

        # Instantiate all four panels and place them in their columns
        self._queue_panel  = ProcessQueuePanel(input_col,
            on_run=self._on_run, on_reset=self._on_reset)
        self._queue_panel.pack(fill="x")

        self._memory_panel = MemoryMapPanel(mem_col)
        self._memory_panel.pack(fill="y")

        self._gantt_panel  = GanttChartPanel(bottom_col)
        self._gantt_panel.pack(fill="x", pady=(0, 14))

        self._stats_panel  = StatisticsPanel(bottom_col)
        self._stats_panel.pack(fill="x")