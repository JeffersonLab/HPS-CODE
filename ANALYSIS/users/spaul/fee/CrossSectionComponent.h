#ifndef CROSS_SECTION_COMPONENT_H
#define CROSS_SECTION_COMPONENT_H
const double pi = 3.1415926535;
const double AMU = .931494095;
const double alpha = 1/137.036;
const double hbar = .1973;

class CrossSectionComponent {
   
 public :
  CrossSectionComponent(){}
  virtual double get_xs_per_mott(double theta){
    return 0;
  }
  virtual double get_relative_sys_error_on_xs(double theta){
    return 0;
  }
  
};

class SimpleCrossSectionComponent : public CrossSectionComponent {

  ;
 public :
  SimpleCrossSectionComponent(double ebeam, double M, double epsilon): _ebeam(ebeam),  _M(M), _epsilon(epsilon){ 

  }
  //mass of scattering center
  double _M;
  // 0 for elastic scattering,  ebind for quasi, resonance energy for inelastic and delta
  double _epsilon;
  double _ebeam;
  double get_xs_per_mott(double theta) {
    double q = 2*_ebeam*sqrt((1-_epsilon/_ebeam)/(1
					       +2*_ebeam/_M*pow(sin(theta/2),2)))*sin(theta/2);
    return pow(get_form_factor(q), 2);
  }
  virtual double get_form_factor(double q){
    return 0;
  }
};

#endif
