/**
 * @file EcalUtils.h
 * @brief Class used to encapsulate several Ecal utilities.
 * @author Omar Moreno, SLAC National Accelerator Laboratory 
 */

#ifndef __ECAL_UTILS_H__
#define __ECAL_UTILS_H__

//----------------//
//   C++ StdLib   //
//----------------//
#include <vector>

//------------------//
//   HPS Analysis   //
//------------------//
#include <FlatTupleMaker.h>

//-------------//
//   HPS DST   //
//-------------//
#include <EcalCluster.h>
#include <HpsParticle.h>

class EcalUtils { 

    public: 

        /** Constructor */
        EcalUtils(); 

        /** Destructor */
        ~EcalUtils(); 

        /** */
        bool hasGoodClusterPair(HpsParticle* particle); 
   
        /** */
        void setCoincidenceTime(double coin_time) { coin_time_ = coin_time; } 

        /** Use loose Ecal cluster selection. */
        void useLooseSelection(bool loose_selection) { loose_selection_ = loose_selection; } 

    private:
  
        double coin_time_{3.0}; 

        double top_time_window_low_{38.625};
        double top_time_window_high_{46.8125}; 
        double bot_time_window_low_{37.25};
        double bot_time_window_high_{47.23};

        bool loose_selection_{false}; 

}; // EcalUtils

#endif // __ECAL_UTILS_H__
