# -*- coding: utf-8 -*-

import socket
import time
from utils import recvMessage, sendMessage


def init():
    global client

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    client.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 60 * 1000, 30 * 1000))
    client.connect(('127.0.0.1', 8888))


def main():
    while True:
        try:
            header = {}
            msg = 'hello,'

            print('send: ' + msg)
            content = {'msg': msg}
            sendMessage(client, header, content)

            header, body = recvMessage(client)
            print('recv: ' + body['msg'])

            time.sleep(10)

        except:
            client.close()
            break


if __name__ == '__main__':
    init()
    main()
