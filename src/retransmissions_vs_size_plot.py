#!/usr/bin/env python2
# coding: utf-8

import plot

class RetransmissionsVsSizePlot(plot.Plot):

    def do_plot(self, plt, fig, db, args):
        statistics = db.get_statistics_by_size(exclude_outliers=args.exclude_outliers)
        data = statistics.items()
        data.sort()
        data = zip(*data)
        sizes = [s / 1000 for s in data[0]]
        avgs = zip(*data[1])[1]

        plt.plot(sizes, avgs)
        plt.xticks(sizes, sizes, fontsize=9, rotation=90)
        plt.xlim([sizes[0], sizes[-1]])
        plt.title(u'Tiempo de transferencia en función del tamaño de archivo')
        plt.xlabel(u'Tamaño de archivo (KB)')
        plt.ylabel(u'Tiempo de transferencia promedio (s)')

    def add_arguments(self, parser):
        parser.add_argument('--exclude-outliers', action='store_true')

if __name__ == '__main__':
    RetransmissionsVsSizePlot()