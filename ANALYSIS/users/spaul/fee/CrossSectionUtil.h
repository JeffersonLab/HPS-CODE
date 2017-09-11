#include "CrossSectionComponent.h"
#include "TH1.h"

TH1 * generate_histogram_from_xs(CrossSectionComponent * xs, double theta_min = 0, double theta_max = .200, int nbins = 200){
  TH1* h = new TH1D("h", "h", nbins, theta_min, theta_max);
  for(int i = 0; i<nbins; i++){
    double theta = (i+.5)*(theta_max-theta_min)/nbins;
    double xs_per_mott = xs->get_xs_per_mott(theta);
    double sys_error = xs->get_relative_sys_error_on_xs(theta)*xs_per_mott;
    h->SetBinContent(i, xs_per_mott);
    h->SetBinError(i, sys_error);
  }
  return h;
}

