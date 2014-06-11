#!/usr/bin/env python2
# coding: utf-8

import argparse
from ptc import Socket, SHUT_WR
from struct import pack
from time import clock
from socket import gethostbyname

def main(server_ip, port, size, ack_delay, loss_probability):
    msg = 'a' * size

    with Socket(ack_delay=ack_delay,
                loss_probability=loss_probability) as sock:
      sock.connect((server_ip, port))
      print 'connection established'

      print 'sending file size...'
      sock.send(pack('I', size))

      print 'sending %d bytes...' % size
      t0 = clock()
      sock.send(msg)
      t1 = clock()

      t = t1 - t0
      print 'took %f seconds' % t

      # Cerramos el stream de escritura pero podemos seguir recibiendo datos.
      sock.shutdown(SHUT_WR)
    print 'all done'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('hostname', help='server hostname')
    parser.add_argument('port', type=int, help='server PTC port')
    parser.add_argument('size', type=int, help='number of bytes to be sent')
    parser.add_argument('-d', '--delay', type=float, default=0.0,
                        help='ACK delay in seconds (default 0)')
    parser.add_argument('-l', '--loss', type=float, default=0.0,
                        help='probability of losing a packet (default 0)')
    args = parser.parse_args()

    main(gethostbyname(args.hostname), args.port, args.size, args.delay, args.loss)