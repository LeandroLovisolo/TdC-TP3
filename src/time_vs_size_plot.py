#!/usr/bin/env python2
# coding: utf-8

import plot

class TimeVsSizePlot(plot.Plot):

    def do_plot(self, plt, fig, db):
        time_vs_size = db.get_time_vs_size()
        sizes = time_vs_size.keys()
        sizes.sort()
        for size in sizes:
            print '%d: %f' % (size, time_vs_size[size])

if __name__ == '__main__':
    TimeVsSizePlot()