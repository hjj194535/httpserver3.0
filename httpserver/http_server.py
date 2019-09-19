#!/usr/bin/env python3
# -*-coding:utf-8-*-
'''
httpserver3.0
获取http请求
解析http请求
将请求发送给WebFrame
从WebFrame接收反馈的数据
将数据组织为responese格式发送给客户端
'''
from socket import *
from threading import Thread
import sys
sys.path.append('/home/tarena/aid1907/month02/day18/httpserver3.0')
from httpserver.config import *
import json
import re

#和frame进行交互
def connect_frame(env):
    s = socket()
    try:
        #链接webframe
        s.connect((frame_ip,frame_port))
    except:
        return
    data = json.dumps(env)#转化为json格式
    s.send(data.encode())#发送请求
    res = s.recv(1024*1024*10).decode()
    return json.loads(res)#{'status':200,'data':'c'}



class HTTPServer:
    def __init__(self):
        self.addr = (host,port)
        #创建套接字
        self.create_socket()
        self.bind()

    # 创建套接字
    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,DEBUG)
    #绑定地址
    def bind(self):
        self.sockfd.bind(self.addr)

    #启动服务
    def server_forever(self):
        self.sockfd.listen(5)
        print("Listen port %d"%port)
        while True:
            try:
                connfd,addr = self.sockfd.accept()
            except KeyboardInterrupt:
                connfd.close()
                self.sockfd.close()
                sys.exit('服务器退出')
            except Exception as e:
                print(e)
                continue
            client = Thread(target=self.handle,args=(connfd,))
            client.setDaemon(True)
            client.start()

    #具体处理客户端请求
    def handle(self,connfd):
        request = connfd.recv(4096).decode()
        print(request)
        pattern = r'(?P<method>[A-Z]+)\s+(?P<info>/\S*)'
        try:
            env = re.match(pattern,request).groupdict()
        except:
            connfd.close()
            return
        else:
            #和frame进行交互
            res = connect_frame(env)
            if res:
                self.send_response(connfd,res)

    def send_response(self,c,res):
        if res['status'] == '200':
            data = "HTTP/1.1 200 OK\r\n"
            data += "Content-Type:text/html\r\n"
            data += '\r\n'
            data += res['data']
        elif res['status'] == '404':
            data = "HTTP/1.1 404 Not Found\r\n"
            data += "Content-Type:text/html\r\n"
            data += '\r\n'
            data += res['data']
        elif res['status'] == '500':
            data = "HTTP/1.1 500 Server Error\r\n"
            data += "Content-Type:text/html\r\n"
            data += '\r\n'
        c.send(data.encode())

if __name__ == '__main__':
    http = HTTPServer()
    http.server_forever()#启动服务


