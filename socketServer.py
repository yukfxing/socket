# -*- coding: utf-8 -*-

import socket
import time
import threading
from utils import recvMessage, sendMessage, timestamp2Date


def init():
    global server

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # server.bind(('172.17.161.79', 8888))
    server.bind(('127.0.0.1', 8888))
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


def dealMsg(con, addr):
    print(addr[0] + ':' + str(addr[1]) + ' connect.')

    while True:
        header, body = recvMessage(con)
        if not body:
            con.close()
            print(addr[0] + ':' + str(addr[1]) + ' disconnect.')
            break

        print(str(addr[1]) + ': ' + body['msg'] + '  ' + timestamp2Date(header['timestamp']))

        # TODO: deal message and return result
        res = dealDetailMsg(header, body)

        header = {}
        sendMessage(con, header, res)
        print (str(server.getsockname()[1]) + ': ' + res['msg'] + '  ' + time.strftime("%Y-%m-%d %H:%M:%S"))


def main():
    while True:
        con, addr = server.accept()
        thread = threading.Thread(target=dealMsg, args=(con, addr))
        thread.setDaemon(True)
        thread.start()


if __name__ == '__main__':
    init()
    main()
