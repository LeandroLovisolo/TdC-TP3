#!/usr/bin/env python2
# coding: utf-8

import plot

class TimeVsSizePlot(plot.Plot):

    def do_plot(self, plt, fig, db):
        statistics = db.get_statistics_by_size()
        data = statistics.items()
        data.sort()
        data = zip(*data)
        sizes = [s / 1000 for s in data[0]]
        avgs = zip(*data[1])[0]

        plt.plot(sizes, avgs)
        plt.xticks(sizes, sizes, fontsize=9, rotation=90)
        plt.xlim([sizes[0], sizes[-1]])
        plt.title(u'Tiempo de transferencia en función del tamaño de archivo')
        plt.xlabel(u'Tamaño de archivo (KB)')
        plt.ylabel(u'Tiempo de transferencia promedio (s)')

if __name__ == '__main__':
    TimeVsSizePlot()