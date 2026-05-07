class ProcessQueuePanel(CardFrame):
    """
    Renders the input table for up to 5 processes.
    Owns validation logic and exposes flash_rows() for animation.
    """

    def __init__(self, parent, on_run, on_reset):
        super().__init__(parent)
        self._on_run    = on_run    # Callback fired when the user clicks "Run FCFS"
        self._on_reset  = on_reset  # Callback fired when the user clicks "Reset"
        self.entries    = {}        # Stores input widgets per process: { pid: {bv, av, be, ae, el} }
        self._run_btn   = None      # Reference to the Run button so we can enable/disable it
        self._build()

    # ── Build ────────────────────────────────────────────────────────────────

    def _build(self):
        # Assemble the full panel: header → column labels → one row per process → buttons
        SectionHeader(self, "①", "PROCESS QUEUE").pack(
            fill="x", padx=18, pady=(16, 8))
        self._build_column_headers()
        for pid in Process.VALID_IDS:
            self._build_process_row(pid)
        tk.Frame(self, bg=AppTheme.BORDER, height=1).pack(
            fill="x", padx=14, pady=12)
        self._build_buttons()

    def _build_column_headers(self):
        # Draws the "Process / CPU Burst Time / Arrival Time" header row
        row = tk.Frame(self, bg=AppTheme.SURFACE)
        row.pack(fill="x", padx=14, pady=(0, 6))
        for txt, w in [
            ("Process", 8),
            ("CPU Burst Time (msec)", 22),
            ("Arrival Time (msec)", 20),
        ]:
            tk.Label(row, text=txt, bg=AppTheme.SURFACE, fg=AppTheme.MUTED,
                font=("Consolas", 9, "bold"),
                width=w, anchor="w").pack(side="left", padx=8, pady=9)

    def _build_process_row(self, pid: str):
        # Builds one input row for a single process containing:
        #   - A colored dot + process ID badge on the left
        #   - A Burst Time entry field
        #   - An Arrival Time entry field
        #   - An inline error label (hidden until validation fails)
        row = tk.Frame(self, bg=AppTheme.CARD)
        row.pack(fill="x", padx=14, pady=5)

        # Colored dot + PID badge
        badge = tk.Frame(row, bg=AppTheme.CARD)
        badge.pack(side="left", padx=6)
        cv = tk.Canvas(badge, width=12, height=12,
            bg=AppTheme.CARD, highlightthickness=0)
        cv.pack(side="left", padx=(0, 6))
        cv.create_oval(1, 1, 12, 12, fill=AppTheme.PROC_COLORS[pid], outline="")
        tk.Label(badge, text=pid, bg=AppTheme.CARD,
            fg=AppTheme.PROC_COLORS[pid],
            font=("Consolas", 10, "bold"), width=3).pack(side="left")

        # StringVars back each entry so we can read/clear them easily
        bv, av = tk.StringVar(), tk.StringVar()

        be = tk.Entry(row, textvariable=bv, bg=AppTheme.SURFACE, fg=AppTheme.TEXT,
            insertbackground=AppTheme.ACCENT, relief="flat",
            font=AppTheme.FONT_MONO, width=14,
            highlightbackground=AppTheme.BORDER, highlightthickness=1)
        be.pack(side="left", padx=(10, 0), ipady=7)

        ae = tk.Entry(row, textvariable=av, bg=AppTheme.SURFACE, fg=AppTheme.TEXT,
            insertbackground=AppTheme.ACCENT, relief="flat",
            font=AppTheme.FONT_MONO, width=14,
            highlightbackground=AppTheme.BORDER, highlightthickness=1)
        ae.pack(side="left", padx=(18, 0), ipady=7)

        # Inline error label — stays empty until validation finds a problem
        el = tk.Label(row, text="", bg=AppTheme.CARD, fg=AppTheme.DANGER,
            font=("Consolas", 8))
        el.pack(side="left", padx=(10, 0))

        # Store all widgets for this process so other methods can access them by pid
        self.entries[pid] = dict(bv=bv, av=av, be=be, ae=ae, el=el)

    def _build_buttons(self):
        # Creates the "Run FCFS" and "Reset" buttons side by side
        btn_row = tk.Frame(self, bg=AppTheme.CARD)
        btn_row.pack(anchor="w", padx=18, pady=(0, 18))

        self._run_btn = HoverButton(btn_row,
            text="▶  Run FCFS",
            bg=AppTheme.ACCENT, fg="#0d1117",
            font=("Consolas", 10, "bold"),
            padx=22, pady=9,
            hover_bg="#79b8ff", hover_fg="#0d1117",
            command=self._on_run)
        self._run_btn.pack(side="left", padx=(0, 12))

        HoverButton(btn_row, text="↺  Reset",
            bg=AppTheme.CARD, fg=AppTheme.MUTED,
            font=AppTheme.FONT_MONO, padx=18, pady=9,
            hover_fg=AppTheme.TEXT,
            command=self._on_reset).pack(side="left")

    # ── Public API ───────────────────────────────────────────────────────────

    def validate(self) -> list[Process] | None:
        """
        Reads all entries.  Empty rows are skipped.
        Returns None if any error is found, else a list of Process objects.
        """
        processes, has_error = [], False
        for pid in Process.VALID_IDS:
            e = self.entries[pid]
            bs  = e["bv"].get().strip()
            as_ = e["av"].get().strip()

            # Reset any previous validation highlights and error messages
            e["be"].config(highlightbackground=AppTheme.BORDER)
            e["ae"].config(highlightbackground=AppTheme.BORDER)
            e["el"].config(text="")

            # Skip rows where both fields are empty (process not being used)
            if bs == "" and as_ == "":
                continue

            err, b, a = "", None, None

            # Validate burst time — must be a positive integer
            if bs == "":
                err = "Burst required"
                e["be"].config(highlightbackground=AppTheme.DANGER)
            else:
                try:
                    b = int(bs)
                    if b < 1:
                        raise ValueError
                except ValueError:
                    err = "Burst ≥ 1"
                    e["be"].config(highlightbackground=AppTheme.DANGER)

            # Validate arrival time — must be a non-negative integer
            if as_ == "":
                err += ("  " if err else "") + "Arrival required"
                e["ae"].config(highlightbackground=AppTheme.DANGER)
            else:
                try:
                    a = int(as_)
                    if a < 0:
                        raise ValueError
                except ValueError:
                    err += ("  " if err else "") + "Arrival ≥ 0"
                    e["ae"].config(highlightbackground=AppTheme.DANGER)

            if err:
                # Show the error message inline and flag that validation failed
                e["el"].config(text=err)
                has_error = True
            elif b is not None and a is not None:
                # Both fields are valid — create a Process object for this row
                processes.append(Process(pid, b, a))

        return None if has_error else processes

    def reset(self):
        # Clear all entry fields, remove validation highlights, and re-enable the Run button
        for pid in Process.VALID_IDS:
            e = self.entries[pid]
            e["bv"].set("")
            e["av"].set("")
            e["be"].config(highlightbackground=AppTheme.BORDER)
            e["ae"].config(highlightbackground=AppTheme.BORDER)
            e["el"].config(text="")
        self.set_run_button_state(normal=True)

    def set_run_button_state(self, normal: bool):
        # Switches the Run button between its active state ("Run FCFS")
        # and its disabled state ("Scheduling...") during animation
        if normal:
            self._run_btn.config(
                state="normal", text="▶  Run FCFS", bg=AppTheme.ACCENT)
        else:
            self._run_btn.config(
                state="disabled", text="⏳ Scheduling...", bg=AppTheme.MUTED)

    def flash_rows(self, processes: list[Process], callback):
        """Flash each active process row's entry borders, then call callback."""
        pid_set = {p.pid for p in processes}
        pids    = [p for p in Process.VALID_IDS if p in pid_set]  # Preserve display order

        def flash(idx, on):
            if idx >= len(pids):
                # All rows have flashed — wait 200 ms then trigger the next animation
                self.after(200, callback)
                return
            pid   = pids[idx]
            color = AppTheme.PROC_COLORS[pid] if on else AppTheme.BORDER
            self.entries[pid]["be"].config(highlightbackground=color)
            self.entries[pid]["ae"].config(highlightbackground=color)
            if on:
                # Keep the highlight on for 180 ms, then flash off
                self.after(180, lambda: flash(idx, False))
            else:
                # After flash-off, move to the next row after 60 ms
                self.after(60,  lambda: flash(idx + 1, True))

        flash(0, True)