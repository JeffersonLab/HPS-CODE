# ///*** get some efficiency plots ***///
import ROOT  
import os
effRebin=1
ROOT.gROOT.SetBatch(True)
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
#runs=['hps_005772','wab_'+det,'tritrig-NOSUMCUT_'+det,'wab-beam-tri-zipFix_'+det]
#legs=['run5772','wab','tritrig-NOSUMCUT','wab-beam-tri']
prefix='fromscratch_'
runs=['hps_005772.1','wab-beam_'+det,'tritrig-beam_'+det]
legs=['run5772','wab','tritrig']
col=[1,4,2,5]
postfix='_tweakpass6_WeighInEclVsY_ElePosSame_OmarsBase_WABCuts'
postfixMC=postfix.replace('tweakpass6','tweakpass7')
#postfixMC='_TrackKiller_3dEff'
#postfixMC=''

doesum=False
########       what to plot    ######################
#histName="h_Ecl_"
xTitles=["Cluster Energy (GeV)","Cluster X Position (mm)","Cluster Y Position (mm)"]
finalState=["GamEm"]
histNames=["p2slope"]
### LX Miss and tot list are the numer/denom plot definintions 
LXMiss=["L2TB","L1NoL2TB"]
tot=["TB","TB"]
LXLabel=["L1","L2"]

outFile=ROOT.TFile("EmGamma-L1HitEfficiencyResults.root","RECREATE")



for kk in range(0,len(histNames)) : 
    histName=histNames[kk]
    fs=finalState[kk]
    xTitle=xTitles[kk]

    effESum=[]
    effEle=[]
    effPos=[]    

    for ii in range(0,len(LXMiss)) :
        denName=tot[ii]
        numName=LXMiss[ii]
        for run in runs : 
            outpre="plots-"+str(ene)+"GeV/"+str(run)
        
            ROOT.gStyle.SetOptStat(0)
            ROOT.gStyle.SetOptTitle(0)
#histFile=ROOT.TFile("OutputHistograms/Data/hps_008087_hpsrun2016_pass0_useGBL_ECalMatch.root")
            if ene==1.05 :
                print 'Loading 1.05GeV File' 
                print prefix+run+postfix
                print prefix+run+postfixMC                
                if os.path.isfile("OutputHistograms/Data/"+prefix+run+postfix+".root"): 
                    histFile=ROOT.TFile("OutputHistograms/Data/"+prefix+run+postfix+".root")
                elif  os.path.isfile("OutputHistograms/MC/"+prefix+run+postfixMC+".root"): 
                    histFile=ROOT.TFile("OutputHistograms/MC/"+prefix+run+postfixMC+".root")
                else: 
                    print "NO FILE FOUND!!!!!   "+"OutputHistograms/MC/"+prefix+run+postfixMC+".root"
            else : 
                print 'Loading 2.3GeV File' 
                if os.path.isfile("OutputHistograms/Data/"+run+postfix): 
                    histFile=ROOT.TFile("OutputHistograms/Data/"+run+postfix)
                elif  os.path.isfile("OutputHistograms/MC/"+run+postfix): 
                    histFile=ROOT.TFile("OutputHistograms/MC/"+run+postfix)
                else: 
                    print "NO FILE FOUND!!!!!   "+"OutputHistograms/MC/"+run+postfix
#get some histograms
            print fs+denName+"-"+histName
            allTB=histFile.Get(fs+denName+"-"+histName)
            missL1=histFile.Get(fs+numName+"-"+histName)
            allTB.SetLineWidth(3)
            missL1.SetLineWidth(3)
            
            denom = allTB.Clone()
            denom.Rebin(effRebin)
            denom.Sumw2()
            numer= missL1.Clone();
            numer.Rebin(effRebin);
            numer.Sumw2();
            numer.SetLineWidth(2)
            denom.SetLineWidth(2)
            eff=ROOT.TGraphAsymmErrors()
            eff.SetName(histName+run+fs+"_"+LXLabel[ii]+"HitInefficiency")
            eff.Divide(numer,denom)
            eff.SetLineWidth(3);
            outFile.cd()
            eff.Write()
            histFile.cd()
        #        outFile.Write()
            legMIDESUM7=ROOT.TLegend(0.1,0.8,0.4,0.9);
            legMIDESUM7.AddEntry(allTB,"#gamma e^{-} :  electron slope","l"); 
            legMIDESUM7.AddEntry(missL1,"Missing "+LXLabel[ii],"l");
            
            
            ct = ROOT.TCanvas("ct","transparent pad",200,10,700,500);
            pad1 = ROOT.TPad("pad1","",0,0,1,1);
            pad2 = ROOT.TPad("pad2","",0,0,1,1);
            pad2.SetFillStyle(4000); #will be transparent
            pad2.SetFillStyle(4000); #will be transparent
            pad1.Draw();
            pad1.cd();
            
            allTB.SetXTitle(xTitle);
            allTB.SetLineColor(1);
            allTB.SetLineColor(2);
            missL1.SetLineColor(3);
            
            allTB.SetYTitle("Events")
            allTB.Draw();  
            missL1.Draw("same");
            
            ct.cd();
            ymin = 0.0;
            ymax = 0.5;
            dy = (ymax-ymin)/0.8; #10 per cent margins top and bottom
            

            xminP =allTB.GetXaxis().GetXmin()
            xmaxP =allTB.GetXaxis().GetXmax()
            dx = (xmaxP-xminP)/0.8; #10 per cent margins left and right
            pad2.Range(xminP-0.1*dx,ymin-0.1*dy,xmaxP+0.1*dx,ymax+0.1*dy);
            pad2.Draw();
            pad2.cd();
            eff.SetLineColor(1);
            eff.Draw("][samese");
            pad2.Update();
            effPos.append(eff)

            axis =ROOT.TGaxis(xmaxP,ymin,xmaxP,ymax,ymin,ymax,50510,"+L");
            axis.SetLabelColor(2);
            axis.SetTitle("Efficiency")
            axis.Draw();
            legMIDESUM7.Draw();
            ct.SaveAs(outpre+histName+postfixMC+LXLabel[ii]+"-inefficiency.pdf");
    

outFile.Close()
