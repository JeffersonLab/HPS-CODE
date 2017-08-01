
/** 
 * @file BumpHunter.cxx
 * @brief
 * @author Omar Moreno <omoreno1@ucsc.edu>
 *         Santa Cruz Institute for Particle Physics
 *         University of California, Santa Cruz
 * @date January 14, 2015
 *
 */

#include <BumpHunter.h>
//#include <RooExpPoly.h>
#include "RooExponential.h"


BumpHunter::BumpHunter(BkgModel model, int poly_order, int res_factor) 
    : comp_model(nullptr), 
      bkg_model(nullptr),
      _model(nullptr),
      signal(nullptr), 
      bkg(nullptr),
      ofs(nullptr),
      _res_factor(res_factor), 
      window_size(0.01),
      _poly_order(poly_order),
	  _model_type(model){

    std::cout << "[ BumpHunter ]: Model type: " << _model_type << std::endl;
    std::cout << "[ BumpHunter ]: Background polynomial: " << _poly_order << std::endl;
    std::cout << "[ BumpHunter ]: Resolution multiplicative factor: " << _res_factor << std::endl;

    // Turn off all messages except errors
    RooMsgService::instance().setGlobalKillBelow(RooFit::ERROR);

    // Independent variable
    variable_map["invariant mass"] = new RooRealVar("Invariant Mass", "Invariant Mass (GeV)", 0., 0.3);

    //   Signal PDF   //
    //----------------//   

    variable_map["A' mass"]  = new RooRealVar("A' Mass",  "A' Mass",  0.03);

    variable_map["A' mass resolution"] 
        = new RooRealVar("A' Mass Resolution", "A' Mass Resolution", this->getMassResolution(0.03));

    signal = new RooGaussian("signal", "signal", *variable_map["invariant mass"],
                             *variable_map["A' mass"], *variable_map["A' mass resolution"]);

    //   Bkg PDF   //
    //-------------//

    std::string name;
    for (int order = 1; order <= _poly_order; ++order) {
        name = "t" + std::to_string(order);
        variable_map[name] = new RooRealVar(name.c_str(), name.c_str(), 0, -5, 5);
        arg_list.add(*variable_map[name]);
    } 

    
    switch(model) { 
        case BkgModel::POLY: {
            std::cout << "[ BumpHunter ]: Modeling the background using a polynomial of order " 
                      << poly_order << std::endl;
            bkg = new RooChebychev("bkg", "bkg", *variable_map["invariant mass"], arg_list);
        } break;
        case BkgModel::EXP_POLY: {
            std::cout << "[ BumpHunter ]: Modeling the background using an exp(poly of order "
                      << poly_order << ")" << std::endl;
            RooChebychev* exp_poly_bkg 
                = new RooChebychev("exp_poly_bkg", "exp_poly_bkg", *variable_map["invariant mass"], arg_list);
            bkg = new RooExponential("bkg", "bkg", *exp_poly_bkg, *(new RooRealVar("const", "const", 1))); 
        } break;
        case BkgModel::EXP_POLY_X_POLY: { 
            std::cout << "[ BumpHunter]: Modeling the background using an exp(-cx)*(poly of order "
                      << poly_order << ")" << std::endl;
            variable_map["c"] = new RooRealVar("const", "const", 0, -200, -0.000001);
            RooChebychev* poly_bkg 
                = new RooChebychev("poly_bkg", "poly_bkg", *variable_map["invariant mass"], arg_list);
            RooExponential* exponential 
                = new RooExponential("exp_bkg", "exp_bkg", *variable_map["invariant mass"], *variable_map["c"]);
            bkg = new RooProdPdf("bkg", "bkg", *poly_bkg, *exponential); 
        } break;
    }

    //   Composite Models   //
    //----------------------//
    std::cout << "[ BumpHunter ]: Creating composite model." << std::endl;

    variable_map["signal yield"] = new RooRealVar("signal yield", "signal yield", 0, -100000, 100000);
    variable_map["bkg yield"] = new RooRealVar("bkg yield", "bkg yield", 300000, 10000, 100000000);

    comp_model = new RooAddPdf("comp model", "comp model", RooArgList(*signal, *bkg), 
                               RooArgList(*variable_map["signal yield"], *variable_map["bkg yield"]));

    bkg_model = new RooAddPdf("bkg model", "bkg model", 
                              RooArgList(*bkg), RooArgList(*variable_map["bkg yield"]));
    _model = comp_model;


    for (auto& element : variable_map) {
        default_values[element.first] = element.second->getVal(); 
        default_errors[element.first] = element.second->getError(); 
    }
}

BumpHunter::~BumpHunter() {

    for (auto& element : variable_map) { 
       delete element.second; 
    }
    variable_map.clear();

    delete signal;
    delete bkg;
    delete comp_model; 
}

/*std::map<double, HpsFitResult*> BumpHunter::fitWindow(TH1* histogram, double start, double end, double step) {

    // Set the range of the mass variable based on the range of the histogram. 
    variable_map["invariant mass"]->setRange(histogram->GetXaxis()->GetXmin(), histogram->GetXaxis()->GetXmax()); 

    // Create a histogram object compatible with RooFit.
    RooDataHist* data = new RooDataHist("data", "data", RooArgList(*variable_map["invariant mass"]), histogram);
    
    // Create a container for the results from the fit to each window.
    std::map<double, HpsFitResult*> results; 
    
    while (start <= end) { 
     
        // Construct a window of size x*(A' mass resolution) around the A' mass
        // hypothesis and do a Poisson likelihood fit within the window range. 
        HpsFitResult* result = this->fitWindow(data, start);

        // Save the result to the map of results
        results[start] = result; 
        if (ofs != nullptr) result->getRooFitResult()->printMultiline(*ofs, 0, kTRUE, "");

        // Increment the A' mass hypothesis
        start += step; 
    
        // Reset all of the parameters to their original values
        this->resetParameters(result->getRooFitResult()->floatParsInit()); 
    }
    
    delete data;

    return results;  
}*/

HpsFitResult* BumpHunter::fitWindow(TH1* histogram, double ap_hypothesis, bool bkg_only, bool save_plots) {

    // Find the lower bound of the histogram
    lower_bound = histogram->GetXaxis()->GetBinCenter(histogram->FindFirstBinAbove());
    this->printDebug("Histogram lower bound: " + std::to_string(lower_bound));

    // Find the upper bound of the histogram
    upper_bound = histogram->GetXaxis()->GetBinCenter(histogram->FindLastBinAbove());
    this->printDebug("Histogram upper bound: " + std::to_string(upper_bound));
   
    // Set the total number of bins 
    bins = histogram->GetNbinsX(); 
    hist_min_mass = histogram->GetXaxis()->GetXmin();
    hist_max_mass = histogram->GetXaxis()->GetXmax();
    variable_map["invariant mass"]->setBins(bins);
    variable_map["invariant mass"]->setRange(hist_min_mass, hist_max_mass);

    // Create a histogram object compatible with RooFit.
    RooDataHist* data = new RooDataHist("data", "data", RooArgList(*variable_map["invariant mass"]), histogram);

    // Construct a window of size x*(A' mass resolution) around the A' mass
    // hypothesis and do a Poisson likelihood fit within the window range. 
    HpsFitResult* result = this->fitWindow(data, ap_hypothesis, bkg_only, false, save_plots);
   
    // Delete the histogram object from memory
    delete data;

    // Return the result
    return result;
}

HpsFitResult* BumpHunter::fitWindow(RooDataHist* data, double ap_hypothesis, bool bkg_only, bool const_sig, bool make_plots) {

    this->printDebug("A' mass hypothesis: " + std::to_string(ap_hypothesis)); 
    RooUniformBinning& binning = (RooUniformBinning&) variable_map["invariant mass"]->getBinning(0);
    ap_hypothesis = binning.binCenter(binning.binNumber(ap_hypothesis));
    this->printDebug("Shifting A' mass hypothesis to nearest bin center: " + std::to_string(ap_hypothesis));  

    // If the A' hypothesis is below the lower bound, throw an exception.  A 
    // fit cannot be performed using an invalid value for the A' hypothesis.
    if (ap_hypothesis < lower_bound) throw std::runtime_error("A' hypothesis is less than the lower bound!"); 

    // Get the mass resolution at the mass hypothesis.  
    double mass_resolution = this->getMassResolution(ap_hypothesis);
    this->printDebug("Mass resolution: " + std::to_string(mass_resolution));

    // Calculate the fit window size
    window_size = mass_resolution*_res_factor;
    this->printDebug("Window size: " + std::to_string(window_size));
     
    // If the window size is larger than the max size, set the window size
    // to the max.
    if (window_size > _max_window_size) {
        this->printDebug("Window size exceeds maximum."); 
        window_size = _max_window_size; 
    }
    
    // Find the starting position of the window. This is set to the low edge of 
    // the bin closest to the calculated value.
    double window_start = ap_hypothesis - window_size/2;
    this->printDebug("Calculated starting position of the window: " + std::to_string(window_start)); 
    window_start = binning.binLow(binning.binNumber(window_start));
    this->printDebug("Starting position of the window: " + std::to_string(window_start)); 

    // Check that the starting edge of the window is above the boundary.  If not
    // set the starting edge of the window to the boundary.  In this case, the
    // A' hypothesis will not be set to the middle of the window.
    if (window_start < this->lower_bound) { 
        this->printDebug("Starting edge of window " + std::to_string(window_start) + " is below lower bound.");
        this->printDebug("Setting edge to lower bound, " + std::to_string(this->lower_bound)); 
        window_start = this->lower_bound;
    }

    double window_end = window_start + window_size;

    this->printDebug("Calculated end position of the window: " + std::to_string(window_end)); 
    window_end = binning.binHigh(binning.binNumber(window_end));
    this->printDebug("Ending position of the window: " + std::to_string(window_end)); 

    // Check that the end edge of the window is within the high bound.  If not,
    // set the starting edge such that end edge is equal to the high bound.
    // TODO: Check that this calculation makes sense.
    if (window_end > this->upper_bound) { 
        this->printDebug("End of window " + std::to_string(window_end) + " is above high bound.");
        this->printDebug("Setting starting edge to " + std::to_string(upper_bound - window_size)); 
        window_start = upper_bound - window_size;  
    }

    // Calculate the total number of bins within the window
    this->printDebug("Bin number @ window end: " + std::to_string(binning.binNumber(window_end)));
    this->printDebug("Bin number @ window start: " + std::to_string(binning.binNumber(window_start)));
    double n_bins = binning.binNumber(window_end) - binning.binNumber(window_start); 

    // If a background only fit was requested, set the signal yield to 0. 
    if (bkg_only) { 
        std::cout << "[ BumpHunter ]: Performing a background only fit." << std::endl;
        // Fix the signal yield at 0.
        variable_map["signal yield"]->setVal(0);
        variable_map["signal yield"]->setConstant(kTRUE);
    }

    // Set the mean of the Gaussian signal distribution
    variable_map["A' mass"]->setVal(ap_hypothesis);

    if (const_sig) variable_map["signal yield"]->setConstant(kTRUE);

    // Set the width of the Gaussian signal distribution
    variable_map["A' mass resolution"]->setVal(this->getMassResolution(ap_hypothesis)); 
    
    // Set the range that will be used in the fit
    std::string range_name = "ap_mass_" + std::to_string(ap_hypothesis) + "gev"; 
    variable_map["invariant mass"]->setRange(range_name.c_str(), window_start, window_end); 
    variable_map["invariant mass"]->setRange(window_start, window_end); 
   
    // Estimate the background normalization within the window by integrating
    // the histogram within the window range.  This should be close to the 
    // background yield in the case where there is no signal present.
    double integral = data->sumEntries(0, range_name.c_str()); 
    variable_map["bkg yield"]->setVal(integral);
    //if (ofs != nullptr) ofs << "Estimated bkg in range (" << start << ", " << start + window_size << "): " << integral; 
    //<< std::endl;

    if(_model_type == 2){ //Try to fit the background to an exponential-only model
                          // before fitting to an exponential*polynomial model.  
                          // in order to set the initial conditions for the exp*poly.
    	for (int order = 1; order <= _poly_order; ++order) {
    	        std::string name = "t" + std::to_string(order);
    	        variable_map[name]->setRange(0, 0);
    	}
    	this->fit(data, false, range_name);
    	for (int order = 1; order <= _poly_order; ++order) {
    	    	        std::string name = "t" + std::to_string(order);
    	    	        variable_map[name]->setRange(-2, 2);
    	}
    }

    // Fit the distribution in the given range
    HpsFitResult* result = this->fit(data, false, range_name); 
   
    //  
    std::string output_path = "fit_result_" + range_name + (bkg_only ? "_bkg" : "_full") + ".png";
    if ((!const_sig) && make_plots) {
        printer->print(variable_map["invariant mass"], data, _model, range_name, output_path, n_bins, ap_hypothesis, bkg_only);
        if (_write_results) { 
     
            // Create the output file name string
            char buffer[100];
            std::string output_file = "results_mass" + std::to_string(ap_hypothesis) + 
                                      "_order" + std::to_string(_poly_order) + 
                                      "_res_factor" + std::to_string(_res_factor) + 
                                      (bkg_only ? "_bkg" : "_full") + 
                                      ".txt";
            std::cout << "[ BumpHunter ]: Writing results to " << output_file << std::endl;
            sprintf(buffer, output_file.c_str()); 

            // Create a file stream  
            ofs = new std::ofstream(buffer, std::ofstream::out); 
            result->getRooFitResult()->printMultiline(*ofs, 0, kTRUE, "");

            ofs->close();
        }
    }

    // Set the total number of bins within the fit window
    result->setNBins(n_bins);
    this->printDebug("bins");
     

    // Set the window size 
    result->setWindowSize(window_size);
    this->printDebug("window size");

    // Set the total number of events within the window
    result->setIntegral(integral); 
    this->printDebug("integral");
 
    // Calculate the size of the background window as 2.56*(mass_resolution)
    double bkg_window_size = std::trunc(mass_resolution*2.56*10000)/10000 + 0.00005;
    result->setBkgWindowSize(bkg_window_size); 
    this->printDebug("bkg size");

    // Find the starting position of the bkg window
    double bkg_window_start = ap_hypothesis - bkg_window_size/2;

    // Create a range for the background window
    std::string bkg_range_name = "ap_mass_" + std::to_string(ap_hypothesis) + "_bkg_est";
    variable_map["invariant mass"]->setRange(bkg_range_name.c_str(), 
            bkg_window_start, bkg_window_start + bkg_window_size);

    
    double bkg_window_integral = data->sumEntries("1", bkg_range_name.c_str()); 
    result->setBkgTotal(bkg_window_integral); 
    this->printDebug("bkg total");

    // TODO: These calculations should be moved out of this method.
    if (!bkg_only & !const_sig) {
        this->calculatePValue(data, result, ap_hypothesis);
        this->getUpperLimit(data,  result, ap_hypothesis);
    }
    
    variable_map["signal yield"]->setConstant(kFALSE);
    
    return result;  
} 

HpsFitResult* BumpHunter::fit(RooDataHist* data, bool migrad_only = false, std::string range_name = "") { 
   
    // Construct a log likelihood using the data set within the range specified
    // above.  This is equivalent to saying that 
    // nll = -ln(L( window_start < x < window_start + window_size | mu, theta))
    // where mu is the signal yield and theta represents the set of all 
    // nuisance parameters which in this case are the background normalization
    // and polynomial constants.  Since the likelihood is being constructed
    // from a histogram, use an extended likelihood.
    RooAbsReal* nll = _model->createNLL(*data, 
            RooFit::Extended(kTRUE), 
            RooFit::Verbose(kTRUE), 
            RooFit::Range(range_name.c_str()), 
            RooFit::SumCoefRange(range_name.c_str())
            );  

    // Instantiate minuit using the constructed likelihood above
    RooMinuit m(*nll);

    // Turn off all print out
    m.setPrintLevel(-1000);

    // Use migrad to minimize the likelihood.  If migrad fails to find a minimum,
    // run simplex in order to run a sparser search for a minimum followed by
    // migrad again.
    int status = m.migrad(); 
    if (status != 0) { 
        m.simplex();
        status = m.migrad();
    }

    // Save the results of the fit
    RooFitResult* result = m.save(); 

    // Delete the constructed negative log likelihood
    delete nll; 

    // Return the saves result
    return new HpsFitResult(result); 
}


void BumpHunter::calculatePValue(RooDataHist* data, HpsFitResult* result, double ap_hypothesis) {

    //  Get the signal yield obtained from the composite fit
    double signal_yield = result->getParameterVal("signal yield");

    // We only care if a signal yield is greater than 0.  In the case that it's
    // less than 0, the p-value is set to 1.
    if (signal_yield <= 0) { 
        result->setPValue(1);
        std::cout << "[ BumpHunter ]: p-value: 1" << std::endl;
        return; 
    }

    // Get the NLL obtained by minimizing the composite model with the signal
    // yield floating.
    double mle_nll = result->getRooFitResult()->minNll();
    printDebug("mu != 0 NLL: " + std::to_string(mle_nll));

    // Reset all parameters to their original values
    this->resetParameters(); 
   
    // Fit the window assuming a background only hypothesis i.e. the signal
    // yield is set to 0.
    HpsFitResult* cond_result = this->fitWindow(data, ap_hypothesis, true);

    // Get the NLL obtained from the Bkg only fit.
    double cond_nll = cond_result->getRooFitResult()->minNll();
    printDebug("mu = 0 NLL: " + std::to_string(cond_nll));
   
    // 1) Calculate the likelihood ratio which is chi2 distributed. 
    // 2) From the chi2, calculate the p-value.
    double q0 = 0; 
    double p_value = 0; 
    this->getChi2Prob(cond_nll, mle_nll, q0, p_value);  

    std::cout << "[ BumpHunter ]: p-value: " << p_value << std::endl;

    // Update the result
    result->setPValue(p_value);
    result->setQ0(q0);  
    
    delete cond_result; 
}

void BumpHunter::printDebug(std::string message) { 
    if (debug) std::cout << "[ BumpHunter ]: " << message << std::endl;
}

void BumpHunter::resetParameters() { 
   
    for (auto& element : variable_map) {
        auto it = default_values.find(element.first);
        if (it == default_values.end()) {
            printDebug("Value " + element.first + " was not found.");
        }
        element.second->setVal(default_values[element.first]);
        element.second->setError(default_errors[element.first]);
    }
    variable_map["invariant mass"]->setRange(hist_min_mass, hist_max_mass);
    variable_map["invariant mass"]->setBins(bins); 
}

/*
void BumpHunter::getUpperLimit(TH1* histogram, HpsFitResult* result, double ap_mass) { 
    
    // Set the range of the mass variable based on the range of the histogram. 
    variable_map["invariant mass"]->setRange(histogram->GetXaxis()->GetXmin(), histogram->GetXaxis()->GetXmax()); 

    // Create a histogram object compatible with RooFit.
    RooDataHist* data = new RooDataHist("data", "data", RooArgList(*variable_map["invariant mass"]), histogram);

    this->getUpperLimit(data, result, ap_mass);
    
    delete data;  
}*/

void BumpHunter::getUpperLimit(RooDataHist* data, HpsFitResult* result, double ap_mass) { 

    std::cout << "[ BumpHunter ]: Calculating upper limit @ m_{A'} = " << ap_mass << std::endl;

    //  Get the signal yield obtained from the signal+bkg fit
    double signal_yield = result->getParameterVal("signal yield");
    this->printDebug("Signal yield @ min NLL: " + std::to_string(signal_yield));

    // Get the minimum NLL value that will be used for testing upper limits.
    // If the signal yield (mu estimator) at the min NLL is < 0, use the NLL
    // obtained when mu = 0.
    double mle_nll = result->getRooFitResult()->minNll();
    if (signal_yield < 0) {

        this->printDebug("Signal yield @ min NLL is < 0. Using NLL when signal yield = 0");

        // Reset all of the parameters to their original values
        this->resetParameters(); 
    
        // Do the fit
        HpsFitResult* null_result = this->fitWindow(data, ap_mass, true, false, false);
    
        // Get the NLL obtained assuming the background only hypothesis
        mle_nll = null_result->getRooFitResult()->minNll(); 
    }
    this->printDebug("MLE NLL: " + std::to_string(mle_nll));     

    double p_value = 1;
    double q0 = 0;
    signal_yield = floor(signal_yield);
    int iteration = 0;
    int max_iterations = 5000;
    while(true) {

        // Reset all of the parameters to their original values
        this->resetParameters(); 

        if (p_value <= 0.053) signal_yield += 1;
        else if (p_value <= 0.10) signal_yield += 30;
        else if (p_value <= 0.2) signal_yield += 100; 
        else signal_yield += 300;  
        this->printDebug("Signal yield: " + std::to_string(signal_yield));
        variable_map["signal yield"]->setVal(signal_yield);

        HpsFitResult* current_result = this->fitWindow(data, ap_mass, false, true);
        
        double cond_nll = current_result->getRooFitResult()->minNll(); 

        this->getChi2Prob(cond_nll, mle_nll, q0, p_value);  

        this->printDebug("p-value after fit: " + std::to_string(p_value)); 
        if (p_value <= 0.05) { 
            std::cout << "[ BumpHunter ]: Upper limit: " << signal_yield << std::endl;
            result->setUpperLimit(signal_yield); 
            delete current_result; 
            break; 
        }
        this->printDebug("iteration number: " + std::to_string(iteration++));
        //avoid infinite loops where p value stops changing.
        if(iteration > max_iterations){
        	std::cout << "[ BumpHunter ]: Warning: Upper limit stuck at: " << signal_yield << " with p value"<< p_value<< std::endl;
        	result->setUpperLimit(signal_yield);
        	delete current_result;
        	break;
        }
        
        delete current_result; 
    }
}

void BumpHunter::getChi2Prob(double cond_nll, double mle_nll, double &q0, double &p_value) {
     
    double diff = cond_nll - mle_nll;
    this->printDebug("Diff: " + std::to_string(diff));
    
    q0 = 2*diff;
    this->printDebug("q0: " + std::to_string(q0));
    
    p_value = ROOT::Math::chisquared_cdf_c(q0, 1);
    this->printDebug("p-value before dividing: " + std::to_string(p_value));  
    p_value *= 0.5;
    this->printDebug("p-value: " + std::to_string(p_value)); 
}

void BumpHunter::setBounds(double lower_bound, double upper_bound) {
    this->lower_bound = lower_bound; 
    this->upper_bound = upper_bound;
    printf("Fit bounds set to [ %f , %f ]\n", this->lower_bound, this->upper_bound);   
}

std::vector<RooDataHist*> BumpHunter::generateToys(TH1* histogram, double n_toys, double ap_hypothesis) { 

    this->resetParameters(); 
    
    // Begin by performing a fit to the background with the signal yield set to
    // 0.
    HpsFitResult* null_result = this->fitWindow(histogram, ap_hypothesis, true, false);

    // Set the total number of bins that will be used when generating the toys 
    variable_map["invariant mass"]->setBins(null_result->getNBins()); 

    std::vector<RooDataHist*> datum;
    for (int toy_n = 0; toy_n < n_toys; ++toy_n) { 
          datum.push_back(comp_model->generateBinned(RooArgSet(*variable_map["invariant mass"]), 
                          null_result->getIntegral(), RooFit::Extended(kTRUE)));  
    }
    variable_map["signal yield"]->setConstant(kFALSE);
    
    return datum;
}

std::vector<HpsFitResult*> BumpHunter::runToys(TH1* histogram, double n_toys, double ap_hypothesis) { 
  
    // Begin by fitting the window of interest with a background only model.  The
    // results are then used to generate n_toys that will be used to evaluate the
    // fitter within the window. 
    std::cout << "[ BumpHunter ]: Generating " << std::to_string(n_toys) 
              << " toy distributions." << std::endl;
    std::vector<RooDataHist*> datum = this->generateToys(histogram, n_toys, ap_hypothesis);
    std::cout << "[ BumpHunter ]: Toy distributions were successfully generated." << std::endl;

    // Write the histograms to a file.
    TFile* file = new TFile("toy_histograms.root", "recreate"); 

    // Loop through all of the toy histograms and fit them.
    std::vector<HpsFitResult*> results;
    int index{0}; 
    for (auto& data : datum) { 
       
        data->createHistogram(("toy_" + std::to_string(index)).c_str(), *variable_map["invariant mass"])->Write();
        // Reset all of the parameters to their original values
        this->resetParameters(); 
        std::cout << "[ BumpHunter ]: running the " << index << "th toy (not bothering with grammar)" << std::endl;
        // Construct a window of size x*(A' mass resolution) around the A' mass
        // hypothesis and do a Poisson likelihood fit within the window range. 
        results.push_back(this->fitWindow(data, ap_hypothesis, false));

        ++index; 
    }

    file->Close(); 
    return results;
}
