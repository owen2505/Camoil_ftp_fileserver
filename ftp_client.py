# 此代码示例tcp套接字实现ftp文件服务器的客户端
from socket import *
import os, sys
import time


class FtpClient(object):
    def __init__(self, sock):
        self.sock = sock

    def do_list(self):  # 查看文件列表
        self.sock.send(b"1")
        data = self.sock.recv(128).decode()
        if data == "ok":
            data = self.sock.recv(4096).decode()
            files = data.split(",")
            for file in files:
                print(file)
        else:
            print(data)

    def do_get(self):  # 下载文件
        filename = input("请输入文件名>>")
        self.sock.send(("2 " + filename.strip()).encode())
        data = self.sock.recv(128).decode()
        if data == "ok":  # 说明文件存在，准备循环接收文件并写入本地文件
            f = open("./target/" + filename, "wb")
            while True:
                data = self.sock.recv(1024)
                if data == b"#":
                    break
                f.write(data)
            f.close()
            print("文件下载完成")
        else:
            print(data)

    def do_put(self):  # 上传文件
        filename = input("请输入文件名>>")
        try:
            f = open(filename, "rb")
        except IOError:
            print("该文件不存在")
            return
        else:
            self.sock.send(("3 " + filename.strip()).encode())
        data = self.sock.recv(128).decode()
        if data == "ok":  # 说明服务端已就绪，准备循环读取本地文件并发送出去
            while True:
                data = f.read(1024)
                if not data:
                    time.sleep(0.1)
                    self.sock.send(b"#")
                    break
                self.sock.send(data)
        f.close()
        print("文件上传完成")

    def do_quit(self):  # 退出客户端
        self.sock.send(b"q")
        self.sock.close()
        os._exit(0)


def menu():
    print("输入下列命令进行网盘操作")
    print("+-------------------+")
    print("1 >> 查看文件列表")
    print("+-------------------+")
    print("2 >> 下载文件")
    print("+-------------------+")
    print("3 >> 上传文件")
    print("+-------------------+")
    print("q >> 退出网盘")
    print("+-------------------+")


def main():
    server_addr = ("192.168.0.61", 8888)
    sockfd = socket()
    try:
        sockfd.connect(server_addr)
    except Exception as e:
        print("连接服务器失败：", e)
        return
    ftp = FtpClient(sockfd)
    while True:
        menu()
        input_value = input("请输入>>")
        if input_value == "1":
            ftp.do_list()
        elif input_value == "2":
            ftp.do_get()
        elif input_value == "3":
            ftp.do_put()
        elif input_value == "q":
            ftp.do_quit()
        else:
            print("命令输入错误")


if __name__ == '__main__':
    main()
