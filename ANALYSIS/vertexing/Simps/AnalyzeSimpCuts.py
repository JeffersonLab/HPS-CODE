import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input file name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-h: this help message'
    print

zTarg = 0.5
ebeam = 2.3

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hz:e:')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-z':
			zTarg = float(arg)
		if opt=='-e':
			ebeam = float(arg)
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

#def tupleToHisto(events,inHisto,histo,nBins,minX,maxX):
#	events.Draw("{0}>>{1}({2},{3},{4})".format(inHisto,histo,nBins,minX,maxX))
#	histo = ROOT.gROOT.FindObject(histo)
#	return histo

#def saveTuplePlot(inHisto,nBins,minX,maxX,outfile,canvas):
#	events.Draw("{0}>>({1},{2},{3})".format(inHisto,nBins,minX,maxX))
#	canvas.Print(outfile+".pdf")

def saveTuplePlot2D(events,inHisto1,inHisto2,nBinsX,minX,maxX,nBinsY,minY,maxY,mincut,maxcut,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0,logY=0):
	events.Draw("{0}:{1}>>histo({2},{3},{4},{5},{6},{7})".format(inHisto2,inHisto1,nBinsX,minX,maxX,nBinsY,minY,maxY))
	histo = ROOT.gROOT.FindObject("histo")
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)
	histo.Draw("COLZ")
	minline = TLine(minX,mincut,maxX,mincut)
	minline.SetLineColor(2)
 	minline.Draw("same")
 	maxline = TLine(minX,maxcut,maxX,maxcut)
	maxline.SetLineColor(2)
 	maxline.Draw("same")
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")
	del histo
def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

#def getHisto(histoTitle,infile):
#	histo = infile.Get(histoTitle)
#	return histo

#def buildLegend(entries,options):
#	legend = TLegend()
#	legend = TLegend(.68,.66,.92,.87)
#	legend.SetBorderSize(0)
#	legend.SetFillColor(0)
#	legend.SetFillStyle(0)
#	legend.SetTextFont(42)
#	legend.SetTextSize(0.035)
#	legend.AddEntry(Histo1,"L0L0","LP")
#	return legend

#def drawHisto(histo,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
#	histo.Draw("")
	#histo.GetXaxis().SetRangeUser(-5,150)
	#histo.GetYaxis().SetRangeUser(0,1.1)
#	histo.SetTitle(plotTitle)
#	histo.GetXaxis().SetTitle(XaxisTitle)
#	histo.GetYaxis().SetTitle(YaxisTitle)
#	histo.SetStats(stats)

#def saveHisto(histo,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
#	drawHisto(histo,XaxisTitle,YaxisTitle,plotTitle,stats)
#	canvas.Print(outfile+".pdf")

def getPlot(string):
	arr = string.split(" ")
	return arr[0]

def getMin(string):
	arr = string.split(" ")
	if(len(arr) < 2): return ""
	else: return float(arr[1])

def getMax(string):
	arr = string.split(" ")
	if(len(arr) < 3): return ""
	else: return float(arr[2])

def getMinCut(string):
	arr = string.split(" ")
	if(len(arr) < 4): return -9999
	else: return float(arr[3])

def getMaxCut(string):
	arr = string.split(" ")
	if(len(arr) < 5): return -9999
	else: return float(arr[4])

nBins = 50
minVZ = -20
maxVZ = 150

outfile = remainder[0]
MCfile = TFile(remainder[1])

MCevents = MCfile.Get("ntuple")

apfiles = []
events = []
mass = []

for i in range(2,len(remainder)):
	apfiles.append(TFile(remainder[i]))
	events.append(apfiles[i-2].Get("ntuple"))
	events[i-2].Draw("triM>>dummy({0},{1},{2})".format(1000,0,1))
	dummy = ROOT.gROOT.FindObject("dummy")
	mass.append(dummy.GetMean())
	del dummy

cuts = []
cuts.append("eleClY*posClY -10000 10000 0")
cuts.append("uncP 0 2.8 0.92 1.495")
cuts.append("eleTrkChisq 0 50 30")
cuts.append("posTrkChisq 0 50 30")
cuts.append("eleP 0 2.8 0.95")
cuts.append("posP 0 2.8 0.95")
cuts.append("bscChisq 0 20 10")
cuts.append("bscChisq-uncChisq 0 10 5")
cuts.append("eleMatchChisq 0 15 10")
cuts.append("posMatchChisq 0 15 10")
cuts.append("abs(eleClT-eleTrkT-43) 0 10 4")
cuts.append("abs(posClT-posTrkT-43) 0 10 4")
cuts.append("abs(eleClT-posClT) 0 10 2")
cuts.append("eleMinPositiveIso+0.5*(eleTrkZ0+{0}*elePY/eleP)*sign(elePY) -5 5 0".format(zTarg))
cuts.append("posMinPositiveIso+0.5*(posTrkZ0+{0}*posPY/posP)*sign(posPY) -5 5 0".format(zTarg))

histos = []
openPDF(outfile,c)

for i in range(len(cuts)):
	plot = getPlot(cuts[i])
	minimum = getMin(cuts[i])
	maximum = getMax(cuts[i])
	mincut = getMinCut(cuts[i])
	maxcut = getMaxCut(cuts[i])
	histos.append(TH1F(cuts[i],cuts[i],nBins,minimum,maximum))
	saveTuplePlot2D(MCevents,"uncVZ",plot,nBins,minVZ,maxVZ,nBins,minimum,maximum,mincut,maxcut,outfile,c,"uncVZ",plot," MC " + plot)
	for j in range(len(events)):
		saveTuplePlot2D(events[j],"uncVZ",plot,nBins,minVZ,maxVZ,nBins,minimum,maximum,mincut,maxcut,outfile,c,"uncVZ",plot,str(mass[j]) + " GeV V " + plot)

closePDF(outfile,c)