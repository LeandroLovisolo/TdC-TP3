#!/usr/bin/env python2
# coding: utf-8

import argparse
from ptc import Socket
from struct import unpack

def main(port, ack_delay, loss_probability):
    received = str()

    while True:
        with Socket(ack_delay=ack_delay,
                    loss_probability=loss_probability) as sock:
            sock.bind(('0.0.0.0', port))
            sock.listen()

            print 'waiting for a client...'
            
            sock.accept()

            print 'connection established'

            size_str = sock.recv(4)
            size = unpack('I', size_str)[0]

            print 'receiving %d bytes...' % size

            while len(received) < size:
                received += sock.recv(size - len(received))

            print 'closing socket...'

            sock.close()
        #print 'received: %s' % received
        print 'disconnected\n'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('port', type=int, help='port to listen to')
    parser.add_argument('-d', '--delay', type=float, default=0.0,
                        help='ACK delay in seconds (default 0)')
    parser.add_argument('-l', '--loss', type=float, default=0.0,
                        help='probability of losing a packet (default 0)')
    args = parser.parse_args()

    main(args.port, args.delay, args.loss)