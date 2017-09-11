

class AbstractRadiativeCorrection{
 public :
  virtual double get_correction_factor(double theta){
    return 0;
  }

};


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
}
