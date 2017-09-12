#include "../omniheader.h"
#include "../constants.h"
class AbstractRadiativeCorrection{
 
 public :
  virtual double get_correction_factor(double theta){
    return 0;
  }

};

/*
class InterpolativeRadiativeCorrection(AbstractRadiativeCorrection){
 public:
  //theta points
  vector <double> _x;
  //correction factor points
  vector <double> _y;
 InterpolativeRadiativeCorrection(std::initializer_list<double> theta, std::initializer_list<double> corr_factor) : _x(theta), _y(corr_factor){

  }

  get_correction_factor(double theta){
    for(i = 0; i<_x.size()-1; i++){
      if(_x[i]<theta && _x[i+1] > theta){
	return _y[i]+(_y[i+1]-_y[i])/(_x[i+1]-_x[i])*(theta-_x[i]);
      }
    }
    return 0;
  }
}*/


double gausc(double x){
  return (std::erf(x/sqrt(2))+1)/2.;
}

class IntegralRadiativeCorrection : public AbstractRadiativeCorrection {
 private:
  double Li2(double x){
    return x + x*x/4. + pow(x,3)/9. + pow(x,4)/16.+ pow(x,5)/25.;
  }
  double f(double x){

    double ret = log(x)*log(1-x)+Li2(-x);
    //cout << x << "  "<< ret << endl;
    return ret;
  }
 public :
  double _t;
  double _b;
  double _ecut;
  double _ebeam;
  double _sigma_e;
 IntegralRadiativeCorrection(double ebeam, double ecut, double t, double b, double sigma_e):
  _t(t), _b(b), _ecut(ecut), _ebeam(ebeam), _sigma_e(sigma_e)
  {
    
  }
  double get_correction_factor(double theta){

    
    double total = 0;
    double sum0 = 0;
    
    
    double step = .99;
    double epsilon = .0001;
    
    double xbrem_prev = .3;
    double epsilon_brem = .0001;

    double me = 0.000511;
    double q2 = pow(_ebeam*2*sin(theta/2),2);//approximate formula
    
    
    double y = -2*alpha/pi*(log(q2/(me*me))-1);
    
    //outer loop = energy loss due to bremsstrahlung

    for(double xbrem = 1-(1-xbrem_prev)*step; xbrem < 1-epsilon_brem; xbrem = 1-(1-xbrem)*step)
      {
	double dxbrem = xbrem - xbrem_prev;
	//double p_brem = 1;

	double p_brem = -y/pow(1-xbrem, y+1);
    	//cout << "pbrem:  " << p_brem << endl;
	
	double xstrag_prev = .3;
	for(double xstrag = 1-(1-xstrag_prev)*step; xstrag < 1- epsilon; xstrag = 1-(1-xstrag)*step)
	  {
	    double p_strag = _b*_t/(1-xstrag)*(xstrag + 3/4.*pow(1-xstrag, 2))*pow(log(1/xstrag),_b*_t);
	    double z = ( _ecut- xbrem*xstrag*_ebeam)/_sigma_e;
	    double c_gaus = (1 -gausc(z));
	    
	    
	    //cout << "a... " << xstrag << "  " << p_strag << "  "<< c_gaus << endl;
	    double dxstrag = xstrag-xstrag_prev;
	    //if((_ebeam-_ecut) < xstrag*_ebeam)
	    
	    total += p_strag * dxstrag * p_brem * dxbrem  * c_gaus;
	    sum0  += p_strag * dxstrag * p_brem * dxbrem;
	    xstrag_prev = xstrag;
	    
	  }
	double c_gaus = (1-gausc((_ecut-_ebeam*xbrem)/_sigma_e));
	double c_strag = (pow(epsilon, _b*_t))*(1-epsilon/2+3/4.*pow(epsilon/2, 2));
  
	total += c_strag * p_brem * dxbrem * c_gaus;	
	sum0  += c_strag * p_brem * dxbrem;
	
	xbrem_prev = xbrem;
      }
    //cout << total << endl;
    double xbrem = 1;
    
    double xstrag_prev = .3;
    double c_brem =  1/pow(epsilon_brem, y);
    for(double xstrag = 1-(1-xstrag_prev)*step; xstrag < 1- epsilon; xstrag = 1-(1-xstrag)*step)
      {
	double p_strag = _b*_t/(1-xstrag)*(xstrag + 3/4.*pow(1-xstrag, 2))*pow(log(1/xstrag),_b*_t);
	double z = ( _ecut- xstrag*_ebeam)/_sigma_e;
	double c_gaus = (1 -gausc(z));
	
	
	//cout << "a... " << xstrag << "  " << p_strag << "  "<< c_gaus << endl;
	double dxstrag = xstrag-xstrag_prev;
	//if((_ebeam-_ecut) < xstrag*_ebeam)
	
	total += p_strag * dxstrag * c_brem* c_gaus ;
	sum0  += p_strag * dxstrag * c_brem;
	xstrag_prev = xstrag;
	
      }

    double c_gaus = (1-gausc((_ecut-_ebeam)/_sigma_e));
    double c_strag =  (pow(epsilon, _b*_t))*(1-epsilon/2+3/4.*pow(epsilon/2, 2));
    total += c_strag * c_brem * c_gaus;
    sum0  += c_strag * c_brem;
    
    

    //contribution from vacuum and vertex corrections
    double delta_vac_vtx =  -(2*alpha)/pi*(-13/12.*(log(q2/(me*me))-1) + 17/36. + 1/2.*f(pow(sin(theta/2),2)));
    
    total*=1+delta_vac_vtx;
    sum0*=1+delta_vac_vtx;
    //cout << sum0 << endl;
    //cout << total <<endl;
      //}
    return total;
  }

};


