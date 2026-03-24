
import threading


class BackendPool:

    def __init__(self, backends):
        self.backends = backends
        self.index = 0
        self.lock = threading.Lock()

    def pick_backend(self):
        with self.lock:
            backend = self.backends[self.index % len(self.backends)]
            self.index += 1
        return backend