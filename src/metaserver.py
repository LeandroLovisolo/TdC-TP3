#!/usr/bin/env python2
# coding: utf-8

import argparse
import signal
import sys
import socket
from struct import unpack
from subprocess import Popen

def main(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection = None
    server_proc = None

    def signal_handler(signal, frame):
        print '[metaserver] Closing metaserver...'
        if connection is not None:
            connection.shutdown(socket.SHUT_RDWR)
            connection.close()
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        if server_proc is not None:
            server_proc.kill()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    sock.bind(('0.0.0.0', port))
    sock.listen(1)

    while True:
        print '[metaserver] Waiting for a connection...'
        connection, client_address = sock.accept()
        print '[metaserver] Connection established.'
        delay, loss = unpack('dd', connection.recv(16))
        print '[metaserver] Received delay=%f, loss=%f. Starting server...' % (delay, loss)
        server_proc = Popen(['./server', '--delay', str(delay), '--loss', str(loss)])
        connection.sendall('OK')
        server_proc.wait()
        server_proc = None
        connection.close()
        connection = None
        print '[metaserver] Connection closed.\n'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=6677, help='metaserver TCP port')
    args = parser.parse_args()

    main(args.port)