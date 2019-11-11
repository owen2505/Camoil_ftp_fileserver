# coding = utf-8
# chat_server.py
"""
Chatroom
env: python3.6
exc: socket and fork
"""
from socket import *
import os, sys
import signal

user = {}


# 处理登录
def do_login(sockfd, name, addr):
    if name in user:
        sockfd.sendto("该昵称已存在！".encode(), addr)
        print("该昵称已存在！")
        return
    sockfd.sendto(b"OK", addr)

    # 通知其他客户端
    msg = "\n%s加入群聊" % name
    for i in user:
        sockfd.sendto(msg.encode(), user[i])
    # 将用户加入user字典
    user[name] = addr


def do_chat(sockfd, name, text):
    msg = "\n%s: %s" % (name, text)
    for i in user:
        if i != name:
            sockfd.sendto(msg.encode(), user[i])


def do_quit(sockfd, name):
    msg = "\n%s退出群聊" % name
    for i in user:
        if i != name:
            sockfd.sendto(msg.encode(), user[i])
        else:
            sockfd.sendto(b"EXIT", user[i])
    del user[name]


def do_requests(sockfd):
    while True:
        data, addr = sockfd.recvfrom(1024)
        msglist = data.decode().split(" ")
        if msglist[0] == "L":
            do_login(sockfd, msglist[1], addr)
        elif msglist[0] == "C":
            # 重新组织消息内容
            text = " ".join(msglist[2:])
            do_chat(sockfd, msglist[1], text)
        elif msglist[0] == "Q":
            do_quit(sockfd, msglist[1])


# 创建网络连接
def main():
    # 创建套接字
    server_addr = ("0.0.0.0", 8888)
    sockfd = socket(AF_INET, SOCK_DGRAM)
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockfd.bind(server_addr)  # 绑定地址
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)  # 忽略子进程退出，系统自动回收子进程
    # 创建一个独立进程用于发送管理员消息
    pid = os.fork()
    if pid < 0:
        print("Error!!!")
    elif pid == 0:
        while True:
            msg = input("管理员消息：")
            msg = "C 管理员消息 " + msg
            sockfd.sendto(msg.encode(), server_addr)
    else:
        # 处理各种客户端请求
        do_requests(sockfd)


if __name__ == "__main__":
    main()
