/**
 * @file: EcalDataWriter.cxx
 * @author: Omar Moreno <omoreno1@ucsc.edu>
 * @section Institution \n
 *          Santa Cruz Institute for Particle Physics
 *          University of California, Santa Cruz
 *  @date: January 7, 2013
 */

#include <EcalDataWriter.h>

EcalDataWriter::EcalDataWriter()
    : clusters_collection_name("EcalClustersCorr") {
}

EcalDataWriter::~EcalDataWriter() {
}

void EcalDataWriter::writeData(EVENT::LCEvent* event, HpsEvent* hps_event) {
    
    // Get the collection of Ecal clusters from the event
    clusters = (IMPL::LCCollectionVec*) event->getCollection(clusters_collection_name);

    // Loop over all clusters and fill the event
    for(int cluster_n = 0; cluster_n < clusters->getNumberOfElements(); ++cluster_n) {  

        // Get an Ecal cluster from the LCIO collection
        cluster = (IMPL::ClusterImpl*) clusters->getElementAt(cluster_n);

        // Add a cluster to the HPS Event
        ecal_cluster = hps_event->addEcalCluster();

        // Set the cluster position
        ecal_cluster->setPosition(cluster->getPosition());

        // Set the cluster energy
        ecal_cluster->setEnergy(cluster->getEnergy());

        // Get the ecal hits used to create the cluster
        EVENT::CalorimeterHitVec calorimeter_hits = cluster->getCalorimeterHits();

        // Loop over all of the Ecal hits and add them to the Ecal cluster.  The
        // seed hit is set to be the hit with the highest energy.  The cluster time
        // is set to be the hit time of the seed hit.
        for(int ecal_hit_n = 0; ecal_hit_n < (int) calorimeter_hits.size(); ++ecal_hit_n) {

            // Get an Ecal hit
            calorimeter_hit = (IMPL::CalorimeterHitImpl*) calorimeter_hits[ecal_hit_n];

            // Add an Ecal hit to the HPS Event
            ecal_hit = hps_event->addEcalHit();

            // Set the energy of the Ecal hit
            ecal_hit->setEnergy(calorimeter_hit->getEnergy());

            // Set the hit time of the Ecal hit
            ecal_hit->setTime(calorimeter_hit->getTime());

            // Set the indices of the crystal
            int index_x = EcalUtils::getIdentifierFieldValue("ix", calorimeter_hit);
            int index_y = EcalUtils::getIdentifierFieldValue("iy", calorimeter_hit);

            ecal_hit->setCrystalIndices(index_x, index_y);

            // Add the hit to the cluster
            ecal_cluster->addHit(ecal_hit);
        }
    }
}
