/**
 * 
 * @file SvtTrack.h
 * @brief Class used to describe an HPS SVT track.
 * @author Omar Moreno <omoreno1@ucsc.edu>
 *         Santa Cruz Institute for Particle Physics
 *         University of California, Santa Cruz
 * @date February 19, 2013
 * 
 */

#include <SvtTrack.h>

ClassImp(SvtTrack)

SvtTrack::SvtTrack()
    : TObject(), 
      svt_hits(new TRefArray()),
      fs_particle(NULL),
      isolation{}, 
      n_hits(0),
      track_volume(-1),
      type(0), 
      d0(0),
      phi0(0),
      omega(0),
      tan_lambda(0),
      z0(0),
      chi_squared(0),
      track_time(0), 
      x_at_ecal(0), 
      y_at_ecal(0), 
      z_at_ecal(0) {
}

SvtTrack::SvtTrack(const SvtTrack &svtTrackObj)
    : TObject(),
      svt_hits(new TRefArray()),
      fs_particle(NULL),
      n_hits(svtTrackObj.n_hits),
      track_volume(svtTrackObj.track_volume),
      type(svtTrackObj.type), 
      d0(svtTrackObj.d0),
      phi0(svtTrackObj.phi0),
      omega(svtTrackObj.omega),
      tan_lambda(svtTrackObj.tan_lambda),
      z0(svtTrackObj.z0),
      chi_squared(svtTrackObj.chi_squared),
      track_time(svtTrackObj.track_time),
      x_at_ecal(svtTrackObj.x_at_ecal), 
      y_at_ecal(svtTrackObj.x_at_ecal), 
      z_at_ecal(svtTrackObj.x_at_ecal) {

    *svt_hits = *svtTrackObj.svt_hits;
    fs_particle = svtTrackObj.fs_particle;
    memcpy(&isolation, svtTrackObj.isolation, 12*sizeof(double));
}


SvtTrack &SvtTrack::operator=(const SvtTrack &svtTrackObj) {
    
    // Check for self-assignment
    if(this == &svtTrackObj) return *this;

    TObject::operator=(svtTrackObj);
    Clear();
    delete svt_hits;

    this->n_hits = svtTrackObj.n_hits; 
    this->track_volume = svtTrackObj.track_volume;
    this->type = svtTrackObj.type;
    this->d0 = svtTrackObj.d0;
    this->phi0 = svtTrackObj.phi0;
    this->omega = svtTrackObj.omega;this->tan_lambda = svtTrackObj.tan_lambda;this->z0 = svtTrackObj.z0;
    this->chi_squared = svtTrackObj.chi_squared;
    this->track_time = svtTrackObj.track_time;
    this->x_at_ecal = svtTrackObj.x_at_ecal;
    this->y_at_ecal = svtTrackObj.y_at_ecal;
    this->z_at_ecal = svtTrackObj.z_at_ecal;

    svt_hits = new TRefArray();
    *svt_hits = *svtTrackObj.svt_hits;
    fs_particle = svtTrackObj.fs_particle;
    memcpy(&isolation, svtTrackObj.isolation, 12*sizeof(double));

    return *this;
}

SvtTrack::~SvtTrack() {
    Clear();
    delete svt_hits;
}

void SvtTrack::Clear(Option_t* /* option */) {
    TObject::Clear(); 
    svt_hits->Delete();
    memset(isolation, 0, sizeof(isolation)); 
    n_hits = 0; 
}

void SvtTrack::setTrackParameters(double d0, double phi0, double omega,
                                  double tan_lambda, double z0) {
    this->d0         = d0;
    this->phi0       = phi0;
    this->omega      = omega;
    this->tan_lambda = tan_lambda;
    this->z0         = z0;
}

void SvtTrack::setPositionAtEcal(const float* position) { 
    x_at_ecal = position[0]; 
    y_at_ecal = position[1];
    z_at_ecal = position[2];
}

int SvtTrack::getCharge() { 
    if (fs_particle == NULL) return 9999;
    return ((HpsParticle*) this->fs_particle.GetObject())->getCharge();
}

std::vector<double> SvtTrack::getMomentum() {
    if (fs_particle == NULL) return {0, 0, 0}; 
    return ((HpsParticle*) this->fs_particle.GetObject())->getMomentum();
}

void SvtTrack::addHit(SvtHit* hit) {
    ++n_hits; 
    svt_hits->Add((TObject*) hit); 
}

TRefArray* SvtTrack::getSvtHits() const {
    return svt_hits;
}
