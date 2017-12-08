#include "CrossSectionComponent.h"
#include "../omniheader.h"
#include "ShellQuasielastic.h"
#ifndef TUNGSTEN_H
#define TUNGSTEN_H

class TungstenElastic : public SimpleCrossSectionComponent{
 public:
 TungstenElastic(double ebeam) :  SimpleCrossSectionComponent(ebeam, 183.84*AMU, 0){
    this->_M = 12*AMU;
    this->_epsilon = 0;
  }
  double _R = 6.58;
  double _z = .480;
  double _w = 0;
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

    double n = 0; //numerator
    double d = 0; //denominator

    double dr = .01;
    for(double r = 0; r<_R+4*_z; r+=dr){
      dr = .001;

      
      double rho = (1 + _w*r*r/(_R*_R))/(1 + exp((r-_R)/_z));

      n+= dr*(4*pi*hbar/q*r*sin(q*r/hbar))*rho;
      d+= dr*(4*pi*r*r)*rho;
    }
    return n/d;
  }
  double get_relative_sys_error_on_xs(double theta){
    return .03;  // made up value
  }
};




class TungstenQuasielastic : public ShellQuasielastic {
 public :
 TungstenQuasielastic(double ebeam) :
  ShellQuasielastic(ebeam, .042, 74, 183.84, .265, .005)
    {
      
    }
};
#endif
