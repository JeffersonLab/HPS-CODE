# ///*** get some efficiency plots for the MIDESUM set of plots   ***///
import ROOT  

ene=2.3

runs=[7809,7807,7808]
effEle=[]
effPos=[]
for run in runs : 
    outpre="plots-"+str(ene)+"GeV/hps_00"+str(run)

    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptTitle(0)
#histFile=ROOT.TFile("OutputHistograms/Data/hps_008087_hpsrun2016_pass0_useGBL_ECalMatch.root")
    if ene==1.05 :
        print 'Loading 1.05GeV File' 
        histFile=ROOT.TFile("OutputHistograms/Data/hps_005772_engrun2015_pass6.root")
    else : 
        histFile=ROOT.TFile("OutputHistograms/Data/hps_00"+str(run)+"_hpsrun2016_pass0_useGBL_ECalMatch.root")

#get some histograms
    h_Ecl_cop180_midESum_pos_side_found_ele=histFile.Get("h_Ecl_cop180_midESum_pos_side_found_ele")
    h_Ecl_cop180_midESum_pos_side_found_ele_found_pos=histFile.Get("h_Ecl_cop180_midESum_pos_side_found_ele_found_pos")
    h_Ecl_cop180_midESum_mis_pos=histFile.Get("h_Ecl_cop180_midESum_mis_pos")
    
    h_Ecl_cop180_midESum_ele_side_found_pos=histFile.Get("h_Ecl_cop180_midESum_ele_side_found_pos")
    h_Ecl_cop180_midESum_ele_side_found_pos_found_ele=histFile.Get("h_Ecl_cop180_midESum_ele_side_found_pos_found_ele")
    h_Ecl_cop180_midESum_mis_ele=histFile.Get("h_Ecl_cop180_midESum_mis_ele")

    denom = h_Ecl_cop180_midESum_pos_side_found_ele.Clone()
    denom.Rebin(4)
    denom.Sumw2()
    numer= h_Ecl_cop180_midESum_pos_side_found_ele_found_pos.Clone();
    numer.Rebin(4);
    numer.Sumw2();
    eff=ROOT.TGraphAsymmErrors()
    eff.Divide(numer,denom)
    eff.SetLineWidth(3);
    legMIDESUM7=ROOT.TLegend(0.1,0.8,0.4,0.9);
    legMIDESUM7.AddEntry(h_Ecl_cop180_midESum_pos_side_found_ele,"Positron-Side Clusters","l"); 
    legMIDESUM7.AddEntry(h_Ecl_cop180_midESum_mis_pos,"No Positron Track","l");


    ct = ROOT.TCanvas("ct","transparent pad",200,10,700,500);
    pad1 = ROOT.TPad("pad1","",0,0,1,1);
    pad2 = ROOT.TPad("pad2","",0,0,1,1);
    pad2.SetFillStyle(4000); #will be transparent
    pad2.SetFillStyle(4000); #will be transparent
    pad1.Draw();
    pad1.cd();

    h_Ecl_cop180_midESum_pos_side_found_ele.SetXTitle("Cluster Energy (GeV)");
    h_Ecl_cop180_midESum_pos_side_found_ele.SetLineColor(1);
    h_Ecl_cop180_midESum_pos_side_found_ele.SetLineColor(2);
    h_Ecl_cop180_midESum_mis_pos.SetLineColor(3);
    
    h_Ecl_cop180_midESum_pos_side_found_ele.Draw();  
    h_Ecl_cop180_midESum_mis_pos.Draw("same");
    
    ct.cd();
    ymin = 0.0;
    ymax = 1.0;
    dy = (ymax-ymin)/0.8; #10 per cent margins top and bottom

    xmin = h_Ecl_cop180_midESum_pos_side_found_ele.GetXaxis().GetXmin()
    xmax = h_Ecl_cop180_midESum_pos_side_found_ele.GetXaxis().GetXmax()
    dx = (xmax-xmin)/0.8; #10 per cent margins left and right
    pad2.Range(xmin-0.1*dx,ymin-0.1*dy,xmax+0.1*dx,ymax+0.1*dy);
    pad2.Draw();
    pad2.cd();
    eff.SetLineColor(1);
    eff.Draw("][samese");
    pad2.Update();
    effPos.append(eff)

    axis =ROOT.TGaxis(xmax,ymin,xmax,ymax,ymin,ymax,50510,"+L");
    axis.SetLabelColor(2);
    axis.Draw();
    legMIDESUM7.Draw();
    ct.SaveAs(outpre+"MIDESUM-cluster-energy-positron-efficiency.pdf");
    

    denom =h_Ecl_cop180_midESum_ele_side_found_pos.Clone();
    denom.Rebin(4);
    denom.Sumw2();
    numer= h_Ecl_cop180_midESum_ele_side_found_pos_found_ele.Clone();
    numer.Rebin(4);
    numer.Sumw2();
    eff=ROOT.TGraphAsymmErrors()
    eff.Divide(numer,denom)
    eff.SetLineWidth(3);
    
    legMIDESUM8=ROOT.TLegend(0.6,0.2,0.9,0.3);
    legMIDESUM8.AddEntry(h_Ecl_cop180_midESum_pos_side_found_ele,"Electron-Side Clusters","l"); 
    legMIDESUM8.AddEntry(h_Ecl_cop180_midESum_mis_pos,"No Electron Track","l");
    
    ct = ROOT.TCanvas("ct","transparent pad",200,10,700,500);
    pad1 = ROOT.TPad("pad1","",0,0,1,1);
    pad2 = ROOT.TPad("pad2","",0,0,1,1);
    pad2.SetFillStyle(4000); #will be transparent
    pad2.SetFillStyle(4000); #will be transparent
    pad1.Draw();
    pad1.cd();

    h_Ecl_cop180_midESum_ele_side_found_pos.SetXTitle("Cluster Energy (GeV)");
    h_Ecl_cop180_midESum_ele_side_found_pos.SetLineColor(1);
    h_Ecl_cop180_midESum_ele_side_found_pos.SetLineColor(2);
    h_Ecl_cop180_midESum_mis_ele.SetLineColor(3);
    
    h_Ecl_cop180_midESum_ele_side_found_pos.Draw();  
    h_Ecl_cop180_midESum_mis_ele.Draw("same");
    
    
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
    effEle.append(eff)

    axis = ROOT.TGaxis(xmax,ymin,xmax,ymax,ymin,ymax,50510,"+L");
    axis.SetLabelColor(2);
    axis.Draw();
    legMIDESUM8.Draw();
    ct.SaveAs(outpre+"MIDESUM-cluster-energy-electron-efficiency.pdf");
    
col=[1,2,4]


legEle=ROOT.TLegend(0.6,0.2,0.8,0.3);
legEle.AddEntry(effEle[0]," 50nA","l"); 
legEle.AddEntry(effEle[1],"200nA","l"); 
legEle.AddEntry(effEle[2],"300nA","l"); 

legPos=ROOT.TLegend(0.6,0.2,0.8,0.3);
legPos.AddEntry(effPos[0]," 50nA","l"); 
legPos.AddEntry(effPos[1],"200nA","l"); 
legPos.AddEntry(effPos[2],"300nA","l"); 

base=ROOT.TH2D("","",100,0.4,1.6,100,0.4,1.0)
base.SetXTitle("Cluster Energy (GeV)");
base.SetYTitle("Electron Efficiency");

ct = ROOT.TCanvas("ct","transparent pad",200,10,700,500);
base.Draw()
effEle[0].Draw("p")
outpre="plots-"+str(ene)+"GeV/"
for i in range(1,len(effEle)): 
    effEle[i].SetLineColor(col[i])
    effEle[i].Draw("p")
legEle.Draw()
ct.SaveAs(outpre+"cluster-energy-electron-efficiency.pdf")
              

#base=ROOT.TH2D("","",100,0.4,1.6,100,0.4,1.0)
base.SetYTitle("Positron Efficiency");

ct = ROOT.TCanvas("ct","transparent pad",200,10,700,500);
base.Draw()
effPos[0].Draw("p")
outpre="plots-"+str(ene)+"GeV/"
for i in range(1,len(effEle)): 
    effPos[i].SetLineColor(col[i])
    effPos[i].Draw("p")
legPos.Draw()    
ct.SaveAs(outpre+"cluster-energy-positron-efficiency.pdf")
