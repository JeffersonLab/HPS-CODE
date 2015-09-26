/**
 *  @section purpose:
 *  @author: Omar Moreno <omoreno1@ucsc.edu>
 *			 Santa Cruz Institute for Particle Physics
 *			 University of California, Santa Cruz
 *  @date: December 12, 2013
 *  @version: 1.0
 *
 */

//--- Utils ---//
//-------------//
#include <EcalUtils.h>

typedef long long long64;

namespace { 

	const std::string encoder_string = "system:6,layer:2,ix:-8,iy:-6";
}

namespace EcalUtils { 

	EVENT::CalorimeterHit* getClusterSeed(IMPL::ClusterImpl* cluster){

		// Get the calorimeter hits from the cluster
		EVENT::CalorimeterHitVec ecal_hits = cluster->getCalorimeterHits(); 

		double seed_energy = 0; 
		float seed_index = -1; 
		for(int ecal_hit_n = 0; ecal_hit_n < (int) ecal_hits.size(); ++ecal_hit_n){
			if(seed_energy < ecal_hits[ecal_hit_n]->getEnergy()){
				seed_energy = ecal_hits[ecal_hit_n]->getEnergy();
				seed_index = ecal_hit_n; 
			}
		}

		return ecal_hits[seed_index]; 
	} 

	UTIL::BitFieldValue getIdentifierFieldValue(std::string field, EVENT::CalorimeterHit* hit){

		UTIL::BitField64 decoder(encoder_string);
		long64 value = long64( hit->getCellID0() & 0xffffffff ) | ( long64( hit->getCellID1() ) << 32 ) ;
		decoder.setValue(value); 

		return decoder[field]; 

	}

	int getQuadrant(int ix, int iy){
		if(ix > 0){
			if(iy > 0) return 1; 
			else return 4; 
		} else { 
			if(iy > 0) return 2;
			else return 3;  
		}
	}

	std::vector<double> getShowerMoments(IMPL::ClusterImpl* cluster, IMPL::LCCollectionVec* ecal_hits_relations)
	{
		// Get the cluster position
		std::vector<double> cluster_position(3,0);
		cluster_position.assign((cluster->getPosition()), (cluster->getPosition())+3);

		// Get the cluster energy
		double cluster_energy = cluster->getEnergy();

		// Get the calorimeter hits associated with the cluster
		EVENT::CalorimeterHitVec cluster_hits = cluster->getCalorimeterHits();
		int n_hits = cluster_hits.size();

		int n_moments = 3;
		std::vector<double> moments(3,0);
		IMPL::CalorimeterHitImpl *cluster_hit = NULL;
		IMPL::LCRelationImpl* ecal_hits_relation = NULL;
		std::vector<double> hit_position(3,0);

		// Loop over all calorimeter hits and calculate the shower moments
		for(int hit_n = 0; hit_n < n_hits; ++hit_n){
		
			cluster_hit = (IMPL::CalorimeterHitImpl*) cluster_hits[hit_n];

			for(int rel_n = 0; rel_n < ecal_hits_relations->getNumberOfElements(); ++rel_n){
				ecal_hits_relation = (IMPL::LCRelationImpl*) ecal_hits_relations->getElementAt(rel_n);
				if(ecal_hits_relation->getFrom() == cluster_hit){
					hit_position[0] = ((IMPL::LCGenericObjectImpl*) ecal_hits_relation->getTo())->getDoubleVal(0);
					hit_position[1] = ((IMPL::LCGenericObjectImpl*) ecal_hits_relation->getTo())->getDoubleVal(1);
					hit_position[2] = ((IMPL::LCGenericObjectImpl*) ecal_hits_relation->getTo())->getDoubleVal(2);
					break;
				}
			}
			
			double r; 
			for(int index = 0; index < 3; ++index){
				hit_position[index] -= cluster_position[index]; 
				r = hit_position[index]*hit_position[index]; 
			}
			r = std::sqrt(r); 

			moments[0] += cluster_hits [hit_n]-> getEnergy ()*r;
			moments[1] += cluster_hits[hit_n]->getEnergy()*pow(r,2);
			moments[2] += cluster_hits [hit_n]-> getEnergy ()*pow (r, 3);
		}

		for (int n_moment = 0; n_moment < n_moments; ++n_moment){
			moments[n_moment] /= cluster_energy;
		}

		return moments;
	}	
}

