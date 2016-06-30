import array
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph

def makePlots(c,goodEvents,badEvents,filename,name,var,nbins,xmin,xmax,cut,forward):
    c.Clear()
    c.Divide(2,2)
    c.cd(1)
    goodEvents.Draw("{}>>good({},{},{})".format(var,nbins,xmin,xmax),cut,"")
    gDirectory.Get("good").SetTitle(var+", good events")
    c.cd(2)
    badEvents.Draw("{}>>bad({},{},{})".format(var,nbins,xmin,xmax),cut,"")
    gDirectory.Get("bad").SetTitle(var+", bad events")
    goodHist = gDirectory.Get("good")
    badHist = gDirectory.Get("bad")
    goodEfficiency=0
    badEfficiency=0
    cuts=array.array('d')
    goodEfficiencies=array.array('d')
    badEfficiencies=array.array('d')
    goodEfficiencies.append(0)
    badEfficiencies.append(0)
    nbins=goodHist.GetXaxis().GetNbins()
    goodTotal=goodHist.Integral()+goodHist.GetBinContent(0)+goodHist.GetBinContent(nbins+1)
    badTotal=badHist.Integral()+badHist.GetBinContent(0)+badHist.GetBinContent(nbins+1)
    if forward:
        start=0
        end=nbins+2
        step=1
        cuts.append(goodHist.GetXaxis().GetBinLowEdge(start))
    else:
        start=nbins+1
        end=-1
        step=-1
        cuts.append(goodHist.GetXaxis().GetBinUpEdge(start))
    for i in xrange(start,end,step):
        if forward:
            cuts.append(goodHist.GetXaxis().GetBinUpEdge(i))
        else:
            cuts.append(goodHist.GetXaxis().GetBinLowEdge(i))
        goodEfficiency+=goodHist.GetBinContent(i)/goodTotal
        badEfficiency+=badHist.GetBinContent(i)/badTotal
        goodEfficiencies.append(goodEfficiency)
        badEfficiencies.append(badEfficiency)
        #print "{0}, {1}".format(badEfficiency,goodEfficiency)
    goodEffGraph = TGraph(len(cuts),cuts,goodEfficiencies)
    badEffGraph = TGraph(len(cuts),cuts,badEfficiencies)
    c.cd(3)
    goodEffGraph.SetTitle("Efficiency vs. cut value")
    goodEffGraph.Draw("AL")
    goodEffGraph.GetXaxis().SetRangeUser(xmin,xmax)
    goodEffGraph.GetYaxis().SetRangeUser(0,1)
    badEffGraph.SetLineColor(2)
    badEffGraph.Draw("L")

    rocGraph = TGraph(len(goodEfficiencies),badEfficiencies,goodEfficiencies)
    rocGraph.SetName(var)
    rocGraph.SetTitle("ROC curve")
    rocGraph.GetXaxis().SetRangeUser(0,1)
    rocGraph.GetYaxis().SetRangeUser(0,1)
    c.cd(4)
    rocGraph.Draw("ALP")
    c.Modified()
    c.Print(filename+".pdf","Title:"+name)

def allBut(cuts,i):
    return cuts[:i]+cuts[i+1:]
def makeCutString(cuts):
    return reduce(lambda a,b:a+"&&"+b,[str(i) for i in cuts])
