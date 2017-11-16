/**
 *
 *
 *
 */

#ifndef __HPS_FIT_RESULT_H__
#define __HPS_FIT_RESULT_H__

//------------//
//   RooFit   //
//------------//
#include <RooFitResult.h>
#include <RooRealVar.h>

class HpsFitResult { 

    public: 

        /** Default constructor */
        HpsFitResult(); 

        /** */
        HpsFitResult(RooFitResult* result, double q0 = 0, double p_value = 0, double upper_limit = 0);

        ~HpsFitResult(); 
       
        void addLikelihood(double likelihood) { _likelihoods.push_back(likelihood); }

        void addSignalYield(double signal_yield) { _signal_yields.push_back(signal_yield); }

        /** @return _bins The total number of bins within the fit window. */
        double getNBins() { return _bins; };

        /** @return _integral The integral within the fit window. */
        double getIntegral() { return _integral; };

        /** @return The mass hypothesis used for this fit. */
        double getMass() const { return _mass; };

        /** */
        double getQ0() { return q0; };

        /** */
        double getPValue() { return p_value; };

        /** */
        double getParameterVal(std::string parameter_name); 

        /** */
        RooFitResult* getRooFitResult() { return result; };  

        double getBkgTotal() {return this->bkg_total; };

        double getBkgWindowSize() { return this->bkg_window_size; };  

        /** */
        double getUpperLimit() { return upper_limit; };

        double getUpperLimitPValue() { return _upper_limit_p_value; }; 

        double getUpperLimitFitStatus() { return _upper_limit_fit_status; }; 

        /** @return The size of the fit window used. */
        double getWindowSize() { return this->window_size; }; 

        std::vector<double> getLikelihoods() { return _likelihoods; }
        
        std::vector<double> getSignalYields() { return _signal_yields; }

        //-------------//
        //   Setters   //
        //-------------//

        /** Set the total number of bins within the fit window. */
        void setNBins(double bins) { _bins = bins; };

        void setBkgTotal(double bkg_total) { this->bkg_total = bkg_total; };
        
        void setBkgWindowSize(double bkg_window_size) { this->bkg_window_size = bkg_window_size; };  

        void setIntegral(double integral) { _integral = integral; };

        /** */
        double setQ0(double q0) { this->q0 = q0; };

        /** */
        void setPValue(double p_value) { this->p_value = p_value; };  
        
        /** */
        void setRooFitResult(RooFitResult* result) { this->result = result; }; 

        /** 
         * Set mass hypothesis used for this fit. 
         * 
         * @param mass The mass hypothesis. 
         */
        void setMass(double mass) { _mass = mass; };

        /**
         * Set the 2 sigma upper limit.
         *
         * @param upper_limit The 2 sigma upper limit.
         */
        void setUpperLimit(double upper_limit) { this->upper_limit = upper_limit; };

        /** Set the p-value at the end of the upper limit calculation. */
        void setUpperLimitPValue(double upper_limit_p_value) { _upper_limit_p_value = upper_limit_p_value; }

        /** Set the fit status at the end of the upper limit calculation. */
        void setUpperLimitFitStatus(double upper_limit_fit_status) { 
            _upper_limit_fit_status = upper_limit_fit_status; 
        }

        /**
         * Set the size of the fit window used to get this results.
         *
         * @oaram window_size The size of the fit window.
         */
        void setWindowSize(double window_size) { this->window_size = window_size; }; 

    private: 

        /** Result associated with RooFit. */
        RooFitResult* result; 

        std::vector<double> _likelihoods; 

        std::vector<double> _signal_yields; 

        double bkg_total;

        double bkg_window_size;

        /** Total number of bins within the fit window. */
        double _bins{0}; 

        /** Total number of events within the fit window. */
        double _integral{0};

        /** Mass hypothesis. */
        double _mass{0}; 

        /** q0 value */
        double q0;
        
        /** p-value. */
        double p_value;

        /** 2 sigma upper limit on the signal. */
        double upper_limit; 

        /** p-value at the upper limit. */
        double _upper_limit_p_value{-9999};

        /** Fit status at the end of the upper limit calculation. */
        double _upper_limit_fit_status{-9999};  
        
        /*** Size of the fit window. */
        double window_size;

}; // HpsFitResult

#endif // __HPS_FIT_RESULT_H__
