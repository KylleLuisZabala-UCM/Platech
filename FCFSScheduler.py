class FCFSScheduler:
    """
    Pure First-Come-First-Serve scheduling algorithm.
    No UI dependencies — easy to unit test in isolation.
    """

    def schedule(self, processes: list[Process]) -> list[Process]:
        """
        Sort by arrival time (VALID_IDS index breaks ties),
        then compute start, ct, tat, wt for each process.
        Returns the same list sorted and mutated in place.
        """
        # Sort processes by arrival time.
        # If two processes arrive at the same time, the one with
        # the lower index in VALID_IDS goes first (e.g. P1 before P2).
        processes.sort(key=lambda p: (p.arrival, Process.VALID_IDS.index(p.pid)))

        t = 0  # t = current CPU clock time
        for p in processes:
            # If the CPU is idle (no process has arrived yet),
            # jump the clock forward to when this process arrives.
            if t < p.arrival:
                t = p.arrival

            p.start = t              # The moment this process starts executing
            p.ct    = t + p.burst    # Completion time: starts + full burst duration
            p.tat   = p.ct - p.arrival  # Turnaround time: total time from arrival to finish
            p.wt    = p.tat - p.burst   # Waiting time: time spent waiting, not executing
            t = p.ct  # Advance the clock to when this process finishes

        return processes