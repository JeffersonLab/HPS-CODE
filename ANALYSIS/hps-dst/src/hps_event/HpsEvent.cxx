/**
 *
 * @file HpsEvent.cxx
 * @brief Event class used to encapsulate event information and physics 
 *        collections.
 * @author Omar Moreno <omoreno1@ucsc.edu>
 *         Santa Cruz Institute for Particle Physics
 *         University of California, Santa Cruz
 * @date February 19, 2013
 *
 */

#include <HpsEvent.h>

// TODO: Add documentation

ClassImp(HpsEvent)

HpsEvent::HpsEvent()
    : TObject(), 
      bsc_moller_candidates(new TClonesArray("HpsParticle", 1000)), 
      bsc_v0_candidates(new TClonesArray("HpsParticle", 1000)),
      ecal_clusters(new TClonesArray("EcalCluster", 1000)),
      ecal_hits(new TClonesArray("EcalHit", 1000)),
      fs_particles(new TClonesArray("HpsParticle", 1000)),
      gbl_strips_data(new TClonesArray("GblStripData", 1000)),
      gbl_tracks(new TClonesArray("GblTrack", 1000)),
      gbl_tracks_data(new TClonesArray("GblTrackData", 1000)),
      mc_particles(new TClonesArray("HpsMCParticle", 1000)),
      tc_moller_candidates(new TClonesArray("HpsParticle", 1000)), 
      tc_v0_candidates(new TClonesArray("HpsParticle", 1000)),
      tracks(new TClonesArray("SvtTrack", 1000)),
      svt_hits(new TClonesArray("SvtHit", 1000)),
      uc_moller_candidates(new TClonesArray("HpsParticle", 1000)), 
      uc_v0_candidates(new TClonesArray("HpsParticle", 1000)),
      event_number(0),
      pair0_trigger(0), 
      pair1_trigger(0), 
      pulser_trigger(0),
      run_number(0),
      single0_trigger(0), 
      single1_trigger(0), 
      svt_bias_state(0), 
      svt_burstmode_noise(0), 
      svt_position_state(0),
      n_tracks(0),
      n_svt_hits(0),
      n_ecal_clusters(0), 
      n_ecal_hits(0), 
      n_fs_particles(0),
      n_uc_v0_candidates(0), 
      n_uc_moller_candidates(0), 
      n_bsc_v0_candidates(0),
      n_bsc_moller_candidates(0),
      n_tc_v0_candidates(0), 
      n_tc_moller_candidates(0), 
      n_mc_particles(0),
      n_gbl_tracks_data(0),
      n_gbl_strips_data(0) {
}

HpsEvent::HpsEvent(const HpsEvent &hpsEventObj)
    : TObject(hpsEventObj),
      bsc_moller_candidates(new TClonesArray("HpsParticle", 1000)), 
      bsc_v0_candidates(new TClonesArray("HpsParticle", 1000)),
      ecal_clusters(new TClonesArray("EcalCluster", 1000)),
      ecal_hits(new TClonesArray("EcalHit", 1000)),
      fs_particles(new TClonesArray("HpsParticle", 1000)),
      gbl_strips_data(new TClonesArray("GblStripData", 1000)),
      gbl_tracks(new TClonesArray("GblTrack", 1000)),
      gbl_tracks_data(new TClonesArray("GblTrackData", 1000)),
      mc_particles(new TClonesArray("HpsMCParticle", 1000)),
      tc_moller_candidates(new TClonesArray("HpsParticle", 1000)), 
      tc_v0_candidates(new TClonesArray("HpsParticle", 1000)),
      tracks(new TClonesArray("SvtTrack", 1000)),
      svt_hits(new TClonesArray("SvtHit", 1000)),
      uc_moller_candidates(new TClonesArray("HpsParticle", 1000)), 
      uc_v0_candidates(new TClonesArray("HpsParticle", 1000)) {

    this->event_number = hpsEventObj.event_number;
    this->pair0_trigger = hpsEventObj.pair0_trigger;  
    this->pair1_trigger = hpsEventObj.pair1_trigger;  
    this->pulser_trigger = hpsEventObj.pulser_trigger;  
    this->run_number = hpsEventObj.run_number; 
    this->single0_trigger = hpsEventObj.single0_trigger;  
    this->single1_trigger = hpsEventObj.single1_trigger;
    this->svt_bias_state = hpsEventObj.svt_bias_state; 
    this->svt_burstmode_noise = hpsEventObj.svt_burstmode_noise;
    this->svt_position_state = hpsEventObj.svt_position_state;   
    this->n_tracks = hpsEventObj.n_tracks; 
    this->n_svt_hits = hpsEventObj.n_svt_hits;
    this->n_ecal_clusters = hpsEventObj.n_ecal_clusters;
    this->n_ecal_hits = hpsEventObj.n_ecal_hits;
    this->n_fs_particles = hpsEventObj.n_fs_particles;
    this->n_uc_v0_candidates = hpsEventObj.n_uc_v0_candidates;
    this->n_uc_moller_candidates = hpsEventObj.n_uc_moller_candidates;
    this->n_bsc_v0_candidates = hpsEventObj.n_bsc_v0_candidates;
    this->n_bsc_moller_candidates = hpsEventObj.n_bsc_moller_candidates;
    this->n_tc_v0_candidates = hpsEventObj.n_tc_v0_candidates;
    this->n_tc_moller_candidates = hpsEventObj.n_tc_moller_candidates;
    this->n_mc_particles = hpsEventObj.n_mc_particles;
    this->n_gbl_tracks = hpsEventObj.n_gbl_tracks;
    this->n_gbl_tracks_data = hpsEventObj.n_gbl_tracks_data;
    this->n_gbl_strips_data = hpsEventObj.n_gbl_strips_data;

    
    *bsc_moller_candidates = *hpsEventObj.bsc_moller_candidates;
    *bsc_v0_candidates = *hpsEventObj.bsc_v0_candidates;
    *ecal_clusters = *hpsEventObj.ecal_clusters;
    *ecal_hits = *hpsEventObj.ecal_hits;
    *gbl_strips_data = *hpsEventObj.gbl_strips_data;
    *gbl_tracks = *hpsEventObj.gbl_tracks;
    *gbl_tracks_data = *hpsEventObj.gbl_tracks_data;
    *fs_particles = *hpsEventObj.fs_particles;
    *mc_particles = *hpsEventObj.mc_particles;
    *tc_moller_candidates = *hpsEventObj.tc_moller_candidates;
    *tc_v0_candidates = *hpsEventObj.tc_v0_candidates;
    *tracks    = *hpsEventObj.tracks;
    *svt_hits  = *hpsEventObj.svt_hits;  
    *uc_moller_candidates = *hpsEventObj.uc_moller_candidates;
    *uc_v0_candidates = *hpsEventObj.uc_v0_candidates;
}


HpsEvent::~HpsEvent() {

    // Clear the event of all stored data
    Clear();
    
    // Delete all of the collections
    delete bsc_moller_candidates;
    delete bsc_v0_candidates;
    delete ecal_clusters; 
    delete ecal_hits;
    delete fs_particles;
    delete gbl_strips_data;
    delete gbl_tracks;
    delete gbl_tracks_data;
    delete mc_particles;
    delete tc_moller_candidates;
    delete tc_v0_candidates;
    delete tracks; 
    delete svt_hits;
    delete uc_moller_candidates;
    delete uc_v0_candidates;
}

HpsEvent &HpsEvent::operator=(const HpsEvent &hpsEventObj) {
    // Check for self-assignment
    if (this == &hpsEventObj) return *this;

    TObject::operator=(hpsEventObj);
    this->~HpsEvent();
    this->event_number = hpsEventObj.event_number; 
    this->pair0_trigger = hpsEventObj.pair0_trigger;  
    this->pair1_trigger = hpsEventObj.pair1_trigger;  
    this->pulser_trigger = hpsEventObj.pulser_trigger;  
    this->run_number   = hpsEventObj.run_number; 
    this->single0_trigger = hpsEventObj.single0_trigger;  
    this->single1_trigger = hpsEventObj.single1_trigger;
    this->svt_bias_state = hpsEventObj.svt_bias_state; 
    this->svt_burstmode_noise = hpsEventObj.svt_burstmode_noise;
    this->svt_position_state = hpsEventObj.svt_position_state;   
    this->n_tracks = hpsEventObj.n_tracks; 
    this->n_svt_hits = hpsEventObj.n_svt_hits;
    this->n_ecal_clusters = hpsEventObj.n_ecal_clusters;
    this->n_ecal_hits = hpsEventObj.n_ecal_hits;
    this->n_fs_particles = hpsEventObj.n_fs_particles;
    this->n_uc_v0_candidates = hpsEventObj.n_uc_v0_candidates;
    this->n_uc_moller_candidates = hpsEventObj.n_uc_moller_candidates;
    this->n_bsc_v0_candidates = hpsEventObj.n_bsc_v0_candidates;
    this->n_bsc_moller_candidates = hpsEventObj.n_bsc_moller_candidates;
    this->n_tc_v0_candidates = hpsEventObj.n_tc_v0_candidates;
    this->n_tc_moller_candidates = hpsEventObj.n_tc_moller_candidates;
    this->n_mc_particles = hpsEventObj.n_mc_particles;
    this->n_gbl_tracks = hpsEventObj.n_gbl_tracks; 
    this->n_gbl_tracks_data = hpsEventObj.n_gbl_tracks_data; 
    this->n_gbl_strips_data = hpsEventObj.n_gbl_strips_data; 

    bsc_moller_candidates = new TClonesArray("HpsParticle", 1000);
    bsc_v0_candidates = new TClonesArray("HpsParticle", 1000);
    ecal_clusters = new TClonesArray("EcalCluster", 1000); 
    ecal_hits = new TClonesArray("EcalHit", 1000);
    fs_particles = new TClonesArray("HpsParticle", 1000);
    gbl_strips_data = new TClonesArray("GblStripData", 1000);
    gbl_tracks = new TClonesArray("GblTrack", 1000);
    gbl_tracks_data = new TClonesArray("GblTrackData", 1000);
    mc_particles = new TClonesArray("HpsMCParticle", 1000);
    tc_moller_candidates = new TClonesArray("HpsParticle", 1000);
    tc_v0_candidates = new TClonesArray("HpsParticle", 1000);
    tracks = new TClonesArray("SvtTrack", 1000);
    svt_hits = new TClonesArray("SvtHit", 1000);
    uc_moller_candidates = new TClonesArray("HpsParticle", 1000);
    uc_v0_candidates = new TClonesArray("HpsParticle", 1000);

    *bsc_moller_candidates = *hpsEventObj.bsc_moller_candidates;
    *bsc_v0_candidates = *hpsEventObj.bsc_v0_candidates;
    *ecal_clusters = *hpsEventObj.ecal_clusters;
    *ecal_hits = *hpsEventObj.ecal_hits;
    *gbl_strips_data = *hpsEventObj.gbl_strips_data;
    *gbl_tracks = *hpsEventObj.gbl_tracks;
    *gbl_tracks_data = *hpsEventObj.gbl_tracks_data;
    *fs_particles = *hpsEventObj.fs_particles;
    *mc_particles = *hpsEventObj.mc_particles;
    *tc_moller_candidates = *hpsEventObj.tc_moller_candidates;
    *tc_v0_candidates = *hpsEventObj.tc_v0_candidates;
    *tracks    = *hpsEventObj.tracks;
    *svt_hits  = *hpsEventObj.svt_hits;  
    *uc_moller_candidates = *hpsEventObj.uc_moller_candidates;
    *uc_v0_candidates = *hpsEventObj.uc_v0_candidates;

    return *this;     
}

void HpsEvent::Clear(Option_t * /*option*/) {
    
    TObject::Clear(); 
    
    bsc_moller_candidates->Clear("C");
    bsc_v0_candidates->Clear("C");
    ecal_clusters->Clear("C");
    ecal_hits->Clear("C");
    fs_particles->Clear("C");
    gbl_strips_data->Clear("C");
    gbl_tracks->Clear("C");
    gbl_tracks_data->Clear("C");
    tc_moller_candidates->Clear("C");
    tc_v0_candidates->Clear("C");
    mc_particles->Clear("C");
    tracks->Clear("C");
    svt_hits->Clear("C");
    uc_moller_candidates->Clear("C");
    uc_v0_candidates->Clear("C");
    
    n_ecal_clusters = 0;
    n_ecal_hits = 0;
    n_tracks = 0;  
    n_svt_hits = 0;
    n_fs_particles = 0;
    n_uc_v0_candidates = 0;
    n_uc_moller_candidates = 0;
    n_bsc_v0_candidates = 0;
    n_bsc_moller_candidates = 0;
    n_tc_v0_candidates = 0;
    n_tc_moller_candidates = 0;
    n_mc_particles = 0;
    n_gbl_tracks = 0;
    n_gbl_tracks_data = 0;
    n_gbl_strips_data = 0;
}


SvtTrack* HpsEvent::addTrack() {
    return (SvtTrack*) tracks->ConstructedAt(n_tracks++);
}

SvtHit* HpsEvent::addSvtHit() {
    return (SvtHit*) svt_hits->ConstructedAt(n_svt_hits++);
}

EcalCluster* HpsEvent::addEcalCluster() {
    return (EcalCluster*) ecal_clusters->ConstructedAt(n_ecal_clusters++);
}

EcalHit* HpsEvent::addEcalHit() {
    return (EcalHit*) ecal_hits->ConstructedAt(n_ecal_hits++);
}

HpsParticle* HpsEvent::addParticle(HpsParticle::ParticleType type) {
    
    // FIXME: This should probably be using a map instead of a giant switch 
    //        statement.
    switch (type) { 
        case HpsParticle::FINAL_STATE_PARTICLE:
            return (HpsParticle*) fs_particles->ConstructedAt(n_fs_particles++); 
        case HpsParticle::UC_V0_CANDIDATE: 
            return (HpsParticle*) uc_v0_candidates->ConstructedAt(n_uc_v0_candidates++);
        case HpsParticle::BSC_V0_CANDIDATE:
            return (HpsParticle*) bsc_v0_candidates->ConstructedAt(n_bsc_v0_candidates++);
        case HpsParticle::TC_V0_CANDIDATE:
            return (HpsParticle*) tc_v0_candidates->ConstructedAt(n_tc_v0_candidates++);
        case HpsParticle::UC_MOLLER_CANDIDATE: 
            return (HpsParticle*) uc_moller_candidates->ConstructedAt(n_uc_moller_candidates++);
        case HpsParticle::BSC_MOLLER_CANDIDATE:
            return (HpsParticle*) bsc_moller_candidates->ConstructedAt(n_bsc_moller_candidates++);
        case HpsParticle::TC_MOLLER_CANDIDATE:
            return (HpsParticle*) tc_moller_candidates->ConstructedAt(n_tc_moller_candidates++);
        default: 
            throw std::runtime_error("[ HpsEvent ]: Particle type is invalid."); 
    }
}

HpsMCParticle* HpsEvent::addHpsMCParticle() {
    return (HpsMCParticle*) mc_particles->ConstructedAt(n_mc_particles++);
}


int HpsEvent::getNumberOfParticles(HpsParticle::ParticleType type) const {
    
    // FIXME: This should probably be using a map instead of a giant switch 
    //        statement.
    switch (type) {
        case HpsParticle::FINAL_STATE_PARTICLE:
            return n_fs_particles;
        case HpsParticle::UC_V0_CANDIDATE: 
            return n_uc_v0_candidates;  
        case HpsParticle::BSC_V0_CANDIDATE:
            return n_bsc_v0_candidates;
        case HpsParticle::TC_V0_CANDIDATE:
            return n_tc_v0_candidates; 
        case HpsParticle::UC_MOLLER_CANDIDATE: 
            return n_uc_moller_candidates;  
        case HpsParticle::BSC_MOLLER_CANDIDATE:
            return n_bsc_moller_candidates;
        case HpsParticle::TC_MOLLER_CANDIDATE:
            return n_tc_moller_candidates; 
        default: 
            throw std::runtime_error("[ HpsEvent ]: Particle type is invalid."); 
    }
}

GblTrack* HpsEvent::addGblTrack() {
    return (GblTrack*) gbl_tracks->ConstructedAt(n_gbl_tracks++);
}

GblTrackData* HpsEvent::addGblTrackData() {
    return (GblTrackData*) gbl_tracks_data->ConstructedAt(n_gbl_tracks_data++);
}

GblStripData* HpsEvent::addGblStripData() {
    return (GblStripData*) gbl_strips_data->ConstructedAt(n_gbl_strips_data++);
}

SvtTrack* HpsEvent::getTrack(int track_index) {
    return (SvtTrack*) tracks->At(track_index);
}

GblTrack* HpsEvent::getGblTrack(int gbl_track_index) {
    return (GblTrack*) gbl_tracks->At(gbl_track_index);
}

GblTrackData* HpsEvent::getGblTrackData(int track_data_index) {
    return (GblTrackData*) gbl_tracks_data->At(track_data_index);
}

GblStripData* HpsEvent::getGblStripData(int gbl_strip_data_index) {
    return (GblStripData*) gbl_strips_data->At(gbl_strip_data_index);
}

SvtHit* HpsEvent::getSvtHit(int hit_index) {
    return (SvtHit*) svt_hits->At(hit_index);
}

EcalCluster* HpsEvent::getEcalCluster(int ecal_cluster_index) {
    return (EcalCluster*) ecal_clusters->At(ecal_cluster_index);
}

EcalHit* HpsEvent::getEcalHit(int ecal_hit_index) {
    return (EcalHit*) ecal_hits->At(ecal_hit_index);
}

HpsMCParticle* HpsEvent::getMCParticle(int mc_particle_index) {
    return (HpsMCParticle*) mc_particles->At(mc_particle_index);
}

HpsParticle* HpsEvent::getParticle(HpsParticle::ParticleType type, int particle_index) {
    
    // FIXME: This should probably be using a map instead of a giant switch 
    //        statement.
    switch (type) { 
        case HpsParticle::FINAL_STATE_PARTICLE:
            return (HpsParticle*) fs_particles->At(particle_index); 
        case HpsParticle::UC_V0_CANDIDATE: 
            return (HpsParticle*) uc_v0_candidates->At(particle_index);
        case HpsParticle::BSC_V0_CANDIDATE: 
            return (HpsParticle*) bsc_v0_candidates->At(particle_index);
        case HpsParticle::TC_V0_CANDIDATE: 
            return (HpsParticle*) tc_v0_candidates->ConstructedAt(particle_index);
        case HpsParticle::UC_MOLLER_CANDIDATE: 
            return (HpsParticle*) uc_moller_candidates->At(particle_index);
        case HpsParticle::BSC_MOLLER_CANDIDATE: 
            return (HpsParticle*) bsc_moller_candidates->At(particle_index);
        case HpsParticle::TC_MOLLER_CANDIDATE: 
            return (HpsParticle*) tc_moller_candidates->ConstructedAt(particle_index);
        default:
            throw std::runtime_error("[ HpsEvent ]: Particle type is invalid."); 
    }
}
