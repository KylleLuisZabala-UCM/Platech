class MemoryManager:
    """
    Dynamic memory allocation model.
    Divides available RAM equally among scheduled processes.
    """

    TOTAL_MB = 64  # Total simulated RAM in megabytes
    OS_MB    = 8   # Memory reserved for the OS Kernel (always allocated first)

    def allocate(self, processes: list[Process]) -> list[dict]:
        """
        Returns a list of memory segment dicts:
            { label, mb, color, is_process }
        Always starts with the OS segment and ends with a
        Free segment if there is leftover memory.
        """
        # Calculate how much RAM is available after the OS takes its share
        available = self.TOTAL_MB - self.OS_MB

        # Split the available memory equally among all scheduled processes
        per_proc  = math.floor(available / len(processes))

        # Any leftover MB that couldn't be split evenly becomes "Free" memory
        free_mb   = available - per_proc * len(processes)

        # Always start with the OS Kernel segment at the top
        segments = [{"label": "OS Kernel", "mb": self.OS_MB,
                     "color": "#2d333b", "is_process": False}]

        # Add one segment per process, each with its assigned color
        for p in processes:
            segments.append({
                "label":      p.pid,
                "mb":         per_proc,
                "color":      AppTheme.PROC_COLORS[p.pid],
                "is_process": True,
            })

        # If there's any leftover memory, add a Free segment at the bottom
        if free_mb > 0:
            segments.append({"label": "Free", "mb": free_mb,
                              "color": "#1c2333", "is_process": False})
        return segments