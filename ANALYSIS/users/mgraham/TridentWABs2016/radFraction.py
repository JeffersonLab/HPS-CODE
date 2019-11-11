#!/usr/bin/python

import sys
import math
import ROOT 
import argparse
import os
import numpy as np
from subprocess import Popen, PIPE

def makePretty(h, xname, yname,  color = 1, lwid = 3 , ltype=1) : 
     if color == 5:  color = 36
     if color == 3:  color = 46
     h.SetLineColor(color);
     h.SetLineWidth(lwid);
     h.SetLineStyle(ltype);
     h.SetXTitle(xname);
     h.SetYTitle(yname);
     h.SetMinimum(0.0);

def getAxisTitle(name): 
     if "eSum" in name: 
          return "Energy Sum (GeV)"
     if "pairMass" in name: 
          return "Invariant Mass (GeV)"
     if "eDiff" in name: 
          return "Energy Difference (GeV)"
     if "clTimeDiff" in name: 
          return "Cluster Pair #delta t (ns)"
     if "p1Mom" in name or "p2Mom" in name: 
          return "Momentum (GeV)"
     if "coplanarity" in name: 
          return "Cluster Coplanarity (degrees)" 
     if "V0PyTimesP2Py" in name: 
          return "Pair Py (GeV)" 
     if "v0Chi2" in name: 
          return "v0 Chi^2!" 
     if "ClusterSlope" in name: 
          return "Cluster Slope" 
     if "d0" in name: 
          return "d0 (mm)"
     if "z0" in name: 
          return "z0 (mm)"
     if "phi0" in name: 
          return "phi0"
     if "slope" in name: 
          return "Track Slope"
     if "TrkTime" in name: 
          return "Track Time (ns)"
     if "TrkChi2overNHits" in name: 
          return "Chi^2!/NDF"
     return ""
     
     
def main() : 
     makeRatioPlot=False
     normToArea=False
     addMCHistos=True
#    addMCHistos=True #this only makes sense right now if we only have MC samples that should add..i.e. not "wab-beam-tri"
#    iLumi5772=4403638.0/1000.0 # ub^-1  run 5772 unblind sample 
     iLumi5772=42.366*1000.0 # ub^-1  run 5772 full run
     iLumi=1.4*1000.0 # ub^-1  run 5754 
#wabv3AF_200MeV_5mrad
     wabXS=770.3*1000.0 #ub...this is the lower peak 
     wabNGen=10000*1000*10#  v6 detector
#tritrig with ESum>0.5 GeV and 5mrad
     tritrigMG5XS= 2.777*1000.0 #ub
     tritrigMG5NGen=10000.0*10*10#  v6 detector
#tritrig MG5 with ECut>0.5 GeV..generation looks better
#     tritrigwabbeamXS = 1314883000.0/1e6  #ub .. 1314 ub ... seems a bit low compared to Takashi
#     tritrigwabbeamNGen=10000*10*994 
######  RAD MG5  (no xchange) 5mrad
#  I think I prefer to use 100010 events/readout file * 50 readout files
     radMG5XS = 0.1074*1000.0#ub
     radMG5NGen = 10000*10*10#v6 detector
############
#wab-beam-tri Luminosity
     wabBeamTriMG5Lumi=0.0861*1000 #ub^-1
#     wabBeamLumi=100*100*8004.68/1e6 #ub^-1
#     triBeamLumi=100*99*8004.68/1e6 #ub^-1

     ROOT.gROOT.SetBatch(True) 

#goodRuns='golden-runs-Feb10-2016.txt'
#with open(goodRuns,"r") as tmp:
#    lines = tmp.readlines()
    
     dataPath="OutputHistograms/Data/"
     datapass="_tweakpass6_"
#     label="NoESumCut_WeighInEclVsY_ElePosSame_MattsBase_TrkChiSq"
#     label="NoESumCut_WeighInEclVsY_ElePosSame_MattsBase_OmarsBase"
#     label="NoESumCut_WeighInEclVsY_ElePosSame_MattsBase_V0ChiSq"
     label="NoESumCut_WeighInEclVsY_ElePosSame_OmarsBase"
#     label="NoESumCut_WeighInEclVsY_ElePosSame_OmarsBase_WABD0_WABPt"
     datalabel=datapass+""+label
#     label="_pass6_WABs_PureAndConverted"
#     label="_pass6_WABs_PureAndConverted_NoESumCut_LooseDtCut"
#     label="_pass6_WABs_PureAndConverted"
#     mcTag="_KillInEnergy"
#     mcTag="_KillInMomentum"
#     mcTag="_WeighInEclVsY_ElePosSeparate"
     mcTag=""
     plotFilePostFix=""
#     plotFilePostFix="_ScaleWABBy0pt87"
#     plotFilePostFix="_ScaleWABBy0pt87_NoRatios"
     mcpass="_tweakpass7_"
     mcPath="OutputHistograms/MC/"
     mcLabel="_HPS-EngRun2015-Nominal-v6-0"+mcpass+label
     prefix="fromscratch_"
#     run="hps_005772"
#     dataNorm=[1/iLumi5772]
     run="hps_005772.1"
     dataNorm=[1/iLumi5772 * (471./111.0)] #only running through a fraction of the DSTs for speed. 
#     run="hps_005772.11"
#     dataNorm=[1/iLumi5772 * (471./11.0)] #only running through a fraction of the DSTs for speed. 
     print 'Scaling RAD-MG5 sample by '+str(radMG5XS/radMG5NGen)

     mcSamples=["wab","tritrig","RAD","wab-beam-tri"]
     mcNorm=[wabXS/wabNGen,tritrigMG5XS/tritrigMG5NGen,radMG5XS/radMG5NGen,1/wabBeamTriMG5Lumi]
     mcLegends=["Wide-Angle Brem","Full-Diagram Tridents","Radiative Tridents", "Wab-Beam-Tri"]
#     mcScale=[0.81*0.87,0.76*.87,0.81*0.87,0.76,0.76,0.76]
#     mcSamples=["wab-beam-tri"]
#     mcNorm=[1/wabBeamTriMG5Lumi]
#     mcLegends=["Wab-Beam-Tri"]
     mcScale=[1,1,1,1,1,1]
     dataFile=ROOT.TFile(dataPath+prefix+run+datalabel+".root")
     dataFile.cd()
     allKeys = ROOT.gDirectory.GetListOfKeys()
     mcFile=[]

     for sample in mcSamples:     
          print 'loading '+mcPath+prefix+sample+mcLabel+mcTag+".root"
          mcFile.append(ROOT.TFile(mcPath+prefix+sample+mcLabel+mcTag+".root"))
#          print 'loading '+mcPath+prefix+sample+mcLabel+label+".root"
#          mcFile.append(ROOT.TFile(mcPath+prefix+sample+mcLabel+label+".root"))
          
     if normToArea :
          mcTag=mcTag+"_normToArea"
     plotFileName="SummaryPlots/allplots"+datalabel+mcTag+plotFilePostFix+".pdf"
#loop through all of the histograms
     cnt=0     
     for key in allKeys : 
          canvas=ROOT.TCanvas("Dumb Canvas")
          h = key.ReadObj()
          if not h.GetEntries() > 0  : continue
          is2D =False
#          if type(h) is ROOT.TH2D: continue
          if type(h) is ROOT.TH2D: is2D=True
          if is2D : 
               canvas.Divide(2,2)     
          canvas.cd(1)
          totalCrossSection=h.Integral()*dataNorm[0]
          h.Sumw2(True)
          hname=h.GetName()    
          print hname+' ' +str(len(mcFile))
          print "data cross-section = "+str(totalCrossSection)+" ub  "+str(h.GetEntries())+" entries"
          if normToArea : 
               h.Scale(10000.0/h.Integral())                
          else: 
               h.Scale(dataNorm[0])
          max=h.GetMaximum()
          if normToArea : 
               makePretty(h,getAxisTitle(h.GetTitle()),"Arbitrary")
          else: 
               makePretty(h,getAxisTitle(h.GetTitle()),"#sigma (#mub)")


          mchList=[]
          mchLabList=[]
          mchScaleList=[]
          addCnt=0
          for ii in range(len( mcFile)) :
               mcf=mcFile[ii]
               mch=mcf.Get(hname)
               if not mch: 
                    print hname+' '+str(ii)+ ' does not exist!'
                    continue
               mch.Sumw2(True)
               mcCrossSection=mch.Integral()*mcNorm[ii]*mcScale[ii]
               print mcSamples[ii]+" MC cross-section = "+str(mcCrossSection) +" ub using "+str(mch.GetEntries())+" entries"
               if normToArea: 
                    mch.Scale(10000.0/mch.Integral())                
               else : 
                    mch.Scale(mcNorm[ii]*mcScale[ii])                
               mchList.append(mch)
               mchLabList.append(mcLegends[ii])
               mchScaleList.append(mcScale[ii])
               makePretty(mch,"foo","bar",ii+2)               
               tm=mch.GetMaximum()
               if tm > max : 
                    max=tm
               if addMCHistos and mch is not None:                    
                    if addCnt==0 : 
                         mchAdd=mch.Clone()
                         mchAdd.SetDirectory(0)
                    elif ii<2: 
                         mchAdd.Add(mch.Clone())                    
                    addCnt+=1

          if addMCHistos and mchAdd is not None: 
               makePretty(mchAdd,"foo","bar",9)
               mchList.append(mchAdd)
               mchLabList.append("Tridents+WABs")
               mchScaleList.append("")
               if mchAdd.GetMaximum()>max : 
                    max= mchAdd.GetMaximum()
               

            #do something to them...
          leg=ROOT.TLegend(0.1,0.9,0.37,0.73)               
          leg.SetTextSize(0.032)
          leg.AddEntry(h,"Run 5772","l")


          if not is2D and makeRatioPlot:
               # Upper plot will be in pad1
               pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0);
               pad1.SetBottomMargin(0)
               pad1.SetGridx()
               pad1.Draw()
               pad1.cd()
               h.SetMaximum(1.2*max)

          if "Missing" in hname: 
               h.SetMinimum(0.01)
               h.SetMaximum(10*max)

          if is2D: 
               h.SetTitle(h.GetTitle()+' Data')
               h.Draw("colz")
          else:
               h.SetStats(0)     
               h.SetMaximum(1.2*max)
               h.Draw("ehist")
          for i in range(0,len(mchList)) :
               mch= mchList[i]  
               if is2D : 
                    canvas.cd(i+2)                         
                    mch.SetTitle(mch.GetTitle()+' '+mchLabList[i]+' x'+str(mchScaleList[i]))
                    mch.Draw("colz")
               else: 
                    if "Missing" in hname: 
                         mch.SetMinimum(h.GetMinimum())
                    mch.Draw("esame")
                    leg.AddEntry(mch,mchLabList[i],"l")
#                    leg.AddEntry(mch,mchLabList[i]+' x'+str(mchScaleList[i]),"l")
                    i+=1
               if not is2D: 
                    leg.Draw()

          if not is2D and makeRatioPlot: 
#...this is for monkeying with axis labels
#               h1->GetYaxis()->SetLabelSize(0.);
#               axis =ROOT.TGaxis( -5, 20, -5, 220, 20,220,510,"");
#               axis.SetLabelFont(43); 
#               axis.SetLabelSize(15);
#               axis.Draw();
               canvas.cd()
               pad2 = ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
               pad2.SetTopMargin(0)
               pad2.SetBottomMargin(0.2)
               pad2.SetGridx() 
               pad2.Draw()
               pad2.cd()   

               ratio=h.Clone()
               #  take the ratio with the last mchList histogram...
               ratio.SetLineColor(1)
               ratio.SetMinimum(0.5) 
               ratio.SetMaximum(1.5)
               ratio.Sumw2()
               ratio.SetStats(0)     
               ratio.Divide(mchList[-1])
               ratio.SetMarkerStyle(21)
               ratio.SetTitle("")
               ratio.GetYaxis().SetTitle("ratio data/MC ")
               ratio.GetYaxis().SetNdivisions(505)
               ratio.GetYaxis().SetTitleSize(20)
               ratio.GetYaxis().SetTitleFont(43)
#               ratio.GetYaxis().SetTitleOffset(1.55)
               ratio.GetYaxis().SetLabelFont(43)
               ratio.GetYaxis().SetLabelSize(15)
               ratio.GetXaxis().SetTitleSize(20)
               ratio.GetXaxis().SetTitleFont(43)
               ratio.GetXaxis().SetTitleOffset(2.)
               ratio.GetXaxis().SetLabelFont(43)
               ratio.GetXaxis().SetLabelSize(15)               
               ratio.Draw("ep")
               xmin=ratio.GetXaxis().GetXmin()
               xmax=ratio.GetXaxis().GetXmax()
               tl=ROOT.TLine(xmin,1,xmax,1)
               tl.Draw()
               

          if "Missing"  in hname :
               canvas.SetLogy(True)
          else: 
               canvas.SetLogy(False)
          if key == allKeys.First(): 
               canvas.Print(plotFileName+"(")
          elif key == allKeys.Last() : 
               print "Closing File"
               canvas.Print(plotFileName+")")
          else :
               canvas.Print(plotFileName)

if __name__ == "__main__":
     main()
