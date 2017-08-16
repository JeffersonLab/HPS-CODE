
import math
import numpy as np
import Plotter
import ROOT as r

from numpy import linalg as la
from scipy.stats import norm

class SignalAnalysis(object):

    def __init__(self): 
        self.initialize()

    def initialize(self): 
        
        self.ntuple = {}
        self.plt_vars = [
            # Counters
            'track_count', 'top_track_count', 'bot_track_count',
            'n_v0', 'n_v0_iso',
        ]
        
        self.kin_vars = [
           
            # Ecal clusters
            'top_cluster_energy', 'top_cluster_time', 'top_cluster_x', 
            'bot_cluster_energy', 'bot_cluster_time', 'bot_cluster_x',
            'ecal_cluster_dt',

            # Track parameters
            'ttrk_d0', 'ttrk_omega', 'ttrk_tan_lambda', 'ttrk_z0',
            'btrk_d0', 'btrk_omega', 'btrk_tan_lambda', 'btrk_z0',
            
            # E/p
            'top_eop', 'bot_eop'
        ]

        self.v0_vars = [
            # Vertex
            'mass', 'v0_chi2',
            'v0_p', 'v0_px', 'v0_py', 'v0_pz',  
            'vx', 'vy', 'vz'
        ]

        self.cut_vars = [

            # Cuts
            'has_opp_clusters', 
            'pass_trk_match', 'pass_fee', 'pass_v0_p_cut', 
            'pass_cluster_dt_cut', 'pass_trk_chi2',
            'pass_v0_chi2_cut', 'pass_trk_cluster_dt',
            'has_l1', 'has_l2'
        ]

        self.plt_vars = np.concatenate([self.plt_vars, self.v0_vars, 
                                        self.cut_vars, self.kin_vars])

        for variable in self.plt_vars: 
            self.ntuple[variable] = []

        self.run_number = 0

    def has_opp_clusters(self, particle):
        
        # Get the daughter particles composing this particle.
        daughters = particle.getParticles()
        
        # Check that the mother particle has exactly two daughters.
        if daughters.GetEntriesFast() != 2: return False

        # Check that the two daughters have an Ecal cluster associated
        # with them.
        if particle.getClusters().GetEntriesFast() != 2: return False

        cluster0 = particle.getClusters().At(0)
        cluster1 = particle.getClusters().At(1)

        # Make sure the clusters are in opposite Ecal volumes
        if cluster0.getPosition()[1]*cluster1.getPosition()[1] > 0: return False
        
        return True

    def has_good_match(self, particle):

        # Check that the two daughters have an SvtTrack associated with them.
        if particle.getTracks().GetEntriesFast() != 2: return False

        daughters = particle.getParticles()

        for index in xrange(0, 2): 
            if daughters.At(index).getGoodnessOfPID() > 10: return False

        return True

    def pass_fee_cut(self, particle):
        
        for index in xrange(0, 2): 
            trk = particle.getTracks().At(index)
            pvec = trk.getMomentum()
            p = la.norm(pvec)
            if p >= .75*1.056: return False

        return True

    def pass_v0_p_cut(self, particle): 

        pvec = particle.getMomentum()
        p = la.norm(pvec)
        if (p <= .8*1.056) or (p >= 1.18*1.056) : return False

        return True

    def pass_trk_cluster_dt_cut(self, particle):

        # Check that the two daughters have an Ecal cluster associated
        # with them.
        if particle.getClusters().GetEntriesFast() != 2: return False

        # Check that the two daughters have an SvtTrack associated with them.
        if particle.getTracks().GetEntriesFast() != 2: return False
        
        for index in xrange(0, 2): 
            trk_cluster_dt = (particle.getClusters().At(index).getClusterTime() - 
                    particle.getTracks().At(index).getTrackTime())
            trk_cluster_dt = math.fabs(trk_cluster_dt - 43)
            if trk_cluster_dt >= 4.5: return False

        return True
        

    def pass_trk_chi2_cut(self, particle):
        
        # Check that the two daughters have an Ecal cluster associated
        # with them.
        if particle.getTracks().GetEntriesFast() != 2: return False

        for index in xrange(0, 2): 
            if particle.getTracks().At(index).getChi2() >= 40: return False

        return True

    def pass_v0_chi2_cut(self, particle):
        if particle.getVertexFitChi2() >= 75: return False
        return True

    def pass_cluster_dt_cut(self, particle): 

        # Check that the two daughters have an Ecal cluster associated
        # with them.
        if particle.getClusters().GetEntriesFast() != 2: return False

        cluster_dt = (particle.getClusters().At(0).getClusterTime() - 
                particle.getClusters().At(1).getClusterTime())

        if math.fabs(cluster_dt) >= 2: return False
        return True


    def process(self, event): 
       
        self.run_number = event.getRunNumber()

        # First check that the event contains GBL tracks.  Without GBL 
        # tracks, v0 particles can't be created.  In the case tracks haven't
        # been found, skip the event.
        if event.getNumberOfGblTracks() == 0: return
        self.ntuple['track_count'].append(event.getNumberOfGblTracks())

        # Split the tracks into top and bottom collections
        top_trks = []
        bot_trks = []
        for track_n in xrange(0, event.getNumberOfGblTracks()):
            track = event.getGblTrack(track_n)
            if track.isTopTrack(): top_trks.append(track)
            else: bot_trks.append(track)

        self.ntuple['top_track_count'].append(len(top_trks))
        self.ntuple['bot_track_count'].append(len(bot_trks))

        v0_col_type = r.HpsParticle.TC_V0_CANDIDATE
        #v0_col_type = r.HpsParticle.UC_MOLLER_CANDIDATE
        v0_count = event.getNumberOfParticles(v0_col_type)
        self.ntuple['n_v0'].append(v0_count)

        # Only look at events where the electrons are isolated i.e. each
        # volume only has a single track
        if len(top_trks)*len(bot_trks) != 1: return
        self.ntuple['n_v0_iso'].append(v0_count)

        for particle_n in xrange(0, v0_count): 

            particle = event.getParticle(v0_col_type, particle_n)

            # We only care to look at v0 particles created from GBL tracks
            if particle.getType() < 32: continue

            vpvec = particle.getMomentum()
            vp = la.norm(vpvec) 

            self.ntuple['mass'].append(particle.getMass())
            self.ntuple['v0_chi2'].append(particle.getVertexFitChi2())
            self.ntuple['v0_p'].append(vp)
            self.ntuple['v0_px'].append(vpvec[0])
            self.ntuple['v0_py'].append(vpvec[1])
            self.ntuple['v0_pz'].append(vpvec[2])
            self.ntuple['vx'].append(particle.getVertexPosition()[0])
            self.ntuple['vy'].append(particle.getVertexPosition()[1])
            self.ntuple['vz'].append(particle.getVertexPosition()[2])

            ttrk_params = {'d0':-9999, 'omega':-9999, 'tan_lambda':-9999, 
                           'z0':-9999, 'p': -9999, 'theta': -9999} 
            btrk_params = {'d0':-9999, 'omega':-9999, 'tan_lambda':-9999, 
                           'z0':-9999, 'p': -9999, 'theta': -9999} 
            top_has_l1 = False
            bot_has_l1 = False
            top_has_l2 = False
            bot_has_l2 = False
            
            if particle.getTracks().GetEntriesFast() == 2:

                tindex = 0
                bindex = 1
                if particle.getTracks().At(1).isTopTrack(): 
                    tindex = 1
                    bindex = 0

                ttrk = particle.getTracks().At(tindex)
                btrk = particle.getTracks().At(bindex)

                ttrk_params['d0'] = ttrk.getD0()
                ttrk_params['omega'] = ttrk.getOmega()
                ttrk_params['tan_lambda'] = ttrk.getTanLambda()
                ttrk_params['z0'] = ttrk.getZ0()

                btrk_params['d0'] = btrk.getD0()
                btrk_params['omega'] = btrk.getOmega()
                btrk_params['tan_lambda'] = btrk.getTanLambda()
                btrk_params['z0'] = btrk.getZ0()

                ttrk_pvec = ttrk.getMomentum()
                btrk_pvec = btrk.getMomentum()
        
                ttrk_params['p'] = la.norm(ttrk_pvec)
                btrk_params['p'] = la.norm(btrk_pvec)

                ttrk_params['theta'] = math.acos(ttrk_pvec[2]/ttrk_params['p'])*180.0/3.14159 
                btrk_params['theta'] = math.acos(btrk_pvec[2]/btrk_params['p'])*180.0/3.14159 

                for hit_index in xrange(0, ttrk.getSvtHits().GetEntriesFast()): 
                    hit = ttrk.getSvtHits().At(hit_index)
                    if hit.getLayer() == 1: top_has_l1 = True
                    if hit.getLayer() == 2: top_has_l2 = True

                for hit_index in xrange(0, btrk.getSvtHits().GetEntriesFast()): 
                    hit = btrk.getSvtHits().At(hit_index)
                    if hit.getLayer() == 1: bot_has_l1 = True
                    if hit.getLayer() == 2: bot_has_l2 = True

            self.ntuple['ttrk_d0'].append(ttrk_params['d0'])
            self.ntuple['ttrk_omega'].append(ttrk_params['omega'])
            self.ntuple['ttrk_tan_lambda'].append(ttrk_params['tan_lambda'])
            self.ntuple['ttrk_z0'].append(ttrk_params['z0'])

            self.ntuple['btrk_d0'].append(btrk_params['d0'])
            self.ntuple['btrk_omega'].append(btrk_params['omega'])
            self.ntuple['btrk_tan_lambda'].append(btrk_params['tan_lambda'])
            self.ntuple['btrk_z0'].append(btrk_params['z0'])
 
            has_l1 = False
            has_l2 = False
            if (top_has_l1 & bot_has_l1): has_l1 = True
            if (top_has_l2 & bot_has_l2): has_l2 = True
            
            self.ntuple['has_l1'].append(has_l1)
            self.ntuple['has_l2'].append(has_l2)

            tclust_e = 9999
            tclust_t = -5000
            bclust_e = 9999
            bclust_t = 5000
            tclust_x = -9999
            bclust_x = -9999
            if particle.getClusters().GetEntriesFast() == 2:
                tindex = 0
                bindex = 1
                if particle.getClusters().At(1).getPosition()[1] > 0: 
                    tindex = 1
                    bindex = 0

                tclust = particle.getClusters().At(tindex)
                bclust = particle.getClusters().At(bindex)

                tclust_e = tclust.getEnergy()
                tclust_t = tclust.getClusterTime()
                tclust_x = tclust.getPosition()[0]
                bclust_e = bclust.getEnergy()
                bclust_t = bclust.getClusterTime()
                bclust_x = bclust.getPosition()[0]
            
            self.ntuple['top_cluster_energy'].append(tclust_e)
            self.ntuple['top_cluster_time'].append(tclust_t)
            self.ntuple['top_cluster_x'].append(tclust_x)
            self.ntuple['bot_cluster_energy'].append(bclust_e)
            self.ntuple['bot_cluster_time'].append(bclust_t)
            self.ntuple['bot_cluster_x'].append(bclust_x)
            self.ntuple['ecal_cluster_dt'].append(tclust_t - bclust_t)

            self.ntuple['top_eop'].append(tclust_e/ttrk_params['p'])
            self.ntuple['bot_eop'].append(bclust_e/btrk_params['p'])

            # Require the two v0 tracks to be in opposite volumes.
            self.ntuple['has_opp_clusters'].append(self.has_opp_clusters(particle))

            # The two tracks must be matched to different clusters.
            self.ntuple['pass_trk_match'].append(self.has_good_match(particle))

            # Make sure the electrons aren't beam e-
            self.ntuple['pass_fee'].append(self.pass_fee_cut(particle))
          
            #
            self.ntuple['pass_trk_cluster_dt'].append(self.pass_trk_cluster_dt_cut(particle))

            #
            self.ntuple['pass_trk_chi2'].append(self.pass_trk_chi2_cut(particle))

            #
            self.ntuple['pass_v0_p_cut'].append(self.pass_v0_p_cut(particle))

            #
            self.ntuple['pass_v0_chi2_cut'].append(self.pass_v0_chi2_cut(particle))
            
            #
            self.ntuple['pass_cluster_dt_cut'].append(self.pass_cluster_dt_cut(particle))

    def finalize(self): 
       
        for variable in self.plt_vars: 
            self.ntuple[variable] = np.array(self.ntuple[variable])

        cut_flow = {}
        for variable in self.v0_vars: 
            cut_flow[variable] = [self.ntuple[variable]]
      
        for variable in self.kin_vars: 
            cut_flow[variable] = [self.ntuple[variable]]

        cut = np.ones(len(self.ntuple['mass']), dtype=bool)
        for variable in self.cut_vars:
            cut = cut & self.ntuple[variable]
            for v0_var in self.v0_vars:
                cut_flow[v0_var].append(self.ntuple[v0_var][cut])

            for kin_var in self.kin_vars:
                cut_flow[kin_var].append(self.ntuple[kin_var][cut])

        plt_labels=['All', 
                    'Clusters in opposite volumes',
                    'Track-cluster match $\chi^{2} <$ 10',
                    '$p_{e} <=$ 0.75*1.056 GeV', 
                    '0.8*1.056 < $p(v_{0}) <$ 1.18$E_{beam}$',
                    'abs(Cluster-track dt) - 43 ns < 4.5 ns',
                    'Track $\chi^{2} <$ 40', 
                    '$v_{0}$ $\chi^{2} <$ 75',
                    'Ecal clust pair dt < 2 ns', 
                    'Has L1 hit', 
                    'Has L2 hit']

        plt = Plotter.Plotter('ap_analysis_%s' % self.run_number)

        plt.plot_hists([
                        self.ntuple['track_count'],
                        self.ntuple['top_track_count'],
                        self.ntuple['bot_track_count']
                       ], 
                       np.linspace(0, 30, 31),
                       labels=['All', 'Top', 'Bottom'],
                       ylog=True,
                       x_label='Track Multiplicity')

        plt.plot_hists([
                        self.ntuple['n_v0'],
                        self.ntuple['n_v0_iso']
                       ], 
                       np.linspace(0, 100, 101),
                       labels=['All', 'Isolated Tracks'],
                       ylog=True,
                       x_label='V$_{0}(e^-e^-)$ Multiplicity')

        plt.create_root_hist('n_v0_iso', 
                             self.ntuple['n_v0_iso'],
                             100, 0, 100, 
                             "v_{0}(e^{-}e^{-}$)")
       
        plt.plot_hists(cut_flow['mass'], 
                       np.linspace(0, 0.08, 251),
                       labels=plt_labels,
                       ylog=True,
                       label_loc=10,
                       x_label='$m(e^-e^-)$ GeV')

        for index in xrange(0, len(cut_flow['mass'])):
            plt.create_root_hist('mass - %s' % plt_labels[index], 
                cut_flow['mass'][index], 
                250, 0, .08, 
                'm(e^{-}e^{-}) GeV')

        plt.plot_hists(cut_flow['v0_chi2'], 
                       np.linspace(0, 100, 101),
                       labels=plt_labels,
                       ylog=True,
                       label_loc=10,
                       x_label='$v_{0}$ $\chi^{2}$')

        plt.plot_hists(cut_flow['v0_p'], 
                       np.linspace(0, 2.0, 201),
                       labels=plt_labels,
                       ylog=True,
                       label_loc=10,
                       x_label='$p(v_{0})$ GeV')

        for index in xrange(0, len(cut_flow['v0_p'])):
            plt.create_root_hist('v0_p - %s' % plt_labels[index], 
                cut_flow['v0_p'][index], 
                200, 0, 2.0, 
                'p(v_{0}) GeV')

        
        plt.plot_hist2d(cut_flow['mass'][len(cut_flow['mass']) - 1], 
                        cut_flow['v0_p'][len(cut_flow['v0_p']) - 1],
                        np.linspace(0.02, 0.05, 251),
                        np.linspace(0.75, 1.25, 201),
                        x_label='$m(e^-e^-)$ GeV',
                        y_label='$p(v_{0})$ GeV')

        plt.plot_hists(cut_flow['v0_px'], 
                       np.linspace(-0.1, 0.1, 101),
                       labels=plt_labels,
                       ylog=True,
                       label_loc=10,
                       x_label='$p_{x}(v_{0})$ GeV')
        
        for index in xrange(0, len(cut_flow['v0_px'])):
            plt.create_root_hist('v0_px - %s' % plt_labels[index], 
                cut_flow['v0_px'][index], 
                100, -0.1, 0.1, 
                'p_{x}(v_{0}) GeV')
        
        plt.plot_hists(cut_flow['v0_py'], 
                       np.linspace(-0.1, 0.1, 101),
                       labels=plt_labels,
                       ylog=True,
                       label_loc=10,
                       x_label='$p_{y}(v_{0})$ GeV')

        for index in xrange(0, len(cut_flow['v0_py'])):
            plt.create_root_hist('v0_py - %s' % plt_labels[index], 
                cut_flow['v0_py'][index], 
                100, -0.1, 0.1, 
                'p_{y}(v_{0}) GeV')

        plt.plot_hists(cut_flow['v0_pz'], 
                       np.linspace(0, 2.0, 201),
                       labels=plt_labels,
                       ylog=True,
                       label_loc=10,
                       x_label='$p_{z}(v_{0})$ GeV')

        for index in xrange(0, len(cut_flow['v0_pz'])):
            plt.create_root_hist('v0_pz - %s' % plt_labels[index], 
                cut_flow['v0_pz'][index], 
                200, 0, 2.0, 
                'p_{z}(v_{0}) GeV')

        plt.plot_hists(cut_flow['vx'], 
                       np.linspace(-1, 1, 101),
                       labels=plt_labels,
                       ylog=True,
                       label_loc=10,
                       x_label='$v_{0}$ x (mm)')

        for index in xrange(0, len(cut_flow['vx'])):
            plt.create_root_hist('vx - %s' % plt_labels[index], 
                cut_flow['vx'][index], 
                100, -1, 1, 
                'v_{x} (mm)')

        plt.plot_hists(cut_flow['vy'], 
                       np.linspace(-1, 1, 101),
                       labels=plt_labels,
                       ylog=True,
                       label_loc=10,
                       x_label='$v_{0}$ y (mm)')

        for index in xrange(0, len(cut_flow['vy'])):
            plt.create_root_hist('vy - %s' % plt_labels[index], 
                cut_flow['vy'][index], 
                100, -1, 1, 
                'v_{y} (mm)')

        plt.plot_hists(cut_flow['vz'], 
                       np.linspace(-1, 1, 101),
                       labels=plt_labels,
                       ylog=True,
                       label_loc=10,
                       x_label='$v_{0}$ z (mm)')
        
        for index in xrange(0, len(cut_flow['vz'])):
            plt.create_root_hist('vz - %s' % plt_labels[index], 
                cut_flow['vz'][index], 
                100, -1, 1, 
                'v_{z} (mm)')

        plt.plot_hists(cut_flow['ttrk_d0'], 
                       np.linspace(-10, 10, 101),
                       labels=plt_labels,
                       ylog=True,
                       label_loc=10,
                       x_label='Top track d0 (mm)')
        
        plt.plot_hists(cut_flow['btrk_d0'], 
                       np.linspace(-10, 10, 101),
                       labels=plt_labels,
                       ylog=True,
                       label_loc=10,
                       x_label='Bottom track d0 (mm)')

        plt.plot_hists(cut_flow['top_cluster_energy'], 
                       np.linspace(0.0, 1.5, 251),
                       labels=plt_labels,
                       ylog=True,
                       label_loc=10,
                       x_label='Top cluster energy (GeV)')

        plt.plot_hists(cut_flow['bot_cluster_energy'], 
                       np.linspace(0.0, 1.5, 251),
                       labels=plt_labels,
                       ylog=True,
                       label_loc=10,
                       x_label='Bottom cluster energy (GeV)')

        plt.plot_hist2d(cut_flow['top_cluster_energy'][0], 
                        cut_flow['bot_cluster_energy'][0],
                        np.linspace(0.0, 1.5, 251),
                        np.linspace(0.0, 1.5, 251),
                        x_label='Top cluster energy (GeV)',
                        y_label='Bottom cluster energy (GeV)')

        plt.plot_hist2d(cut_flow['top_cluster_energy'][len(cut_flow['top_cluster_energy']) - 1], 
                        cut_flow['bot_cluster_energy'][len(cut_flow['bot_cluster_energy']) - 1],
                        np.linspace(0.0, 1.5, 251),
                        np.linspace(0.0, 1.5, 251),
                        x_label='Top cluster energy (GeV)',
                        y_label='Bottom cluster energy (GeV)')

        plt.plot_hists(cut_flow['top_cluster_time'], 
                       np.linspace(0, 80, 161),
                       labels=plt_labels,
                       ylog=True,
                       label_loc=10,
                       x_label='Top cluster time (ns)')

        plt.plot_hists(cut_flow['bot_cluster_time'], 
                       np.linspace(0, 80, 161),
                       labels=plt_labels,
                       ylog=True,
                       label_loc=10,
                       x_label='Bottom cluster time (ns)')

        plt.plot_hist2d(cut_flow['top_cluster_time'][0], 
                        cut_flow['bot_cluster_time'][0],
                        np.linspace(0, 80, 161),
                        np.linspace(0, 80, 161),
                        x_label='Top cluster time (ns)',
                        y_label='Bottom cluster time (ns)')

        plt.plot_hist2d(cut_flow['top_cluster_x'][0], 
                        cut_flow['bot_cluster_x'][0],
                        np.linspace(-200, 100, 151),
                        np.linspace(-200, 100, 151),
                        x_label='Top cluster x (mm)',
                        y_label='Bottom cluster x (mm)')

        plt.create_root_hist2d('Ecal cluster x vs Ecal cluster x', 
                               cut_flow['top_cluster_x'][len(cut_flow['top_cluster_x']) - 1], 
                               cut_flow['bot_cluster_x'][len(cut_flow['bot_cluster_x']) - 1],
                               150, -200, 100, 
                               150, -200, 100)

        for index in xrange(0, len(cut_flow['top_cluster_x'])):
            plt.create_root_hist('top_cluster_x - %s' % plt_labels[index], 
                cut_flow['top_cluster_x'][index], 
                150, -200, 100, 
                'Top cluster x (mm)')

        for index in xrange(0, len(cut_flow['bot_cluster_x'])):
            plt.create_root_hist('bot_cluster_x - %s' % plt_labels[index], 
                cut_flow['bot_cluster_x'][index], 
            150, -200, 100, 
                'Bottom cluster x (mm)')

        plt.plot_hists(cut_flow['ecal_cluster_dt'], 
                       np.linspace(-10, 10, 101),
                       labels=plt_labels,
                       ylog=True,
                       label_loc=10,
                       x_label='Cluster dt (ns)')

        plt.plot_hists(cut_flow['top_eop'], 
                       np.linspace(0, 2, 101),
                       labels=plt_labels,
                       ylog=True,
                       label_loc=10,
                       x_label='E/p')
        
        plt.plot_hists(cut_flow['bot_eop'], 
                       np.linspace(0, 2, 101),
                       labels=plt_labels,
                       ylog=True,
                       label_loc=10,
                       x_label='E/p')

        plt.plot_hist2d(cut_flow['mass'][len(cut_flow['mass']) - 1], 
                        cut_flow['top_eop'][len(cut_flow['top_eop']) - 1],
                        np.linspace(0.025, 0.04, 251),
                        np.linspace(0, 2, 101),
                        x_label='$m(e^-e^-)$ GeV',
                        y_label='E/p')

        plt.close()
