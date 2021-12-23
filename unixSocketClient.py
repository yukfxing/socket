# -*- coding: utf-8 -*-

import socket
import time
from utils import recvMessage, sendMessage

UNIX_SOCKET_PATH = './unix.sock'


def init():
    global client

    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect(UNIX_SOCKET_PATH)


def main():
    while True:
        try:
            header = {}
            msg = 'hello,'

            print('send: ' + msg)
            body = {'msg': msg}
            sendMessage(client, header, body)

            header, recvData = recvMessage(client)
            print('recv: ' + recvData['msg'])

            time.sleep(10)

        except:
            client.close()
            break


if __name__ == '__main__':
    init()
    main()
