# coding = utf-8
# chat_client.py
"""
Chatroom
env: python3.6
exc: socket and fork
"""
from socket import *
import os, sys
import signal


def local_server():
    sock_file = "./sock"
    if os.path.exists(sock_file):
        os.remove(sock_file)
    sockfd = socket(AF_UNIX, SOCK_STREAM)
    sockfd.bind(sock_file)
    sockfd.listen(2)
    c, addr = sockfd.accept()


# 发送消息
def send_msg(sockfd, name, server_addr):
    while True:
        try:
            text = input("请输入>>")
        except KeyboardInterrupt:
            text = "quit"
        if text.strip() == "quit":
            # 发送退出信号给服务器
            sockfd.sendto(("Q " + name).encode(), server_addr)
            print("子进程退出")
            os._exit(0)  # 退出子进程
        msg = "C %s %s" % (name, text)
        sockfd.sendto(msg.encode(), server_addr)


# 接收消息
def recv_msg(sockfd):
    while True:
        data, addr = sockfd.recvfrom(2048)
        # 如果服务器发来退出消息，父进程退出
        if data.decode() == "EXIT":
            os._exit(0)
        print(data.decode() + "\n请输入>>", end="")


def main():
    server_addr = ("192.168.0.61", 8888)
    sockfd = socket(AF_INET, SOCK_DGRAM)
    while True:
        name = input("请输入群昵称>>")
        msg = "L " + name
        sockfd.sendto(msg.encode(), server_addr)
        data, addr = sockfd.recvfrom(1024)
        if data.decode() == "OK":
            print("您已进入群聊")
            break
        else:
            print(data.decode())
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)  # 忽略子进程退出，系统自动回收子进程
    pid = os.fork()  # 创建子进程用于发送消息
    if pid < 0:
        sys.exit("Error")
    elif pid == 0:  # 子进程
        print("子进程开始执行")
        send_msg(sockfd, name, server_addr)
    else:  # 父进程
        print("父进程开始执行")
        recv_msg(sockfd)


if __name__ == '__main__':
    main()
