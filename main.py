import backends
import proxy 
import config
import socket
import threading
from dashboard import Dashboard
from health import HealthChecker 

def main():

    # Load config, and pass in the "backends" list to the BackendPool 
    cfg = config.load_config()
    bp = backends.BackendPool(cfg["backends"]) # Tracks all backends, and connection counts
    
    # Start the health checker thread
    hc = HealthChecker(bp)
    hc.start()
    
    # Start the dashboard thread in the background
    # Will refresh every 2 seconds
    dashboard = Dashboard(bp)
    dashboard.start()

    # Listening TCP socekt on port 8080
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", cfg["listen_port"]))
    s.listen()

    while True:
        cs, addr = s.accept()

        backend = bp.pick_backend()

        # Spawn a new thread per client
        # proxy.handle_connections is what forwards bytes between client and server
        host, port = backend.split(":")
        handler_thread = threading.Thread(target=proxy.handle_connections, args=(cs, (host, int(port)), bp))
        handler_thread.start()

if __name__ == "__main__":
    main()