/**
 *	@section purpose:
 *  @author: Omar Moreno <omoreno1@ucsc.edu>
 *			 Santa Cruz Institute for Particle Physics
 *			 University of California, Santa Cruz
 *  @date: December 16, 2013
 *  @version: 1.0
 *
 */

#include <TrackUtils.h>

namespace { 
		const double param = 2.99792458e-04; 	
}

namespace TrackUtils { 

    
    double getX0(IMPL::TrackImpl* track){
        return -1*getDoca(track)*sin(getPhi0(track));  
    }

    double getY0(IMPL::TrackImpl* track){
        return getDoca(track)*cos(getPhi0(track)); 
    };

    double getR(IMPL::TrackImpl* track){
        return 1.0/track->getOmega(); 
    }; 
    
    double getDoca(IMPL::TrackImpl* track){
        return track->getD0();     
    };
    
    double getPhi0(IMPL::TrackImpl* track){
        return track->getPhi(); 
    };

    double getPhi(IMPL::TrackImpl* track, std::vector<double> position){ 
          double x = sin(getPhi0(track)) - (1/getR(track))*(position[0] - getX0(track)); 
          double y = cos(getPhi0(track)) + (1/getR(track))*(position[1] - getY0(track)); 
    
        return atan2(x, y); 
    }; 
    
    double getZ0(IMPL::TrackImpl* track){
        return track->getZ0(); 
    
    }; 
    
    double getTanLambda(IMPL::TrackImpl* track){
        return track->getTanLambda(); 
    }; 
    
    double getSinTheta(IMPL::TrackImpl* track){
       return 1/sqrt(1 + pow(getTanLambda(track), 2));  
    }; 
    
    double getCosTheta(IMPL::TrackImpl* track){
        return getTanLambda(track)/sqrt(1 + pow(getTanLambda(track), 2)); 
    }; 

    double getXc(IMPL::TrackImpl* track){ 
        return (getR(track) - getDoca(track))*sin(getPhi0(track)); 
    };

    double getYc(IMPL::TrackImpl* track){
        return -(getR(track) - getDoca(track))*cos(getPhi0(track));   
    };

	std::vector<double> getMomentumVector(IMPL::TrackImpl* track, double b_field){
		std::vector<double> p(3,0); 
		double pt = std::abs(getR(track)*b_field*param);
		
		p[0] = pt*cos(getPhi0(track)); 
		p[1] = pt*sin(getPhi0(track)); 
		p[2] = pt*getTanLambda(track); 		
		
		return p; 	
	};

	double getMomentum(IMPL::TrackImpl* track, double b_field){
	
		std::vector<double> p_vector = getMomentumVector(track, b_field); 
		double p_sum = 0;
        
        for (double p : p_vector) { 
            p_sum += p*p;  
        } 

		return sqrt(p_sum); 
	};

	int getCharge(IMPL::TrackImpl* track){
		int charge; 
		track->getOmega() > 0 ? charge = 1 : charge = -1; 
		return charge; 		
	};

	int getLayer(EVENT::TrackerHit* tracker_hit){

		int z = (int) round(tracker_hit->getPosition()[0]/100);
		switch(z){
			case 1: return 1;
			case 2: return 2;
			case 3: return 3;
			case 5: return 4;
			case 7: return 5;
			case 9: return 6;
			default: return -1;
		}
	}
}
