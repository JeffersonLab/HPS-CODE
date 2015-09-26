/**
 * 
 * @file SvtDataWriter.cxx
 * @brief Data writer used to convert LCIO Tracks and TrackerHits
 *        to SvtTracks and SvtHits and add them to the HPS event.
 * @author Omar Moreno <omoreno1@ucsc.edu>
 *         Santa Cruz Institute for Particle Physics
 *         University of California, Santa Cruz
 * @date January 2, 2013
 *
 */

#include <SvtDataWriter.h>

SvtDataWriter::SvtDataWriter()  
    : track_data_collection_name("TrackData"), 
      track_data_rel_collection_name("TrackDataRelations") { 
}

SvtDataWriter::~SvtDataWriter() {
}

void SvtDataWriter::writeData(EVENT::LCEvent* event, HpsEvent* hps_event) {
   
    // Get the collection of 3D hits from the LCIO event. If no such collection 
    // exist, a DataNotAvailableException is thrown
    EVENT::LCCollection* tracker_hits = (EVENT::LCCollection*) event->getCollection("RotatedHelicalTrackHits");

    // Create a map from an LCIO TrackerHit to a SvtHit. This will be used when
    // assigning references to a track
    // TODO: Use an unordered map for faster access
    std::map<EVENT::TrackerHit*, SvtHit*> svt_hit_map; 

    // Loop over all of the 3D hits in the LCIO event and add them to the 
    // HPS event
    for (int tracker_hit_n = 0; tracker_hit_n < tracker_hits->getNumberOfElements(); ++tracker_hit_n) { 
        
        // Get a 3D hit from the list of hits
        EVENT::TrackerHit* tracker_hit = (EVENT::TrackerHit*) tracker_hits->getElementAt(tracker_hit_n);

        // Add an SvtHit object to the HPS event
        SvtHit* svt_hit = hps_event->addSvtHit();

        // Set the SvtHit layer
        svt_hit->setLayer(TrackUtils::getLayer(tracker_hit));
                
        // Rotate the position of the LCIO TrackerHit and Set the position
        // of the SvtHit
        double hit_position_lcsim[3];
        memcpy(&hit_position_lcsim, tracker_hit->getPosition(), 3*sizeof(double));   
        double hit_position_jlab[3] = {0}; 
        hit_position_jlab[0] = hit_position_lcsim[1]; 
        hit_position_jlab[1] = hit_position_lcsim[2]; 
        hit_position_jlab[2] = hit_position_lcsim[0]; 
        svt_hit->setPosition(hit_position_jlab);

        // Set the covariance matrix of the SvtHit
        svt_hit->setCovarianceMatrix(tracker_hit->getCovMatrix());
                
        // Set the time of the SvtHit
        svt_hit->setTime(tracker_hit->getTime());

        // Map the TrackerHit object to the corresponding SvtHit object. This
        // will be used later when setting references for hits on tracks.
        svt_hit_map[tracker_hit] = svt_hit; 
    }

    // Get all track collections from the event
    std::vector<EVENT::LCCollection*> track_collections = DstUtils::getCollections(event, EVENT::LCIO::TRACK);

    // Get the collection of LCRelations between track data variables 
    // (TrackData) and the corresponding track.
    EVENT::LCCollection* track_data 
        = (EVENT::LCCollection*) event->getCollection(track_data_rel_collection_name);

    // Instantiate a LCRelation navigator which will allow faster access
    // to TrackData objects  
    UTIL::LCRelationNavigator* track_data_nav = new UTIL::LCRelationNavigator(track_data);

    // Loop over all the track collections and process them
    for (auto tracks : track_collections) { 
        
        // Loop over all the LCIO Tracks and add them to the HPS event.
        for (int track_n = 0; track_n < tracks->getNumberOfElements(); ++track_n) {
        
            // Get a LCIO Track from the LCIO event
            EVENT::Track* track = (EVENT::Track*) tracks->getElementAt(track_n);

            // Add an SvtTrack object to the HPS event
            SvtTrack* svt_track = hps_event->addTrack(); 
            
            // Set the SvtTrack track parameters
            svt_track->setTrackParameters(track->getD0(), 
                                          track->getPhi(), 
                                          track->getOmega(), 
                                          track->getTanLambda(), 
                                          track->getZ0());
           
            // Set the SvtTrack type
            svt_track->setType(track->getType()); 

            // Set the SvtTrack fit chi^2
            svt_track->setChi2(track->getChi2());

            // Set the position of the extrapolated track at the Ecal face. The
            // extrapolation uses the full 3D field map.
            svt_track->setPositionAtEcal(track->getTrackStates()[1]->getReferencePoint()); 
        
            // Get the list of TrackData associated with the LCIO Track
            EVENT::LCObjectVec track_data_list = track_data_nav->getRelatedFromObjects(track);
            
            // The container of TrackData objects should only contain a single
            //  object.  If not, throw an exception.
            if (track_data_list.size() != 1) { 
                throw std::runtime_error("[ SvtDataWriter ]: The data structure has the wrong format.");
            }

            // Get the TrackData GenericObject associated with the LCIO Track
            IMPL::LCGenericObjectImpl* track_datum = (IMPL::LCGenericObjectImpl*) track_data_list.at(0);

            // Check that the TrackData data structure is correct.  If it's
            // not, throw a runtime exception.   
            if (track_datum->getNDouble() != 12 || track_datum->getNFloat() != 1 
                    || track_datum->getNInt() != 1) {
                throw std::runtime_error("[ SvtDataWriter ]: The collection " + track_data_collection_name 
                        + " has the wrong structure.");
            }

            // Set the SvtTrack isolation values
            for (int iso_index = 0; iso_index < track_datum->getNDouble(); ++iso_index) { 
                svt_track->setIsolation(iso_index, track_datum->getDoubleVal(iso_index));
            }
        
            // Set the SvtTrack time
            svt_track->setTrackTime(track_datum->getFloatVal(0));

            // Set the volume (top/bottom) in which the SvtTrack resides
            svt_track->setTrackVolume(track_datum->getIntVal(0));
        
            // Get the collection of 3D hits associated with a LCIO Track
            EVENT::TrackerHitVec tracker_hits = track->getTrackerHits();

            //  Iterate through the collection of 3D hits (TrackerHit objects)
            //  associated with a track, find the corresponding hits in the HPS
            //  event and add references to the track
            for (auto tracker_hit : tracker_hits) { 
                
                // Add a reference to the hit
                svt_track->addHit(svt_hit_map[tracker_hit]);  
            }
        }
    }

    // Delete the LCRelations navigator object
    delete track_data_nav;
}
