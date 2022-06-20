import socket
import sys
import threading
from urllib.request import urlopen
import json

rendezvous = ('de1.localtonet.com', 54078)

# connect to rendezvous
print('connecting to rendezvous server')

res = json.loads(urlopen('https://api.ipify.org?format=json'))

print(f"Your ip: {res['ip']}")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((res["ip"], 50001))
sock.sendto(b'0', rendezvous)

while True:
    data = sock.recv(1024).decode()

    if data.strip() == 'ready':
        print('checked in with server, waiting')
        break

data = sock.recv(1024).decode()
ip, sport, dport = data.split(' ')
sport = int(sport)
dport = int(dport)

print('\ngot peer')
print('  ip:          {}'.format(ip))
print('  source port: {}'.format(sport))
print('  dest port:   {}\n'.format(dport))

# punch hole
# equiv: echo 'punch hole' | nc -u -p 50001 x.x.x.x 50002
print('punching hole')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', sport))
sock.sendto(b'0', (ip, dport))

print('ready to exchange messages\n')

sock = None

def listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', sport))
    print(str(sock))

    while True:
        data = sock.recv(1024)
        print('\rpeer: {}\n> '.format(data.decode()), end='')

listener = threading.Thread(target=listen, daemon=True);
listener.start()

# # send messages
# # equiv: echo 'xxx' | nc -u -p 50002 x.x.x.x 50001
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', dport))
print(f"sock2: {str(sock)}")

while True:
    msg = input('> ')
    sock.sendto(msg.encode(), (ip, sport))