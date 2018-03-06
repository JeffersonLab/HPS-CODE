import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F, TF1, TH1
from ROOT import RooDataSet, RooRealVar, RooArgSet, RooFormulaVar, RooWorkspace, RooAbsData, RooFit, RooAbsReal, RooArgList, RooDataHist, RooHistPdf, RooLandau, RooGaussian, RooNumConvPdf
sys.argv = tmpargv

isL0 = False

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input file name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-l: is L0 detectors'
    print '\t-h: this help message'
    print

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hl')

# Parse the command line arguments
for opt, arg in options:
		if opt=='l':
			isL0 = True
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

outfile = remainder[0]
infile = TFile(remainder[1])

def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

def getHisto(histoTitle,infile):
	histo = infile.Get(histoTitle)
	return histo

def drawHisto(histo,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	histo.Draw("")
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)
	histo.Write(plotTitle)

def saveHisto(histo,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	drawHisto(histo,XaxisTitle,YaxisTitle,plotTitle,stats)
	canvas.Print(outfile+".pdf")

def saveGaussHisto(histo,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	fit = TF1("fit","gaus")
	histo.Fit("fit")
	drawHisto(histo,XaxisTitle,YaxisTitle,plotTitle,stats)
	canvas.Print(outfile+".pdf")
	sigma = []
	sigma.append(fit.GetParameter(2))
	sigma.append(fit.GetParError(2))
	return sigma

def saveLandauHisto(histo,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	fit = TF1("fit","landau")
	histo.Fit("fit")
	drawHisto(histo,XaxisTitle,YaxisTitle,plotTitle,stats)
	canvas.Print(outfile+".pdf")
	peak = []
	peak.append(fit.GetParameter(1))
	peak.append(fit.GetParError(1))
	return peak

def saveLandauHistoSignalToNoise(histo,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	signal_to_noise = RooRealVar("signal_to_noise", "Signal to Noise", 0, 50)
	landau_data = RooDataHist("landau_data", "landau_data", RooArgList(signal_to_noise), histo)

	ml = RooRealVar("ml","mean landau",25, 20, 26)
	sl = RooRealVar("sl","sigma landau", 5, 2, 10)
	landau = RooLandau("lx","lx",signal_to_noise,ml,sl)
  
	mg = RooRealVar("mg","mg",0) ;
	sg = RooRealVar("sg","sg", 2, 1, 8)
	gauss = RooGaussian("gauss","gauss",signal_to_noise,mg,sg)

	lxg = RooNumConvPdf("lxg", "lxg", signal_to_noise, landau, gauss)

	result = lxg.fitTo(landau_data)

	frame = signal_to_noise.frame()
	landau_data.plotOn(frame)

	lxg.plotOn(frame)

	frame.Draw("")
	frame.SetTitle(plotTitle)
	frame.GetXaxis().SetTitle(XaxisTitle)
	frame.GetYaxis().SetTitle(YaxisTitle)
	frame.SetStats(stats)
	frame.Write(plotTitle)

	canvas.Print(outfile+".pdf")

	peak = []
	
	#if(result is not None):
	#	mean = RooRealVar(result.floatParsFinal().find("landau_mean"))
	#	err = RooRealVar(mean.errorVar())
	#	peak.append(mean.GetVal())
	#	peak.append(err.GetVal())
	#else:
	#	peak.append(0)
	#	peak.append(0)
	peak.append(0)
	peak.append(0)
	return peak

def saveLandauHistoAmplitude(histo,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	amplitude = RooRealVar("amplitude", "Cluster Amplitude", 0, 5000)
	landau_data = RooDataHist("landau_data", "landau_data", RooArgList(amplitude), histo)

	ml = RooRealVar("ml","mean landau",1500., 1000, 2000)
	sl = RooRealVar("sl","sigma landau", 250, 100, 1000)
	landau = RooLandau("lx","lx",amplitude,ml,sl)
  
	mg = RooRealVar("mg","mg",0) ;
	sg = RooRealVar("sg","sg", 100, 20, 500)
	gauss = RooGaussian("gauss","gauss",amplitude,mg,sg)

	lxg = RooNumConvPdf("lxg", "lxg", amplitude, landau, gauss)

	result = lxg.fitTo(landau_data)

	print "Data is Fit!"

	frame = amplitude.frame()
	landau_data.plotOn(frame)

	lxg.plotOn(frame)

	frame.Draw("")
	frame.SetTitle(plotTitle)
	frame.GetXaxis().SetTitle(XaxisTitle)
	frame.GetYaxis().SetTitle(YaxisTitle)
	frame.SetStats(stats)
	frame.Write(plotTitle)

	canvas.Print(outfile+".pdf")

	peak = []
	
	#if(result is not None):
	#	mean = RooRealVar(result.floatParsFinal().find("landau_mean"))
	#	err = RooRealVar(mean.errorVar())
	#	peak.append(mean.GetVal())
	#	peak.append(err.GetVal())
	#else:
	#	peak.append(0)
	#	peak.append(0)
	peak.append(0)
	peak.append(0)
	return peak

def buildSensorArray(isL0):
	sensors = []
	if(not isL0):
		sensors.append("module_L1b_halfmodule_axial_sensor0")
		sensors.append("module_L1b_halfmodule_stereo_sensor0")
		sensors.append("module_L1t_halfmodule_axial_sensor0")
		sensors.append("module_L1t_halfmodule_stereo_sensor0")
		sensors.append("module_L2b_halfmodule_axial_sensor0")
		sensors.append("module_L2b_halfmodule_stereo_sensor0")
		sensors.append("module_L2t_halfmodule_axial_sensor0")
		sensors.append("module_L2t_halfmodule_stereo_sensor0")
		sensors.append("module_L3b_halfmodule_axial_sensor0")
		sensors.append("module_L3b_halfmodule_stereo_sensor0")
		sensors.append("module_L3t_halfmodule_axial_sensor0")
		sensors.append("module_L3t_halfmodule_stereo_sensor0")
		sensors.append("module_L4b_halfmodule_axial_hole_sensor0")
		sensors.append("module_L4b_halfmodule_axial_slot_sensor0")
		sensors.append("module_L4b_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L4b_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L4t_halfmodule_axial_hole_sensor0")
		sensors.append("module_L4t_halfmodule_axial_slot_sensor0")
		sensors.append("module_L4t_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L4t_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L5b_halfmodule_axial_hole_sensor0")
		sensors.append("module_L5b_halfmodule_axial_slot_sensor0")
		sensors.append("module_L5b_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L5b_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L5t_halfmodule_axial_hole_sensor0")
		sensors.append("module_L5t_halfmodule_axial_slot_sensor0")
		sensors.append("module_L5t_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L5t_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L6b_halfmodule_axial_hole_sensor0")
		sensors.append("module_L6b_halfmodule_axial_slot_sensor0")
		sensors.append("module_L6b_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L6b_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L6t_halfmodule_axial_hole_sensor0")
		sensors.append("module_L6t_halfmodule_axial_slot_sensor0")
		sensors.append("module_L6t_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L6t_halfmodule_stereo_slot_sensor0")

	else:
		sensors.append("module_L1b_halfmodule_axial_hole_sensor0")
		sensors.append("module_L1b_halfmodule_axial_slot_sensor0")
		sensors.append("module_L1b_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L1b_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L1t_halfmodule_axial_hole_sensor0")
		sensors.append("module_L1t_halfmodule_axial_slot_sensor0")
		sensors.append("module_L1t_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L1t_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L2b_halfmodule_axial_sensor0")
		sensors.append("module_L2b_halfmodule_stereo_sensor0")
		sensors.append("module_L2t_halfmodule_axial_sensor0")
		sensors.append("module_L2t_halfmodule_stereo_sensor0")
		sensors.append("module_L3b_halfmodule_axial_sensor0")
		sensors.append("module_L3b_halfmodule_stereo_sensor0")
		sensors.append("module_L3t_halfmodule_axial_sensor0")
		sensors.append("module_L3t_halfmodule_stereo_sensor0")
		sensors.append("module_L4b_halfmodule_axial_sensor0")
		sensors.append("module_L4b_halfmodule_stereo_sensor0")
		sensors.append("module_L4t_halfmodule_axial_sensor0")
		sensors.append("module_L4t_halfmodule_stereo_sensor0")
		sensors.append("module_L5b_halfmodule_axial_hole_sensor0")
		sensors.append("module_L5b_halfmodule_axial_slot_sensor0")
		sensors.append("module_L5b_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L5b_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L5t_halfmodule_axial_hole_sensor0")
		sensors.append("module_L5t_halfmodule_axial_slot_sensor0")
		sensors.append("module_L5t_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L5t_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L6b_halfmodule_axial_hole_sensor0")
		sensors.append("module_L6b_halfmodule_axial_slot_sensor0")
		sensors.append("module_L6b_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L6b_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L6t_halfmodule_axial_hole_sensor0")
		sensors.append("module_L6t_halfmodule_axial_slot_sensor0")
		sensors.append("module_L6t_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L6t_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L7b_halfmodule_axial_hole_sensor0")
		sensors.append("module_L7b_halfmodule_axial_slot_sensor0")
		sensors.append("module_L7b_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L7b_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L7t_halfmodule_axial_hole_sensor0")
		sensors.append("module_L7t_halfmodule_axial_slot_sensor0")
		sensors.append("module_L7t_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L7t_halfmodule_stereo_slot_sensor0")
	return sensors

def processLandauPlot(landau, lm_val, le_val):
    return 0

def plotLandauGaussSignalToNoise(infile,outfile,histoname,canvas):
	outhistoTitle = histoname + " Fitted Peak"
	histo = TH1F(outhistoTitle,outhistoTitle,len(sensors),0,len(sensors))
	for i in range(len(sensors)):
		histoTitle = sensors[i] + " - " + histoname
		inhisto = getHisto(histoTitle,infile)
		peak = saveLandauHisto(inhisto,outfile,canvas,"Signal To Noise [ADC Counts]","",sensors[i] + " Fitted Signal To Noise (hits on clean track)",1)
		#peak = saveLandauHistoSignalToNoise(inhisto,outfile,canvas,"Signal To Noise [ADC Counts]","",sensors[i] + " Fitted Signal To Noise (hits on clean track)",1)
		histo.SetBinContent(i+1,peak[0])
		histo.SetBinError(i+1,peak[1])
	saveHisto(histo,outfile,canvas,"Sensor Number","Signal To Noise MPV [ADC Counts]","Fitted Signal To Noise MPV (hits on clean track)")
	del histo

def plotLandauGaussAmplitude(infile,outfile,histoname,canvas):
	outhistoTitle = histoname + " Fitted Peak"
	histo = TH1F(outhistoTitle,outhistoTitle,len(sensors),0,len(sensors))
	for i in range(len(sensors)):
		histoTitle = sensors[i] + " - " + histoname
		inhisto = getHisto(histoTitle,infile)
		peak = saveLandauHistoAmplitude(inhisto,outfile,canvas,"Cluster Amplitude [ADC Counts]","",sensors[i] + " Fitted Cluster Amplitude (hits on clean track)",1)
		peak = saveLandauHisto(inhisto,outfile,canvas,"Cluster Amplitude [ADC Counts]","",sensors[i] + " Fitted Cluster Amplitude (hits on clean track)",1)
		histo.SetBinContent(i+1,peak[0])
		histo.SetBinError(i+1,peak[1])
	saveHisto(histo,outfile,canvas,"Sensor Number","Cluster Amplitude MPV [ADC Counts]","Fitted Cluster Amplitude MPV (hits on clean track)")
	del histo

def plotGauss(infile,outfile,histoname,canvas):
	outhistoTitle = histoname + " Fitted Sigma"
	histo = TH1F(outhistoTitle,outhistoTitle,len(sensors),0,len(sensors))
	for i in range(len(sensors)):
		histoTitle = sensors[i] + " - " + histoname
		inhisto = getHisto(histoTitle,infile)
		sigma = saveGaussHisto(inhisto,outfile,canvas,"Hit Time [ns]","",sensors[i] + " Fitted Hit Time (hits on clean track)",1)
		histo.SetBinContent(i+1,sigma[0])
		histo.SetBinError(i+1,sigma[1])
	saveHisto(histo,outfile,canvas,"Sensor Number","Hit Time Sigma [ns]","Fitted Hit Time Sigma (hits on clean track)")
	del histo

SigToNoiseHistoName = "Track Signal to Noise"
ClusterAmpHistoName = "Tracker Cluster Charge"
#SigToNoiseHistoName = "Multiple Hit Signal to Noise"
#ClusterAmpHistoName = "Multiple Hit Cluster Charge"
HitTimeHistoName = "Track Single Hit Cluster Time"
sensors = buildSensorArray(isL0)
rootfile = TFile(outfile+".root","recreate")

outfile_sigtonoise = outfile+"_sigtonoise"
openPDF(outfile_sigtonoise ,c)
plotLandauGaussSignalToNoise(infile,outfile_sigtonoise,SigToNoiseHistoName,c)
closePDF(outfile_sigtonoise,c)

outfile_amplitude = outfile+"_clusteramplitude"
openPDF(outfile_amplitude ,c)
plotLandauGaussAmplitude(infile,outfile_amplitude,ClusterAmpHistoName,c)
closePDF(outfile_amplitude,c)

outfile_hittime = outfile+"_hittime"
openPDF(outfile_hittime,c)
plotGauss(infile,outfile_hittime,HitTimeHistoName,c)
closePDF(outfile_hittime,c)

rootfile.Close()
