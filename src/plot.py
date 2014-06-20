# coding: utf-8

import argparse
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt

from database import DB


class Plot:

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-o', '--output-path', help='path on which to save the plot')
        self.add_arguments(parser)
        args = parser.parse_args()
        
        output_path = args.output_path

        plt.rcParams['text.latex.preamble']=[r'\usepackage{lmodern}']
        plt.rcParams.update({'text.usetex':        True,
                             'text.latex.unicode': True,
                             'font.family':        'lmodern',
                             'font.size':          10,
                             'axes.titlesize':     10,
                             'legend.fontsize':    10,
                             'legend.labelspacing':0.2})

        fig = plt.figure()
        fig.set_size_inches(6, 4) 

        db = DB()
        self.do_plot(plt, fig, db, args)

        plt.tight_layout()

        if output_path is not None:
            plt.savefig(output_path, dpi=1000, box_inches='tight')
        else:
            plt.show()

    def add_arguments(self, parser):
        pass

    def do_plot(self, plt, fig, db, args):
        raise NotImplementedError