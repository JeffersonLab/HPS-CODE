/**
 *	@author:	Omar Moreno <omoreno1@ucsc.edu>
 *	@section institution
 *				Santa Cruz Institute for Particle Physics
 *				University of California, Santa Cruz
 *	@date:		February 11, 2014
 *
 */

#ifndef _MC_PARTICLE_DATA_WRITER_H_
#define _MC_PARTICLE_DATA_WRITER_H_

//--- C++ ---//
//-----------//
#include <math.h>

//--- DST ---//
//-----------//
#include <DataWriter.h>

//--- LCIO ---//
//------------//
#include <IMPL/LCCollectionVec.h>
#include <IMPL/MCParticleImpl.h>
#include <Exceptions.h>

//--- HPS Event ---//
//-----------------//
#include <HpsMCParticle.h>

class MCParticleDataWriter : public DataWriter {

	public:

		MCParticleDataWriter();
		~MCParticleDataWriter();

		//
		void writeData(EVENT::LCEvent*, HpsEvent*);

		//
		void setMCParticleCollectionName(std::string mc_particles_collection_name){
			this->mc_particles_collection_name = mc_particles_collection_name;
		}

	private:

		std::string mc_particles_collection_name;

		IMPL::LCCollectionVec* mc_particles;
		IMPL::MCParticleImpl* mc_particle;

		HpsMCParticle* hps_mc_particle;

}; // MCParticleDataWriter

#endif // _MC_PARTICLE_DATA_WRITER_H_
