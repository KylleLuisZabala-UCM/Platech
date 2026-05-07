class CPUSchedulerApp(tk.Tk):
    """
    The main window of the app.
    Acts like a TV — it doesn't display content itself,
    it just switches which screen is currently showing.
    """

    def __init__(self):
        # Start everything up: set title, background color,
        # minimum size, apply dark theme, and show the welcome screen first.
        super().__init__()
        self.title("CPU Scheduler Simulator — FCFS")
        self.configure(bg=AppTheme.BG)
        self.resizable(True, True)
        self.minsize(1000, 680)

        AppTheme.apply_ttk_style(ttk.Style(self))
        self._current_screen = None  # Tracks whichever screen is currently visible
        self.show_welcome()

    def _replace_screen(self, screen: tk.Frame, geometry: str):
        # The "channel switcher" — destroys the old screen,
        # resizes the window, then displays the new screen.
        # Only one screen is visible at a time.
        if self._current_screen:
            self._current_screen.destroy()
        self.geometry(geometry)
        screen.pack(fill="both", expand=True)
        self._current_screen = screen

    def show_welcome(self):
        # Switch to the Welcome Screen.
        # Passes show_simulator as a callback so the screen
        # can trigger navigation when the user clicks "Launch."
        self._replace_screen(
            WelcomeScreen(self, on_launch=self.show_simulator),
            "720x600")

    def show_simulator(self):
        # Switch to the Simulator Screen.
        # Passes show_welcome as a callback so the screen
        # can navigate back when the user clicks "Back."
        self._replace_screen(
            SimulatorScreen(self, on_back=self.show_welcome),
            "1200x820")


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Create the app window and start the Tkinter event loop.
    # The event loop keeps the window open and listens for user interactions.
    app = CPUSchedulerApp()
    app.mainloop()