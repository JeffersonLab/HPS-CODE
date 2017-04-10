/**
 * @file TridentAnalysis.h
 * @brief Analysis used to look at Tridents.
 * @author Omar Moreno, SLAC National Accelerator Laboratory
 */


#ifndef __TRIDENT_ANALYSIS_H__
#define __TRIDENT_ANALYSIS_H__

//------------------//
//   HPS Analysis   //
//------------------//
#include <AnalysisUtils.h>
#include <HpsAnalysis.h>
#include <EcalUtils.h>
#include <FlatTupleMaker.h>
#include <TrackClusterMatcher.h>

//-------------//
//   HPS DST   //
//-------------//
#include <HpsEvent.h>
#include <HpsParticle.h>

class TridentAnalysis : public HpsAnalysis { 

    public: 

        /** Constructor */
        TridentAnalysis(); 

        /** Destructor */
        ~TridentAnalysis();

        /** Initialize an HPS analysis. */
        void initialize(); 

        /**
         * Process an HpsEvent.
         *
         * @param event HpsEvent that will be processed.
         */
        void processEvent(HpsEvent* event); 

        /** Finalize an HPS analysis. */
        void finalize(); 

        /** Initialize histograms used in this analysis. */
        void bookHistograms(); 

        /** @return A string representation of this analysis. */
        std::string toString();

       /** Enable/disable debug */
       void setDebug(bool debug) { _debug = debug; }; 
    
    protected: 

        /** Name of the class */
        std::string class_name; 
    
    private: 

        /** Get the number of shared hits between the given tracks. */
        int getSharedHitCount(SvtTrack* ftrack, SvtTrack* strack);
        
        std::vector<int> getSharedLayersVec( std::vector<GblTrack*> trks, GblTrack* ftrk);

        std::vector<GblTrack*> getSharedTracks(HpsEvent* event, GblTrack* trk);

        GblTrack* getBestChi2(std::vector<GblTrack*> trks);

        HpsParticle* getBestVertexFitChi2(std::vector<HpsParticle*> particles);

        //std::map<GblTrack*, int> buildSharedHitMap(HpsEvent* event);

        bool electronsShareHits(std::vector<HpsParticle*> particles, std::map<GblTrack*, int> shared_hit_map); 

        HpsParticle* getBestElectronChi2(std::vector<HpsParticle*> particles);

        bool passFeeCut(HpsParticle* particle); 

        void printDebug(std::string message); 

        /** Utility used to create ROOT ntuples. */
        FlatTupleMaker* tuple{new FlatTupleMaker("trident_analysis.root", "results")}; 

        /** Track-Ecal cluster matcher. */
        TrackClusterMatcher* matcher{new TrackClusterMatcher()}; 

        /** A set of Ecal utilities */
        EcalUtils* ecal_utils{new EcalUtils()};

        /** Total number of events processed */
        double _event_counter{0};

        /** Total number of events with tracks */
        double _event_has_track{0};

        /** Total number of events with a positron */
        double event_has_positron{0};

        /** Events with an isolated positron */
        double _event_has_iso_positron{0};

        /** Total number of events with only a single positron. */
        double event_has_single_positron{0};

        /** Total events with positron that passes initial selection */
        double _event_has_usable_positron{0};

        /** Total positrons that pass initial selection. */
        double _positron_counter{0};

        /** Total number of events with a good cluster pair */
        double event_has_good_cluster_pair{0};

        double total_v0_good_cluster_pair{0}; 

        double total_v0_good_track_match{0};

        /** Total number of v0 before cuts. */
        double _v0_counter{0};

        /** Total v0's created from positrons in the map. */
        double _v0_pos_counter{0};

        /** Total number of v0's that pass the FEE cut. */
        double _v0_pass_fee{0}; 

        /** Total v0 candidates */
        double _v0_cands{0};

        bool _debug{false};

}; // TridentAnalysis

#endif // __TRIDENT_ANALYSIS_H__
