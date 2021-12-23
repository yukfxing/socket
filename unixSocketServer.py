# -*- coding: utf-8 -*-

import os
import socket
import time
import threading
from utils import recvMessage, sendMessage, timestamp2Date

UNIX_SOCKET_PATH = './unix.sock'


def init():
    global server

    if os.path.exists(UNIX_SOCKET_PATH):
        os.remove(UNIX_SOCKET_PATH)

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(UNIX_SOCKET_PATH)
    server.listen(10)


def dealDetailMsg(header, msg):
    timestamp = header['timestamp']
    message = msg['msg']

    if time.time() - timestamp > 60 * 60:
        res = {
            'ret': 'Error',
            'errorMsg': 'message timeout'
        }
    else:
        res = {
            'ret': 'OK',
            'msg':  message + ' recv ok'
        }

    return res


def dealMsg(con):
    print('client connect.')

    while True:
        header, body = recvMessage(con)
        if not body:
            con.close()
            print('client disconnect.')
            break

        print(body['msg'] + '  ' + timestamp2Date(header['timestamp']))

        res = dealDetailMsg(header, body)

        header = {}
        sendMessage(con, header, res)
        print (res['msg'] + '  ' + time.strftime("%Y-%m-%d %H:%M:%S"))


def main():
    while True:
        con, addr = server.accept()
        thread = threading.Thread(target=dealMsg, args=(con,))
        thread.setDaemon(True)
        thread.start()


if __name__ == '__main__':
    init()
    main()

