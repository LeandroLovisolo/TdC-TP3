#!/usr/bin/env python2
# coding: utf-8

import argparse
import socket
from struct import pack
from ptc import Socket as PTCSocket, SHUT_WR
import sys
from time import time


def ptc_client(server_ip, size):
    with PTCSocket() as sock:
        print '[client] Connecting...'
        sock.connect((server_ip, 6677))
        print '[client] Connection established.'
        print '[client] Sending file size...'
        sock.send(pack('I', size))
        print '[client] Uploading %d bytes...' % size
        t0 = time()
        sock.send('a' * size)
        sock.shutdown(SHUT_WR) # Cerramos el stream de escritura pero podemos seguir recibiendo datos.
    t1 = time()
    t = t1 - t0
    print '[client] Upload time: %f seconds' % t
    print '[client] Connection closed.'
    return t

def transfer(hostname, port=6677, delay=0, loss=0, size=1000):
    server_ip = socket.gethostbyname(hostname)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print '[metaclient] Connecting to metaserver...'
    sock.connect((server_ip, port))
    print '[metaclient] Connected. Requesting delay=%f, loss=%f...' % (delay, loss)
    sock.sendall(pack('dd', delay, loss))
    response = sock.recv(2)
    if response != 'OK':
        sys.exit('[metaclient] ERROR: received invalid answer from metaserver: %s' % response)
    print '[metaclient] PTC server up. Connecting...'
    t = ptc_client(server_ip, size)
    sock.close()
    print '[metaclient] Connection closed.'
    return t

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('hostname', help='server hostname')
    parser.add_argument('size', type=int, help='number of bytes to be sent')
    parser.add_argument('-p', '--port', type=int, default=6677, help='metaserver TCP port')
    parser.add_argument('-d', '--delay', type=float, default=0.0,
                        help='server ACK packet delay in seconds (default 0)')
    parser.add_argument('-l', '--loss', type=float, default=0.0,
                        help='server probability of losing an ACK packet (default 0)')    
    args = parser.parse_args()

    transfer(args.hostname, args.port, args.delay, args.loss, args.size)
