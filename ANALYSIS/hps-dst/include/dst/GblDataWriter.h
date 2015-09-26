/**
 *	@file GblDataWriter.h
 *	@brief Class used to write GBL collections to the DST.
 *	@author Per Hansson Adrian <phansson@slac.stanford.edu>
 *	         SLAC
 *	@author Omar Moreno <omoreno1@ucsc.edu>
 *	         Santa Cruz Institute for Particle Physics
 *	         University of California, Santa Cruz
 *	@date Feb. 12, 2014
 */

#ifndef __GBL_DATA_WRITER_H__
#define __GBL_DATA_WRITER_H__

//------------------//
//--- C++ StdLib ---//
//------------------//
#include <cstdlib>
#include <cmath>
#include <iostream>
#include <limits>

//------------//
//--- LCIO ---//
//------------//
#include <IMPL/LCCollectionVec.h>
#include <IMPL/LCGenericObjectImpl.h>
#include <IMPL/LCRelationImpl.h>
#include <UTIL/LCRelationNavigator.h>
#include <IMPL/TrackImpl.h>

//---------------//
//--- HPS DST ---//
//---------------//
#include <DataWriter.h>

//-----------------//
//--- HPS Event ---//
//-----------------//
#include <GblTrackData.h>
#include <GblStripData.h>

//-------------//
//--- Utils ---//
//-------------//
#include <HpsGblFitter.h>

// Forward declarations
class SvtTrack; 

class GblDataWriter : public DataWriter {

    public:

        /**
         * Default constructor.
         */
        GblDataWriter();

        /**
         * Destructor.
         */
        ~GblDataWriter();

        /**
         * Enable/Disable debug output.
         *
         * @param debug : true to enable debug, false to disable it.
         */
        void setDebug(bool debug);
        
        /**
         * Main processing method used to read GBL collections from an LCEvent
         * and write them to an HpsEvent.
         *
         * @param event : LCEvent object to read GBL LCIO collection from
         * @pram hps_event : HpsEvent object that the collections will be written to
         */
        void writeData(EVENT::LCEvent* event, HpsEvent* hps_event);

        /**
         * Set the magnetic field strength in Tesla
         *
         * @param b_field : The magnetic field strength
         */
        void setBField(const double b_field) { this->b_field = b_field; };

    private:

        HpsGblFitter* gbl_fitter; 

        double b_field;

        std::string track_col_name;
        std::string trk_to_gbltrk_rel_col_name;
        std::string gbltrk_to_gblstrip_rel_col_name;

        bool debug;
			

}; // GblDataWriter

#endif // __GBL_DATA_WRITER_H__
