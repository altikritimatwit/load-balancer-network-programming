
import threading

class BackendPool:

    def __init__(self, backends):
        self.backends = backends
        self.healthy_backends = list(backends)
        self.index = 0
        self.lock = threading.Lock()

    def pick_backend(self):
        with self.lock:
            backend = self.healthy_backends[self.index % len(self.healthy_backends)]
            self.index += 1
        return backend