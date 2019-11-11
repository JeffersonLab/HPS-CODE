import ROOT 
ROOT.gROOT.SetBatch(True) 

#f=ROOT.TFile("OutputHistograms/Data/fromscratch_hps_005772_pass6_WABs_PureAndConverted.root")
f=ROOT.TFile("OutputHistograms/MC/fromscratch_tri-beam_HPS-EngRun2015-Nominal-v5-0_pass6_WABs_PureAndConverted_NoESumCut_WeighInEclVsY.root")
p1slope=f.Get("EpEmTB-p1slope")
xmin=p1slope.GetXaxis().GetXmin()
xmax=p1slope.GetXaxis().GetXmax()
nbins=p1slope.GetNbinsX()

asymHist=ROOT.TH1D("posAsym","posAsym",int(nbins/2),0,xmax)

for i in range(nbins/2,nbins): 
    negVal=p1slope.GetBinContent(int(nbins)-i-1)
    posVal=p1slope.GetBinContent(i)
    print str(int(nbins)-i-1)+" "+str(negVal)+"  "+str(i)+"  "+str(posVal)
    asym=(posVal-negVal)/(posVal+negVal)
#    asym=(posVal-negVal)
    asymHist.SetBinContent(i-int(nbins/2),asym)

ct=ROOT.TCanvas()
asymHist.SetYTitle("(N_{+slope}-N_{-slope})/(N_{+slope}+N_{-slope})")
asymHist.SetXTitle("|slope|")
asymHist.Draw()
#ct.SaveAs("SinglePlots/pos-asym.pdf")
ct.SaveAs("SinglePlots/tri-beam-pos-asym.pdf")


p2slope=f.Get("EpEmTB-p2slope")
xmin=p2slope.GetXaxis().GetXmin()
xmax=p2slope.GetXaxis().GetXmax()
nbins=p2slope.GetNbinsX()

asymHistEle=ROOT.TH1D("eleAsym","eleAsym",int(nbins/2),0,xmax)

for i in range(nbins/2,nbins): 
    negVal=p2slope.GetBinContent(int(nbins)-i-1)
    posVal=p2slope.GetBinContent(i)
    print str(int(nbins)-i-1)+" "+str(negVal)+"  "+str(i)+"  "+str(posVal)
    asym=(posVal-negVal)/(posVal+negVal)
#    asym=(posVal-negVal)
    asymHistEle.SetBinContent(i-int(nbins/2),asym)

ct=ROOT.TCanvas()
asymHistEle.SetYTitle("(N_{+slope}-N_{-slope})/(N_{+slope}+N_{-slope})")
asymHistEle.SetXTitle("|slope|")
asymHistEle.Draw()
ct.SaveAs("SinglePlots/tri-beam-ele-asym.pdf")

ct=ROOT.TCanvas()
asymHist.SetLineWidth(4)
asymHistEle.SetLineWidth(4)
asymHist.SetLineColor(2)
asymHist.SetMinimum(-1)
asymHist.SetMaximum(1)
leg=ROOT.TLegend(0.2,0.8,0.3,0.9)
leg.AddEntry(asymHist,"Positron","l")
leg.AddEntry(asymHistEle,"Electron","l")
asymHist.Draw()
asymHistEle.Draw("same")
leg.Draw()
#ct.SaveAs("SinglePlots/slope-asym.pdf")
ct.SaveAs("SinglePlots/tri-beam-slope-asym.pdf")

