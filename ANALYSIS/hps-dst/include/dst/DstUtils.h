/**
 *
 * @file DstUtils.h
 * @brief A set of utility methods used by the DST writers and maker.
 * @author Omar Moreno <omoreno1@ucsc.edu>
 *         Santa Cruz Institute for Particle Physics (SCIPP)
 *         University of California, Santa Cruz
 * @date September 1, 2015
 *
 */

#ifndef __DST_UTILS_H__
#define __DST_UTILS_H__

//------------------//
//--- C++ StdLib ---//
//------------------//
#include <string>
#include <vector>
#include <iostream>

//------------//
//--- LCIO ---//
//------------//
#include <EVENT/LCEvent.h>
#include <EVENT/LCCollection.h>

namespace DstUtils { 

    /**
     * Get all LCIO collections of the given type from the event.
     *
     * @param event The LCIO event
     * @param type The LCIO collection type
     * @return A vector containing all LCIO collections of the given type
     */
    std::vector<EVENT::LCCollection*> getCollections(EVENT::LCEvent* event, std::string type); 

} // DstUtils

#endif // __DST_UTILS_H__
