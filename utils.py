# -*- coding: utf-8 -*-

import struct
import json
import time


MAX_RECV_SIZE = 1024


def packPackage(header, content):
    headJson = json.dumps(header)
    bodyJson = json.dumps(content)

    headerLen = len(headJson)
    bodyLen = len(bodyJson)

    totalLen = headerLen + bodyLen + 12

    package = struct.pack("iii{headerLen}s{bodyLen}s".format(headerLen=headerLen, bodyLen=bodyLen),
                           totalLen, headerLen, bodyLen, headJson, bodyJson)

    return package


def unpackPackage(package, size):
    data = struct.unpack('{size}s'.format(size=size), package)
    return data[0]


def batchRecvPackage(con, size):
    recvData = ''

    if size < MAX_RECV_SIZE:
        recvData = con.recv(size)
    else:
        recvLen = 0
        while recvLen < size:
            if recvLen + MAX_RECV_SIZE < size:
                data = con.recv(MAX_RECV_SIZE)
            else:
                data = con.recv(size - recvLen)

            recvLen += len(data)
            recvData += data

    return recvData


def package2Dict(package, size):
    packJson = unpackPackage(package, size)
    data = json.loads(packJson.decode())

    return data


def recvMessage(con):
    try:
        # recv package length
        lenData = con.recv(12)
        if not lenData:
            return None, None

        totalLen, headerLen, bodyLen = struct.unpack('iii', lenData)

        # recv package header
        header = con.recv(headerLen)
        header = package2Dict(header, headerLen)

        # recv package body
        body = batchRecvPackage(con, bodyLen)
        body = package2Dict(body, bodyLen)

        return header, body
    except:
        return None, None


def sendMessage(con, header, content):
    header.update({
        'timestamp': int(time.time())
    })
    msg = packPackage(header, content)
    con.send(msg)



def packMsg(header, content):
    contentJson = json.dumps(content)
    header.update({
        'timestamp': int(time.time()),
        'bodySize': len(contentJson)
    })
    headerJson = json.dumps(header)
    headerSize = len(headerJson)
    packHeaderSize = struct.pack('!l', headerSize)

    sendMsg = packHeaderSize + headerJson.encode() + contentJson.encode()
    return sendMsg


def unPackHeader(packHeaderSize):
    headerSize = struct.unpack('!l', packHeaderSize)
    return headerSize[0]


def recvMsg(con):
    try:
        # recv package header size
        packHeaderSize = con.recv(4)
        if not packHeaderSize:
            return None, None

        headerSize = unPackHeader(packHeaderSize)

        # recv package header
        header = con.recv(headerSize)
        header = json.loads(header.decode())

        # recv package content
        recvData = ''
        bodySize = header['bodySize']
        if bodySize < MAX_RECV_SIZE:
            recvData = con.recv(bodySize)
        else:
            recvLen = 0
            while recvLen < bodySize:
                if recvLen + MAX_RECV_SIZE < bodySize:
                    data = con.recv(MAX_RECV_SIZE)
                else:
                    data = con.recv(bodySize - recvLen)

                recvLen += len(data)
                recvData += data

        content = json.loads(recvData)
        return header, content
    except:
        return None, None


def sendMsg(con, header, content):
    msg = packMsg(header, content)
    con.send(msg)



def timestamp2Date(timestamp):
    timeArray = time.localtime(timestamp)
    date = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

    return date
