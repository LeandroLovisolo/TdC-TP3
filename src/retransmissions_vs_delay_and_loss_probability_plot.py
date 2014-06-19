#!/usr/bin/env python2
# coding: utf-8

import plot

class RetransmissionsVsDelayAndLossProbabilityPlot(plot.Plot):

    def do_plot(self, plt, fig, db):
        colors = ['Green', 'DarkCyan', 'Indigo', 'Brown', 'DarkGoldenRod', 'Crimson',
                  'Orange', 'GreenYellow', 'DarkMagenta', 'MidnightBlue', 'DimGray']
        loss_probabilities = db.get_loss_probabilities()

        for loss in loss_probabilities:
            statistics = db.get_statistics_by_delay_and_loss_probability(loss)

            data = statistics.items()
            data.sort()
            data = zip(*data)
            delays = [s * 1000 for s in data[0]]
            retransmissions = zip(*data[1])[1]

            plt.plot(delays, retransmissions, color=colors.pop(), label=str(loss), lw=2)

        plt.xticks(delays, delays, fontsize=9, rotation=90)
        plt.xlim([delays[0], delays[-1]])
        plt.title(u'Cantidad de retransmisiones en función del retraso en envío de ACKs')
        plt.xlabel(u'Retraso en envío de ACKs (ms)')
        plt.ylabel(u'Retransmisiones')
        plt.legend(loc=2, title=u"Probabilidad de\npérdida de ACKs")

if __name__ == '__main__':
    RetransmissionsVsDelayAndLossProbabilityPlot()