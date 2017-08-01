/**
 * @file AnalysisUtils.cxx
 * @brief A set of utilities commonly used when doing analysis
 * @author Omar Moreno, SLAC National Accelerator Laboratory
 */


#include <AnalysisUtils.h>

double AnalysisUtils::getMagnitude(std::vector<double> v) { 
    return sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2]);
}

double AnalysisUtils::getInvariantMass(SvtTrack* track_0, SvtTrack* track_1) {

    double p0 = AnalysisUtils::getMagnitude(track_0->getMomentum());
    double p1 = AnalysisUtils::getMagnitude(track_1->getMomentum()); 

    // Calculate the invariant mass
    double energy[2];
    double electron_mass = 0.000510998928;

    energy[0] = sqrt(p0*p0 + electron_mass*electron_mass);
    energy[1] = sqrt(p1*p1 + electron_mass*electron_mass);

    double px_sum = track_0->getMomentum()[0] + track_1->getMomentum()[0];
    double py_sum = track_0->getMomentum()[1] + track_1->getMomentum()[1];
    double pz_sum = track_0->getMomentum()[2] + track_1->getMomentum()[2];

    double p_sum = sqrt(px_sum*px_sum + py_sum*py_sum + pz_sum*pz_sum);

    return sqrt(pow(energy[0]+energy[1], 2) - pow(p_sum, 2));
}


