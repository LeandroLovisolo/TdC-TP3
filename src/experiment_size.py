#!/usr/bin/env python2
# coding: utf-8

import argparse

from metaclient import transfer
from database import DB

n = 10
size_min = 50000
size_max = 1000000
size_step = 50000
sizes = range(size_min, size_max + size_step, size_step)

def main(hostname, port):
    db = DB()

    for size in sizes:
        for i in range(0, n):
            print '\nTamaño %d, medición %d/%d...' % (size, i + 1, n)
            t, retransmissions = transfer(hostname=hostname, port=port, size=size)
            db.register(DB.SIZE, t, retransmissions, size)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('hostname', help='metaserver hostname')
    parser.add_argument('-p', '--port', type=int, default=6677, help='metaserver TCP port')
    args = parser.parse_args()

    main(args.hostname, args.port)




