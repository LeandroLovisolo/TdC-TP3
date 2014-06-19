#!/usr/bin/env python2
# coding: utf-8

import plot

class TimeVsSizePlot(plot.Plot):

    def do_plot(self, plt, fig, db):
        time_vs_size = db.get_time_vs_size()
        data = time_vs_size.items()
        data.sort()
        data = zip(*data)
        sizes = list(data[0])
        avgs = list(data[1])

        plt.plot(sizes, avgs)
        plt.xticks(sizes, sizes, fontsize=9, rotation=90)
        plt.title(u'Tiempo de transferencia en función del tamaño de archivo')
        plt.xlabel(u'Tamaño de archivo (B)')
        plt.ylabel(u'Tiempo de transferencia promedio (s)')

if __name__ == '__main__':
    TimeVsSizePlot()