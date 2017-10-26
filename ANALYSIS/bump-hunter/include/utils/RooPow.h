/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitModels                                                     *
 * Authors:                                                                  *
 *   SJP, Sebouh Jacob Paul  W & M     sebouh.paul@gmail.com
 *                                                                           *
  *****************************************************************************/
 #ifndef ROO_POW
 #define ROO_POW

 #include "RooAbsPdf.h"
 #include "RooRealProxy.h"

 class RooRealVar;
 class RooAbsReal;

 class RooPow : public RooAbsPdf {
 public:
   RooPow() {} ;
   RooPow(const char *name, const char *title,
        RooAbsReal& _x, RooAbsReal& _x0, RooAbsReal& _b);
   RooPow(const RooPow& other, const char* name=0);
   virtual TObject* clone(const char* newname) const { return new RooPow(*this,newname); }
   inline virtual ~RooPow() { } ;

   //Int_t getAnalyticalIntegral(RooArgSet& allVars, RooArgSet& analVars, const char* rangeName=0) const ;
   //Double_t analyticalIntegral(Int_t code, const char* rangeName=0) const ;

 protected:
   RooRealProxy x;
   RooRealProxy x0;
   RooRealProxy b;

   Double_t evaluate() const;

 private:
   //ClassDef(RooPow,1) // Pow PDF
 };

 #endif
