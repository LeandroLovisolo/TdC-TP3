#!/usr/bin/env python2
# coding: utf-8

import argparse
from ptc import Socket
from struct import unpack

def main(ack_delay, ack_loss_probability):
    with Socket(ack_delay=ack_delay,
                ack_loss_probability=ack_loss_probability) as sock:
        sock.bind(('0.0.0.0', 6677))
        sock.listen()

        print '[PTC server] Waiting for a client...'
        print sock.accept()
        print '[PTC server] Connection established.'
        size = unpack('I', sock.recv(4))[0]
        print '[PTC server] Receiving %d bytes...' % size
        received = str()
        while len(received) < size:
            received += sock.recv(size - len(received))
        sock.close()
        print '[PTC server] Received %d bytes. Connection closed.' % size

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--delay', type=float, default=0.0,
                        help='ACK packet delay in seconds (default 0)')
    parser.add_argument('-l', '--loss', type=float, default=0.0,
                        help='probability of losing an ACK packet (default 0)')
    args = parser.parse_args()

    main(args.delay, args.loss)