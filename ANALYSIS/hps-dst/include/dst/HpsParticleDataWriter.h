/**
 *
 * @file HpsParticleDataWriter.h
 * @brief Data writer used to convert LCIO ReconstructedParticle objects
 *        to {@link HpsParticle} objects and add them to an event.
 * @author Omar Moreno <omoreno1@ucsc.edu>
 *         Santa Cruz Institute for Particle Physics
 *         University of California, Santa Cruz
 * @date March 31, 2014
 *
 */

#ifndef __HPS_PARTICLE_WRITER_H__
#define __HPS_PARTICLE_WRITER_H__

//------------------//
//--- C++ StdLib ---//
//------------------//
#include <string>
#include <map>

//------------//
//--- LCIO ---//
//------------//
#include <EVENT/LCCollection.h>
#include <EVENT/ReconstructedParticle.h>
#include <EVENT/Vertex.h>
#include <Exceptions.h>

//-----------//
//--- DST ---//
//-----------//
#include <DataWriter.h>

//-----------------//
//--- HPS Event ---//
//-----------------//
#include <HpsParticle.h>
#include <HpsEvent.h>

class HpsParticleDataWriter : public DataWriter { 

    public: 

        /** Default constructor */
        HpsParticleDataWriter();

        /** Destructor */ 
        ~HpsParticleDataWriter(); 

        /**
         * Make {@link HpsParticle} objects out of LCIO ReconstructedParticles
         * and add them to the event ({@link HpsEvent} object).
         *
         * @param lc_event LCIO event from which the ReconstructedParticle 
         *                 collections are retrieved from.
         * @param hps_event {@link HpsEvent} object to which the 
         *                  {@link HpsParticle}s will be added to. 
         */
        void writeData(EVENT::LCEvent* lc_event, HpsEvent* hps_event);

    private:

        /**
         * Make {@link HpsParticle} objects of the given 
         * {@link HpsParticle::ParticleType} out of LCIO ReconstructedParticles
         * and add them to an {@link HpsEvent} object.
         *
         * @param type The type of particle that is being requested e.g. 
         *             HpsParticle::FINAL_STATE_PARTICLE.
         * @param particles The collection of LCIO ReconstructedParticles
         * @param hps_event {@link HpsEvent} object to which the 
         *                  {@link HpsParticle}s will be added to. 
         */
        void writeParticleData(HpsParticle::ParticleType type, EVENT::LCCollection* particles, HpsEvent* hps_event); 

        /** LCIO Collection name of final state particles */
        std::string fs_particles_collection_name;
        
        /** LCIO Collection name of unconstrained V0 candidates */
        std::string uc_v0_candidates_collection_name; 

        /** LCIO Collection name of unconstrained V0 candidates */
        std::string uc_moller_candidates_collection_name; 

        /** LCIO Collection name of beam spot constrained V0 candidates */
        std::string bsc_v0_candidates_collection_name; 

        /** LCIO Collection name of beam spot constrained V0 candidates */
        std::string bsc_moller_candidates_collection_name; 

        /** LCIO Collection name of target constrained V0 candidates */
        std::string tc_v0_candidates_collection_name; 

        /** LCIO Collection name of target constrained V0 candidates */
        std::string tc_moller_candidates_collection_name; 

        /** 
         * Map from an {@link HpsParticle::ParticleType} to the LCIO collection
         * name 
         */
        std::map<HpsParticle::ParticleType, std::string> particle_collections;

}; // HpsParticleWriter

#endif // __HPS_PARTICLE_WRITER_H__
