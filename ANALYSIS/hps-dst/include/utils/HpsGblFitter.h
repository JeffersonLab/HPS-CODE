/**
 * @file: HpsGblFitter.h
 * @brief: GBL track refit
 * @author: Per Hansson Adrian <phansson@slac.stanford.edu>
 *          SLAC
 * @date: February 13, 2014 
 */

#ifndef __HPS_GBL_FITTER_H__
#define __HPS_GBL_FITTER_H__

//------------------//
//--- C++ StdLib ---//
//------------------//
#include <cstdlib>
#include <cmath>
#include <map>

//-----------//
//--- GBL ---//
//-----------//
#include <GblTrajectory.h>
#include <GblPoint.h>
#include <MilleBinary.h>

//------------//
//--- ROOT ---//
//------------//
#include <TMatrixD.h>
#include <TRandom.h>
#include <TRandom3.h>

//-----------//
//--- DST ---//
//-----------//
#include <GblStripData.h>
#include <GblTrackData.h>
#include <GblTrack.h>

class HpsGblFitter {

    public:

        enum HpsGblFitStatus {
            OK,INVALIDTRAJ,ERROR
        };

        /**
         * Default Constructor
         */
        HpsGblFitter();

        /**
         * Destructor
         */
        ~HpsGblFitter();
        
        /**
         * Do a GBL refit.
         *
         * @param track : GblTrackData that will be used to fit the track
         * @return GBL fit status
         */
        HpsGblFitStatus fit(const GblTrackData* track);  
        
        /**
         * Clear the fitter of any previous fit information.
         */
        void clear();
        
        /**
         * Enable/Disable debug output.
         *
         * @param debug : true to enable debug, false to disable it.
         */
        void setDebug(const bool debug) { this->debug = debug; };

        /**
         * Set the magnetic field strength in Tesla
         *
         * @param b_field : The magnetic field strength
         */
        void setBField(const double b_field); 

        /**
         * Set the GBL track properties based on the information from the fit.
         *
         * @param track : A GBL track object
         * @param track_data : The GBL track data used in the track refit
         */
        void setTrackProperties(GblTrack* track, const SvtTrack* seed_track, const GblTrackData* track_data);

    private:

        TMatrixD gblSimpleJacobianLambdaPhi(double ds, double cosl, double bfac);

        gbl::GblTrajectory * m_traj;
        TRandom *m_r;
        
        double b_field;
        double chi2;
        double lost_weight;
       
        int ndf;

        bool debug;
}; // HpsGblFitter

#endif // __HPS_GBL_FITTER_H__
