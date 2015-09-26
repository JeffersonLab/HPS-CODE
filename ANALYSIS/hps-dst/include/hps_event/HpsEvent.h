/**
 *
 * @file HpsEvent.h
 * @brief Event class used to encapsulate event information and physics 
 *        collections.
 * @author Omar Moreno <omoreno1@ucsc.edu>
 *         Santa Cruz Institute for Particle Physics
 *         University of California, Santa Cruz
 * @date February 19, 2013
 *
 */

#ifndef __HPS_EVENT_H__
#define __HPS_EVENT_H__

//------------------//
//--- C++ StdLib ---//
//------------------//
#include <iostream>
#include <assert.h>

//-----------//
//-- ROOT ---//
//-----------//
#include <TObject.h>
#include <TClonesArray.h>

//-----------------//
//--- HPS Event ---//
//-----------------//
#include <SvtTrack.h>
#include <SvtHit.h>
#include <EcalCluster.h> 
#include <EcalHit.h>
#include <HpsParticle.h>
#include <HpsMCParticle.h>
#include <GblTrackData.h>
#include <GblStripData.h>
#include <GblTrack.h>

class HpsEvent : public TObject { 

    // TODO: Add documentation

    public:

        /** Constructor */
        HpsEvent();

        /** 
         * Copy Constructor
         *
         * @param hpsEventObj An HpsEvent object 
         */
        HpsEvent(const HpsEvent &hpsEventObj);

        /** Destructor */
        ~HpsEvent();    
        
        /**
         * Copy assignment operator 
         *
         * @param hpsEventObj An HpsEvent object
         */ 
        HpsEvent &operator=(const HpsEvent &hpsEventObj);

        /** */
        void Clear(Option_t *option="");
        
        /** */
        SvtTrack*       addTrack();
        
        /** */
        SvtHit*         addSvtHit();
        
        /** */
        EcalCluster*    addEcalCluster();
        
        /** */
        EcalHit*        addEcalHit();
        
        /**
         * Create an {@link HpsParticle} object with the given 
         * {@link HpsParticle::ParticleType} and add it to the
         * event.
         *
         * @param type The type of particle that is being requested e.g. 
         *             HpsParticle::FINAL_STATE_PARTICLE.
         * @return A pointer to the newly created HpsParticle object. 
         */
        HpsParticle*    addParticle(HpsParticle::ParticleType type); 
        
        /** */
        HpsMCParticle*  addHpsMCParticle();
        
        /** */
        GblTrack*       addGblTrack();
        
        /** */
        GblTrackData*   addGblTrackData();
        
        /** */
        GblStripData*   addGblStripData();

        //--- Setters ---//
        //---------------//

        /**
         *
         */
        void setEventNumber(int event_number){ this->event_number = event_number; };

        /**
         *
         */
        void setPair0Trigger(const int pair0_trigger) { this->pair0_trigger = pair0_trigger; };
        
        /**
         *
         */
        void setPair1Trigger(const int pair1_trigger) { this->pair1_trigger = pair1_trigger; };
        
        /**
         *
         */
        void setPulserTrigger(const int pulser_trigger) { this->pulser_trigger = pulser_trigger; };

        /**
         *
         */
        void setRunNumber(int run_number){ this->run_number = run_number; };

        /**
         *
         */
        void setSingle0Trigger(const int single0_trigger) { this->single0_trigger = single0_trigger; };

        /**
         *
         */
        void setSingle1Trigger(const int single1_trigger) { this->single1_trigger = single1_trigger; };
       
        /**
         * Set the state of the SVT bias during the event i.e. was it on or 
         * off? 
         *
         * @param svt_bias_state The state of the SVT bias. It's set to 0 if 
         *                       the bias was off or 1 if it was on.
         */ 
        void setSvtBiasState(const int svt_bias_state) { this->svt_bias_state = svt_bias_state; }; 

        /**
         * Set the flag indicating whether the event was affected by SVT burst
         * noise.
         *
         * @param svt_burstmode_noise Flag indicating whether an event was affected
         *                        by SVT burst noise.  It's set to 0 if it was
         *                        or 1 if it wasn't.
         */
        void setSvtBurstModeNoise(const int svt_burstmode_noise) { this->svt_burstmode_noise = svt_burstmode_noise; };

        /**
         * Set the state of indicating whether the SVT was open or closed 
         * during an event. 
         *
         * @param svt_position_state The state indicating whether the SVT was 
         *                           open or closed. It's set to 0 if the SVT 
         *                           was open or 1 if it was closed. 
         */ 
        void setSvtPositionState(const int svt_position_state) { this->svt_position_state = svt_position_state; }; 

        /**
         *
         */
        void setTriggerTimeStamp(const long trigger_time_stamp) { this->trigger_time_stamp = trigger_time_stamp; }; 
      
        //--- Getters ---//
        //---------------//

        /** */
        EcalCluster*   getEcalCluster(int);
        
        /** */
        EcalHit*       getEcalHit(int);
        
        /** */
        GblStripData*  getGblStripData(int);
       
        /** */
        GblTrack*      getGblTrack(int);
        
        /** */
        GblTrackData*  getGblTrackData(int);
        
        /** */
        HpsMCParticle* getMCParticle(int);
        
        /**
         *
         */ 
        int getEventNumber() const  { return event_number; };

        /** */
        int getNumberOfEcalClusters()   const  { return n_ecal_clusters; };
       
        /** */ 
        int getNumberOfGblStripData()   const  { return n_gbl_strips_data; };
        
        /** */
        int getNumberOfGblTracks()      const  { return n_gbl_tracks; };

        /** */
        int getNumberOfGblTracksData()  const  { return n_gbl_tracks_data; };
        
        /**
         * Get the number of particles ({@link HpsParticle} objects) of the 
         * given {@link HpsParticle::ParticleType} in the event.
         *
         * @param type The type of particle that is being requested e.g. 
         *             HpsParticle::FINAL_STATE_PARTICLE.
         * @return The number of particles of the given type in the event.
         */
        int getNumberOfParticles(HpsParticle::ParticleType type) const; 
        
        /** */
        int getNumberOfSvtHits()        const  { return n_svt_hits; };

        /** */
        int getNumberOfTracks()         const  { return n_tracks; };

        /**
         * Get the particle object ({@link HpsParticle}) of the given type and
         * at the given position in the container from the event.  See the class
         * {@link HpsParticle} for the type of particles that are available.
         *
         * @param type The type of particle that is being requested e.g. 
         *             HpsParticle::FINAL_STATE_PARTICLE.
         * @param particle_index The position of the particle in the container
         * @return An HpsParticle object of the given type and at the given 
         *         position in the container
         * @throws std::runtime_error if the given type is invalid
         *
         */
        HpsParticle*   getParticle(HpsParticle::ParticleType type, int particle_index); 
        
        /**
         *
         */ 
        int getRunNumber() const  { return run_number; };

        /** */
        SvtHit*        getSvtHit(int);

        /** */
        SvtTrack*      getTrack(int);
        
        //---//
        
        /**
         * Indicate whether a pair0 trigger was registered for the event.
         *
         * @return Returns true if a pair0 trigger was registered for the,
         *         false otherwise.
         */
        bool isPair0Trigger() const { return pair0_trigger == 1; };

        /**
         * Indicate whether a pair1 trigger was registered for the event.
         *
         * @return Returns true if a pair1 trigger was registered for the,
         *         false otherwise.
         */      
        bool isPair1Trigger() const { return pair1_trigger == 1; };

        /**
         * Indicate whether a pulser (random) trigger was registered for the 
         * event.
         *
         * @return Returns true if a pulser trigger was registered for the,
         *         false otherwise.
         */
        bool isPulserTrigger() const { return pulser_trigger == 1; };

        /**
         * Indicate whether a single0 trigger was registered for the event.
         *
         * @return Returns true if a single0 trigger was registered for the,
         *         false otherwise.
         */
        bool isSingle0Trigger() const { return single0_trigger == 1; };

        /**
         * Indicate whether a single1 trigger was registered for the event.
         *
         * @return Returns true if a single1 trigger was registered for the,
         *         false otherwise.
         */
        bool isSingle1Trigger() const { return single1_trigger == 1; };

        /**
         * Indicate whether the SVT bias was on during the event.
         *
         * @return Returns true if the bias was one, false otherwise.
         */
        bool isSvtBiasOn() const { return svt_bias_state == 1; };

        /**
         * Indicates whether the SVT was open or closed during an event.
         *
         * @return Returns true if the SVT was closed, false otherwise.
         */ 
        bool isSvtClosed() const { return svt_position_state == 1; }; 

        /**
         * Indicates whether the event was affected by SVT burst noise.
         *
         * @return Returns true if the event has SVT burst noise, false 
         *         otherwise. 
         */
        bool hasSvtBurstModeNoise() const { return svt_burstmode_noise == 0; }; 

        ClassDef(HpsEvent, 1);  

    private:

        /** Collection of beam spot constrained Moller candidates */
        TClonesArray* bsc_moller_candidates; //->
        /** Collection of beam spot constrained v0 candidates */
        TClonesArray* bsc_v0_candidates;     //->
        /** Collection of Ecal clusters */
        TClonesArray* ecal_clusters;         //->
        /** Collection of Ecal hits */
        TClonesArray* ecal_hits;             //->
        /** Collection of final state particles */
        TClonesArray* fs_particles;          //->
        /** Collection of GBLStripClusterData Generic Objects */
        TClonesArray* gbl_strips_data;       //->
        /** Collection of GBL tracks */
        TClonesArray* gbl_tracks;            //->
        /** Collection of GBLTrackData Generic Objects */
        TClonesArray* gbl_tracks_data;       //->
        /** Collection of Monte Carlo particles */
        TClonesArray* mc_particles;          //->
        /** Collection of target constrained Moller candidates */
        TClonesArray* tc_moller_candidates;  //->
        /** Collection of target constrained v0 candidates */
        TClonesArray* tc_v0_candidates;      //->
        /** Collection of SVT tracks */ 
        TClonesArray* tracks;                //->
        /** Collection of SVT 3D hits */
        TClonesArray* svt_hits;              //->
        /** Collection of unconstrained Moller candidates */
        TClonesArray* uc_moller_candidates;  //->
        /** Collection of unconstrained v0 candidates */
        TClonesArray* uc_v0_candidates;      //->

        //-- Event information --//
        //-----------------------//

        /** Event number */
        int event_number;
        
        /** 
         * Flag indicating that a pair0 trigger was registered. It's 
         * set to 1 if it was registered or 0 if it wasn't.
         */
        int pair0_trigger;
        
        /** 
         * Flag indicating that a pair1 trigger was registered. It's 
         * set to 1 if it was registered or 0 if it wasn't.
         */
        int pair1_trigger;
        
        /** 
         * Flag indicating that a pulser (random) trigger was registered. It's 
         * set to 1 if it was registered or 0 if it wasn't.
         */
        int pulser_trigger;
        
        /** Run number */
        int run_number;
        
        /** 
         * Flag indicating that a singles0 trigger was registered. It's 
         * set to 1 if it was registered or 0 if it wasn't.
         */
        int single0_trigger;
        
        /** 
         * Flag indicating that a singles1 trigger was registered. It's 
         * set to 1 if it was registered or 0 if it wasn't.
         */
        int single1_trigger;
        
        /** 
         * Flag indicating the state of the SVT bias. It's set to 0 if the bias
         * was off or 1 if it was on.
         */
        int svt_bias_state;
        
        /**
         * Flag indicating whether the event was affected by SVT burst noise. 
         * It's set to 0 if the event saw burst noise or 1 if it was fine.
         */ 
        int svt_burstmode_noise; 
        
        /** 
         * Flag indicating whether the SVT was open or closed.  It's set to 0 if 
         * the SVT was open or 1 if it was closed.
         */ 
        int svt_position_state;
        
        /** Trigger time stamp */
        long trigger_time_stamp;

        int n_tracks;
        int n_svt_hits;
        int n_ecal_clusters;
        int n_ecal_hits;
        int n_fs_particles;
        int n_uc_v0_candidates;
        int n_uc_moller_candidates;
        int n_bsc_v0_candidates;
        int n_bsc_moller_candidates;
        int n_tc_v0_candidates;
        int n_tc_moller_candidates; 
        int n_mc_particles;
        int n_gbl_tracks;
        int n_gbl_tracks_data;
        int n_gbl_strips_data;
        
};

#endif


