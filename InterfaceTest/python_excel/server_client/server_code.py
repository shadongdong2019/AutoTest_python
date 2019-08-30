import socketserver, os


class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        base_path = '/home/'
        conn = self.request
        print('connected...')
        while True:
            pre_data = conn.recv(102400).decode()
            # 获取请求方法，文件名，文件大小
            cmd, file_name, file_size = pre_data.split('|')
            # 已经接收文件的大小
            recv_size = 0
            # 上传文件路径拼接
            file_dir = os.path.join(base_path, file_name)
            f = open(file_dir, 'wb')
            Flag = True
            while Flag:
                # 未上传完毕
                if int(file_size) > recv_size:
                    data = conn.recv(102400)
                    recv_size += len(data)
                else:
                    recv_size = 0
                    Flag = False
                    continue
                # 写入文件
                f.write(data)
            print('upload successed')
            f.close()


instance = socketserver.ThreadingTCPServer(('39.107.66.190', 7777), MyServer)
instance.serve_forever()