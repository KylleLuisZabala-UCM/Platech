"""
CPU Scheduler Simulator — First Come First Serve + Dynamic Memory Allocation
Members:
    Zabala, Kylle Luis L.
    Rodrigo, Ahron Daniel A.
    Resuelo, Hanna Gabrielle N.

Requirements: Python 3.x  (tkinter ships with standard Python)
Run: python cpu_scheduler_fcfs.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math

# ── THEME ──────────────────────────────────────────────────────────────
BG      = "#0d1117"
SURFACE = "#161b22"
CARD    = "#1c2333"
BORDER  = "#30363d"
TEXT    = "#e6edf3"
MUTED   = "#8b949e"
ACCENT  = "#58a6ff"
SUCCESS = "#2ecc71"
WARNING = "#f1c40f"
DANGER  = "#e74c3c"

PROC_COLORS = {
    "P1": "#c0392b",
    "P2": "#2980b9",
    "P3": "#4a5568",
    "P4": "#27ae60",
    "P5": "#d35400",
}

TOTAL_MEM_MB = 64
OS_MEM_MB    = 8
PROC_IDS     = ["P1", "P2", "P3", "P4", "P5"]
MEM_H        = 340   # fixed memory canvas height


# ── FCFS ALGORITHM ─────────────────────────────────────────────────────
def run_fcfs(processes):
    sorted_procs = sorted(processes,
        key=lambda p: (p["arrival"], PROC_IDS.index(p["id"])))
    t, results = 0, []
    for p in sorted_procs:
        if t < p["arrival"]:
            t = p["arrival"]
        start = t
        ct    = t + p["burst"]
        tat   = ct - p["arrival"]
        wt    = tat - p["burst"]
        results.append({**p, "start": start, "ct": ct, "tat": tat, "wt": wt})
        t = ct
    return results


# ── MAIN APPLICATION ───────────────────────────────────────────────────
class CPUSchedulerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CPU Scheduler Simulator — FCFS")
        self.configure(bg=BG)
        self.resizable(True, True)
        self.minsize(1000, 680)
        self._mem_done_callback = None

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(".",
            background=BG, foreground=TEXT,
            fieldbackground=CARD, bordercolor=BORDER,
            troughcolor=SURFACE, selectbackground=ACCENT,
            selectforeground="#0d1117", font=("Consolas", 10))
        style.configure("Treeview",
            background=CARD, foreground=TEXT,
            fieldbackground=CARD, rowheight=32,
            borderwidth=0, font=("Consolas", 10))
        style.configure("Treeview.Heading",
            background=SURFACE, foreground=MUTED,
            font=("Consolas", 9, "bold"), relief="flat", borderwidth=0)
        style.map("Treeview",
            background=[("selected", "#1f3a5f")],
            foreground=[("selected", ACCENT)])
        style.configure("TScrollbar",
            background=SURFACE, troughcolor=CARD,
            arrowcolor=MUTED, borderwidth=0)

        self._show_welcome()

    # ────────────────────────────────────────────
    #  WELCOME
    # ────────────────────────────────────────────
    def _show_welcome(self):
        self.geometry("720x600")
        self._clear()

        frame = tk.Frame(self, bg=BG)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="OPERATING SYSTEMS  ·  LAB PROJECT",
            bg=BG, fg=ACCENT, font=("Consolas", 9, "bold")).pack(pady=(56, 0))

        tk.Label(frame, text="CPU Scheduler Simulator",
            bg=BG, fg="#ffffff", font=("Consolas", 26, "bold")).pack(pady=(8, 2))

        tk.Label(frame,
            text="First Come First Serve  ·  Dynamic Memory Allocation",
            bg=BG, fg=ACCENT, font=("Consolas", 11)).pack(pady=(0, 32))

        mcard = tk.Frame(frame, bg=CARD,
            highlightbackground=BORDER, highlightthickness=1,
            padx=56, pady=24)
        mcard.pack()

        tk.Label(mcard, text="— PROJECT MEMBERS —",
            bg=CARD, fg=MUTED,
            font=("Consolas", 8, "bold")).pack(pady=(0, 14))

        for pid, name in [
            ("P1", "Zabala, Kylle Luis L."),
            ("P2", "Rodrigo, Ahron Daniel A."),
            ("P3", "Resuelo, Hanna Gabrielle N."),
        ]:
            row = tk.Frame(mcard, bg=CARD)
            row.pack(anchor="w", pady=5)
            cv = tk.Canvas(row, width=12, height=12, bg=CARD, highlightthickness=0)
            cv.pack(side="left", padx=(0, 8))
            cv.create_oval(1, 1, 12, 12, fill=PROC_COLORS[pid], outline="")
            tk.Label(row, text=name, bg=CARD, fg=TEXT,
                font=("Consolas", 10)).pack(side="left")

        btn = tk.Button(frame,
            text="▶  LAUNCH SIMULATOR",
            bg=ACCENT, fg="#0d1117",
            font=("Consolas", 11, "bold"),
            relief="flat", padx=40, pady=14,
            cursor="hand2",
            command=self._show_simulator)
        btn.pack(pady=44)
        btn.bind("<Enter>", lambda e: btn.config(bg="#79b8ff"))
        btn.bind("<Leave>", lambda e: btn.config(bg=ACCENT))

    # ────────────────────────────────────────────
    #  SIMULATOR SCREEN
    # ────────────────────────────────────────────
    def _show_simulator(self):
        self.geometry("1200x820")
        self._clear()

        # ── Header ──────────────────────────────
        hdr = tk.Frame(self, bg=SURFACE,
            highlightbackground=BORDER, highlightthickness=1)
        hdr.pack(fill="x")

        tk.Label(hdr, text="CPU Scheduler Simulator",
            bg=SURFACE, fg="#fff",
            font=("Consolas", 14, "bold")).pack(side="left", padx=20, pady=12)
        tk.Label(hdr, text="FCFS  ·  Dynamic Memory Allocation",
            bg=SURFACE, fg=ACCENT,
            font=("Consolas", 9)).pack(side="left", pady=12)

        back = tk.Button(hdr, text="← Back",
            bg=SURFACE, fg=MUTED,
            font=("Consolas", 9), relief="flat",
            padx=14, pady=8, cursor="hand2",
            command=self._show_welcome)
        back.pack(side="right", padx=20, pady=10)
        back.bind("<Enter>", lambda e: back.config(fg=ACCENT))
        back.bind("<Leave>", lambda e: back.config(fg=MUTED))

        # ── Outer scrollable area ────────────────
        self._outer_canvas = tk.Canvas(self, bg=BG, highlightthickness=0)
        sb = ttk.Scrollbar(self, orient="vertical",
            command=self._outer_canvas.yview)
        self._outer_canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self._outer_canvas.pack(fill="both", expand=True)

        self._main_frame = tk.Frame(self._outer_canvas, bg=BG)
        self._outer_canvas.create_window((0, 0), window=self._main_frame, anchor="nw")
        self._main_frame.bind("<Configure>", lambda e:
            self._outer_canvas.configure(
                scrollregion=self._outer_canvas.bbox("all")))
        self._outer_canvas.bind_all("<MouseWheel>", lambda e:
            self._outer_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        # ── TOP ROW: Process Queue (left) | Memory Map (right) ──
        top_row = tk.Frame(self._main_frame, bg=BG)
        top_row.pack(fill="x", padx=24, pady=(20, 0))

        self._input_col = tk.Frame(top_row, bg=BG)
        self._input_col.pack(side="left", fill="both", expand=True, padx=(0, 16))

        self._mem_col = tk.Frame(top_row, bg=BG)
        self._mem_col.pack(side="left", fill="y", anchor="n")

        # ── BOTTOM: Gantt + Stats (full width) ──
        self._bottom_col = tk.Frame(self._main_frame, bg=BG)
        self._bottom_col.pack(fill="x", padx=24, pady=(16, 24))

        self._build_input_section()
        self._build_memory_panel()
        self._build_gantt_section()
        self._build_stats_section()

    # ────────────────────────────────────────────
    #  ① PROCESS QUEUE
    # ────────────────────────────────────────────
    def _build_input_section(self):
        card = tk.Frame(self._input_col, bg=CARD,
            highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill="x")

        sec_hdr = tk.Frame(card, bg=CARD)
        sec_hdr.pack(fill="x", padx=18, pady=(16, 8))
        tk.Label(sec_hdr, text="①", bg=CARD, fg=ACCENT,
            font=("Consolas", 10, "bold")).pack(side="left", padx=(0, 8))
        tk.Label(sec_hdr, text="PROCESS QUEUE",
            bg=CARD, fg=MUTED,
            font=("Consolas", 8, "bold")).pack(side="left")

        col_hdr = tk.Frame(card, bg=SURFACE)
        col_hdr.pack(fill="x", padx=14, pady=(0, 6))
        for txt, w in [("Process", 8), ("CPU Burst Time (msec)", 22), ("Arrival Time (msec)", 20)]:
            tk.Label(col_hdr, text=txt, bg=SURFACE, fg=MUTED,
                font=("Consolas", 9, "bold"),
                width=w, anchor="w").pack(side="left", padx=8, pady=9)

        self.entries = {}
        for pid in PROC_IDS:
            row = tk.Frame(card, bg=CARD)
            row.pack(fill="x", padx=14, pady=5)

            badge = tk.Frame(row, bg=CARD)
            badge.pack(side="left", padx=6)
            cv = tk.Canvas(badge, width=12, height=12,
                bg=CARD, highlightthickness=0)
            cv.pack(side="left", padx=(0, 6))
            cv.create_oval(1, 1, 12, 12, fill=PROC_COLORS[pid], outline="")
            tk.Label(badge, text=pid, bg=CARD, fg=PROC_COLORS[pid],
                font=("Consolas", 10, "bold"), width=3).pack(side="left")

            bv, av = tk.StringVar(), tk.StringVar()

            be = tk.Entry(row, textvariable=bv, bg=SURFACE, fg=TEXT,
                insertbackground=ACCENT, relief="flat",
                font=("Consolas", 10), width=14,
                highlightbackground=BORDER, highlightthickness=1)
            be.pack(side="left", padx=(10, 0), ipady=7)

            ae = tk.Entry(row, textvariable=av, bg=SURFACE, fg=TEXT,
                insertbackground=ACCENT, relief="flat",
                font=("Consolas", 10), width=14,
                highlightbackground=BORDER, highlightthickness=1)
            ae.pack(side="left", padx=(18, 0), ipady=7)

            el = tk.Label(row, text="", bg=CARD, fg=DANGER,
                font=("Consolas", 8))
            el.pack(side="left", padx=(10, 0))

            self.entries[pid] = dict(bv=bv, av=av, be=be, ae=ae, el=el)

        tk.Frame(card, bg=BORDER, height=1).pack(fill="x", padx=14, pady=12)

        btn_row = tk.Frame(card, bg=CARD)
        btn_row.pack(anchor="w", padx=18, pady=(0, 18))

        self._run_btn = tk.Button(btn_row,
            text="▶  Run FCFS",
            bg=ACCENT, fg="#0d1117",
            font=("Consolas", 10, "bold"),
            relief="flat", padx=22, pady=9,
            cursor="hand2",
            command=self._on_run)
        self._run_btn.pack(side="left", padx=(0, 12))
        self._run_btn.bind("<Enter>", lambda e: self._run_btn.config(bg="#79b8ff"))
        self._run_btn.bind("<Leave>", lambda e: self._run_btn.config(bg=ACCENT))

        rst = tk.Button(btn_row, text="↺  Reset",
            bg=CARD, fg=MUTED,
            font=("Consolas", 10), relief="flat",
            padx=18, pady=9, cursor="hand2",
            command=self._reset)
        rst.pack(side="left")
        rst.bind("<Enter>", lambda e: rst.config(fg=TEXT))
        rst.bind("<Leave>", lambda e: rst.config(fg=MUTED))

    # ────────────────────────────────────────────
    #  ② MEMORY MAP
    # ────────────────────────────────────────────
    def _build_memory_panel(self):
        card = tk.Frame(self._mem_col, bg=CARD,
            highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill="y")

        sec_hdr = tk.Frame(card, bg=CARD)
        sec_hdr.pack(fill="x", padx=18, pady=(16, 8))
        tk.Label(sec_hdr, text="②", bg=CARD, fg=ACCENT,
            font=("Consolas", 10, "bold")).pack(side="left", padx=(0, 8))
        tk.Label(sec_hdr, text="MEMORY MAP (MB)",
            bg=CARD, fg=MUTED,
            font=("Consolas", 8, "bold")).pack(side="left")

        self._mem_canvas = tk.Canvas(card,
            bg=SURFACE, width=210, height=MEM_H,
            highlightthickness=0)
        self._mem_canvas.pack(padx=14, pady=(0, 10))
        self._mem_canvas.after(50, self._draw_mem_idle)

        tk.Frame(card, bg=BORDER, height=1).pack(fill="x", padx=14, pady=(0, 10))

        self._mem_legend = tk.Frame(card, bg=CARD)
        self._mem_legend.pack(fill="x", padx=14, pady=(0, 16))

    def _draw_mem_idle(self):
        c = self._mem_canvas
        c.delete("all")
        w = c.winfo_width() or 210
        c.create_rectangle(0, 0, w, MEM_H, fill=SURFACE, outline="")
        c.create_text(w // 2, MEM_H // 2,
            text="Awaiting\nprocesses...",
            fill=MUTED, font=("Consolas", 9), justify="center")

    def _draw_memory(self, results):
        """Step ②: animate Memory Map segments top-to-bottom."""
        for w in self._mem_legend.winfo_children():
            w.destroy()

        per_proc = math.floor((TOTAL_MEM_MB - OS_MEM_MB) / len(results))
        free_mb  = TOTAL_MEM_MB - OS_MEM_MB - per_proc * len(results)

        segs = [{"label": "OS Kernel", "mb": OS_MEM_MB, "color": "#2d333b", "pid": False}]
        for p in results:
            segs.append({"label": p["id"], "mb": per_proc,
                         "color": PROC_COLORS[p["id"]], "pid": True})
        if free_mb > 0:
            segs.append({"label": "Free", "mb": free_mb, "color": "#1c2333", "pid": False})

        c = self._mem_canvas
        c.delete("all")
        h, w = MEM_H, (c.winfo_width() or 210)

        positions = []
        y = 0
        for seg in segs:
            seg_h = max(int((seg["mb"] / TOTAL_MEM_MB) * h), 22)
            positions.append((seg, y, seg_h))
            y += seg_h

        def draw_up_to(n):
            c.delete("all")
            for i, (seg, sy, sh) in enumerate(positions):
                if i >= n:
                    break
                c.create_rectangle(0, sy, w, sy + sh,
                    fill=seg["color"], outline="#0d1117", width=1)
                c.create_text(w // 2, sy + sh // 2,
                    text=f"{seg['label']}\n{seg['mb']} MB",
                    fill="#ffffff", font=("Consolas", 8, "bold"),
                    justify="center")
            for w2 in self._mem_legend.winfo_children():
                w2.destroy()
            for i, (seg, _, _) in enumerate(positions):
                if i >= n or not seg["pid"]:
                    continue
                row = tk.Frame(self._mem_legend, bg=CARD)
                row.pack(anchor="w", pady=2)
                cv2 = tk.Canvas(row, width=10, height=10,
                    bg=CARD, highlightthickness=0)
                cv2.pack(side="left", padx=(0, 5))
                cv2.create_rectangle(0, 0, 10, 10, fill=seg["color"], outline="")
                tk.Label(row, text=f"{seg['label']} — {seg['mb']} MB",
                    bg=CARD, fg=MUTED,
                    font=("Consolas", 8)).pack(side="left")

        def animate_mem(n=0):
            draw_up_to(n + 1)
            if n + 1 < len(positions):
                self.after(110, lambda: animate_mem(n + 1))
            elif self._mem_done_callback:
                self.after(200, self._mem_done_callback)

        animate_mem(0)

    # ────────────────────────────────────────────
    #  ③ GANTT CHART
    # ────────────────────────────────────────────
    def _build_gantt_section(self):
        card = tk.Frame(self._bottom_col, bg=CARD,
            highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill="x", pady=(0, 14))

        sec_hdr = tk.Frame(card, bg=CARD)
        sec_hdr.pack(fill="x", padx=18, pady=(16, 8))
        tk.Label(sec_hdr, text="③", bg=CARD, fg=ACCENT,
            font=("Consolas", 10, "bold")).pack(side="left", padx=(0, 8))
        tk.Label(sec_hdr, text="GANTT CHART",
            bg=CARD, fg=MUTED,
            font=("Consolas", 8, "bold")).pack(side="left")

        self._gantt_canvas = tk.Canvas(card,
            bg=SURFACE, height=68,
            highlightthickness=0)
        self._gantt_canvas.pack(fill="x", padx=18, pady=(0, 4))

        self._time_canvas = tk.Canvas(card,
            bg=CARD, height=26,
            highlightthickness=0)
        self._time_canvas.pack(fill="x", padx=18, pady=(0, 16))

        self._gantt_canvas.after(60, lambda:
            self._draw_placeholder(self._gantt_canvas, 68,
                "Run FCFS to see the Gantt chart"))

    # ────────────────────────────────────────────
    #  ④ PROCESS STATISTICS
    # ────────────────────────────────────────────
    def _build_stats_section(self):
        card = tk.Frame(self._bottom_col, bg=CARD,
            highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill="x")

        sec_hdr = tk.Frame(card, bg=CARD)
        sec_hdr.pack(fill="x", padx=18, pady=(16, 8))
        tk.Label(sec_hdr, text="④", bg=CARD, fg=ACCENT,
            font=("Consolas", 10, "bold")).pack(side="left", padx=(0, 8))
        tk.Label(sec_hdr, text="PROCESS STATISTICS  —  WT · CT · TAT",
            bg=CARD, fg=MUTED,
            font=("Consolas", 8, "bold")).pack(side="left")

        tree_wrap = tk.Frame(card, bg=CARD)
        tree_wrap.pack(fill="x", padx=18, pady=(0, 12))

        cols = ("Process", "Arrival (ms)", "Burst (ms)",
                "Completion (ms)", "Waiting (ms)", "Turnaround (ms)")
        self._tree = ttk.Treeview(tree_wrap, columns=cols,
            show="headings", height=5)
        for col, cw in zip(cols, [100, 120, 110, 140, 120, 145]):
            self._tree.heading(col, text=col)
            self._tree.column(col, width=cw, anchor="center")
        self._tree.pack(fill="x")

        for pid in PROC_IDS:
            self._tree.insert("", "end",
                values=(pid, "—", "—", "—", "—", "—"),
                tags=(pid.lower(),))
            self._tree.tag_configure(pid.lower(), foreground=PROC_COLORS[pid])

        tk.Frame(card, bg=BORDER, height=1).pack(fill="x", padx=18, pady=(4, 14))

        avg_row = tk.Frame(card, bg=CARD)
        avg_row.pack(fill="x", padx=18, pady=(0, 20))

        self._avg_labels = {}
        for key, label, color in [
            ("wt",  "Avg Waiting Time",    WARNING),
            ("tat", "Avg Turnaround Time", SUCCESS),
            ("ct",  "Avg Completion Time", ACCENT),
        ]:
            box = tk.Frame(avg_row, bg=SURFACE,
                highlightbackground=BORDER, highlightthickness=1,
                padx=18, pady=14)
            box.pack(side="left", expand=True, fill="x", padx=(0, 10))
            tk.Label(box, text=label.upper(),
                bg=SURFACE, fg=MUTED,
                font=("Consolas", 7, "bold")).pack(anchor="w")
            lbl = tk.Label(box, text="— ms",
                bg=SURFACE, fg=color,
                font=("Consolas", 16, "bold"))
            lbl.pack(anchor="w", pady=(6, 0))
            self._avg_labels[key] = lbl

    # ────────────────────────────────────────────
    #  VALIDATION
    # ────────────────────────────────────────────
    def _validate(self):
        inputs, has_error = [], False
        for pid in PROC_IDS:
            e = self.entries[pid]
            bs  = e["bv"].get().strip()
            as_ = e["av"].get().strip()
            e["be"].config(highlightbackground=BORDER)
            e["ae"].config(highlightbackground=BORDER)
            e["el"].config(text="")

            if bs == "" and as_ == "":
                continue

            err, b, a = "", None, None

            if bs == "":
                err = "Burst required"
                e["be"].config(highlightbackground=DANGER)
            else:
                try:
                    b = int(bs)
                    if b < 1: raise ValueError
                except ValueError:
                    err = "Burst ≥ 1"
                    e["be"].config(highlightbackground=DANGER)

            if as_ == "":
                err += ("  " if err else "") + "Arrival required"
                e["ae"].config(highlightbackground=DANGER)
            else:
                try:
                    a = int(as_)
                    if a < 0: raise ValueError
                except ValueError:
                    err += ("  " if err else "") + "Arrival ≥ 0"
                    e["ae"].config(highlightbackground=DANGER)

            if err:
                e["el"].config(text=err)
                has_error = True
            elif b is not None and a is not None:
                inputs.append({"id": pid, "burst": b, "arrival": a})

        return None if has_error else inputs

    # ────────────────────────────────────────────
    #  RESET
    # ────────────────────────────────────────────
    def _reset(self):
        for pid in PROC_IDS:
            e = self.entries[pid]
            e["bv"].set("")
            e["av"].set("")
            e["be"].config(highlightbackground=BORDER)
            e["ae"].config(highlightbackground=BORDER)
            e["el"].config(text="")

        self._gantt_canvas.delete("all")
        self._time_canvas.delete("all")
        self._draw_placeholder(self._gantt_canvas, 68, "Run FCFS to see the Gantt chart")

        for row in self._tree.get_children():
            self._tree.delete(row)
        for pid in PROC_IDS:
            self._tree.insert("", "end",
                values=(pid, "—", "—", "—", "—", "—"),
                tags=(pid.lower(),))
            self._tree.tag_configure(pid.lower(), foreground=PROC_COLORS[pid])

        for key in self._avg_labels:
            self._avg_labels[key].config(text="— ms")

        self._draw_mem_idle()
        for w in self._mem_legend.winfo_children():
            w.destroy()

        self._run_btn.config(state="normal", text="▶  Run FCFS", bg=ACCENT)

    # ────────────────────────────────────────────
    #  RUN — animation order:
    #  ① Process Queue flash
    #  ② Memory Map segments
    #  ③ Gantt Chart blocks
    #  ④ Process Statistics rows + averages
    # ────────────────────────────────────────────
    def _on_run(self):
        inputs = self._validate()
        if inputs is None:
            messagebox.showerror("Validation Error",
                "Please fix the highlighted fields.")
            return
        if not inputs:
            messagebox.showwarning("No Input",
                "Enter at least one process.")
            return

        self._results = run_fcfs(inputs)
        self._run_btn.config(state="disabled", text="⏳ Scheduling...", bg=MUTED)

        # ① Flash process queue, then kick off ②
        self._flash_input_rows(inputs,
            callback=self._start_memory_animation)

    def _start_memory_animation(self):
        """② Memory Map → then ③ Gantt"""
        self._mem_done_callback = self._start_gantt_animation
        self._draw_memory(self._results)

    def _start_gantt_animation(self):
        """③ Gantt Chart → then ④ Stats"""
        self._animate_gantt(self._results,
            callback=lambda: self._animate_stats(self._results, callback=None))

    # ────────────────────────────────────────────
    #  ANIMATION ①: Flash Process Queue rows
    # ────────────────────────────────────────────
    def _flash_input_rows(self, inputs, callback):
        pid_set = {p["id"] for p in inputs}
        pids = [p for p in PROC_IDS if p in pid_set]

        def flash(idx, on):
            if idx >= len(pids):
                self.after(200, callback)
                return
            pid = pids[idx]
            e = self.entries[pid]
            color = PROC_COLORS[pid] if on else BORDER
            e["be"].config(highlightbackground=color)
            e["ae"].config(highlightbackground=color)
            if on:
                self.after(180, lambda: flash(idx, False))
            else:
                self.after(60, lambda: flash(idx + 1, True))

        flash(0, True)

    # ────────────────────────────────────────────
    #  ANIMATION ③: Gantt Chart blocks
    # ────────────────────────────────────────────
    def _animate_gantt(self, results, callback):
        self._gantt_canvas.delete("all")
        self._time_canvas.delete("all")

        self._gantt_canvas.update_idletasks()
        bar_w = max(self._gantt_canvas.winfo_width(), 600)

        end_time   = results[-1]["ct"]
        first_time = results[0]["start"] if results[0]["start"] > 0 else 0
        total_span = max(end_time - first_time, 1)

        segments = []
        prev_end = first_time

        if results[0]["start"] > 0:
            segments.append({"kind": "idle",
                "w": max(int((results[0]["start"] / total_span) * bar_w), 10)})
            prev_end = results[0]["start"]

        for p in results:
            if p["start"] > prev_end:
                gap = p["start"] - prev_end
                segments.append({"kind": "idle",
                    "w": max(int((gap / total_span) * bar_w), 10)})
            blk_w = max(int((p["burst"] / total_span) * bar_w), 32)
            segments.append({"kind": "proc", "proc": p, "w": blk_w})
            prev_end = p["ct"]

        x = 0
        for seg in segments:
            seg["x"] = x
            x += seg["w"]

        def draw_segment(idx):
            if idx >= len(segments):
                self._draw_time_axis(results, total_span, first_time, bar_w)
                self._run_btn.config(state="normal", text="▶  Run FCFS", bg=ACCENT)
                if callback:
                    callback()
                return
            seg = segments[idx]
            sx, sw = seg["x"], seg["w"]
            if seg["kind"] == "idle":
                self._gantt_canvas.create_rectangle(
                    sx, 0, sx + sw, 68, fill="#2d333b", outline="#0d1117")
                self._gantt_canvas.create_text(
                    sx + sw // 2, 34, text="IDLE",
                    fill=MUTED, font=("Consolas", 8))
                self.after(80, lambda: draw_segment(idx + 1))
            else:
                p = seg["proc"]
                self._animate_block_grow(sx, sw, PROC_COLORS[p["id"]], p,
                    done_cb=lambda: self.after(60, lambda: draw_segment(idx + 1)))

        draw_segment(0)

    def _animate_block_grow(self, sx, sw, color, proc, done_cb, step=0):
        STEPS = 12
        current_w = int(sw * (step + 1) / STEPS)
        self._gantt_canvas.delete(f"grow_{sx}")
        self._gantt_canvas.create_rectangle(
            sx, 0, sx + current_w, 68,
            fill=color, outline="#0d1117", width=1,
            tags=f"grow_{sx}")
        if step + 1 >= STEPS:
            self._gantt_canvas.create_text(
                sx + sw // 2, 24, text=proc["id"],
                fill="#fff", font=("Consolas", 9, "bold"))
            self._gantt_canvas.create_text(
                sx + sw // 2, 46, text=f"{proc['burst']}ms",
                fill="white", font=("Consolas", 7))
            done_cb()
        else:
            self.after(18, lambda: self._animate_block_grow(
                sx, sw, color, proc, done_cb, step + 1))

    def _draw_time_axis(self, results, total_span, first_time, bar_w):
        ticks = set()
        for p in results:
            ticks.add(p["start"])
            ticks.add(p["ct"])
        if results[0]["start"] == 0:
            ticks.add(0)
        prev_px = -30
        for t in sorted(ticks):
            px = int((t - first_time) / total_span * bar_w)
            if px - prev_px > 18:
                self._time_canvas.create_line(px, 0, px, 6, fill=BORDER)
                self._time_canvas.create_text(px, 17,
                    text=str(t), fill=MUTED, font=("Consolas", 7))
                prev_px = px

    # ────────────────────────────────────────────
    #  ANIMATION ④: Stats table rows + averages
    # ────────────────────────────────────────────
    def _animate_stats(self, results, callback):
        for row in self._tree.get_children():
            self._tree.delete(row)

        scheduled_ids = {p["id"] for p in results}
        for pid in PROC_IDS:
            if pid not in scheduled_ids:
                self._tree.insert("", "end",
                    values=(pid, "—", "—", "—", "—", "—"),
                    tags=(pid.lower(),))
                self._tree.tag_configure(pid.lower(), foreground=PROC_COLORS[pid])

        def insert_row(idx):
            if idx >= len(results):
                self._animate_averages(results, callback)
                return
            p = results[idx]
            self._tree.insert("", "end",
                values=(p["id"], p["arrival"], p["burst"],
                        p["ct"], p["wt"], p["tat"]),
                tags=(p["id"].lower(),))
            self._tree.tag_configure(p["id"].lower(), foreground=PROC_COLORS[p["id"]])
            self.after(130, lambda: insert_row(idx + 1))

        insert_row(0)

    def _animate_averages(self, results, callback):
        n = len(results)
        target = {
            "wt":  round(sum(p["wt"]  for p in results) / n, 2),
            "tat": round(sum(p["tat"] for p in results) / n, 2),
            "ct":  round(sum(p["ct"]  for p in results) / n, 2),
        }
        STEPS = 20

        def tick(step):
            frac = (step + 1) / STEPS
            for key, lbl in self._avg_labels.items():
                lbl.config(text=f"{round(target[key] * frac, 2)} ms")
            if step + 1 < STEPS:
                self.after(30, lambda: tick(step + 1))
            else:
                for key, lbl in self._avg_labels.items():
                    lbl.config(text=f"{target[key]} ms")
                if callback:
                    self.after(200, callback)

        tick(0)

    # ────────────────────────────────────────────
    #  UTILS
    # ────────────────────────────────────────────
    def _draw_placeholder(self, canvas, height, text):
        canvas.delete("all")
        canvas.update_idletasks()
        w = max(canvas.winfo_width(), 400)
        canvas.create_rectangle(0, 0, w, height, fill=SURFACE, outline="")
        canvas.create_text(w // 2, height // 2,
            text=text, fill=MUTED,
            font=("Consolas", 9), justify="center")

    def _clear(self):
        for w in self.winfo_children():
            w.destroy()


# ── ENTRY POINT ────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = CPUSchedulerApp()
    app.mainloop()
