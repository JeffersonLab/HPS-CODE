
import numpy as np
import ROOT as r
import matplotlib
import matplotlib.pyplot as plt
import root_numpy as rnp

from itertools import izip
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import LogNorm


class Plotter(object):

    def __init__(self, file_path): 
        
        plt.style.use('bmh')
        matplotlib.rcParams.update({'font.size': 20})
        matplotlib.rcParams['axes.facecolor'] = 'white'
        matplotlib.rcParams['legend.numpoints'] = 1
        matplotlib.rcParams['legend.fontsize'] = 12
        
        self.pdf = PdfPages(file_path + '.pdf')
        print '[ Plotter ] Saving plots to %s' % (file_path + '.pdf')

        self.rfile = r.TFile(file_path + '.root', 'recreate')
        print '[ Plotter ] Writing histograms to %s' % (file_path + '.root')

    def plot_hist(self, values, bins, **params):
       
        name = None
        if 'name' in params: 
            name = params['name']
 
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 10))
        
        label=None
        if 'label' in params:
            label=params['label']
            ax.legend()
       
        norm = False
        if 'norm' in params: 
            norm = True

        if 'ylog' in params:
            if norm: ax.set_yscale('log')
            else: ax.set_yscale('symlog')

        if 'x_label' in params:
            ax.set_xlabel(params['x_label'])


        ax.hist(values, bins, histtype='step', lw=1.5, label=label, normed=norm)

        self.pdf.savefig(bbox_inches='tight')
        plt.close()

    def plot_hist2d(self, x_values, y_values, bins_x, bins_y, **params):

        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 10))
        
        if 'x_label' in params:
            ax.set_xlabel(params['x_label'])

        if 'y_label' in params:
            ax.set_ylabel(params['y_label'])
        im = ax.hist2d(x_values, y_values, bins=[bins_x, bins_y], norm=LogNorm())

        fig.colorbar(im[3], ax=ax) 
        
        self.pdf.savefig(bbox_inches='tight')
        plt.close()

    def plot_hists(self, values, bins, **params):
    
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 10))

        label=None

        norm = False
        if 'norm' in params: 
            norm = True

        if 'ylog' in params:
            if norm: ax.set_yscale('log')
            else: ax.set_yscale('symlog')
        
        if 'xlog' in params:
            if norm: ax.set_xscale('log')
            else: ax.set_xscale('symlog')

        if 'x_label' in params:
            ax.set_xlabel(params['x_label'])

        labels = None
        if 'labels' in params:
            labels = params['labels']

        label_loc=0
        box = None
        if 'label_loc' in params: 
            if params['label_loc'] == 10: 
                box = ax.get_position()
                ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
            else:
                label_loc=params['label_loc']

        for x_arr, label in izip(values, labels):
            ax.hist(x_arr, bins, histtype='step', lw=1.5, normed=norm, label=label)

        if box:
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        else: 
            ax.legend(loc=label_loc)

        self.pdf.savefig(bbox_inches='tight')
        plt.close()

    def plot_graph(self, x, y, x_err, y_err, **params):
       
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 10))
        
        label=None
        if 'label' in params:
            label=params['label']
            ax.legend()
       
        if 'x_label' in params:
            ax.set_xlabel(params['x_label'])

        if 'y_label' in params:
            ax.set_ylabel(params['y_label'])

        if 'ylim' in params: 
            ax.set_ylim(params['ylim'])

        if 'xlog' in params:
            ax.set_xscale('symlog')

        if 'ylog' in params:
            ax.set_yscale('log')

        ax.errorbar(x, y, x_err, y_err, markersize=10, marker='o', 
                    linestyle='-', fmt='', label=label)

        self.pdf.savefig(bbox_inches='tight')
        plt.close()


    def plot_graphs(self, x, y, x_err, y_err, **params):
       
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 10))
        
        labels=None
        if 'labels' in params:
            labels=params['labels']

        label_loc=0
        if 'label_loc' in params: 
            label_loc=params['label_loc']
       
        if 'x_label' in params:
            ax.set_xlabel(params['x_label'])

        if 'y_label' in params:
            ax.set_ylabel(params['y_label'])

        if 'ylim' in params: 
            ax.set_ylim(params['ylim'])
        
        if 'xlog' in params:
            ax.set_xscale('symlog')

        for index in xrange(0, len(x)):
            ax.errorbar(x[index], y[index], 0, 0, 
                        markersize=6, marker='o', 
                        linestyle='-', fmt='', label=labels[index])

        if labels: ax.legend(loc=label_loc)
        
        self.pdf.savefig(bbox_inches='tight')
        plt.close()

    def create_root_hist(self, name, values, bins, x_min, x_max, x_label, **params):
        
        color = 1
        if 'color' in params: 
            color=params['color']

        histo = r.TH1F(name, name, bins, x_min, x_max)
        histo.GetXaxis().SetTitle(x_label)
        histo.SetLineColor(color)
        histo.SetLineWidth(2)
        bin_width = histo.GetXaxis().GetBinWidth(1)
        
        weights = np.empty(len(values))
        if 'lumi' in params: 
            weights.fill(1/(bin_width*float(params['lumi'])))
        else: weights.fill(1)
        
        rnp.fill_hist(histo, values, weights=weights)
        histo.Write()

    def create_root_hist2d(self, name, x_vals, y_vals, bins_x, x_min, x_max, bins_y, y_min, y_max, **params): 

        histo = r.TH2F(name, name, bins_x, x_min, x_max, bins_y, y_min, y_max)
        rnp.fill_hist(histo, np.column_stack((x_vals, y_vals)))
        histo.Write()

    def close(self):
        self.pdf.close()
        self.rfile.Close()



        

