import socket
import threading
import time

class HealthChecker:
    def __init__(self, backend_pool, interval=5, timeout=2):
        self.backend_pool = backend_pool
        self.interval = interval
        self.timeout = timeout
        self.running = True

    def check_backend(self, backend):
        host, port = backend.split(":")
        try:
            with socket.create_connection((host, int(port)), timeout=self.timeout):
                return True
        except OSError:
            return False

    def run(self):
        while self.running:
            with self.backend_pool.lock:
                # making a copy of the backends so that our client threads can still access the origninal lock
                all_backends = list(self.backend_pool.backends)
        
            healthy = [b for b in all_backends if self.check_backend(b)]

            with self.backend_pool.lock:
                self.backend_pool.healthy_backends = healthy

            print("Healthy backends:", healthy)
            time.sleep(self.interval)

    def start(self):
        threading.Thread(target=self.run, daemon=True).start()