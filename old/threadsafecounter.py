import threading


class ThreadSafeCounter:
    """
    Creates a thread safe counter
    """
    def __init__(self, start_value=0):
        self.value = start_value
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.value += 1

    def decrement(self):
        with self.lock:
            self.value -= 1

    def get_value(self):
        with self.lock:
            return self.value