/**
 *	@file GblDataWriter.cxx
 *	@brief Class used to write GBL collections to the DST.
 *	@author Per Hansson Adrian <phansson@slac.stanford.edu>
 *	         SLAC
 *	@author Omar Moreno <omoreno1@ucsc.edu>
 *	         Santa Cruz Institute for Particle Physics
 *	         University of California, Santa Cruz
 *	@date Feb. 12, 2014
 */

#include <GblDataWriter.h>

// definition of generic collection sizes
// these will need to be matched to the input DST
static const unsigned int GBL_TRACK_DATA_DOUBLES = 14;
static const unsigned int GBL_TRACK_DATA_INTS = 1;
static const unsigned int GBL_STRIP_DATA_DOUBLES = 22;
static const unsigned int GBL_STRIP_DATA_INTS = 1;
static const unsigned int PRJ_PER_TO_CL_N_ELEMENTS = 9; // n matrix elements in projection matrix

GblDataWriter::GblDataWriter() 
    : gbl_fitter(new HpsGblFitter()),
      b_field(std::numeric_limits<double>::quiet_NaN()),
      track_col_name("MatchedTracks"), 
      trk_to_gbltrk_rel_col_name("TrackToGBLTrack"), 
      gbltrk_to_gblstrip_rel_col_name("GBLTrackToStripData"),
      debug(false) { 
}

GblDataWriter::~GblDataWriter() {
    delete gbl_fitter;
}

void GblDataWriter::setDebug(bool debug) {
    debug = debug;
}

void GblDataWriter::writeData(EVENT::LCEvent* event, HpsEvent* hps_event) {

    // Check that the b-field has been set.  If it hasn't, throw a runtime 
    // exception. The b-field is needed by the GBL fitter.
    if (std::isnan(b_field)) { 
        throw std::runtime_error("[ GblDataWriter ]: The b-field has not been set.");
    }
   
    // Set the B-field that will be used by the fitter 
    gbl_fitter->setBField(b_field);
    gbl_fitter->setDebug(debug);

    if (debug) {
        std::cout << "GblDataWriter: write data start " << std::endl;
    }

    // Get the collection of LCRelations between a GblTrackData and the 
    // corresponding Track (seed track). If the event doesn't have the
    // specified collection, throw an exception. Usually, if this 
    // collection is missing, something went wrong at the recon stage.
	IMPL::LCCollectionVec* trk_to_gbltrk_relations = NULL;
    try {
		trk_to_gbltrk_relations 
            = (IMPL::LCCollectionVec*) event->getCollection(trk_to_gbltrk_rel_col_name);
    } catch(EVENT::DataNotAvailableException e) {
        throw std::runtime_error("[ GblDataWriter ]: The collection " 
                  + trk_to_gbltrk_rel_col_name + " couldn't be found");
    }

    // Get the collection of LCRelations between a GblStripData (GBL hit) 
    // object and the corresponding GblTrackData object.  If the event
    // doesn't have the specified collection, throw an exception. Usually, 
    // it this collection is missing, something went wrong at the recon stage.
	IMPL::LCCollectionVec* gbltrk_to_gblstrip_relations = NULL;
    try {
        gbltrk_to_gblstrip_relations 
            = (IMPL::LCCollectionVec*) event->getCollection(gbltrk_to_gblstrip_rel_col_name);
    } catch(EVENT::DataNotAvailableException e) {
        throw std::runtime_error("[ GblDataWriter ]: The collection " 
                  + gbltrk_to_gblstrip_rel_col_name + " couldn't be found");
    }

    // Create a relation navigator between GblTrackData and GblStrips.  
    // This allows for quick retrieval of GblStrips associated with a 
    // GblTrackData object.
    // TODO: Should this move outside of this loop?
    UTIL::LCRelationNavigator* rel_gbl_strip_nav = new UTIL::LCRelationNavigator(gbltrk_to_gblstrip_relations);

    // Loop over all Track to GblTrackData relations
    for (int rel_n = 0; rel_n < trk_to_gbltrk_relations->getNumberOfElements(); ++rel_n) {

        // Get a Track to GblTrackData relation from the event        
		IMPL::LCRelationImpl* trk_to_gbltrk_relation 
            = (IMPL::LCRelationImpl*) trk_to_gbltrk_relations->getElementAt(rel_n);

        
        // Get the GblTrackData from the relation
		IMPL::LCGenericObjectImpl* gbl_track_data 
            = (IMPL::LCGenericObjectImpl*) trk_to_gbltrk_relation->getTo();

        // Get the track related to the GblTrackData
		IMPL::TrackImpl* track = (IMPL::TrackImpl*) trk_to_gbltrk_relation->getFrom(); 
        
        // Check that the data structure is the correct length.  If it's not, throw a 
        // runtime exception.  
        // Should this only be checked a few times?  What kind of perfomance hit is this
        // causing?
        if (gbl_track_data->getNInt() !=  GBL_TRACK_DATA_INTS) {
            throw std::runtime_error("[ GblDataWriter ]: Error! The data structure has the wrong number of ints");
        }

        // Check that the data structure is the correct length
        if (gbl_track_data->getNDouble() != GBL_TRACK_DATA_DOUBLES) {
            throw std::runtime_error("[ GblDataWriter ]: Error! The data structure has the wrong number of doubles");
        }
        
        // Add a GblTrackData object to the HpsEvent
		GblTrackData* hps_gbl_track_data = hps_event->addGblTrackData();

        // Loop through all of the tracks in the HpsEvent and find the one
        // that matches the track associated with the GblTrackData
        // TODO: The seed track shouldn't be associated with a GblTrack instead
        //       of a GblTrackData object.
        SvtTrack* svt_track = NULL;
        for (int track_n = 0; track_n < hps_event->getNumberOfTracks(); ++track_n) { 
            
            // Use the track fit chi^2 to find the match
            // TODO: Verify that the track fit chit^2 is enough to conclude
            //       that the tracks match  
            if (track->getChi2() == hps_event->getTrack(track_n)->getChi2()) {
                svt_track = hps_event->getTrack(track_n); 
                hps_gbl_track_data->setTrack(svt_track);
                break;  
            }
        }

        // Add the elements of the projection matrix
        for (unsigned int idx = 0; idx < PRJ_PER_TO_CL_N_ELEMENTS; ++idx) {
             unsigned int row = static_cast<unsigned int>(floor(static_cast<double>(idx)/3.0));
             unsigned int col = idx % 3;        
            //std::cout << "prjmat " << idx << "," << row << "," << col << " -> " 
            //          << gblTrackGeneric->getDoubleVal(5+idx) << std::endl;
            hps_gbl_track_data->setPrjPerToCl(row, col, gbl_track_data->getDoubleVal(5+idx));
        }   
 
        // Get the list of GblStrips that are related to the GblTrackData object
        EVENT::LCObjectVec gbl_strips = rel_gbl_strip_nav->getRelatedToObjects(gbl_track_data);
            
        if (debug) {
            std::cout << "GblDataWriter: found " << gbl_strips.size() 
                      << " GBL strips for this GBL track data object" << std::endl;
        }
       
        // Add all GblStrips to the GblTrackData object 
        for (uint gbl_strip_n = 0; gbl_strip_n < gbl_strips.size(); ++gbl_strip_n) {
            
            if (debug) {
                std::cout << "GblDataWriter: processing GBLStrip " << gbl_strip_n << std::endl;
            }

            // Get the nth GblStrip from the collection
            IMPL::LCGenericObjectImpl* gbl_strip = (IMPL::LCGenericObjectImpl*) gbl_strips.at(gbl_strip_n);

            // Add the GblStrip to the HpsEvent
            GblStripData* hps_gbl_strip = hps_event->addGblStripData();

            if ( gbl_strip->getNInt() !=  GBL_STRIP_DATA_INTS ) {
                throw std::runtime_error("[ GblDataWriter ]: Error! The data structure has the wrong number of ints");
            }

            if ( gbl_strip->getNDouble() != GBL_STRIP_DATA_DOUBLES ) {
                throw std::runtime_error("[ GblDataWriter ]: Error! The data structure has the wrong number of doubles");
            }
            
            // Set the GBL strip ID
            hps_gbl_strip->SetId(gbl_strip->getIntVal(0));

            hps_gbl_strip->SetPath3D(gbl_strip->getDoubleVal(0));
            
            hps_gbl_strip->SetPath(gbl_strip->getDoubleVal(1));
            
            hps_gbl_strip->SetU(gbl_strip->getDoubleVal(2),
                    gbl_strip->getDoubleVal(3),
                    gbl_strip->getDoubleVal(4));
            
            hps_gbl_strip->SetV(gbl_strip->getDoubleVal(5),
                    gbl_strip->getDoubleVal(6),
                    gbl_strip->getDoubleVal(7));
            
            hps_gbl_strip->SetW(gbl_strip->getDoubleVal(8),
                    gbl_strip->getDoubleVal(9),
                    gbl_strip->getDoubleVal(10));
            
            hps_gbl_strip->SetGlobalTrackDir(gbl_strip->getDoubleVal(11),
                    gbl_strip->getDoubleVal(12),
                    gbl_strip->getDoubleVal(13));
            
            hps_gbl_strip->SetPhi(gbl_strip->getDoubleVal(14));
            
            hps_gbl_strip->SetUmeas(gbl_strip->getDoubleVal(15));
            
            hps_gbl_strip->SetTrackPos(gbl_strip->getDoubleVal(16),
                    gbl_strip->getDoubleVal(17),
                    gbl_strip->getDoubleVal(18));
            
            hps_gbl_strip->SetUmeasErr(gbl_strip->getDoubleVal(19));
            
            hps_gbl_strip->SetMSAngle(gbl_strip->getDoubleVal(20));
            
            hps_gbl_strip->SetLambda(gbl_strip->getDoubleVal(21));

            // Add a reference to the GblTrackData object
            hps_gbl_track_data->addStrip(hps_gbl_strip); 
        
        }  // GBLStripData

        if (debug) {
            std::cout << "GblDataWriter: Track parameters from LCIO GblTrackData collection: " << std::endl;
            std::cout << "kappa: " << gbl_track_data->getDoubleVal(0) << "\n"
                      << "theta: " << gbl_track_data->getDoubleVal(1) << "\n"
                      << "phi:   " << gbl_track_data->getDoubleVal(2) << "\n"
                      << "d0:    " << gbl_track_data->getDoubleVal(3) << "\n"
                      << "z0:    " << gbl_track_data->getDoubleVal(4) << std::endl;
            std::cout << "GblDataWriter: Track parameters calculated by DST GblTrackData\n" 
                      << hps_gbl_track_data->toString() << std::endl;
        }

        //--- GBL refit ---//
        //-----------------//

        // Clear any previous fit information
        gbl_fitter->clear();

        // Do the GBL refit
        HpsGblFitter::HpsGblFitStatus fit_status = gbl_fitter->fit(hps_gbl_track_data);

        // If the fit was successful, add a GBL track to the event
        if (fit_status == HpsGblFitter::OK) { 
            
            if (debug) { 
                std::cout << "[ GblDataWriter ]: Fit was successful!" << std::endl;
                std::cout << "[ GblDataWriter ]: Adding a GBL track to the event." << std::endl;
            }

            // Add a GBL track to the HpsEvent
            GblTrack* hps_gbl_track = hps_event->addGblTrack(); 

            // Set the GBL track properties
            gbl_fitter->setTrackProperties(hps_gbl_track, svt_track, hps_gbl_track_data);
            
            // Set the seed SvtTrack associated with this GblTrack
            hps_gbl_track->setSeedTrack(svt_track);  
 
        } else { 
            
            if (debug) { 
                std::cout << "[ GblDataWriter ]: Fit failed!" << std::endl;
            }
        }

    } // GBLTrackData

    delete rel_gbl_strip_nav;

    if (debug) {
        std::cout << "GblDataWriter: write data end " << std::endl;
    }
}


