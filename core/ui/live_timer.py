from rich.panel import Panel
from rich.live import Live
import threading
import time


class LiveTimer:
    def __init__(self, console, message="⏳ Ejecutando modelo..."):
        self.console = console
        self.message = message
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self._run, daemon=True)

    def _run(self):
        start_time = time.time()
        self.console.print("\n")
        with Live(
            Panel(f"{self.message} 0s", style="#FFA500"),
            refresh_per_second=1
        ) as live:
            while not self.stop_event.is_set():
                elapsed = int(time.time() - start_time)
                live.update(
                    Panel(f"{self.message} {elapsed}s", style="#FFA500")
                )
                time.sleep(1)

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_event.set()
        self.thread.join()
