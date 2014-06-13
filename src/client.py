#!/usr/bin/env python2
# coding: utf-8

import argparse
from ptc import Socket, SHUT_WR
from struct import pack
from time import time
from socket import gethostbyname

def main(server_ip, size):
    with Socket() as sock:
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

      

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('hostname', help='server hostname')
    parser.add_argument('size', type=int, help='number of bytes to be uploaded')
    args = parser.parse_args()

    main(gethostbyname(args.hostname), args.size)