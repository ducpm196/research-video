import socket, sys, threading
kv = dict(t.split('=') for t in sys.stdin.read().split())
msg_b, rep_b = kv['msg'].encode(), kv['reply'].encode()
syn_s, srv_s = int(kv['syn_seq']), int(kv['srv_seq'])
s = socket.socket(); s.settimeout(3.0); s.bind(('127.0.0.1', 0)); s.listen(1); p = s.getsockname()[1]
def srv():
    try:
        c, _ = s.accept(); _ = c.recv(64); c.sendall(rep_b); c.close()
    finally: s.close()
t = threading.Thread(target=srv, daemon=True); t.start()
cl = socket.create_connection(('127.0.0.1', p), timeout=3.0)
cl.sendall(msg_b); got = cl.recv(64).decode(); cl.close(); t.join(timeout=3.0)
print(f'tcp_echo={got}')
print(f'syn_ack_ack={syn_s + 1}')
print(f'final_ack={srv_s + 1}')
