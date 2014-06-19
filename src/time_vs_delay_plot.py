#!/usr/bin/env python2
# coding: utf-8

import plot

class TimeVsDelayPlot(plot.Plot):

    def do_plot(self, plt, fig, db):
        loss_probabilities = db.get_time_vs_delay_loss_probabilities()
        loss = loss_probabilities[0]

        time_vs_delay = db.get_time_vs_delay(loss)

        data = time_vs_delay.items()
        data.sort()
        data = zip(*data)
        delays = [s * 1000 for s in data[0]]
        avgs = list(data[1])

        plt.plot(delays, avgs)
        plt.xticks(delays, delays, fontsize=9, rotation=90)
        plt.xlim([delays[0], delays[-1]])
        plt.title(u'Tiempo de transferencia en función del retraso en envío de ACKS')
        plt.xlabel(u'Retraso en envío de ACKS (ms)')
        plt.ylabel(u'Tiempo de transferencia promedio (s)')

if __name__ == '__main__':
    TimeVsDelayPlot()