import socket, threading
s = socket.socket(); s.settimeout(3.0); s.bind(('127.0.0.1', 0)); s.listen(1); p = s.getsockname()[1]
def srv():
    try:
        c, _ = s.accept(); _ = c.recv(8); c.sendall(b'PONG'); c.close()
    finally:
        s.close()
t = threading.Thread(target=srv, daemon=True); t.start()
cl = socket.create_connection(('127.0.0.1', p), timeout=3.0); cl.sendall(b'PING'); msg = cl.recv(8).decode(); cl.close(); t.join(timeout=3.0)
print(f'tcp_echo={msg}')
print(f'syn_ack_ack={100 + 1}')
print(f'final_ack={500 + 1}')
