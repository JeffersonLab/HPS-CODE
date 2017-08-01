/**
 * @file AnalysisUtils.h
 * @brief A set of utilities commonly used when doing analysis
 * @author Omar Moreno, SLAC National Accelerator Laboratory
 */

#ifndef __ANALYSIS_UTILS_H__
#define __ANALYSIS_UTILS_H__

//----------------//
//   C++ StdLib   //
//----------------//
#include <vector>
#include <cmath>

//-------------//
//   HPS DST   //
//-------------//
#include <SvtTrack.h>

namespace AnalysisUtils { 

    /**
     * Get the magnitude of a 3D vector.  If the vector doesn't
     * contain exactly three elements, an exception is thrown.
     *
     * @param v : 3D vector
     * @return Magnitude of the vector
     */
    double getMagnitude(std::vector<double> v);

    /**
     * Calculate the invariant mass of a pair of tracks.
     *
     * @param track_0 SVT track composing a pair
     * @param track_1 SVT track composing a pair
     * @return invariant mass of the track pair
     */
    double getInvariantMass(SvtTrack* track_0, SvtTrack* track_1);
    
    /**
     *
     */
    template <typename T> int sgn(T val) {
        return (T(0) < val) - (val < T(0));
    }

}

#endif // __ANALYSIS_UTILS_H__
