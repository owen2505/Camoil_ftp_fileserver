# 此代码示例tcp套接字实现ftp文件服务器的客户端
from socket import *
import os, sys
import signal
import time

file_path = "./ftpserver/"


# 新式类
class FtpServer(object):
    def __init__(self, sock):
        self.sock = sock

    def do_list(self):
        file_list = os.listdir(file_path)
        # os.listdir()方法用于返回指定的文件夹包含的文件或文件夹的名字的列表
        # 它不包括 '.' 和'..' 即使它在文件夹中
        # 只支持在 Unix, Windows下使用
        if not file_list:
            self.sock.send("文件库为空".encode())
        self.sock.send(b"ok")
        time.sleep(0.1)  # 延迟防止沾包
        files = ""
        for file in file_list:
            # 判断非隐藏文件和普通文件
            if file[0] != "." and os.path.isfile(file_path + file):
                files = files + file + ","
        # 将拼接好的文件名字符串发送给客户端
        self.sock.send(files.encode())

    def do_get(self, filename):
        try:
            f = open(file_path + filename, "rb")
        except IOError:
            self.sock.send("该文件不存在".encode())
            return
        else:
            self.sock.send(b"ok")
            time.sleep(0.1)  # 延迟防止沾包
        while True:
            data = f.read(1024)
            if not data:
                time.sleep(0.1)
                self.sock.send(b"#")
                break
            self.sock.send(data)
        f.close()
        print("文件发送完成")

    def do_put(self, filename):
        self.sock.send(b"ok")
        f = open(file_path + filename, "wb")
        while True:
            data = self.sock.recv(1024)
            if data == b"#":
                break
            f.write(data)
        f.close()
        print("文件接收完成")


# 将客户端请求处理封装成函数，扔到子进程中去执行
def client_handle(sock):
    ftp = FtpServer(sock)
    while True:
        data = sock.recv(1024).decode()
        if not data or data == "q":
            sock.close()
            return
        elif data == "1":
            ftp.do_list()
        elif data[0] == "2":
            filename = data.split(" ")[-1]
            print("被下载的文件：", filename)
            ftp.do_get(filename)
        elif data[0] == "3":
            filename = data.split(" ")[-1]
            print("被上传的文件：", filename)
            ftp.do_put(filename)


def main():
    # 创建监听套接字
    server_addr = ("0.0.0.0", 8888)
    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # 设置端口可立即重用
    sockfd.bind(server_addr)
    sockfd.listen(5)

    # 处理僵尸进程
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    print("等待客户端连接...")
    # 循环等待客户端链接
    while True:
        try:
            sockconn, addr = sockfd.accept()
        except KeyboardInterrupt:
            sockfd.close()
            sys.exit("服务器退出！")
        except Exception as e:
            print("Error:", e)
            continue
        print("已连接的客户端：", addr)
        # 创建子进程处理客户端请求
        pid = os.fork()
        if pid == 0:
            sockfd.close()  # 在子进程中用不到流式套接字，将其关闭
            client_handle(sockconn)  # 处理客户端请求
            print("客户端：", addr, "退出")
            os._exit(0)  # 客户端退出后要结束对应的进程
        # 无论父进程创建进程成功或者失败都是循环接收客户端请求
        else:
            sockconn.close()  # 在父进程中用不到连接套接字，将其关闭


if __name__ == '__main__':
    main()
