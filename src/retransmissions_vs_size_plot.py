#!/usr/bin/env python2
# coding: utf-8

import plot

class RetransmissionsVsSizePlot(plot.Plot):

    def do_plot(self, plt, fig, db, args):
        statistics = db.get_statistics_by_size(exclude_outliers=args.exclude_outliers)
        keys = statistics.keys()
        keys.sort()
        sizes = [size / 1000 for size in keys]
        avg_retxs = [statistics[key]['avg_retx'] for key in keys]
        stdev_retxs = [statistics[key]['stdev_retx'] for key in keys]

        plt.errorbar(sizes, avg_retxs, yerr=stdev_retxs)
        plt.xticks(sizes, sizes, rotation=90)
        plt.xlim([sizes[0], sizes[-1]])
        plt.title(u'Cantidad de retransmisiones en función del tamaño de archivo')
        plt.xlabel(u'Tamaño de archivo (KB)')
        plt.ylabel(u'Retransmisiones promedio')

    def add_arguments(self, parser):
        parser.add_argument('--exclude-outliers', action='store_true')

if __name__ == '__main__':
    RetransmissionsVsSizePlot()