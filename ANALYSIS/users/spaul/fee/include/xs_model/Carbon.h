#include "CrossSectionComponent.h"
#include "../omniheader.h"
#include "ShellQuasielastic.h"
#include "DeltaResonance.h"
#include "TwoNucleonKnockout.h"
#ifndef CARBON_H
#define CARBON_H

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

class CarbonDeltaResonance : public DeltaResonance {
 public :
 CarbonDeltaResonance(double ebeam, double ecut) :
  DeltaResonance(ebeam, ebeam-ecut, 6,6)
  {
    
  }
};

class CarbonTwoNucleonKnockout : public TwoNucleonKnockout {
 public :
 CarbonTwoNucleonKnockout(double ebeam, double ecut) :
  TwoNucleonKnockout(ebeam, ebeam-ecut, 6,6)
  {
    
  }
};
  


class CarbonQuasielastic : public ShellQuasielastic {
 public :
 CarbonQuasielastic(double ebeam) :
  ShellQuasielastic(ebeam, .025, 6, 12, .221, .005)
    {
      
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
#endif
