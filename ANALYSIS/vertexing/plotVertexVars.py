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
    print '\t-t: use full truth plots'
    print '\t-m: minimum uncVZ'
    print '\t-n: maximum uncVZ'
    print '\t-b: number of bins'
    print '\t-e: beam energy'
    print '\t-t: track time diff offset'
    print '\t-x: beam x position'
    print '\t-y: beam y position'
    print '\t-z: target z position'
    print '\t-p: only plot 1D'
    print '\t-q: only make quick plots'
    print '\t-h: this help message'
    print

fullTruth = False
minVZ = -30
maxVZ = 30
nBins = 100
energy = 2.3
trackTDiff = 55
beamX = 0.0
beamY = 0.0
targZ = -4.0
plot2D = True
quickPlots = False
nentries = 99999999999999

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'tm:n:b:e:t:x:y:z:s:pqh')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-t':
			fullTruth = True
		if opt=='-m':
			minVZ = float(arg)
		if opt=='-n':
			maxVZ = float(arg)
		if opt=='-b':
			nBins = float(arg)
		if opt=='-e':
			energy = float(arg)
		if opt=='-t':
			trackTDiff = float(arg)
		if opt=='-x':
			beamX = float(arg)
		if opt=='-y':
			beamY = float(arg)
		if opt=='-z':
			targZ = float(arg)
		if opt=='-s':
			nentries = int(arg)
		if opt=='-p':
			plot2D = False
		if opt=='-q':
			quickPlots = True
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

def saveTuplePlot(events,inHisto,nBins,minX,maxX,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",nentries=0,stats=0,logY=0):
	events.Draw("{0}>>histo({1},{2},{3})".format(inHisto,nBins,minX,maxX),"","",nentries)
	histo = ROOT.gROOT.FindObject("histo")
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)
	histo.Draw()
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")
	histo.Write(plotTitle)
	del histo


def saveTuplePlot2D(events,inHisto1,inHisto2,nBinsX,minX,maxX,nBinsY,minY,maxY,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",nentries=0,stats=0,logY=0):
	events.Draw("{0}:{1}>>histo({2},{3},{4},{5},{6},{7})".format(inHisto2,inHisto1,nBinsX,minX,maxX,nBinsY,minY,maxY),"","",nentries)
	histo = ROOT.gROOT.FindObject("histo")
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)
	histo.Draw("COLZ")
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")
	histo.Write(plotTitle)
	del histo

def saveFitPlot(events,inHisto,nBins,minX,maxX,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",nentries=0,stats=1,logY=0):
	events.Draw("{0}>>histo({1},{2},{3})".format(inHisto,nBins,minX,maxX),"","",nentries)
	histo = ROOT.gROOT.FindObject("histo")
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)
	histo.Fit("gaus")
	histo.Draw()
	canvas.SetLogy(logY)
	canvas.Print(outfile+".pdf")
	histo.Write(plotTitle)
	del histo

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

def getPlot(string):
	arr = string.split(" ")
	return arr[0]

def getPlot2D(string):
	arr = string.split(" ")
	if(len(arr) < 2): return ""
	else: return arr[1]

def getMinX(string):
	arr = string.split(" ")
	if(len(arr) < 2): return -9999
	else: return float(arr[1])

def getMaxX(string):
	arr = string.split(" ")
	if(len(arr) < 3): return -9999
	else: return float(arr[2])

def getMinX2D(string):
	arr = string.split(" ")
	if(len(arr) < 3): return -9999
	else: return float(arr[2])

def getMaxX2D(string):
	arr = string.split(" ")
	if(len(arr) < 4): return -9999
	else: return float(arr[3])

def getMinY(string):
	arr = string.split(" ")
	if(len(arr) < 5): return -9999
	else: return float(arr[4])

def getMaxY(string):
	arr = string.split(" ")
	if(len(arr) < 6): return -9999
	else: return float(arr[5])

outfile = remainder[0]

events = TChain("ntuple")
for i in range(1,len(remainder)):
    events.Add(remainder[i])

rootfile = TFile(outfile+".root","recreate")

plots = []
plots.append("uncVZ {0} {1}".format(minVZ,maxVZ))
plots.append("uncM 0 {0}".format(0.1*energy))
plots.append("uncPX -{0} {0}".format(0.05*energy))
plots.append("uncPY -{0} {0}".format(0.05*energy))
plots.append("uncPZ 0 {0}".format(1.6*energy))
plots.append("uncP 0 {0}".format(1.6*energy))
plots.append("uncChisq 0 20")
plots.append("bscChisq 0 20")
plots.append("sqrt(uncCovZZ) 0 15")
plots.append("eleClT 20 80")
plots.append("posClT 20 80")
plots.append("eleClE 0 {0}".format(1.6*energy))
plots.append("posClE 0 {0}".format(1.6*energy))
plots.append("elePX -{0} {0}".format(0.05*energy))
plots.append("posPX -{0} {0}".format(0.05*energy))
plots.append("elePY -{0} {0}".format(0.05*energy))
plots.append("posPY -{0} {0}".format(0.05*energy))
plots.append("elePZ 0 {0}".format(1.6*energy))
plots.append("posPZ 0 {0}".format(1.6*energy))
plots.append("eleP 0 {0}".format(1.6*energy))
plots.append("posP 0 {0}".format(1.6*energy))
plots.append("eleTrkChisq 0 50")
plots.append("posTrkChisq 0 50")
plots.append("eleTrkT -20 20")
plots.append("posTrkT -20 20")
plots.append("eleClT-posClT -10 10")
plots.append("eleClT-eleTrkT-{0} -10 10".format(trackTDiff))
plots.append("posClT-posTrkT-{0} -10 10".format(trackTDiff))
plots.append("eleTrkZ0 -3 3")
plots.append("posTrkZ0 -3 3")
plots.append("eleTrkD0 -7 7")
plots.append("posTrkD0 -7 7")
plots.append("eleTrkLambda -0.1 0.1")
plots.append("posTrkLambda -0.1 0.1")
plots.append("eleMatchChisq 0 15")
plots.append("posMatchChisq 0 15")

if(not quickPlots):
	plots.append("eleClE/eleP 0 3")
	plots.append("posClE/posP 0 3")
	plots.append("(eleTrkZ0+eleTrkLambda*{0})*sign(eleTrkLambda) -3 3".format(targZ))
	plots.append("(posTrkZ0+posTrkLambda*{0})*sign(posTrkLambda) -3 3".format(targZ))
	plots.append("(eleTrkZ0+eleTrkLambda*uncVZ)*sign(eleTrkLambda) -3 3")
	plots.append("(posTrkZ0+posTrkLambda*uncVZ)*sign(posTrkLambda) -3 3")
	plots.append("(eleTrkZ0+eleTrkLambda*uncVZ)*sign(eleTrkLambda)-uncVY -3 3")
	plots.append("(posTrkZ0+posTrkLambda*uncVZ)*sign(posTrkLambda)-uncVY -3 3")
	plots.append("eleTrkOmega 0 0.001")
	plots.append("posTrkOmega -0.001 0")
	plots.append("eleTrkPhi -0.2 0.4")
	plots.append("posTrkPhi -0.4 0.2")
	plots.append("bscChisq-uncChisq 0 15")
	plots.append("elePhiKink1 -0.005 0.005")
	plots.append("posPhiKink1 -0.005 0.005")
	plots.append("elePhiKink2 -0.005 0.005")
	plots.append("posPhiKink2 -0.005 0.005")
	plots.append("elePhiKink3 -0.005 0.005")
	plots.append("posPhiKink3 -0.005 0.005")
	plots.append("eleLambdaKink1 -0.01 0.01")
	plots.append("posLambdaKink1 -0.01 0.01")
	plots.append("eleLambdaKink2 -0.01 0.01")
	plots.append("posLambdaKink2 -0.01 0.01")
	plots.append("eleLambdaKink3 -0.01 0.01")
	plots.append("posLambdaKink3 -0.01 0.01")
	plots.append("eleIsoStereo -5 10")
	plots.append("posIsoStereo -5 10")
	plots.append("eleIsoAxial -5 10")
	plots.append("posIsoAxial -5 10")
	plots.append("nSVTHits 0 1000")
	plots.append("nSVTHitsL1 0 400")
	plots.append("nSVTHitsL1b 0 400")
	plots.append("nPos 0 10")
	plots.append("(eleP-posP)/uncP -1 1")
	plots.append("(atan(eleClY/(eleClX-42.5))-atan(posClY/(posClX-42.5)))*180/3.14+180 0 300")
	plots.append("uncTargProjX-{0} -4 4".format(beamX))
	plots.append("uncTargProjY-{0} -2 2".format(beamY))
	plots.append("(uncTargProjX-{0})/uncTargProjXErr -10 10".format(beamX))
	plots.append("(uncTargProjY-{0})/(sqrt(uncCovYY)+sqrt(uncCovZZ)*uncPY/uncPZ+(uncVZ-{0})*(uncMomYErr/uncPZ+uncPY*uncMomZErr/uncPZ**2)) -10 10".format(beamY))
	plots.append("(uncVX-{0})/sqrt(uncCovXX) -10 10".format(beamX))
	plots.append("(uncVY-{0})/sqrt(uncCovYY) -10 10".format(beamY))
	plots.append("(uncVZ-{0})/sqrt(uncCovZZ) -10 10".format(targZ))

plots2D = []
plots2D.append("uncM uncVZ 0 {2} {0} {1}".format(minVZ,maxVZ,0.1*energy))
plots2D.append("eleTrkEcalX eleTrkEcalY -300 300 -100 100")
plots2D.append("posTrkEcalX posTrkEcalY -300 300 -100 100")

if(not quickPlots):
	plots2D.append("posMatchChisq eleMatchChisq 0 15 0 15")
	plots2D.append("eleTrkEcalX eleTrkEcalY -300 300 -100 100")
	plots2D.append("posTrkEcalX posTrkEcalY -300 300 -100 100")
	plots2D.append("eleTrkExtrpXAxialTopL1 eleTrkExtrpYAxialTopL1 -40 40 -20 20")
	plots2D.append("posTrkExtrpXAxialTopL1 posTrkExtrpYAxialTopL1 -40 40 -20 20")
	plots2D.append("eleTrkExtrpXStereoTopL1 eleTrkExtrpYStereoTopL1 -40 40 -20 20")
	plots2D.append("posTrkExtrpXStereoTopL1 posTrkExtrpYStereoTopL1 -40 40 -20 20")
	plots2D.append("eleTrkExtrpXAxialBotL1 eleTrkExtrpYAxialBotL1 -40 40 -20 20")
	plots2D.append("posTrkExtrpXAxialBotL1 posTrkExtrpYAxialBotL1 -40 40 -20 20")
	plots2D.append("eleTrkExtrpXStereoBotL1 eleTrkExtrpYStereoBotL1 -40 40 -20 20")
	plots2D.append("posTrkExtrpXStereoBotL1 posTrkExtrpYStereoBotL1 -40 40 -20 20")
	plots2D.append("eleTrkExtrpXSensorAxialTopL1 eleTrkExtrpYSensorAxialTopL1 -30 30 -30 30")
	plots2D.append("posTrkExtrpXSensorAxialTopL1 posTrkExtrpYSensorAxialTopL1 -30 30 -30 30")
	plots2D.append("eleTrkExtrpXSensorStereoTopL1 eleTrkExtrpYSensorStereoTopL1 -30 30 -30 30")
	plots2D.append("posTrkExtrpXSensorStereoTopL1 posTrkExtrpYSensorStereoTopL1 -30 30 -30 30")
	plots2D.append("eleTrkExtrpXSensorAxialBotL1 eleTrkExtrpYSensorAxialBotL1 -30 30 -30 30")
	plots2D.append("posTrkExtrpXSensorAxialBotL1 posTrkExtrpYSensorAxialBotL1 -30 30 -30 30")
	plots2D.append("eleTrkExtrpXSensorStereoBotL1 eleTrkExtrpYSensorStereoBotL1 -30 30 -30 30")
	plots2D.append("posTrkExtrpXSensorStereoBotL1 posTrkExtrpYSensorStereoBotL1 -30 30 -30 30")
	plots2D.append("eleFirstHitX eleFirstHitY -40 40 -20 20")
	plots2D.append("posFirstHitX posFirstHitY -40 40 -20 20")
	plots2D.append("uncTargProjX-{0} uncTargProjY-{1} -4 4 -2 2".format(beamX,beamY))
	plots2D.append("(uncTargProjX-{0})/uncTargProjXErr (uncTargProjY-{1})/(sqrt(uncCovYY)+sqrt(uncCovZZ)*uncPY/uncPZ+(uncVZ-{0})*(uncMomYErr/uncPZ+uncPY*uncMomZErr/uncPZ**2)) -10 10 -10 10".format(beamX,beamY))
	plots2D.append("(uncVX-{0})/sqrt(uncCovXX) (uncVY-{1})/sqrt(uncCovYY) -10 10 -10 10".format(beamX,beamY))
	plots2D.append("eleClE eleTrkEcalY 0 {0} -100 100".format(1.6*energy))
	plots2D.append("posClE posTrkEcalY 0 {0} -100 100".format(1.6*energy))
	plots2D.append("eleClE/eleP eleTrkEcalY 0 2 -100 100")
	plots2D.append("posClE/posP posTrkEcalY 0 2 -100 100")

fitGaus = []
fitGaus.append("uncVZ {0} {1}".format(minVZ,maxVZ))
fitGaus.append("uncVY -1 1")
fitGaus.append("uncVX -3 3")

openPDF(outfile,c)

for i in range(len(plots)):
	plot = getPlot(plots[i])
	minX = getMinX(plots[i])
	maxX = getMaxX(plots[i])
	saveTuplePlot(events,plot,nBins,minX,maxX,outfile,c,plot,"",plot,nentries)
	if(plot2D): saveTuplePlot2D(events,"uncVZ",plot,nBins,minVZ,maxVZ,nBins,minX,maxX,outfile,c,"uncVZ",plot,plot+" vs uncVZ",nentries)

for i in range(len(plots2D)):
	plot1 = getPlot(plots2D[i])
	plot2 = getPlot2D(plots2D[i])
	minX = getMinX2D(plots2D[i])
	maxX = getMaxX2D(plots2D[i])
	minY = getMinY(plots2D[i])
	maxY = getMaxY(plots2D[i])
	saveTuplePlot2D(events,plot1,plot2,nBins,minX,maxX,nBins,minY,maxY,outfile,c,plot1,plot2,plot2+" vs "+plot1,nentries)

gStyle.SetOptFit()

for i in range(len(fitGaus)):
	plot = getPlot(fitGaus[i])
	minX = getMinX(fitGaus[i])
	maxX = getMaxX(fitGaus[i])
	saveFitPlot(events,plot,nBins,minX,maxX,outfile,c,plot,"",plot,nentries)

closePDF(outfile,c)

rootfile.Close()