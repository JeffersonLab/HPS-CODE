
import ROOT  
import os

def getEfficiencyPlot(num, den, effRebin = 1 ) :
    denom =den.Clone()
    denom.Rebin(effRebin)
    denom.Sumw2()
    numer=num.Clone()
    numer.Rebin(effRebin)
    numer.Sumw2()
    eff=ROOT.TGraphAsymmErrors()
    eff.Divide(numer,denom)
    eff.SetLineWidth(3)
    return eff

def setPad(pad, xmin,xmax,ymin,ymax) : 

    dy = (ymax-ymin)/0.8 #10 per cent margins top and bottom
    dx = (xmax-xmin)/0.8 #10 per cent margins left and right
    pad.Range(xmin-0.1*dx,ymin-0.1*dy,xmax+0.1*dx,ymax+0.1*dy)
        
def plotEff(num,den,effRebin,xtitle,outname) : 
    ct = ROOT.TCanvas("ct","transparent pad",200,10,700,500)
    eff=ROOT.TGraphAsymmErrors()
    eff=getEfficiencyPlot(num,den,effRebin)

    legMIDESUM9=ROOT.TLegend(0.6,0.2,0.9,0.3)
    legMIDESUM9.AddEntry(den,"All Pairs","l") 
    legMIDESUM9.AddEntry(num,"Found Both Tracks","l")
    
    pad1 = ROOT.TPad("pad1","",0,0,1,1)
    pad2 = ROOT.TPad("pad2","",0,0,1,1)
    pad2.SetFillStyle(4000) #will be transparent
    pad2.SetFillStyle(4000) #will be transparent
    pad1.Draw()
    pad1.cd()

    den.SetXTitle(xtitle)
    den.SetLineColor(1)
    num.SetLineColor(2)
    
    den.Draw()  
    num.Draw("same")
    ymin=0.0
    ymax = 1.0
    xmin =den.GetXaxis().GetXmin()
    xmax =den.GetXaxis().GetXmax()
    setPad(pad2,xmin,xmax,ymin,ymax)
    ct.cd()
    pad2.Draw()
    pad2.cd()
    eff.SetLineColor(1)
    eff.Draw("][samese")
    pad2.Update()
    axis = ROOT.TGaxis(xmax,ymin,xmax,ymax,ymin,ymax,50510,"+L")
    axis.SetLabelColor(2)
    axis.Draw()
    legMIDESUM9.Draw()
    ct.SaveAs(outname)
    return eff
