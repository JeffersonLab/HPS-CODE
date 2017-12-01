#include "CrossSectionComponent.h"
#ifndef SHELL_QUASIELASTIC
#define SHELL_QUASIELASTIC
class ShellQuasielastic : public SimpleCrossSectionComponent {
 public :
  double _Z;
  double _N;
  double _kF;
  double _delta_kF;
 ShellQuasielastic(double ebeam, double ebind, double Z, double N, double kF, double delta_kF) :
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
    double quasi_e = fermi_block*(pow(Gep,2)*_Z + pow(Gen,2)*_N)/(_Z*_Z*(1+tau));


    double mup = 2.793;
    double mun = -1.913;
    double Gmp = (1 + .12*tau)/(1 + 10.97*tau + 18.86*tau*tau + 6.55*tau*tau*tau)*mup;
    double Gmn = (1+2.33*tau)/(1 + 14.72*tau + 24.20*tau*tau + 84.1*tau*tau*tau)*mun;

    //approximation
    double theta = 2*asin(q/(2*_ebeam));
    double epsilon = pow(1+2*(1+tau)*pow(tan(theta/2),2),-1);
    double quasi_m = fermi_block*(pow(Gmp,2)*_Z + pow(Gmn,2)*_N)*tau/(_Z*_Z*(1+tau)*epsilon);
  
  return sqrt(quasi_e+quasi_m);
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
#endif
