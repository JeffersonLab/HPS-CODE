# ///*** get some efficiency plots for the MIDESUM set of plots   ***///
import ROOT  
import os
effRebin=1
ROOT.gROOT.SetBatch(True)

ene=1.05
det='HPS-EngRun2015-Nominal-v5-0'
#runs=['hps_007809','hps_007807','hps_007808','tritrig_'+det,'wab_'+det]
runs=['hps_005772','wab_'+det,'tritrig-NOSUMCUT_'+det,'wab-beam-tri-zipFix_'+det]
legs=['run5772','wab','tritrig-NOSUMCUT','wab-beam-tri']
col=[1,2,4,3,5]
#postfix='_engrun2015_pass6_useGBL_ECalMatch.root'
postfix='_engrun2015_pass6_TopBot_LeftRight.root'

doesum=False


#histName="h_Ecl_"
xTitles=["Cluster Energy (GeV)","Cluster X Position (mm)","Cluster Y Position (mm)"]
histNames=["h_XvsY_"]
cuts="cop180_"
#cuts="cop180_Holly_"
#cuts="cop180_midESum_"
#cuts="cop180_SuperFid"
posSide="pos_side_found_ele"
eleSide="ele_side_found_pos"
posSideFound="pos_side_found_ele_found_pos"
eleSideFound="ele_side_found_pos_found_ele"


outFile=ROOT.TFile(cuts+"TwoD-EfficiencyResults.root","RECREATE")


for kk in range(0,len(histNames)) : 
    histName=histNames[kk]
    xTitle=xTitles[kk]

    effESum=[]
    effEle=[]
    effPos=[]    
    for run in runs : 
        outpre="plots-"+str(ene)+"GeV/"+str(run)
        
        ROOT.gStyle.SetOptStat(0)
        ROOT.gStyle.SetOptTitle(0)
#histFile=ROOT.TFile("OutputHistograms/Data/hps_008087_hpsrun2016_pass0_useGBL_ECalMatch.root")
        if ene==1.05 :
            print 'Loading 1.05GeV File' 
            if os.path.isfile("OutputHistograms/Data/"+run+postfix): 
                histFile=ROOT.TFile("OutputHistograms/Data/"+run+postfix)
            elif  os.path.isfile("OutputHistograms/MC/"+run+postfix): 
                histFile=ROOT.TFile("OutputHistograms/MC/"+run+postfix)
            else: 
                print "NO FILE FOUND!!!!!   "+"OutputHistograms/MC/"+run+postfix
        else : 
            print 'Loading 2.3GeV File' 
            if os.path.isfile("OutputHistograms/Data/"+run+postfix): 
                histFile=ROOT.TFile("OutputHistograms/Data/"+run+postfix)
            elif  os.path.isfile("OutputHistograms/MC/"+run+postfix): 
                histFile=ROOT.TFile("OutputHistograms/MC/"+run+postfix)
            else: 
                print "NO FILE FOUND!!!!!   "+"OutputHistograms/MC/"+run+postfix
#get some histograms
        print histName+cuts+posSide
        pos_side_found_ele=histFile.Get(histName+cuts+posSide)
        print histName+cuts+posSideFound
        pos_side_found_ele_found_pos=histFile.Get(histName+cuts+posSideFound)
        print histName+cuts+eleSide
        ele_side_found_pos=histFile.Get(histName+cuts+eleSide)
        print histName+cuts+eleSideFound
        ele_side_found_pos_found_ele=histFile.Get(histName+cuts+eleSideFound)
        ele_side_found_pos.Print("v")
#############
        denom = pos_side_found_ele.Clone()
        denom.Sumw2()
        numer= pos_side_found_ele_found_pos.Clone();
        numer.Sumw2();
#        eff=ROOT.TH2D()
        numer.Divide(denom)
        numer.SetTitle(histName+run+"_posEff")
        numer.SetName(histName+run+"_posEff")
        outFile.cd()
        numer.Write()
        ct = ROOT.TCanvas("ct","transparent pad",200,10,700,500);
        numer.Draw("colz");
        ct.SaveAs(outpre+histName+cuts+"-positron-efficiency.pdf");
    
###############################
        denom =ele_side_found_pos.Clone();
        denom.Sumw2();
        numer=ele_side_found_pos_found_ele.Clone();
        numer.Sumw2();
#        eff=ROOT.TH2D()
        numer.Divide(denom)
        numer.SetTitle(histName+run+"_eleEff")
        numer.SetName(histName+run+"_eleEff")
        outFile.cd()
        numer.Write()
        ct = ROOT.TCanvas("ct","transparent pad",200,10,700,500);
        numer.Draw("colz");
        ct.SaveAs(outpre+histName+cuts+"-electron-efficiency.pdf");   
###############################
  
outFile.Close()
