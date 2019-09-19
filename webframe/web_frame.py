#!/usr/bin/env python3
# -*-coding:utf-8-*-
'''
模拟网站的后端行为
1.从httpserver 接收具体请求
根据请求进行逻辑处理和数据处理
将数据反馈给httpserver
'''
import os
from socket import *
import json
import sys
sys.path.append('/home/tarena/aid1907/month02/day18/httpserver3.0')
from webframe.settings import *

from multiprocessing import Process

class Applicaion:
    def __init__(self):
        self.host = host
        self.port = port
        self.addr = (host,port)
        self.create_socket()
        self.bind()

    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,DEBUG)
    def bind(self):
        self.sockfd.bind(self.addr)

    def send_html(self,info,connfd):
        filepath = STATIC_DIR + info
        if not os.path.exists(filepath):
            filepath = STATIC_DIR + '/404.html'
        with open(filepath) as f:
            try:
                msg = json.dumps({'status': '200', 'data': f.read()})
            except:
                connfd.close()
            else:
                connfd.send(msg.encode())


    def handle(self,connfd):
        request = connfd.recv(1024*1024*10).decode()
        data = json.loads(request)
        info = data['info']
        if info == '/' or info[-5:] == '.html':
            if info == '/':
                info = '/index.html'
            self.send_html(info, connfd)



    def start(self):
        self.sockfd.listen(5)
        print('Listen port ',self.port)
        while True:
            connfd,addr = self.sockfd.accept()
            print('Connect from ',addr)
            client = Process(target=self.handle,args=(connfd,))
            client.daemon = True
            client.start()



if __name__ == '__main__':
    app = Applicaion()
    app.start()