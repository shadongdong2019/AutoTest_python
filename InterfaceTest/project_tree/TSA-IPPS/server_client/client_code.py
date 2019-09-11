#!/usr/bin/env python
#_*_ encoding=utf-8 _*_


import socket,sys,os

ip_port = ('39.107.66.190',7777)
sk = socket.socket()
sk.connect(ip_port)

container = {'key':'','data':''}
while True:
    input_data = input('path:')
    print(input_data)
    cmd,path = input_data.split('|')  #/home/ma|/home/ma/hd.txt
    file_name = os.path.basename(path)
    print(file_name)
    file_size = os.stat(path).st_size
    print(file_size)
    print(cmd)
    print()
    sk.send((cmd+"|"+file_name+"|"+str(file_size)).encode())
    send_size = 0
    f = open(path,'rb')
    Flag = True
    while Flag:
        if send_size + 1024 > file_size:
            data = f.read(file_size - send_size)
            Flag = False
        else:
            data = f.read(1024)
            send_size += 1024
        sk.send(data)
    f.close()
sk.close()