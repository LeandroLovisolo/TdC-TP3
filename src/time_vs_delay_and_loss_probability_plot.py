#!/usr/bin/env python2
# coding: utf-8

import plot

class TimeVsDelayAndLossProbabilityPlot(plot.Plot):

    def do_plot(self, plt, fig, db, args):
        colors = ['Green', 'DarkCyan', 'Fuchsia', 'Brown', 'DarkGoldenRod', 'Salmon',
                  'Orange', 'GreenYellow', 'Red', 'MidnightBlue', 'DimGray']
        loss_probabilities = db.get_loss_probabilities()

        for loss in loss_probabilities:
            statistics = db.get_statistics_by_delay_and_loss_probability(loss)
            keys = statistics.keys()
            keys.sort()
            delays = [int(delay * 1000) for delay in keys]
            avg_times = [statistics[key]['avg_time'] for key in keys]

            plt.plot(delays, avg_times, color=colors.pop(), label=str(loss), lw=2)

        plt.xticks(delays, delays, rotation=90)
        plt.xlim([delays[0], delays[-1]])
        plt.title(u'Tiempo de transferencia en función del retraso en envío de ACKs')
        plt.xlabel(u'Retraso en envío de ACKs (ms)')
        plt.ylabel(u'Tiempo de transferencia promedio (s)')
        plt.legend(loc=2, title=u"Probabilidad de\npérdida de ACKs")

if __name__ == '__main__':
    TimeVsDelayAndLossProbabilityPlot()