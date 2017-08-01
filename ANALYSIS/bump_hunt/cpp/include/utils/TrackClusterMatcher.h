/**
 * @file TrackClusterMatcher.h
 * @brief  Class used to encapsulate various utilities related to track-cluster
 *         matching.
 * @author Omar Moreno, SLAC National Accelerator Laboratory
 */

#ifndef __TRACK_CLUSTER_MATCHER_H__
#define __TRACK_CLUSTER_MATCHER_H__

//------------------//
//--- C++ StdLib ---//
//------------------//
#include <map>

//-----------------//
//--- HPS Event ---//
//-----------------//
#include <SvtTrack.h>
#include <EcalCluster.h>
#include <HpsParticle.h>

class TrackClusterMatcher {

    public: 

        /**
         * Constructor.
         */
        TrackClusterMatcher();

        /**
         * Destructor.
         */
        ~TrackClusterMatcher();

        /**
         *
         */
        bool  hasGoodMatch(HpsParticle* particle); 

        /** Use loose track-cluster matching requirement. */
        void useLooseSelection(bool loose_selection) { loose_selection_ = loose_selection; } 

    private:

        bool loose_selection_{false};

}; // TrackClusterMatcher 

#endif // __TRACK_CLUSTER_MATCHER_H__
