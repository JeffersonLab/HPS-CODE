#include "CrossSectionComponent.h"
#include "../omniheader.h"
class CarbonElastic : public SimpleCrossSectionComponent{
 public:
 CarbonElastic(double ebeam) :  SimpleCrossSectionComponent(ebeam, 12*AMU, 0){
    this->_M = 12*AMU;
    this->_epsilon = 0;
  }
  double _R = 8;
  const double _a[17] =
    {0.15721e-1, 0.38732e-1,
     0.36808e-1, 0.14671e-1,
     -0.43277e-2, -0.97752e-2,
     -0.68908e-2, -0.27631e-2,
     -0.63568e-3, 0.71809e-4,
     0.18441e-3,  0.75066e-4,
     0.51069e-4,  0.14308e-4,
     0.23170e-5, 0.68465e-6,
     0};
  const double _nParams = 17;
  const double _Z = 6;
  double get_form_factor(double q){
    double f = 0;
    double f0 = 0;

    for(int i = 1; i<=_nParams-1; i++){
      double df = _R*_R*pow(-1,i)*hbar*sin(q*_R/hbar)/(q*(i*i*pi*pi-q*q*_R*_R/(hbar*hbar)));
      f += 4*pi*df*_a[i-1];
      double df0 =  _R*_R*_R*pow(-1,i)/(i*i*pi*pi);
      f0 += 4*pi*df0*_a[i-1];
    }
    return -f/_Z;
  }
  double get_relative_sys_error_on_xs(double theta){
    double q = _ebeam*sin(theta/2)*2; //ignore the recoil for this part
    if(q< .197)  // Cardman's dataset goes from .1 to 1 fm^-1
      return .006;
    else  //Sick's dataset goes from 1 to 4 fm^-1
      return .03+.02*(q-.197)/.160;
  }
};

class InterpolateInelasticFormFactor : public SimpleCrossSectionComponent {
 public : 
 InterpolateInelasticFormFactor(double ebeam, double M, double epsilon, initializer_list<double> x, initializer_list<double> y) :  SimpleCrossSectionComponent(ebeam, M, epsilon), _x(x), _y(y)
  {

  }
  
  vector<double> _x;
  vector<double> _y;
  
  double get_form_factor(double q){
    if(q <= _x[0])
      return sqrt(_y[0]*pow(q/_x[0],4));
    for(int i = 0; i<_x.size()-1; i++){
      if(_x[i]<q && _x[i+1]>=q){
	return sqrt(_y[i] + (q-_x[i])*(_y[i+1]-_y[i])/(_x[i+1]-_x[i]));
      }
    }
    return 0;
  }
  //I got these by counting pixels on a graph.  
  double get_relative_sys_error_on_xs(double theta){
    return .1;
  }
};


class CarbonInelastic2Plus : public InterpolateInelasticFormFactor{
 public :
 CarbonInelastic2Plus(double ebeam) : InterpolateInelasticFormFactor(
      ebeam,
      12*AMU,
      .00443,
      { 0.118, 0.158, 0.197, .24, .28, .32, .36, .39, .43},
      { 4.28e-3, 9.43e-3, 1.33e-2, 1.45e-2, 1.18e-2, 7.87e-3, 4.52e-3, 2.11e-3, 7.54e-4})
      {
	
      }
};

class CarbonInelastic3Minus : public InterpolateInelasticFormFactor{
 public :
 CarbonInelastic3Minus(double ebeam) : InterpolateInelasticFormFactor(
      ebeam,
      12*AMU,
      .00964,
      { .162, .183, .20, .22, .24, .25, .27, .29, .31, .33, .35, .37},
      { 3.0e-3, 3.9e-3, 4.7e-3, 5.0e-3, 4.7e-3, 4.4e-3, 4.5e-3, 4.0e-3, 3.7e-3, 3.1e-3, 1.9e-3, 1.4e-3})
      {
	
      }
};

class Quasielastic : public SimpleCrossSectionComponent {
 public :
  double _Z;
  double _N;
  double _kF;
  double _delta_kF;
 Quasielastic(double ebeam, double ebind, double Z, double N, double kF, double delta_kF) :
  SimpleCrossSectionComponent(ebeam, .938, ebind), _Z(Z), _N(N), _kF(kF), _delta_kF(delta_kF)
  {
    
  }

  double get_form_factor(double q){
    double q2 = q*q;
    double r = q/_kF; //ratio of momentum transfer to fermi momentum                                                                      
    double fermi_block = 3*r/4.-pow(r,3)/16.;
    if(r>2) fermi_block = 1;

    fermi_block *= .8 ;  //doug's c factor. spectroscopic factor.    +- 10 ;  

    double tau = q2/(.938*.938*4);

    double Gd = 1/pow(1+q2/.71,2);
    //double Ge = _Z*((1 - .24*tau)/(1 + 10.98*tau + 12.82*tau*tau + 21.97*tau*tau*tau)) + _N*1.7*tau/(1+3.3*tau)/pow(1+q2/(0.71),2);
    double Gep = (1 - .24*tau)/(1 + 10.98*tau + 12.82*tau*tau + 21.97*tau*tau*tau);
    double Gen = 1.7*tau/(1+3.3*tau)*Gd;

    
    double quasi = fermi_block*(pow(Gep,2)*_Z + pow(Gen,2)*_N)/(_Z*_Z*(1+tau));
    return sqrt(quasi);
  }
  double get_relative_sys_error_on_xs(double theta){
    double q2 = pow(2*_ebeam*sin(theta/2),2);
    double sysFF = hypot(.01,.015*q2/(.13));  //some guess as to how much the uncertainty on the form factors are.  
    
    double q = sqrt(q2);
    double x = q/_kF;

    double sysPB = x < 2 ? (1-x*x/4)/(1-x*x/12)*_delta_kF : 0;
    return sqrt(4*pow(sysFF,2) + pow(sysPB,2)+ pow(.1,2));
  }
};


class CarbonQuasielastic : public Quasielastic {
 public :
 CarbonQuasielastic(double ebeam) :
  Quasielastic(ebeam, .025, 6, 12, .221, .005)
    {
      
    }
};

class DeltaResonance : public SimpleCrossSectionComponent {
 public :
  double _Z;
 DeltaResonance(double ebeam, double Z) :
  SimpleCrossSectionComponent(ebeam, .938, .1232-.938),
    _Z(Z)
    {
      
    }
  
  double get_form_factor(double q){
    
    return 0;  //TODO find the form factor
  }
  double get_relative_sys_error_on_xs(double theta){
    return 0;  //TODO find the error on the form factor
  }
};

//the most complete model of carbon I can get as of yet.
/*class CarbonFullModel : public CrossSectionComponent{
  CarbonFullModel(double ebeam){
    vector<CrossSectionComponent*> components();
    components.pushback(new CarbonElastic(ebeam));
    components.pushback(new CarbonQuasielastic(ebeam));
    components.pushback(new CarbonInelastic3Minus(ebeam));
    components.pushback(new CarbonInelastic2Plus(ebeam));
  }
  double get_xs_per_mott(
  }*/
