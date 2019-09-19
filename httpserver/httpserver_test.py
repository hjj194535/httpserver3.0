from socket import *

s = socket()
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(('0.0.0.0',8080))
s.listen(3)

c,addr = s.accept()
data = c.recv(1024).decode()
print(data)
c.send("{'status:'200','data':'ccc'}".encode())