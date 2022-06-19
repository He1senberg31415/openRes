import socket

udpip = "de1.localtonet.com"
udpport = 50708

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(b"test", (udpip, udpport))