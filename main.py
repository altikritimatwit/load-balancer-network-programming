import backends
import proxy 
import config
import socket
import threading

def main():

    cfg = config.load_config()
    bp = backends.BackendPool(cfg["backends"])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind(("", cfg["listen_port"]))
    s.listen()

    while True:
        cs, addr = s.accept()

        backend = bp.pick_backend()

        handler_thread = threading.Thread(target=proxy.handle_connections, args=(cs, backend))
        handler_thread.start()

if __name__ == "__main__":
    main()