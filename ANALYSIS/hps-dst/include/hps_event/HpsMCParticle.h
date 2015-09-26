/**
 *	@author:	Omar Moreno <omoreno1@ucsc.edu>
 *	@section institution
 *				Santa Cruz Institute for Particle Physics
 *				University of California, Santa Cruz
 *	@version:	v 1.0
 *	@date:		February 11, 2014
 *
 */

#ifndef _HPS_MC_PARTICLE_H_
#define _HPS_MC_PARTICLE_H_

//-- ROOT ---//
//-----------//
#include <TObject.h>

//--- HPS Event ---//
//-----------------//
#include <MCParticle.h>

class HpsMCParticle : public TObject, public MCParticle {

	public:

		HpsMCParticle();
		HpsMCParticle(const HpsMCParticle &);
		~HpsMCParticle();
		HpsMCParticle &operator=(const HpsMCParticle &);

		void Clear(Option_t *option="");

		void setPDG(const int pdg){ this->pdg = pdg; };
		void setCharge(const int charge){ this->charge = charge; };
		void setGeneratorStatus(const int generator_status){ this->generator_status = generator_status; };
		void setEnergy(const double energy){ this->energy = energy; };
		void setMass(const double mass){ this->mass = mass; };
		void setMomentum(const double*);
		void setEndpoint(const double*);

		int getPDG() const { return pdg; };
		int getCharge() const { return charge; };
		int getGeneratorStatus() const { return generator_status; };
		double getEnergy() const { return energy; };
		double getMass() const { return mass; };
		std::vector<double> getMomentum() const;
		std::vector<double> getEndpoint() const;

		ClassDef(HpsMCParticle, 1)

	private:

		int pdg;
		int charge;
		int generator_status;

		double energy;
		double mass;
		double px;
		double py;
		double pz;
		double endpt_x;
		double endpt_y;
		double endpt_z;

}; // HpsMCParticle

#endif // _HPS_MC_PARTICLE_H_
