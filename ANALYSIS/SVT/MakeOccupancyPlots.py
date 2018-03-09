import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F, TF1, TH1
sys.argv = tmpargv

#author Matt Solt mrsolt@slac.stanford.edu
#This script makes plots for SVT NIM paper from org.hps.svt.OccupancyPlots driver 

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input file name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-l: is L0 detectors'
    print '\t-n: Number of strips away from edge (default 0)'
    print '\t-s: Is this a calibration file (default false)'
    print '\t-h: this help message'
    print

#default parameters
isL0 = False
nEdge = 0
isCalibration = False

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'ln:hs')

# Parse the command line arguments
for opt, arg in options:
	if opt=='-l':
		isL0 = True
	if opt=='-n':
		nEdge = int(arg)
	if opt=='-s':
		isCalibration = True
	if opt=='-h':
		print_usage()
		sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

#input/output files
outfile = remainder[0]
infile = TFile(remainder[1])

#open PDF
def openPDF(outfile,canvas):
	c.Print(outfile+".pdf[")

#close PDF
def closePDF(outfile,canvas):
	c.Print(outfile+".pdf]")

#get histogram
def getHisto(histoTitle,infile):
	histo = infile.Get(histoTitle)
	return histo

#get edge channel of interest
def getEdge(inhisto,nEdge):
	chan = nEdge + 1
	edge = 0
	if "stereo" in inhisto.GetTitle():
		edge = inhisto.GetSize() - 2
		chan = edge - nEdge
	return inhisto.GetBinContent(chan)

#Draw histogram
def drawHisto(histo,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	histo.Draw("")
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)
	histo.Write(plotTitle)

#Save histogram
def saveHisto(histo,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	drawHisto(histo,XaxisTitle,YaxisTitle,plotTitle,stats)
	canvas.Print(outfile+".pdf")

#Build sensor array
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

#Plot occupancies
def plot(infile,outfile,sensors,histoname,nEdge,canvas,isCalibration=False):
	outhistoTitleEdge = histoname + " Edge"
	histoEdge = TH1F(outhistoTitleEdge,outhistoTitleEdge,len(sensors),0,len(sensors))
	outhistoTitleMax = histoname + " Maximum"
	histoMax = TH1F(outhistoTitleMax,outhistoTitleMax,len(sensors),0,len(sensors))
	for i in range(len(sensors)):
		histoTitle = sensors[i] + " - " + histoname
		inhisto = getHisto(histoTitle,infile)
		saveHisto(inhisto,outfile,canvas,"","",histoTitle)
		histoEdge.SetBinContent(i+1,getEdge(inhisto,nEdge))
		histoMax.SetBinContent(i+1,inhisto.GetMaximum())
	if(not isCalibration):
		saveHisto(histoEdge,outfile,canvas,"Sensor Number","",outhistoTitleEdge)
	saveHisto(histoMax,outfile,canvas,"Sensor Number","",outhistoTitleMax)
	del histoEdge
	del histoMax

#Grab histogram names
StripOccupancyHistoName = "Occupancy"
ClusterOccupancyHistoName = "Cluster Occupancy"
sensors = buildSensorArray(isL0)
rootfile = TFile(outfile+".root","recreate")

#Plot strip occupancy plots
outfile_strip = outfile+"_stripoccupancy"
openPDF(outfile_strip ,c)
plot(infile,outfile_strip,sensors,StripOccupancyHistoName,nEdge,c,isCalibration)
closePDF(outfile_strip,c)

#Plot cluster occupancy plots if the file is not a calibration file
if(not isCalibration):
	outfile_cluster = outfile+"_clusteroccupancy"
	openPDF(outfile_cluster ,c)
	plot(infile,outfile_cluster,sensors,ClusterOccupancyHistoName,nEdge,c)
	closePDF(outfile_cluster,c)

rootfile.Close()