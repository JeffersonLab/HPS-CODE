/**
 * 
 * @file SvtTrack.h
 * @brief Class used to describe an HPS SVT track.
 * @author Omar Moreno <omoreno1@ucsc.edu>
 *         Santa Cruz Institute for Particle Physics
 *         University of California, Santa Cruz
 * @date February 19, 2013
 * 
 */

#ifndef __SVT_TRACK_H__
#define __SVT_TRACK_H__

//------------------//
//--- C++ StdLib ---//
//------------------//
#include<vector>
#include <stdio.h>

//------------//
//--- ROOT ---//
//------------//
#include <TObject.h>
#include <TClonesArray.h>
#include <TRefArray.h>
#include <TRef.h>

//-----------------//
//--- HPS Event ---//
//-----------------//
#include <HpsParticle.h>

/** Forward declarations */
class SvtHit;

class SvtTrack : public TObject {

    // TODO: Add more documentation

    public:

        /** Constructor */
        SvtTrack();

        /**
         * Copy constructor
         *
         * @param svtTrackObj An SvtTrack object
         */
        SvtTrack(const SvtTrack &svtTrackObj);

        /** Destructor */
        ~SvtTrack();

        /**
         * Copy assignment operator
         *
         * @param svtTrackObj An SvtTrack object
         */
        SvtTrack &operator=(const SvtTrack &svtTrackObj);
       
        /** Reset the SvtTrack object */ 
        void Clear(Option_t *option="");

        /**
         * Add a reference to an SvtHit.
         *
         * @param hit : An SvtHit
         */
        void addHit(SvtHit* hit); 

        /**
         * Set the track parameters.
         *
         * @param d0 Distance of closest approach to the reference point.
         * @param phi0 The azimuthal angle of the momentum at the distance of
         *             closest approach. 
         * @param omega The curvature of the track.
         * @param tan_lambda The slope of the track in the SY plane.
         * @param z0 The y position of the track at the distance of closest 
         *           approach.
         */
        void setTrackParameters(const double d0, 
                const double phi0, 
                const double omega, 
                const double tan_lambda,
                const double z0);
        
        /**
         * Set the chi^2 of the fit to the track.
         *
         * @param chi_squared The chi^2 of the fit to the track.
         */
        void setChi2(const double chi_squared) { this->chi_squared = chi_squared; };
       
        /**
         * Set the track time.
         *
         * @param track_time The track time.
         */
        void setTrackTime(const double track_time) { this->track_time = track_time; };

        /**
         * Set the isolation variable of the given layer.
         *
         * @param layer Layer number associated with the given isolation value.
         * @param isolation The isolation variable. 
         */ 
        void setIsolation(const int layer, const double isolation) { this->isolation[layer] = isolation; };

        /**
         * The the volume (Top/Bottom) that the track is located in.
         *
         * @param track_volume The track volume.
         */
        void setTrackVolume(const int track_volume) { this->track_volume = track_volume; };

        /**
         * Set the HpsParticle associated with this track.  This can be used to
         * retrieve additional track properties such as the momentum and charge.
         *
         * @param fs_particle : Final state HpsParticle associated with this track
         */
        void setParticle(HpsParticle* fs_particle) { this->fs_particle = (TObject*) fs_particle; };

        /**
         * Set the extrapolated track position at the Ecal face. The 
         * extrapolation is assumed to use the full 3D field map.
         *
         * @parm position The extrapolated track position at the Ecal
         */
        void setPositionAtEcal(const float* position);

        /**
         * Set the track type.  For more details, see {@link StrategyType} and
         * {@link TrackType}.
         *
         * @param type The track type. 
         */
        void setType(const int type) { this->type = type; }; 

        /**
         * Get the distance of closest approach to the reference point.
         *
         * @return The distance of closest approach to the reference point.
         */
        double getD0() const { return d0; };
        
        /**
         * Get the azimuthal angle of the momentum at the distance of closest
         * approach.
         *
         * @return The azimuthal angle of the momentum at the distance of 
         *         closest approach.  
         */
        double getPhi0() const { return phi0; };
        
        /**
         * Get the curvature of the track.
         *
         * @return The curvature of the track.
         */
        double getOmega() const { return omega; };
        
        /**
         * Get the slope of the track in the SY plane.
         * 
         * @return The curvature of the track in the SY plane.
         */
        double getTanLambda() const { return tan_lambda; };

        /**
         * Get the y position of the track at the distance of closest approach.
         *
         * @return The y position of the track at the distance of closest 
         *         approach.
         */
        double getZ0() const { return z0; };
        
        /**
         * Get the chi^2 of the fit to the track.
         *
         * @return the chi^2 of the fit to the track.
         */
        double getChi2() const { return chi_squared; };

        /**
         * Get the time of the track.
         *
         * @return The track time.
         */
        double getTrackTime() const { return track_time; }; 

        /**
         * Get the isolation value of the given layer.
         *
         * @param layer The SVT layer of interest.
         * @return The isolation value of the given layer.
         */
        double getIsolation(const int layer) const { return isolation[layer]; }; 

        /**
         * Get the charge of a the track.
         *
         * @return The charge associated of the track.
         */
        int getCharge(); 

        /**
         * Get the track type.
         *
         * @return The track type.
         */
        int getType() const { return type; }; 

        /**
         * Get the track momentum.
         *
         * @return The track momentum.
         */
        std::vector<double> getMomentum(); 
        
        /**
         * Get an array of references to the hits associated with this track.
         *
         * @return A reference to the hits associated with this track.
         */
        TRefArray* getSvtHits() const;

        /**
         * Get the {@link HpsParticle} associated with this track.
         *
         * @return The {@link HpsParticle} associated with this track.
         */
        TRef getParticle() const { return fs_particle; }; 

        /**
         * @returns True if the track is in the top SVT volume, false otherwise.
         */
        bool isTopTrack() const { return track_volume ? false : true; };

        /**
         * @return True if the track is in the bottom SVT volume, false otherwise.
         */
        bool isBottomTrack() const { return track_volume ? true : false; };

        ClassDef(SvtTrack, 1);

    private:

        /** Reference to the 3D hits associated with this track. */
        TRefArray* svt_hits; 

        /** Reference to the reconstructed particle associated with this track. */
        TRef fs_particle;

        /** Array used to store the isolation variables for each of the sensor layers. */
        double isolation[12];

        /** The number of 3D hits associated with this track. */
        int n_hits; 

        /** The volume to which this track belongs to. */
        int track_volume; 

        /** The track type. */
        int type; 

        /** The distance of closest approach to the reference point. */
        double d0; 
       
        /**
         * The azimuthal angle of the momentum at the position of closest
         * approach to the reference point. 
        */
        double phi0;
        
        /**
         * The track curvature. The curvature is positive (negative) if the particle has a
         * positive (negative) charge.
         */
        double omega; 

        /**
         * The slope of the track in the SY plane where S is the arc length of 
         * the helix in the xz plane.
         */ 
        double tan_lambda;
        
        /** 
         * The y position of the track at the distance of closest approach 
         * in the xz plane.
         */
        double z0; 
        
        /** The chi^2 of the track fit. */ 
        double chi_squared;

        /** 
         * The time of the track.  This is currently the average time of all
         * hits composing the track.
         */
        double track_time;
        
        /** The x position of the extrapolated track at the Ecal face. */ 
        double x_at_ecal;
        
        /** The y position of the extrapolated track at the Ecal face. */ 
        double y_at_ecal;
        
        /** The z position of the extrapolated track at the Ecal face. */ 
        double z_at_ecal;
            
}; // SvtTrack

#endif // __SVT_TRACK_H__
