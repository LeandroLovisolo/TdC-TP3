#!/usr/bin/env python2
# coding: utf-8

import plot

class RetransmissionsVsDelayAndLossProbabilityPlot(plot.Plot):

    def do_plot(self, plt, fig, db, args):
        colors = ['Green', 'DarkCyan', 'Fuchsia', 'Brown', 'DarkGoldenRod', 'Salmon',
                  'Orange', 'GreenYellow', 'Red', 'MidnightBlue', 'DimGray']
        loss_probabilities = db.get_loss_probabilities()

        for loss in loss_probabilities:
            statistics = db.get_statistics_by_delay_and_loss_probability(
                loss, exclude_outliers=args.exclude_outliers)
            keys = statistics.keys()
            keys.sort()
            delays = [int(delay * 1000) for delay in keys]
            avg_retxs = [statistics[key]['avg_retx'] for key in keys]

            plt.plot(delays, avg_retxs, color=colors.pop(), label=str(loss), lw=2)

        plt.xticks(delays, delays, rotation=90)
        plt.xlim([delays[0], delays[-1]])
        plt.title(u'Cantidad de retransmisiones en función del retraso en envío de ACKs')
        plt.xlabel(u'Retraso en envío de ACKs (ms)')
        plt.ylabel(u'Retransmisiones')
        plt.legend(loc=2, title=u"Probabilidad de\npérdida de ACKs")

    def add_arguments(self, parser):
        parser.add_argument('--exclude-outliers', action='store_true')

if __name__ == '__main__':
    RetransmissionsVsDelayAndLossProbabilityPlot()