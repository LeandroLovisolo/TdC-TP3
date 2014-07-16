#!/usr/bin/env python2
# coding: utf-8

import plot

class TimeVsSizePlot(plot.Plot):

    def do_plot(self, plt, fig, db, args):
        statistics = db.get_statistics_by_size()
        keys = statistics.keys()
        keys.sort()
        sizes = [size / 1000 for size in keys]
        avg_times = [statistics[key]['avg_time'] for key in keys]

        plt.plot(sizes, avg_times)
        plt.xticks(sizes, sizes, rotation=90)
        plt.xlim([sizes[0], sizes[-1]])
        plt.title(u'Tiempo de transferencia en función del tamaño de archivo')
        plt.xlabel(u'Tamaño de archivo (KB)')
        plt.ylabel(u'Tiempo de transferencia promedio (s)')

if __name__ == '__main__':
    TimeVsSizePlot()