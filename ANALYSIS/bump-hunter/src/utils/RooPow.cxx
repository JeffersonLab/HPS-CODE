/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitModels                                                     *
 * @(#)root/roofit:$Id$
 * Authors:                                                                  *
 *   WV, Wouter Verkerke, UC Santa Barbara, verkerke@slac.stanford.edu       *
 *   DK, David Kirkby,    UC Irvine,         dkirkby@uci.edu                 *
 *                                                                           *
 * Copyright (c) 2000-2005, Regents of the University of California          *
  *                          and Stanford University. All rights reserved.    *
  *                                                                           *
  * Redistribution and use in source and binary forms,                        *
  * with or without modification, are permitted according to the terms        *
  * listed in LICENSE (http://roofit.sourceforge.net/license.txt)             *
  *****************************************************************************/

 /**
 \file RooPow.cxx
 \class RooPow
 \ingroup Roofit

 Pow p.d.f
 **/

 #include "RooFit.h"

 #include "Riostream.h"
 #include "Riostream.h"
 #include <math.h>


 #include "RooRealVar.h"
 #include "RooPow.h"

 using namespace std;

 //ClassImp(RooPow)


 ////////////////////////////////////////////////////////////////////////////////

 RooPow::RooPow(const char *name, const char *title,
                 RooAbsReal& _x, RooAbsReal& _x0, RooAbsReal& _b) :
   RooAbsPdf(name, title),
   x("x","Dependent",this,_x),
   x0("x0","Offset",this,_x0),
   b("b", "Power", this,_b)
 {
 }


 ////////////////////////////////////////////////////////////////////////////////

 RooPow::RooPow(const RooPow& other, const char* name) :
   RooAbsPdf(other, name), x("x",this,other.x), x0("x0",this,other.x0), b("b",this,other.b)
 {
 }


 ////////////////////////////////////////////////////////////////////////////////
 ///cout << "exp(x=" << x << ",c=" << c << ")=" << exp(c*x) << endl ;

 Double_t RooPow::evaluate() const{
	if(x>x0)
   return pow((x-x0)/(2*x0), b);
	else return 0;
 }


