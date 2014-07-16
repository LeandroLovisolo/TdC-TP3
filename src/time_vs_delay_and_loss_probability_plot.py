#!/usr/bin/env python2
# coding: utf-8

import plot

class TimeVsDelayAndLossProbabilityPlot(plot.Plot):

    def do_plot(self, plt, fig, db, args):
        colors = ['Green', 'DarkCyan', 'Fuchsia', 'Brown', 'DarkGoldenRod', 'Salmon',
                  'Orange', 'GreenYellow', 'Red', 'MidnightBlue', 'DimGray']
        loss_probabilities = db.get_loss_probabilities()

        if args.only_min_and_max_loss_probabilities:
            loss_probabilities = [min(loss_probabilities), max(loss_probabilities)]
            colors = [colors[0], colors[-1]]

        for loss in loss_probabilities:
            statistics = db.get_statistics_by_delay_and_loss_probability(loss)
            keys = statistics.keys()
            keys.sort()
            delays = [int(delay * 1000) for delay in keys]
            avg_times = [statistics[key]['avg_time'] for key in keys]
            stdev_times = [statistics[key]['stdev_time'] for key in keys]

            if args.only_min_and_max_loss_probabilities:
                plt.errorbar(delays, avg_times, stdev_times, color=colors.pop(), label=str(loss), lw=2)
            else:
                plt.plot(delays, avg_times, color=colors.pop(), label=str(loss), lw=2)

        plt.xticks(delays, delays, rotation=90)
        plt.xlim([delays[0], delays[-1]])
        plt.title(u'Tiempo de transferencia en función del retraso en envío de ACKs')
        plt.xlabel(u'Retraso en envío de ACKs (ms)')
        plt.ylabel(u'Tiempo de transferencia promedio (s)')
        plt.legend(loc=2, title=u"Probabilidad de\npérdida de ACKs")

    def add_arguments(self, parser):
        parser.add_argument('--only-min-and-max-loss-probabilities', action='store_true')

if __name__ == '__main__':
    TimeVsDelayAndLossProbabilityPlot()