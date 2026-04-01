import socket
import threading
import time

class HealthChecker:
    def __init__(self, backend_pool, interval=5, timeout=2):
        self.backend_pool = backend_pool
        self.interval = interval    # How often to check backends
        self.timeout = timeout  # How long to wait before declaring a backend unhealthy

    def check_backend(self, backend):
        host, port = backend.split(":")
        # Checks by attempting to open a TCP connection to the backend
        try:
            with socket.create_connection((host, int(port)), timeout=self.timeout):
                return True
        except OSError:
            return False

    def run(self):
        while True:
            with self.backend_pool.lock:
                # Making a copy of the backends so that our client threads can still access the origninal lock
                # Creating the connection in check_backend() can be slow, so rather than doing all that under the lock,
                # we make a copy instead.
                all_backends = list(self.backend_pool.backends)
        
            # Creating list of healthy backends by checking each one
            # Done outside the lock so it doesn't block client threads
            healthy = [b for b in all_backends if self.check_backend(b)]

            # Write back results under the lock
            with self.backend_pool.lock:
                self.backend_pool.healthy_backends = healthy

            time.sleep(self.interval)

    def start(self):
        # Daemon thread means it automatically exits when main.py exits (CTRL+C)
        threading.Thread(target=self.run, daemon=True).start()