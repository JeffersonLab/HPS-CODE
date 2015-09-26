/**
 *
 * @file DstUtils.cxx
 * @brief A set of utility methods used by the DST writers and maker.
 * @author Omar Moreno <omoreno1@ucsc.edu>
 *         Santa Cruz Institute for Particle Physics (SCIPP)
 *         University of California, Santa Cruz
 * @date September 1, 2015
 *
 */

#include <DstUtils.h>

std::vector<EVENT::LCCollection*> DstUtils::getCollections(EVENT::LCEvent* event, std::string type) { 

    // Get a list of collection names from the event    
    std::vector<std::string> collection_names = *event->getCollectionNames();
    
    // Create a container used to store the collections of the given type
    std::vector<EVENT::LCCollection*> collections; 

    // Loop over all the collection names and add those of the given type to
    // container of collections
    for (std::string collection_name : collection_names) { 
        
        // Get the collection of the given name from the LCIO event
        EVENT::LCCollection* collection = event->getCollection(collection_name);

        // If it's of the given type, add it to the container of collections
        if ((collection->getTypeName()).compare(type) == 0) { 
            collections.push_back(collection); 
        }
    }

    return collections;
}
