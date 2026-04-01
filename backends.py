
import threading

class BackendPool:

    def __init__(self, backends):
        self.backends = backends    # List of backends in the form of "host:port"
        self.healthy_backends = list(backends)  # Updated by health checker
        self.index = 0  # For round-robin
        self.lock = threading.Lock()    # Protects shared resources (healthy_backends, index, connection_count)
        self.connection_count = {b: 0 for b in backends}    # Num. of active connections per backend

    def pick_backend(self):
        with self.lock:
            # Round-robin: wrapping mechanism 
            backend = self.healthy_backends[self.index % len(self.healthy_backends)]
            self.index += 1
            # Increment connection count for whichever backend was chosen
            self.connection_count[backend] += 1
        return backend