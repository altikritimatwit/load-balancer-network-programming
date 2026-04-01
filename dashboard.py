import os
import threading
import time

class Dashboard:

    def __init__(self, backend_pool):
        self.backend_pool = backend_pool

    def run(self):
        while True:

            # Clears terminal so it appears live-updating
            os.system('cls' if os.name == 'nt' else 'clear')

            print("------------------   Load Balancer Dashboard ------------------")

            # Under the lock, we grab all the shared data to display on the dashboard
            with self.backend_pool.lock:
                all_backends = list(self.backend_pool.backends)
                healthy_backends = list(self.backend_pool.healthy_backends)
                counts = {b: self.backend_pool.connection_count[b] for b in all_backends}
            
            # Loop through both healthy and unhealthy backends, and print out their status and connection count
            for b in all_backends:
                status = "healthy" if b in healthy_backends else "unhealthy"
                print(f"backend {b} is {status}     |   connections: {counts[b]}")

            print(f"Healthy backends: {healthy_backends}")
            print("----------------------------------------------------------------\n\n")

            time.sleep(2) # Refresh every 2 seconds

    def start(self):
        threading.Thread(target=self.run, daemon=True).start()