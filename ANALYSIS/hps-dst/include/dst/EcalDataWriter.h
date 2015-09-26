/**
 * @file: EcalDataWriter.cxx
 * @author: Omar Moreno <omoreno1@ucsc.edu>
 * @section Institution \n
 *          Santa Cruz Institute for Particle Physics
 *          University of California, Santa Cruz
 *  @date: January 7, 2013
 */

#ifndef __ECAL_DATA_WRITER_H__
#define __ECAL_DATA_WRITER_H__

//-----------//
//--- DST ---//
//-----------//
#include <DataWriter.h>

//-------------//
//--- Utils ---//
//-------------//
#include <EcalUtils.h>

//------------//
//--- LCIO ---//
//------------//
#include <IMPL/LCCollectionVec.h>
#include <IMPL/ClusterImpl.h>
#include <IMPL/CalorimeterHitImpl.h>

//-----------------//
//--- HPS Event ---//
//-----------------//
#include <EcalCluster.h>
#include <EcalHit.h>

class EcalDataWriter : public DataWriter {

    public: 
        
        /**
         * Default constructor
         */
        EcalDataWriter();

        /**
         * Destructor
         */ 
        ~EcalDataWriter(); 

        /**
         * Make EcalClusters and EcalHits out of CalorimeterHits and Clusters
         * and write them to an HpsEvent.
         *
         * @param lc_event : LCSim event from which the CalorimeterHit and 
         *                   Cluster collection is retrieved.
         * @param hps_event : HpsEvent to which the EcalClusters and EcalHits 
         *                    will be written to 
         */        
        void writeData(EVENT::LCEvent* lc_event, HpsEvent* hps_event);     
    
    private:

        std::string clusters_collection_name;

        IMPL::LCCollectionVec* clusters;  
        IMPL::ClusterImpl* cluster;
        IMPL::CalorimeterHitImpl* calorimeter_hit;

        EcalCluster* ecal_cluster;
        EcalHit* ecal_hit;

};  // EcalDataWriter

#endif // __ECAL_DATA_WRITER_H__
