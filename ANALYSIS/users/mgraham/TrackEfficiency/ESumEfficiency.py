# ///*** get some efficiency plots for the MIDESUM set of plots   ***///
import ROOT  
import os
import sys
sys.path.insert(0,'/u/br/mgraham/hps-analysis/python')

from basicUtils import *
effRebin=5
###############################################
# Engineering run (2015) numbers
iLumi=4403638.0/1000.0 # ub^-1  run 5772
#  Average generated XS = 7.06874167417  (E11, pb)from 1111 jobs
wabXS=7.06874167417e11/1e6 #ub 
tritrigXS=1.76*1000.0 #ub
#hps@ifarm1102> python parseAndGetEvents.py 
#Number Passed = 2909346.0 out of 76289361.0
#Average Efficiency = 0.0381356713684 from 1000 jobs
wabNGen=76289361.0*995/1000 #5 dst files missing
#hps@ifarm1102> python parseAndGetEvents.py 
#Number Passed = 8654274.0 out of 45123760.0
#Average Efficiency = 0.191789735607 from 376 jobs
tritrigNGen= 45123760.0 # got all jobs here
wabBeamTriNBunches=500000*10*1000 # number of bunches
wabBeamTriLumi=86.1 #ub^-1
###############################################
#ene=2.3
#det='HPS-PhysicsRun2016-Nominal-v5-0'
#runs=['hps_007809','hps_007807','hps_007808','tritrig_'+det,'wab_'+det]
#runs=['hps_007809','hps_007807','hps_007808','tritrig_'+det]
#legs=['50nA','200nA','300nA','tritrig']
#col=[1,2,4,5,6]
#postfix='_hpsrun2016_pass0_useGBL_ECalMatch.root'

ene=1.05
det='HPS-EngRun2015-Nominal-v5-0'
#runs=['hps_007809','hps_007807','hps_007808','tritrig_'+det,'wab_'+det]
runs=['hps_005772','tritrig_'+det,'wab_'+det]
legs=['run5772','tritrig','wab']
col=[1,2,3]
postfix='_engrun2015_pass6_TopBot_LeftRight_CutPhotons_SuperFiducialCut_Smear_0pt1'
norm=[1/iLumi, tritrigXS/tritrigNGen, wabXS/wabNGen,1/wabBeamTriLumi]



xTitle="Cluster Energy (GeV)"
eSumBothTracks=[]
eSumEleTrack=[]
eSumAll=[]
eSumEff=[]
histFile=[]

histName="h_Ecl_"
cuts="cop160_"
posSide="pos_side_found_ele"
eleSide="ele_side_found_pos"
posSideFound="pos_side_found_ele_found_pos"
eleSideFound="ele_side_found_pos_found_ele"
posMis="mis_pos"
eleMis="mis_ele"

esumName="h_ESum_"
esumAll=""
esumBoth="bothtracks"
ii=0
for run in runs : 
    outpre="plots-"+str(ene)+"GeV/"+str(run)

    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptTitle(0)
#histFile=ROOT.TFile("OutputHistograms/Data/hps_008087_hpsrun2016_pass0_useGBL_ECalMatch.root")
    if ene==1.05 :
        print 'Loading 1.05GeV File' 
        if os.path.isfile("OutputHistograms/Data/"+run+postfix+".root"): 
            histFile.append(ROOT.TFile("OutputHistograms/Data/"+run+postfix+".root"))
        elif  os.path.isfile("OutputHistograms/MC/"+run+postfix+".root"): 
            histFile.append(ROOT.TFile("OutputHistograms/MC/"+run+postfix+".root"))
        else: 
            print "NO FILE FOUND!!!!!   "+"OutputHistograms/MC/"+run+postfix+".root"
    else : 
        print 'Loading 2.3GeV File' 
        if os.path.isfile("OutputHistograms/Data/"+run+postfix+".root"): 
            histFile.append(ROOT.TFile("OutputHistograms/Data/"+run+postfix+".root"))
        elif  os.path.isfile("OutputHistograms/MC/"+run+postfix): 
            histFile.append(ROOT.TFile("OutputHistograms/MC/"+run+postfix+".root"))
        else: 
            print "NO FILE FOUND!!!!!   "+"OutputHistograms/MC/"+run+postfix+".root"
#get some histograms  

    print histName+cuts+esumAll
    esum_all=histFile[ii].Get(esumName+cuts+esumAll)
    eSumAll.append(esum_all.Clone())
    esum_found_both=histFile[ii].Get(esumName+cuts+esumBoth)
    eSumBothTracks.append(esum_found_both.Clone())
   
###############################
    eff=plotEff( esum_found_both, esum_all,effRebin,"ESum (GeV)",outpre+histName+cuts+postfix+"-ESum-efficiency.pdf")
    eSumEff.append(eff.Clone())
    ii+=1

legEle=ROOT.TLegend(0.6,0.2,0.8,0.3);
legPos=ROOT.TLegend(0.6,0.2,0.8,0.3);
legESum=ROOT.TLegend(0.6,0.2,0.8,0.3);


xmin =esum_all.GetXaxis().GetXmin()
xmax =esum_all.GetXaxis().GetXmax()
base=ROOT.TH2D("","",100,xmin,xmax,100,0.0,1.0)
base.SetXTitle("ESum (GeV)");
base.SetYTitle("ESum Efficiency");

ct = ROOT.TCanvas("ct","transparent pad",200,10,700,500);
base.Draw()
eSumEff[0].Draw("p")
legESum.AddEntry(eSumEff[0],legs[0],"l"); 
outpre="plots-"+str(ene)+"GeV/"
for i in range(1,len(eSumEff)): 
    legESum.AddEntry(eSumEff[i],legs[i],"l"); 
    eSumEff[i].SetLineColor(col[i])
    eSumEff[i].Draw("p")
legESum.Draw()    
ct.SaveAs(outpre+histName+cuts+"-ESum-efficiency.pdf")

print 'Subtracting WABs!!!!'+str(len(eSumAll)) 
##### subtract the WABs (via MC) from the "all pairs" data (the denominator for efficiency)
wabESumAll=eSumAll[2]
triESumAll=eSumAll[1]
dataESumAll=eSumAll[0]
dataESumSub=eSumAll[0].Clone()
wabESumBoth=eSumBothTracks[2]
dataESumBoth=eSumBothTracks[0]
scaleToData=norm[2]/norm[0]  #scale from wab events to expected data events
print scaleToData
fudgeFactor=0.65
#wabESumAll.Add(wabESumBoth,-1.0)
wabESumAll.Scale(scaleToData*fudgeFactor)
triESumAll.Scale(norm[1]/norm[0]*fudgeFactor)
dataESumSub.Add(wabESumAll,-1.0)
mcSum=wabESumAll.Clone()
mcSum.Add(triESumAll,1)

#effDataMinusWab=getEfficiencyPlot(dataESumBoth,dataESumSub,effRebin)
effSub=plotEff(dataESumBoth,dataESumSub,effRebin,"ESum (GeV)",outpre+histName+cuts+postfix+"-ESum-efficiency-WABSubtracted.pdf")
ct = ROOT.TCanvas("ct","transparent pad",200,10,700,500)

dataESumAll.SetLineColor(1)
dataESumAll.SetLineWidth(3)
wabESumAll.SetLineColor(2)
triESumAll.SetLineColor(4)
mcSum.SetLineWidth(3)
mcSum.SetLineColor(6)
 
wabESumAll.Draw()
dataESumAll.Draw("same")
triESumAll.Draw("same")
mcSum.Draw("same")
#dataESumAll.Draw("same")
ct.SaveAs(outpre+histName+cuts+postfix+"foo.pdf")


#denom =esum_all.Clone();
#denom.Rebin(effRebin);
#denom.Sumw2();
#numer=esum_found_both.Clone();
#numer.Rebin(effRebin);
#numer.Sumw2();
#eff=ROOT.TGraphAsymmErrors()
#eff.Divide(numer,denom)
