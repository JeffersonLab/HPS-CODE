#!/usr/bin/python

import sys
import math
import ROOT 
import argparse
import os
import numpy as np
from iminuit import Minuit
from subprocess import Popen, PIPE

#evtType=["gemL1","gemL2","cwabL1L1","cwabL1L2","cwabL2L1","cwabL2L2",
#         "triL1L1","triL1L2","triL2L1","triL2L2"]
         
#nEvtType=[55555,333,5678,456,9999,250,
#          11111,333,444,234]

evtType=["gemL1","gemL2","epemL1L1","epemL1L2","epemL2L1","epemL2L2"]
#nEvtType=[55555,333,5678,456,9999,250]
nEvtType=[406872,21407,77719,4249,19634,1021]


def chiSq(swab,stri,fconv,fL1,iL1) :
    print "In chiSq"
    #gamma e-
    mychi=(nEvtType[0]-((1-fconv)*(1-iL1)*swab))**2/nEvtType[0] #gemL1
    mychi=mychi+(nEvtType[1]-((1-fconv)*iL1*swab))**2/nEvtType[1] #geml2
    #e+e-
    mychi=mychi + (nEvtType[2]-(fL1*(1-iL1)*(1-iL1)*fconv*swab+
                                (1-iL1)*(1-iL1)*stri))**2/nEvtType[2] #epemL1L1
    mychi=mychi + (nEvtType[3]-(fL1*iL1*(1-iL1)*fconv*swab+
                                iL1*(1-iL1)*stri))**2/nEvtType[3] #epemL1L2
    mychi=mychi + (nEvtType[4]-((1-fL1)*(1-iL1)*fconv*swab+
                                fL1*iL1*(1-iL1)*fconv*swab+
                                iL1*(1-iL1)*stri))**2/nEvtType[4] #epemL2L1
    mychi=mychi + (nEvtType[5]-((1-fL1)*iL1*fconv*swab+
                                fL1*iL1*iL1*fconv*swab+
                                iL1*iL1*stri))**2/nEvtType[5] #epemL2L2
    return mychi


#def fitFcn(xx,pars) :
#    swap=pars[0]
#    stri=pars[1]
#    fconv=pars[2]
#    fL1=pars[3]
#    iL1=pars[4]
#    x=xx[0]
#    if x==0 : 
#        return (1-fconv)*(1-iL1)*swab #gemL1
#    if x==1 : 
#        return    (1-fconv)*iL1*swab #geml2
#    if x==2 :
#        return fL1*(1-iL1)*(1-iL1)*fconv*swab+ (1-iL1)*(1-iL1)*stri #epemL1L1
#    if x==3 : 
#        return fL1*iL1*(1-iL1)*fconv*swab+iL1*(1-iL1)*stri #epemL1L2
#    if x==4 : 
#        return (1-fL1)*(1-iL1)*fconv*swab+fL1*iL1*(1-iL1)*fconv*swab+iL1*(1-iL1)*stri #epemL2L1
#    if x==5 : 
#        (1-fL1)*iL1*fconv*swab+fL1*iL1*iL1*fconv*swab+iL1*iL1*stri  #epemL2L2
#    return 0.0
    


def main() : 
    m = Minuit(chiSq)


if __name__ == "__main__":
    main()






#// Main function in minimizerExample.C
#void minimizerExample() {
#TFitter* minimizer = new TFitter(2);
#// MAKE IT QUIET!!
#{
#double p1 = -1;
#minimizer->ExecuteCommand("SET PRINTOUT",&p1,1);
#}
#// Tell the minimizer about the function to be minimzed
#minimizer->SetFCN(minuitFunction);
#minimizer->SetParameter(0,"X",2,1,0,0);
#minimizer->SetParameter(1,"Y",2,1,0,0);
#}
