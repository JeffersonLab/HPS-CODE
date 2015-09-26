/**
 *	@author:	Omar Moreno <omoreno1@ucsc.edu>
 *	@section institution
 *				Santa Cruz Institute for Particle Physics
 *				University of California, Santa Cruz
 *	@version:	v 1.0
 *	@date:		February 11, 2014 
 *
 */

#ifndef _MC_PARTICLE_H_
#define _MC_PARTICLE_H_

class MCParticle {

	public: 

		virtual ~MCParticle(){};
		
		virtual double getEnergy() const = 0; 
		virtual std::vector<double> getMomentum() const = 0; 
		virtual int getPDG() const = 0;
		virtual double getMass() const = 0; 
		virtual int getCharge() const = 0;

		virtual void setEnergy(const double) = 0; 
		virtual void setMomentum(const double*) = 0; 
		virtual void setPDG(const int) = 0; 
		virtual void setMass(const double) = 0; 
		virtual void setCharge(const int) = 0; 	

}; // MCParticle

#endif // _MC_PARTICLE_H_
