class Process:
    """Represents a single process with its scheduling attributes."""

    VALID_IDS = ["P1", "P2", "P3", "P4", "P5"]  # Only these process IDs are accepted

    def __init__(self, pid: str, burst: int, arrival: int):
        # Validate all inputs before creating the process —
        # reject invalid IDs, non-positive burst times, or negative arrival times.
        if pid not in self.VALID_IDS:
            raise ValueError(f"Invalid process ID: {pid}")
        if burst < 1:
            raise ValueError("Burst time must be >= 1")
        if arrival < 0:
            raise ValueError("Arrival time must be >= 0")

        self.pid     = pid      # Process identifier (e.g. "P1")
        self.burst   = burst    # How long the process needs the CPU (ms)
        self.arrival = arrival  # When the process enters the ready queue (ms)

        # These fields start at 0 and are filled in by the scheduler after running
        self.start   = 0   # The moment the process actually starts executing
        self.ct      = 0   # Completion time: when the process finishes
        self.tat     = 0   # Turnaround time: ct - arrival (arrival to finish)
        self.wt      = 0   # Waiting time: tat - burst (time spent waiting, not running)

    def to_dict(self) -> dict:
        # Converts the process and all its computed values into a plain dict.
        # Useful for passing data between layers without exposing the object directly.
        return {
            "id":      self.pid,
            "burst":   self.burst,
            "arrival": self.arrival,
            "start":   self.start,
            "ct":      self.ct,
            "tat":     self.tat,
            "wt":      self.wt,
        }