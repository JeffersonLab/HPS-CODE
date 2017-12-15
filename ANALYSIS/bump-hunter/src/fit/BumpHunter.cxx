
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

BumpHunter::BumpHunter(BkgModel model, int poly_order, int res_factor) 
    : comp_model(nullptr), 
      bkg_model(nullptr),
      _model(nullptr),
      signal(nullptr), 
      bkg(nullptr),
      ofs(nullptr),
      _res_factor(res_factor), 
      _poly_order(poly_order) {

    std::cout << "[ BumpHunter ]: Background polynomial: " << _poly_order << std::endl;
    std::cout << "[ BumpHunter ]: Resolution multiplicative factor: " << _res_factor << std::endl;

    // Turn off all messages except errors
    RooMsgService::instance().setGlobalKillBelow(RooFit::FATAL);

    // Independent variable
    mass_ = new RooRealVar("Invariant Mass", "Invariant Mass (GeV)", 0., 0.15);

    //   Signal PDF   //
    //----------------//   

    variable_map["A' mass"]  = new RooRealVar("A' Mass",  "A' Mass",  0.03);

    variable_map["A' mass resolution"] 
        = new RooRealVar("A' Mass Resolution", "A' Mass Resolution", this->getMassResolution(0.03));

    signal = new RooGaussian("signal", "signal", *mass_,
                             *variable_map["A' mass"], *variable_map["A' mass resolution"]);

    //   Bkg PDF   //
    //-------------//

    std::string name;
    for (int order = 1; order <= _poly_order; ++order) {
        name = "t" + std::to_string(order);
        variable_map[name] = new RooRealVar(name.c_str(), name.c_str(), 0, -2, 2);
        arg_list.add(*variable_map[name]);
    } 
    
    switch(model) { 
        case BkgModel::POLY: {
            std::cout << "[ BumpHunter ]: Modeling the background using a polynomial of order " 
                      << poly_order << std::endl;
            bkg = new RooChebychev("bkg", "bkg", *mass_, arg_list);
        } break;
        case BkgModel::EXP_POLY: {
            std::cout << "[ BumpHunter ]: Modeling the background using an exp(poly of order "
                      << poly_order << ")" << std::endl;
            RooChebychev* exp_poly_bkg 
                = new RooChebychev("exp_poly_bkg", "exp_poly_bkg", *mass_, arg_list);
            bkg = new RooExponential("bkg", "bkg", *exp_poly_bkg, *(new RooRealVar("const", "const", 1))); 
        } break;
        case BkgModel::EXP_POLY_X_POLY: { 
            std::cout << "[ BumpHunter]: Modeling the background using an exp(-cx)*(poly of order "
                      << poly_order << ")" << std::endl;
            variable_map["c"] = new RooRealVar("const", "const", 0, -2, -0.000001);
            RooChebychev* poly_bkg 
                = new RooChebychev("poly_bkg", "poly_bkg", *mass_, arg_list);
            RooExponential* exponential 
                = new RooExponential("exp_bkg", "exp_bkg", *mass_, *variable_map["c"]);
            bkg = new RooProdPdf("bkg", "bkg", *poly_bkg, *exponential); 
        } break;
    }


    //   Composite Models   //
    //----------------------//
    std::cout << "[ BumpHunter ]: Creating composite model." << std::endl;

    variable_map["signal yield"] = new RooRealVar("signal yield", "signal yield", 0, -1e13, 1e13);
    variable_map["bkg yield"] = new RooRealVar("bkg yield", "bkg yield", 30000000, -1e13, 1e13);

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

void BumpHunter::initialize(TH1* histogram, double &mass_hypothesis) { 

    // If the lower histogram bound has not been set, find it by searching
    // for the first non-empty bin.
    if (_lower_bound == -9999) { 
        _lower_bound = histogram->GetXaxis()->GetBinCenter(histogram->FindFirstBinAbove());
        this->printDebug("Histogram lower bound: " + std::to_string(_lower_bound));
    }
    
    // If the upper histogram bound has not been set, find it by searching 
    // for the last non-empty bin.
    if (_upper_bound == -9999) {
        _upper_bound = histogram->GetXaxis()->GetBinCenter(histogram->FindLastBinAbove());
        this->printDebug("Histogram upper bound: " + std::to_string(_upper_bound));
    }

    // Set the total number of bins used to bin the mass spectrum 
    bins = histogram->GetNbinsX(); 
    mass_->setBins(bins);
    this->printDebug("Total number of bins: " + std::to_string(bins)); 

    // Shift the mass hypothesis so it sits in the middle of a bin
    this->printDebug("Mass hypothesis: " + std::to_string(mass_hypothesis)); 
    int mbin = histogram->GetXaxis()->FindBin(mass_hypothesis); 
    this->printDebug("Mass hypothesis bin: " + std::to_string(mbin)); 
    mass_hypothesis = histogram->GetXaxis()->GetBinCenter(mbin);  
    this->printDebug("Shifting mass hypothesis to nearest bin center: " + std::to_string(mass_hypothesis));  

    // If the mass hypothesis is below the lower bound, throw an exception.  A 
    // search cannot be performed using an invalid value for the mass hypothesis.
    if (mass_hypothesis < _lower_bound) throw std::runtime_error("Mass hypothesis less than the lower bound!"); 

    // Set the mean of the Gaussian signal distribution
    variable_map["A' mass"]->setVal(mass_hypothesis);

    // Correct the mass to take into account the mass scale systematic
    double corr_mass = this->correctMass(mass_hypothesis);

    // Get the mass resolution at the corrected mass 
    //double mass_resolution = this->getMassResolution(mass_hypothesis);
    double mass_resolution = this->getMassResolution(corr_mass);
    std::cout << "[ BumpHunter ]: Mass resolution: " << mass_resolution << " MeV" << std::endl;

    // Set the width of the Gaussian signal distribution
    variable_map["A' mass resolution"]->setVal(mass_resolution); 

    // Calculate the fit window size
    _window_size = mass_resolution*_res_factor;
    this->printDebug("Window size: " + std::to_string(_window_size));

    // Find the starting position of the window. This is set to the low edge of 
    // the bin closest to the calculated value. If the start position falls 
    // below the lower bound of the histogram, set it to the lower bound.
    double window_start = mass_hypothesis - _window_size/2;
    int window_start_bin = histogram->GetXaxis()->FindBin(window_start);  
    window_start = histogram->GetXaxis()->GetBinLowEdge(window_start_bin);
    if (window_start < _lower_bound) { 
        std::cout << "[ BumpHunter ]: Starting edge of window (" << window_start 
                  << " MeV) is below lower bound." << std::endl;
        window_start_bin = histogram->GetXaxis()->FindBin(_lower_bound);
        window_start = histogram->GetXaxis()->GetBinLowEdge(window_start_bin);
    } 
    std::cout << "[ BumpHunter ]: Setting starting edge of window to " 
              << window_start << " MeV." << std::endl;
    
    // Find the end position of the window.  This is set to the upper edge of 
    // the bin closest to the calculated value. If the window edge falls above
    // the upper bound of the histogram, set it to the upper bound.
    // Furthermore, check that the bin serving as the upper boundary contains
    // events. If the upper bound is shifted, reset the lower window bound.
    double window_end = window_start + _window_size;
    int window_end_bin = histogram->GetXaxis()->FindBin(window_end);
    window_end = histogram->GetXaxis()->GetBinUpEdge(window_end_bin);
    if (window_end > _upper_bound) { 
        std::cout << "[ BumpHunter ]: Upper edge of window (" << window_end 
                  << " MeV) is above upper bound." << std::endl;
        window_end_bin = histogram->GetXaxis()->FindBin(_upper_bound);
        
        int last_bin_above = histogram->FindLastBinAbove(); 
        if (window_end_bin > last_bin_above) window_end_bin = last_bin_above; 
        
        window_end = histogram->GetXaxis()->GetBinUpEdge(window_end_bin);
        window_start_bin = histogram->GetXaxis()->FindBin(window_end - _window_size);  
        window_start = histogram->GetXaxis()->GetBinLowEdge(window_start_bin);
    }
    std::cout << "[ BumpHunter ]: Setting upper edge of window to " 
              << window_end << " MeV." << std::endl;

    // Set the range that will be used in the fit
    range_name_ = "mass_" + std::to_string(mass_hypothesis) + "gev"; 
    mass_->setRange(range_name_.c_str(), window_start, window_end); 
    mass_->setRange(window_start, window_end); 

    // Estimate the background normalization within the window by integrating
    // the histogram within the window range.  This should be close to the 
    // background yield in the case where there is no signal present.
    double integral = histogram->Integral(window_start_bin, window_end_bin);
    variable_map["bkg yield"]->setVal(integral);
    variable_map["bkg yield"]->setError(sqrt(integral)); 
    default_values["bkg yield"] = integral;
    default_errors["bkg yield"] = sqrt(integral);  
    this->printDebug("Window integral: " + std::to_string(integral)); 

    // Calculate the size of the background window as 2.56*(mass_resolution)
    _bkg_window_size = std::trunc(mass_resolution*2.56*10000)/10000 + 0.00005;

    // Find the starting position of the bkg window
    double bkg_window_start = mass_hypothesis - _bkg_window_size/2;

    int bkg_window_start_bin = histogram->GetXaxis()->FindBin(bkg_window_start);  
    int bkg_window_end_bin = histogram->GetXaxis()->FindBin(bkg_window_start + _bkg_window_size);  

    _bkg_window_integral = histogram->Integral(bkg_window_start_bin, bkg_window_end_bin); 
    
    variable_map["signal yield"]->setError(sqrt(_bkg_window_integral));
    
    /*
    TCanvas* canvas = new TCanvas("canvas", "canvas", 800, 800); 
    TH1* histogram_clone = (TH1*) histogram->Clone("clone");
    histogram_clone->GetXaxis()->SetRange(window_start_bin/3, window_end_bin/3);
    histogram_clone->Scale(1/histogram_clone->Integral());
    histogram_clone->Fit("pol1"); 
    variable_map["signal yield"]->setVal(histogram_clone->
    histogram_clone->Draw(""); 
    canvas->SaveAs("test_fit.pdf");   
    */
    

}

HpsFitResult* BumpHunter::performSearch(TH1* histogram, double mass_hypothesis) { 
    
    // Start by setting up the window which will be used to search a resonance.
    this->initialize(histogram, mass_hypothesis);

    // Create a histogram object compatible with RooFit.
    RooDataHist* data = new RooDataHist("data", "data", RooArgList(*mass_), histogram);
    
    // Perform a background only fit
    std::cout << "[ BumpHunter ]: Performing a background only fit." << std::endl;
    // Fix the signal yield at 0.
    variable_map["signal yield"]->setConstant(kTRUE);
    bkg_only_result_ = this->fit(data, range_name_); 

    if (!_batch) { 
        std::string output_path = "fit_result_" + std::string(histogram->GetName()) 
                                  + "_" + std::to_string(mass_hypothesis) + "gev_bkg_only.png";
        printer->print(mass_, data, _model, range_name_, output_path); 
        /*if (_write_results) { 
     
            // Create the output file name string
            char buffer[100];
            std::string output_file = "fit_result_" + std::string(histogram->GetName()) 
                                      + "_" + std::to_string(mass_hypothesis) + "gev" + (bkg_only ? "_bkg" : "_full") + ".txt";
            std::cout << "[ BumpHunter ]: Writing results to " << output_file << std::endl;
            sprintf(buffer, output_file.c_str()); 

            // Create a file stream  
            ofs = new std::ofstream(buffer, std::ofstream::out); 
            result->getRooFitResult()->printMultiline(*ofs, 0, kTRUE, "");

            ofs->close();
        }*/
    }

    // Now perform a full fit (signal+bkg).  Use the background fit parameters 
    // as a starting point, but use the default errors.
    this->resetParameters(bkg_only_result_); 
    variable_map["signal yield"]->setConstant(kFALSE);

    // Fit the distribution in the given range
    HpsFitResult* result = this->fit(data, range_name_); 
    
    if (!_batch) { 
        std::string output_path = "fit_result_" + std::string(histogram->GetName()) 
                      + "_" + std::to_string(mass_hypothesis) + "gev_full.png";
        printer->print(mass_, data, _model, range_name_, output_path); 
    }

    // Persist the mass hypothesis used for this fit
    result->setMass(mass_hypothesis); 

    // Set the window size 
    result->setWindowSize(_window_size);

    // Set the total number of events within the window
    result->setIntegral(default_values["bkg yield"]);

    // Calculate the size of the background window as 2.56*(mass_resolution)
    result->setBkgWindowSize(_bkg_window_size); 

    result->setBkgTotal(_bkg_window_integral); 

    this->calculatePValue(result);
    this->getUpperLimit(data, range_name_, result);

    result->setCorrectedMass(this->correctMass(mass_hypothesis)); 

    return result; 
}

HpsFitResult* BumpHunter::fit(RooDataHist* data, std::string range_name = "") { 
   
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
    m.setNoWarn(); 

    // Activate verbose logging of MINUIT parameter space stepping
    //m.setVerbose(1);

    // Use migrad to minimize the likelihood.  If migrad fails to find a minimum,
    // run simplex in order to run a sparser search for a minimum followed by
    // migrad again.
    //m.hesse();
    int status = m.migrad(); 
   
    /* 
    int iteration = 0; 
    while(status != 0 && !variable_map["signal yield"]->isConstant()) {
        this->printDebug("Fit failed to converge. Using a background only fit for parameter estimation."); 
         
        this->resetParameters(true); 
    
        double bkg = default_values["bkg yield"] - sqrt(default_values["bkg yield"])*iteration; 
        variable_map["bkg yield"]->setVal(bkg);
        variable_map["bkg yield"]->setError(sqrt(bkg)); 
        
        variable_map["signal yield"]->setConstant(kTRUE);
        status = m.migrad();
        
        variable_map["signal yield"]->setConstant(kFALSE);
        status = m.migrad();

        ++iteration; 
    }*/

    int iteration = 0; 
    while (status != 0) { 
        this->printDebug("Failed to converge changing background starting point.");
        
        //this->resetParameters(bkg_only_result_); 

        double bkg = default_values["bkg yield"]; 
        if (iteration%2 == 0) bkg -= 10; 
        else bkg += 10; 
        variable_map["bkg yield"]->setVal(bkg);
        variable_map["bkg yield"]->setError(sqrt(bkg)); 
        

        status = m.migrad();
        this->printDebug("Minuit status after refit: " + std::to_string(status));
        
        ++iteration; 

        if (iteration == 100) break;
    }

    this->printDebug("Minuit status: " + std::to_string(status));

    // Save the results of the fit
    RooFitResult* result = m.save(); 

    // Delete the constructed negative log likelihood
    delete nll; 

    //this->printDebug("Chi2: " + std::to_string(this->getFitChi2(data)));  

    // Return the saves result
    return new HpsFitResult(result); 
}

double BumpHunter::getFitChi2(RooDataHist* data) { 
  
    RooPlot* plot = mass_->frame();  
    data->plotOn(plot, RooFit::Name("data"));  
    _model->plotOn(plot, RooFit::Name("model"));
    double chi2 = plot->chiSquare("model", "data", 1); 
    delete plot; 
    return chi2;  
}

void BumpHunter::calculatePValue(HpsFitResult* result) {

    this->printDebug("Calculating p-value.");

    //  Get the signal yield obtained from the composite fit
    double signal_yield = result->getParameterVal("signal yield");
    this->printDebug("Signal yield: " + std::to_string(signal_yield));


    // In searching for a resonance, a signal is expected to lead to an 
    // excess of events i.e. mu >.  In this case, the mu < 0 case is 
    // meaningless so we set the p-value = 1.  This follows the formulation
    // put forth by Cowen et al. in https://arxiv.org/pdf/1007.1727.pdf. 
    if (signal_yield <= 0) { 
        result->setPValue(1);
        this->printDebug("Signal yield is negative ... setting p-value = 1"); 
        return; 
    }

    // Get the NLL obtained by minimizing the composite model with the signal
    // yield floating.
    double mle_nll = result->getRooFitResult()->minNll();
    printDebug("NLL when mu = " + std::to_string(signal_yield) + ": " + std::to_string(mle_nll));

    // Get the NLL obtained from the Bkg only fit.
    double cond_nll = bkg_only_result_->getRooFitResult()->minNll();
    printDebug("NLL when mu = 0: " + std::to_string(cond_nll));
   
    // 1) Calculate the likelihood ratio which is chi2 distributed. 
    // 2) From the chi2, calculate the p-value.
    double q0 = 0; 
    double p_value = 0; 
    this->getChi2Prob(cond_nll, mle_nll, q0, p_value);  

    std::cout << "[ BumpHunter ]: p-value: " << p_value << std::endl;

    // Update the result
    result->setPValue(p_value);
    result->setQ0(q0);  
    
}

void BumpHunter::printDebug(std::string message) { 
    if (debug) std::cout << "[ BumpHunter ]: " << message << std::endl;
}

void BumpHunter::resetParameters() { 
  
    this->printDebug("Resetting parameters"); 

    for (auto& element : variable_map) {
        
        // Only reset parameters that constant.
        if (element.second->isConstant()) continue;

        auto it = default_values.find(element.first);
        this->printDebug("Value " + element.first + " reset to " + std::to_string(default_values[element.first])); 
        this->printDebug("Error of " + element.first + " reset to " + std::to_string(default_errors[element.first])); 
        if (it == default_values.end()) {
            continue; 
            this->printDebug("Value " + element.first + " was not found.");
        }
        element.second->setVal(default_values[element.first]);
        element.second->setError(default_errors[element.first]);
    }
}

void BumpHunter::resetParameters(HpsFitResult* result) { 
    this->resetParameters(); 
     
    for (auto& element : variable_map) {
        if (element.second->isConstant()) continue;
        double val = static_cast<RooRealVar*>(
                result->getRooFitResult()->floatParsFinal().find(element.first.c_str()))->getVal(); 
        this->printDebug("Value " + element.first + " set to " + std::to_string(val)); 
        element.second->setVal(val); 
    }
}

void BumpHunter::getUpperLimit(RooDataHist* data, std::string range_name, HpsFitResult* result) {

    //std::cout << "[ BumpHunter ]: Calculating upper limit @ m_{A'} = " << ap_mass << std::endl;

    //  Get the signal yield obtained from the signal+bkg fit
    double signal_yield = result->getParameterVal("signal yield");
    this->printDebug("Signal yield @ min NLL: " + std::to_string(signal_yield));

    // Get the minimum NLL value that will be used for testing upper limits.
    // If the signal yield (mu estimator) at the min NLL is < 0, use the NLL
    // obtained when mu = 0.
    double mle_nll = result->getRooFitResult()->minNll();
    if (signal_yield < 0) {

        this->printDebug("Signal yield @ min NLL is < 0. Using NLL when signal yield = 0");

        // Get the NLL obtained assuming the background only hypothesis
        mle_nll = bkg_only_result_->getRooFitResult()->minNll();
        
        signal_yield = 10;
        
        variable_map["signal yield"]->setConstant(kTRUE);
        this->resetParameters(bkg_only_result_);
        variable_map["signal yield"]->setConstant(kFALSE);
    } else { 
        this->resetParameters(result);
    }
    this->printDebug("MLE NLL: " + std::to_string(mle_nll));     
    /*for (int order = 1; order <= _poly_order; ++order) {
        std::string name = "t" + std::to_string(order);
        variable_map[name]->setConstant(kTRUE); 
    }*/ 

    double p_value = result->getPValue();
    this->printDebug("p-value from result: " + std::to_string(p_value));
    double q0 = 0;
    signal_yield = floor(signal_yield) + 10; 
    int fit_counter = 1;
    bool fell_below_threshold = false; 

    while(true) {

        this->printDebug("Setting signal yield to: " + std::to_string(signal_yield));
        variable_map["signal yield"]->setConstant(kFALSE); 
        variable_map["signal yield"]->setVal(signal_yield);
        variable_map["signal yield"]->setConstant(kTRUE);
        std::cout << "[ BumpHunter ]: Current p-value: " << p_value << std::endl;
        std::cout << "[ BumpHunter ]: Setting signal to " << variable_map["signal yield"]->getValV() << std::endl; 

        HpsFitResult* current_result = this->fit(data, range_name); 
        
        double cond_nll = current_result->getRooFitResult()->minNll(); 

        result->addSignalYield(signal_yield); 
        result->addLikelihood(cond_nll); 

        this->getChi2Prob(cond_nll, mle_nll, q0, p_value);  

        this->printDebug("p-value after fit " + std::to_string(fit_counter) + ": " + std::to_string(p_value)); 
    
        if ((p_value <= 0.0455 && p_value > 0.044)) { 
            
            std::cout << "[ BumpHunter ]: Upper limit: " << signal_yield << std::endl;
            std::cout << "[ BumpHunter ]: p-value: " << p_value << std::endl;
            std::cout << "[ BumpHunter ]: Upper limit status: " << current_result->getRooFitResult()->status() << std::endl;

            result->setUpperLimit(signal_yield);
            result->setUpperLimitPValue(p_value); 
            result->setUpperLimitFitStatus(current_result->getRooFitResult()->status());  
            delete current_result; 
            break; 
        }

        ++fit_counter; 

        if (p_value <= 0.044) {
            signal_yield -= 1;
        } else if (p_value <= 0.059) signal_yield += 1;
        else if (p_value <= 0.10) signal_yield += 20;
        else if (p_value <= 0.2) signal_yield += 50; 
        else signal_yield += 100;  
        
        delete current_result; 
    }
}

void BumpHunter::getChi2Prob(double cond_nll, double mle_nll, double &q0, double &p_value) {
    
    this->printDebug("Cond NLL: " + std::to_string(cond_nll)); 
    this->printDebug("Uncod NLL: " + std::to_string(mle_nll));  
    double diff = cond_nll - mle_nll;
    this->printDebug("Delta NLL: " + std::to_string(diff));
    
    q0 = 2*diff;
    this->printDebug("q0: " + std::to_string(q0));
    
    p_value = ROOT::Math::chisquared_cdf_c(q0, 1);
    this->printDebug("p-value before dividing: " + std::to_string(p_value));  
    p_value *= 0.5;
    this->printDebug("p-value: " + std::to_string(p_value)); 
}

void BumpHunter::setBounds(double lower_bound, double upper_bound) {
    _lower_bound = lower_bound; 
    _upper_bound = upper_bound;
    printf("Fit bounds set to [ %f , %f ]\n", _lower_bound, _upper_bound);   
}

double BumpHunter::correctMass(double mass) { 
    double offset = -1.19892320e4*pow(mass, 3) + 1.50196798e3*pow(mass,2) 
                    - 8.38873712e1*mass + 6.23215746; 
    offset /= 100; 
    this->printDebug("Offset: " + std::to_string(offset)); 
    double cmass = mass - mass*offset; 
    this->printDebug("Corrected Mass: " + std::to_string(cmass)); 
    return cmass;
}
