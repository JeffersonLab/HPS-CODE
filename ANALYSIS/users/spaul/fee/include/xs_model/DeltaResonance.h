#include "CrossSectionComponent.h"

#ifndef DELTA_RESONANCE_H
#define DELTA_RESONANCE_H
class DeltaResonance: public SimpleCrossSectionComponent {
  double _a2 = pow(.700,2); //dipole parameter
  double _kF = .220; //fermi momentum (of carbon)
  double _M = .9383; //mass of proton
  double _M_pion = .135; //mass of pion
  double _M_Delta = 1.232; //mass of delta

  double _N ; //number of neutrons
  double _Z ; //number of protons
 public :

  double _scale = 125; //221.088892;//31.29;
 DeltaResonance(double ebeam, double omega_max, int Z, int N):
  _Z(Z), _N(N), _omega_max(omega_max),
  SimpleCrossSectionComponent(ebeam, .938, .1232-.938)
  {
    
  }

  double response(double Q2, double omega){
    double q2 = Q2+omega*omega;
    double q = sqrt(q2);
    double dipole = 1/pow(1+Q2/_a2,4);
    double scale = _scale; 
    double omega_thresh = Q2/(2*(_M +_M_pion));
    if(omega < omega_thresh) return 0;
    double width_thresh = .005;

    double W2 = _M*_M+2*_M*(omega-Q2/(2*_M));
    
    double W2cm = pow(_M_Delta,2);
    
    double width = sqrt(pow(.110,2)+pow(1.1*_kF*q/_M,2)+pow(.140,2));
    double lorentzian = pow(width,2)*W2/(pow(W2-W2cm,2)+pow(width,2)*W2);
    double thresh_scale = omega > omega_thresh ? 1-exp(-(omega-omega_thresh)/width_thresh) : 0;
    return scale*q2*dipole*lorentzian*thresh_scale;
  }

  double get_dxs_per_mott_domega(double theta, double omega){

    double Q2 = 4*_ebeam*(_ebeam-omega)*pow(sin(theta/2),2);
    double q2 = Q2+omega*omega; 
    double integrand = response(Q2, omega)*(Q2/(2*q2)+pow(tan(theta/2),2));
    return integrand;
  }
				 
  
  double _omega_max = 2.306*.15;
  double get_xs_per_mott(double theta){
    double omega = 0;
    double d_omega = .002;
    double integral = 0;
    for(; omega < _omega_max; omega+= d_omega){
      double integrand = get_dxs_per_mott_domega(theta, omega);
      integral+= integrand*d_omega;
    }
    return integral*(_Z + _N)/(_Z*_Z);  //the _Z*_Z factor is because we are comparing to the elastic mott.  
  }
  double get_relative_sys_error_on_xs(double theta){
    return .30;
  }
};
#endif
