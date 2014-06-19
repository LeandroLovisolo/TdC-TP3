#!/usr/bin/env python2
# coding: utf-8

import argparse
import numpy as np

from metaclient import transfer
from database import DB

n = 10
size = 50000

delay_min = 0.0
delay_max = 0.1
delay_step = 0.005
delays = np.arange(delay_min, delay_max + delay_step, delay_step)

loss_min = 0.0
loss_max = 0.5
loss_step = 0.05
losses = np.arange(loss_min, loss_max + loss_step, loss_step)

def main(hostname, port, initial_delay, initial_loss):
    db = DB()

    for loss in losses:
        if loss < initial_loss: continue
        for delay in delays:
            if loss == initial_loss and delay < initial_delay: continue
            for i in range(0, n):
                print '\nDelay %f, probabilidad de pérdida %f, medición %d/%d...' \
                    % (delay, loss, i + 1, n)
                t, retransmissions = transfer(hostname=hostname, port=port, size=size, delay=delay, loss=loss)
                db.register(DB.DELAY_AND_LOSS_PROBABILITY, t, retransmissions, size, delay=delay, loss=loss)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('hostname', help='metaserver hostname')
    parser.add_argument('-p', '--port', type=int, default=6677, help='metaserver TCP port')
    parser.add_argument('-d', '--initial-delay', type=float, default=delay_min, help='initial delay')
    parser.add_argument('-l', '--initial-loss', type=float, default=loss_min, help='initial loss probability')

    args = parser.parse_args()

    main(args.hostname, args.port, args.initial_delay, args.initial_loss)




