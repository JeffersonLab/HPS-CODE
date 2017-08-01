/**
 * @file TrackClusterMatcher.h
 * @brief  Class used to encapsulate various utilities related to track-cluster
 *         matching.
 * @author Omar Moreno, SLAC National Accelerator Laboratory
 */

#include <TrackClusterMatcher.h>

TrackClusterMatcher::TrackClusterMatcher() {  
}

TrackClusterMatcher::~TrackClusterMatcher() { 
}

bool TrackClusterMatcher::hasGoodMatch(HpsParticle* particle) { 

    // Check that the two daughters have an SvtTrack associated with them.
    // If not, return false.
    if (particle->getTracks()->GetEntriesFast() != 2) return false; 

    // Get the daughter particles composing this particle. 
    TRefArray* daughter_particles = particle->getParticles();

    if (((HpsParticle*) daughter_particles->At(0))->getGoodnessOfPID() > 10) return false; 
    if (((HpsParticle*) daughter_particles->At(1))->getGoodnessOfPID() > 10) return false;
   
    if (loose_selection_) return true;

    double top_index = 0;
    double bot_index = 1;
    if (((SvtTrack*) ((HpsParticle*) particle->getTracks()->At(bot_index)))->isTopTrack()) { 
        top_index = 1;
        bot_index = 0;
    }
   
    top_index = 0;
    bot_index = 1;
    if (((EcalCluster*) ((HpsParticle*) particle->getClusters()->At(bot_index)))->getPosition()[1] > 0) { 
        top_index = 1;
        bot_index = 0;
    }

    EcalCluster* top_cluster{(EcalCluster*) ((HpsParticle*) particle->getClusters()->At(top_index))};
    EcalCluster* bot_cluster{(EcalCluster*) ((HpsParticle*) particle->getClusters()->At(bot_index))};

    SvtTrack* top_track{(SvtTrack*) ((HpsParticle*) particle->getTracks()->At(top_index))};
    SvtTrack* bot_track{(SvtTrack*) ((HpsParticle*) particle->getTracks()->At(bot_index))};
    
    double top_track_cluster_dt = top_cluster->getClusterTime() - top_track->getTrackTime();
    double bot_track_cluster_dt = bot_cluster->getClusterTime() - bot_track->getTrackTime();
    
    if (top_track_cluster_dt < 38 || top_track_cluster_dt > 47) return false; 
    if (bot_track_cluster_dt < 36 || bot_track_cluster_dt > 49) return false; 

    return true; 
}

