/**
 *
 *  @file HpsEventBuilder.cxx
 *  @brief Builds {@link HpsEvent} objects out of LCIO events.
 *  @author Omar Moreno <omoreno1@ucsc.edu>
 *          Santa Cruz Institute for Particle Physics
 *          University of California, Santa Cruz
 *  @date   January 6, 2014
 *
 */

#include <HpsEventBuilder.h>

HpsEventBuilder::HpsEventBuilder() 
    : svt_writer(new SvtDataWriter()), 
      ecal_writer(new EcalDataWriter()),
      mc_particle_writer(new MCParticleDataWriter()),
      particle_writer(new HpsParticleDataWriter()),
      gbl_data_writer(new GblDataWriter()),
      hps_trigger_data(NULL),
      trigger_data(NULL),
      trigger_datum(NULL),
      run_gbl(false),
      ecal_only(false) {
}

HpsEventBuilder::~HpsEventBuilder() {
    delete svt_writer;
    delete ecal_writer;     
    delete mc_particle_writer;
    delete particle_writer; 
    delete gbl_data_writer;
}

void HpsEventBuilder::makeHpsEvent(EVENT::LCEvent* event, HpsEvent* hps_event) {
    
    // Clear the HpsEvent from all previous information
    hps_event->Clear();

    //  Check that the event contains more than just the trigger collection.
    //  This is a temp solution to the recon not having an ECal collection
    //  in every event.
    //std::cout << event->getCollectionNames()->size() << std::endl;
    if (event->getCollectionNames()->size() <= 2) return;  

    this->writeEventData(event, hps_event); 

    // Write Ecal data to the HpsEvent
    ecal_writer->writeData(event, hps_event); 

    // If only Ecal data is going to be written to the DST, skip the rest
    // of the writers
    if (ecal_only) return;

    // Write SVT data to the HpsEvent
    svt_writer->writeData(event, hps_event);

    // Write MC particle data to the HpsEvent
    mc_particle_writer->writeData(event, hps_event);

    // Write the HpsParticle data to the HpsEvent
    particle_writer->writeData(event, hps_event); 

    // If GBL has been enabled, process the SVT tracks using GBL and write the
    // data to the HpsEvent
    if (!run_gbl) return;

    // Write info used for GBL to the HpsEvent
    gbl_data_writer->writeData(event, hps_event);

}

void HpsEventBuilder::writeEventData(EVENT::LCEvent* lc_event, HpsEvent* hps_event) { 
    
    // Set the event number
    hps_event->setEventNumber(lc_event->getEventNumber());

    // Set the run number
    hps_event->setRunNumber(lc_event->getRunNumber());

    // Set the trigger timestamp 
    hps_event->setTriggerTimeStamp(lc_event->getTimeStamp()); 

    // Set the SVT bias state
    hps_event->setSvtBiasState(lc_event->getParameters().getIntVal("svt_bias_good")); 
    
    // Set the flag indicating whether the event was affected by SVT burst
    // mode noise 
    hps_event->setSvtBurstModeNoise(lc_event->getParameters().getIntVal("svt_burstmode_noise_good"));

    // Set the SVT position state
    hps_event->setSvtPositionState(lc_event->getParameters().getIntVal("svt_position_good"));

    // Set the trigger data
    try { 
        trigger_data = (IMPL::LCCollectionVec*) lc_event->getCollection("TriggerBank"); 
    } catch(EVENT::DataNotAvailableException e){
    }

    //std::cout << "Number of trigger elements: " << trigger_data->getNumberOfElements() << std::endl;
    for (int trigger_datum_n = 0; trigger_datum_n < trigger_data->getNumberOfElements(); ++trigger_datum_n) { 
       
        trigger_datum = (EVENT::LCGenericObject*) trigger_data->getElementAt(trigger_datum_n); 
        //std::cout << "Bank tag: " << trigger_datum->getIntVal(0) << std::endl;
        if (trigger_datum->getIntVal(0) == 0xe10a) { 
           
            hps_trigger_data = new TriggerData(trigger_datum); 
            hps_event->setSingle0Trigger((int) hps_trigger_data->isSingle0Trigger());
            hps_event->setSingle1Trigger((int) hps_trigger_data->isSingle1Trigger());
            hps_event->setPair0Trigger((int) hps_trigger_data->isPair0Trigger());
            hps_event->setPair1Trigger((int) hps_trigger_data->isPair1Trigger());
            hps_event->setPulserTrigger((int) hps_trigger_data->isPulserTrigger());

            delete hps_trigger_data;
            hps_trigger_data = NULL;
            break;
        }
    }
}

void HpsEventBuilder::setBField(const double b_field) {
    gbl_data_writer->setBField(b_field);
}
