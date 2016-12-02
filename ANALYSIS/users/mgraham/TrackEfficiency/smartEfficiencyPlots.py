# ///*** get some efficiency plots for the MIDESUM set of plots   ***///
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
runs=['hps_005772','wab_'+det,'tritrig-NOSUMCUT_'+det,'wab-beam-tri-zipFix_'+det]
legs=['run5772','wab','tritrig-NOSUMCUT','wab-beam-tri']
#runs=['hps_005772','tritrig_'+det,'wab_'+det]
#legs=['run5772','tritrig','wab']
col=[1,4,2,5]
postfix='_engrun2015_pass6_TopBot_LeftRight'
postfixMC='_TrackKiller_Momentum'
#postfixMC=''

doesum=False
########       what to plot    ######################
#histName="h_Ecl_"
xTitles=["Cluster Energy (GeV)","Cluster X Position (mm)","Cluster Y Position (mm)"]
histNames=["h_Ecl_","h_EclX_","h_EclY_"]

#cuts="cop180_Holly_"
cuts="cop180_midESum_SuperFid"
#cuts="cop180_"
#cuts="cop180_SuperFid"
posSide="pos_side_found_ele"
eleSide="ele_side_found_pos"
posSideFound="pos_side_found_ele_found_pos"
eleSideFound="ele_side_found_pos_found_ele"
posMis="mis_pos"
eleMis="mis_ele"


esumName="h_ESum_"
esumAll=""
esumBoth="bothtracks"

outFile=ROOT.TFile(cuts+"EfficiencyResults.root","RECREATE")

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
            if os.path.isfile("OutputHistograms/Data/"+run+postfix+".root"): 
                histFile=ROOT.TFile("OutputHistograms/Data/"+run+postfix+".root")
            elif  os.path.isfile("OutputHistograms/MC/"+run+postfix+postfixMC+".root"): 
                histFile=ROOT.TFile("OutputHistograms/MC/"+run+postfix+postfixMC+".root")
            else: 
                print "NO FILE FOUND!!!!!   "+"OutputHistograms/MC/"+run+postfix+postfixMC+".root"
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
        pos_side_found_ele_found_pos=histFile.Get(histName+cuts+posSideFound)
        mis_pos=histFile.Get(histName+cuts+posMis)
        
        ele_side_found_pos=histFile.Get(histName+cuts+eleSide)
        ele_side_found_pos_found_ele=histFile.Get(histName+cuts+eleSideFound)
        mis_ele=histFile.Get(histName+cuts+eleMis)
        
        print histName+cuts+esumAll
        if doesum: 
            esum_all=histFile.Get(esumName+cuts+esumAll)
            esum_found_both=histFile.Get(esumName+cuts+esumBoth)
            
        denom = pos_side_found_ele.Clone()
        denom.Rebin(effRebin)
        denom.Sumw2()
        numer= pos_side_found_ele_found_pos.Clone();
        numer.Rebin(effRebin);
        numer.Sumw2();
        eff=ROOT.TGraphAsymmErrors()
        eff.SetName(histName+run+"_posEff")
        eff.Divide(numer,denom)
        eff.SetLineWidth(3);
        outFile.cd()
        eff.Write()
        histFile.cd()
#        outFile.Write()
        legMIDESUM7=ROOT.TLegend(0.1,0.8,0.4,0.9);
        legMIDESUM7.AddEntry(pos_side_found_ele,"Positron-Side Clusters","l"); 
        legMIDESUM7.AddEntry(mis_pos,"No Positron Track","l");


        ct = ROOT.TCanvas("ct","transparent pad",200,10,700,500);
        pad1 = ROOT.TPad("pad1","",0,0,1,1);
        pad2 = ROOT.TPad("pad2","",0,0,1,1);
        pad2.SetFillStyle(4000); #will be transparent
        pad2.SetFillStyle(4000); #will be transparent
        pad1.Draw();
        pad1.cd();

        pos_side_found_ele.SetXTitle(xTitle);
        pos_side_found_ele.SetLineColor(1);
        pos_side_found_ele.SetLineColor(2);
        mis_pos.SetLineColor(3);
    
        pos_side_found_ele.Draw();  
        mis_pos.Draw("same");
    
        ct.cd();
        ymin = 0.0;
        ymax = 1.0;
        dy = (ymax-ymin)/0.8; #10 per cent margins top and bottom


        xminP =pos_side_found_ele.GetXaxis().GetXmin()
        xmaxP =pos_side_found_ele.GetXaxis().GetXmax()
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
        axis.Draw();
        legMIDESUM7.Draw();
        ct.SaveAs(outpre+histName+cuts+postfixMC+"-positron-efficiency.pdf");
    
###############################
        denom =ele_side_found_pos.Clone();
        denom.Rebin(effRebin);
        denom.Sumw2();
        numer=ele_side_found_pos_found_ele.Clone();
        numer.Rebin(effRebin);
        numer.Sumw2();
        eff=ROOT.TGraphAsymmErrors()
        eff.SetName(histName+run+"_eleEff")
        eff.Divide(numer,denom)
        eff.SetLineWidth(3)
        outFile.cd()
        eff.Write()
        histFile.cd()
#        outFile.Write()
    
        legMIDESUM8=ROOT.TLegend(0.6,0.2,0.9,0.3);
        legMIDESUM8.AddEntry(pos_side_found_ele,"Electron-Side Clusters","l"); 
        legMIDESUM8.AddEntry(mis_pos,"No Electron Track","l");
    
        ct = ROOT.TCanvas("ct","transparent pad",200,10,700,500);
        pad1 = ROOT.TPad("pad1","",0,0,1,1);
        pad2 = ROOT.TPad("pad2","",0,0,1,1);
        pad2.SetFillStyle(4000); #will be transparent
        pad2.SetFillStyle(4000); #will be transparent
        pad1.Draw();
        pad1.cd();

        ele_side_found_pos.SetXTitle(xTitle);
        ele_side_found_pos.SetLineColor(1);
        ele_side_found_pos.SetLineColor(2);
        mis_ele.SetLineColor(3);
        
        ele_side_found_pos.Draw();  
        mis_ele.Draw("same");
        
        xminE =ele_side_found_pos.GetXaxis().GetXmin()
        xmaxE =ele_side_found_pos.GetXaxis().GetXmax()
        
    
        ct.cd();
        dy = (ymax-ymin)/0.8; #10 per cent margins top and bottom
        dx = (xmaxE-xminE)/0.8; #10 per cent margins left and right
        pad2.Range(xminE-0.1*dx,ymin-0.1*dy,xmaxE+0.1*dx,ymax+0.1*dy);
        pad2.Draw();
        pad2.cd();
        eff.SetLineColor(1);
        eff.Draw("][samese");
        #   effWABElectron.SetLineColor(kBlue);
#effWABElectron.Draw("][samese");
        pad2.Update();
        effEle.append(eff)
        
        axis = ROOT.TGaxis(xmaxE,ymin,xmaxE,ymax,ymin,ymax,50510,"+L");
        axis.SetLabelColor(2);
        axis.Draw();
        legMIDESUM8.Draw();
        ct.SaveAs(outpre+histName+cuts+postfixMC+"-electron-efficiency.pdf");
   
###############################
        if doesum: 
            denom =esum_all.Clone();
            denom.Rebin(effRebin);
            denom.Sumw2();
            numer=esum_found_both.Clone();
            numer.Rebin(effRebin);
            numer.Sumw2();
            eff=ROOT.TGraphAsymmErrors()
            eff.Divide(numer,denom)
            eff.SetLineWidth(3);
            
            legMIDESUM9=ROOT.TLegend(0.6,0.2,0.9,0.3);
            legMIDESUM9.AddEntry(esum_all,"All Pairs","l"); 
            legMIDESUM9.AddEntry(esum_found_both,"Found Both Tracks","l");
    
            ct = ROOT.TCanvas("ct","transparent pad",200,10,700,500);
            pad1 = ROOT.TPad("pad1","",0,0,1,1);
            pad2 = ROOT.TPad("pad2","",0,0,1,1);
            pad2.SetFillStyle(4000); #will be transparent
            pad2.SetFillStyle(4000); #will be transparent
            pad1.Draw();
            pad1.cd();
            
            esum_all.SetXTitle("ESum (GeV)");
            esum_all.SetLineColor(1);
            esum_found_both.SetLineColor(2);
            
            esum_all.Draw();  
            esum_found_both.Draw("same");
            
            xmin =esum_all.GetXaxis().GetXmin()
            xmax =esum_all.GetXaxis().GetXmax()
            ct.cd();
            dy = (ymax-ymin)/0.8; #10 per cent margins top and bottom
            dx = (xmax-xmin)/0.8; #10 per cent margins left and right
            pad2.Range(xmin-0.1*dx,ymin-0.1*dy,xmax+0.1*dx,ymax+0.1*dy);
            pad2.Draw();
            pad2.cd();
            eff.SetLineColor(1);
            eff.Draw("][samese");
            #   effWABElectron.SetLineColor(kBlue);
        #effWABElectron.Draw("][samese");
            pad2.Update();
            effESum.append(eff)

            axis = ROOT.TGaxis(xmax,ymin,xmax,ymax,ymin,ymax,50510,"+L");
            axis.SetLabelColor(2);
            axis.Draw();
            legMIDESUM9.Draw();
            ct.SaveAs(outpre+histName+cuts+"-ESum-efficiency.pdf"); 

            
    legEle=ROOT.TLegend(0.6,0.2,0.8,0.3);
    legPos=ROOT.TLegend(0.6,0.2,0.8,0.3);
    legESum=ROOT.TLegend(0.6,0.2,0.8,0.3);
#xmin =pos_side_found_ele.GetXaxis().GetXmin()
#xmax =pos_side_found_ele.GetXaxis().GetXmax()
    base=ROOT.TH2D("","",100,xminE,xmaxE,100,0.0,1.0)
    base.SetXTitle(xTitle);
    base.SetYTitle("Electron Efficiency");

    ct = ROOT.TCanvas("ct","transparent pad",200,10,700,500);
    base.Draw()
    effEle[0].Draw("p")
    legEle.AddEntry(effEle[0],legs[0],"l"); 
    outpre="plots-"+str(ene)+"GeV/"
    for i in range(1,len(effEle)): 
        legEle.AddEntry(effEle[i],legs[i],"l"); 
        effEle[i].SetLineColor(col[i])
        effEle[i].Draw("p")
    legEle.Draw()
    ct.SaveAs(outpre+histName+cuts+postfixMC+"-electron-efficiency.pdf")
              

#base=ROOT.TH2D("","",100,0.4,1.6,100,0.4,1.0)
    base=ROOT.TH2D("","",100,xminP,xmaxP,100,0.0,1.0)
    base.SetXTitle(xTitle);
    base.SetYTitle("Positron Efficiency");
    
    ct = ROOT.TCanvas("ct","transparent pad",200,10,700,500);
    base.Draw()
    effPos[0].Draw("p")
    legPos.AddEntry(effPos[0],legs[0],"l"); 
    outpre="plots-"+str(ene)+"GeV/"
    for i in range(1,len(effPos)): 
        legPos.AddEntry(effPos[i],legs[i],"l"); 
        effPos[i].SetLineColor(col[i])
        effPos[i].Draw("p")
    legPos.Draw()    
    ct.SaveAs(outpre+histName+cuts+postfixMC+"-positron-efficiency.pdf")

    if doesum: 
        xmin =esum_all.GetXaxis().GetXmin()
        xmax =esum_all.GetXaxis().GetXmax()
        base=ROOT.TH2D("","",100,xmin,xmax,100,0.0,1.0)
        base.SetXTitle("ESum (GeV)");
        base.SetYTitle("ESum Efficiency");
        
        ct = ROOT.TCanvas("ct","transparent pad",200,10,700,500);
        base.Draw()
        effESum[0].Draw("p")
        legESum.AddEntry(effESum[0],legs[0],"l"); 
        outpre="plots-"+str(ene)+"GeV/"
        for i in range(1,len(effESum)): 
            legESum.AddEntry(effESum[i],legs[i],"l"); 
            effESum[i].SetLineColor(col[i])
            effESum[i].Draw("p")
        legESum.Draw()    
        ct.SaveAs(outpre+histName+cuts+postfixMC+"-ESum-efficiency.pdf")

outFile.Close()
