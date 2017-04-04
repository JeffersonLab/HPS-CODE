/**
 * @file EcalUtils.cxx
 * @brief Class used to encapsulate several Ecal utilities.
 * @author Omar Moreno, SLAC National Accelerator Laboratory 
 */

#include <EcalUtils.h>

EcalUtils::EcalUtils() { 
}

EcalUtils::~EcalUtils() { 
}

bool EcalUtils::hasGoodClusterPair(HpsParticle* particle) { 

    // Get the daughter particles composing this particle. 
    TRefArray* daughter_particles = particle->getParticles();
        
    // Check that the mother particle has exactly two daughters. If not, return
    // false.
    if (daughter_particles->GetEntriesFast() != 2) return false;

    // Check that the two daughters have an Ecal cluster associated with them.
    // If not, return false.
    if (particle->getClusters()->GetEntriesFast() != 2) return false; 

    double top_index = 0;
    double bot_index = 1;
    if (static_cast<EcalCluster*>(particle->getClusters()->At(bot_index))->getPosition()[1] > 0) { 
        top_index = 1;
        bot_index = 0;
    }

    EcalCluster* top{static_cast<EcalCluster*>(particle->getClusters()->At(top_index))};
    EcalCluster* bot{static_cast<EcalCluster*>(particle->getClusters()->At(bot_index))};

    // Make sure the clusters are in opposite Ecal volumes. 
    if (top->getPosition()[1]*bot->getPosition()[1] > 0) {
        return false;
    }

    if (loose_selection_) return true;

    return true; 
}


