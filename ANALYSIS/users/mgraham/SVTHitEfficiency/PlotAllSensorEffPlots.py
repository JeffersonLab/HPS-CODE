import sys
import re
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F

#  originally written by Matt Solt for 2015 SVT hit efficiency; 
#  modified by Matt Graham 5/2019 to add MC/Data Ratio Plots & getting efficiency
#  from TGraphAsymErrors of the track distributions (allows us to add histograms)

sys.argv = tmpargv
ROOT.gROOT.SetBatch(True) 
isL0 = False

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input file name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-l: if file uses L0 detector'
    print '\t-h: this help message'
    print

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hl')

print(options)
print(remainder)
# Parse the command line arguments
for opt, arg in options:
		if opt=='l':
			isL0 = True
		if opt=='-h':
			print_usage()
			sys.exit(0)


outfile = remainder[0]
print(outfile)
infile = TFile(remainder[1])
infile.Print()

#mcfile=TFile("SVTEfficiencyData/tritrig-WB_HPS-PhysicsRun2016-Pass2-svt-efficiency-no-killing-all.root")
#mcfile=TFile("OutputHistograms/MC/tritrig-beam_2500kBunches_pass4_v4_5_0_svt_efficiency_allow_missed_sensor.root")
mcfile=TFile("OutputHistograms/MC/tritrig-beam_2500kBunches_pass4_v4_5_0_svt_efficiency_allow_missed_sensor_5sigma_weighted_ratios_rereco.root")
#mcfile=TFile("OutputHistograms/MC/tritrig-beam_2500kBunches_pass4_v4_5_0_svt_efficiency_allow_missed_sensor_5sigma_weighted_ratios_scalekilling_2pt0.root")
#mcfile=TFile("OutputHistograms/MC/tritrig-beam_2500kBunches_pass4_v4_5_0_svt_efficiency_allow_missed_sensor_5sigma_weighted_ratios_scalekilling_First3pt0_Second2pt0.root")

#mcfile=TFile("SVTEfficiencyData/tritrig-WB_HPS-PhysicsRun2016-Pass2-svt-efficiency-cluster-killing-allow-missed-sensor-all.root")
#mcfile=TFile("SVTEfficiencyData/tritrig-WB_HPS-PhysicsRun2016-Pass2-svt-efficiency-cluster-killing-5-sigma-L1b-axial-all.root")
#mcfile=TFile("SVTEfficiencyData/tritrig-WB_HPS-PhysicsRun2016-Pass2-svt-efficiency-cluster-killing-5-sigma-L1-L6-all.root")
#mcfile=TFile("SVTEfficiencyData/tritrig-WB_HPS-PhysicsRun2016-Pass2-svt-efficiency-cluster-killing-5-sigma-L1-L6-all.root")
#mcfile=TFile("SVTEfficiencyData/tritrig-WB_HPS-PhysicsRun2016-Pass2-svt-efficiency-cluster-killing-5-sigma-L1t-axial-all.root")
#mcfile=TFile("SVTEfficiencyData/tritrig-WB_HPS-PhysicsRun2016-Pass2-svt-efficiency-cluster-killing-weighted-ratios-all.root")
#mcfile=TFile("SVTEfficiencyData/tritrig-WB_HPS-PhysicsRun2016-Pass2-svt-efficiency-cluster-killing-weighted-ratios-all.root")
writeRatioFiles=False
#writeRatioFiles=True

def openPDF(outfile,canvas):
	canvas.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	canvas.Print(outfile+".pdf]")

def getHisto(histoTitle,infile):
	histo = infile.Get(histoTitle)
	return histo

def drawHisto(histo,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	histo.Draw("COLZ")
	if(plotTitle == ""): histo.SetTitle(histo.GetTitle())
	else: histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)

def drawTGraph(histo,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	histo.Draw("AP")
	if(plotTitle == ""): histo.SetTitle(histo.GetTitle())
	else: histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
        histo.GetYaxis().SetRangeUser(0.8,1.01)
#	histo.SetStats(stats)

def drawTGraphWithMC(histo,histomc,histomcTot,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
    default=-666
    minX=default
    maxX=default
    mintrks=10
    maxtrksCutOff=2
    for i in range(0,histomcTot.GetNbinsX()-1): 
        mcTot=histomcTot.GetBinContent(i)
        binXLo=histomcTot.GetBinLowEdge(i)
        binXHi=histomcTot.GetBinLowEdge(i)+histomcTot.GetBinWidth(i)
        if minX==default and mcTot>mintrks: 
            minX=binXLo
        if minX!=default and maxX==default and mcTot<maxtrksCutOff: 
            maxX=binXHi
    
    histo.Draw("AP")
    histomc.SetLineColor(2)
    histomc.Draw("][samese")
    print("xmin, xmax before fixing "+str(minX)+' '+str(maxX))
    if(plotTitle == ""): histo.SetTitle(histo.GetTitle())
    else: histo.SetTitle(plotTitle)
    histo.GetXaxis().SetTitle(XaxisTitle)
    histo.GetYaxis().SetTitle(YaxisTitle)
    histo.GetYaxis().SetRangeUser(0.8,1.01)
#    histo.GetYaxis().SetRangeUser(0.0,1.01)
    if minX==default: 
        print("Fixing minX:  new minX = "+str(minX))
        minX=histomcTot.GetXaxis().GetXmin()
    if minX!=default and maxX==default: 
        maxX=histomcTot.GetXaxis().GetXmax()
        print("Fixing maxX:  new maxX  = "+str(maxX))
    if maxX>minX: 
        print("xmin, xmax after fixing "+str(minX)+' '+str(maxX))
        histo.GetXaxis().SetLimits(minX,maxX)
        histomc.GetXaxis().SetLimits(minX,maxX)
    histo.Draw("AP")  ### draw it again to pick up new TAxis...weird!
    histomc.Draw("][samese")
#	histo.SetStats(stats)

#draw the ratio of efficiencies
def drawRatioGraph(histoHit,histoTot,histomcHit,histomcTot,ratio,line,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):

    #use these to adjust X-range
    default=-666
    minX=default
    maxX=default
    mintrks=10
    maxtrksCutOff=2
    for i in range(0,histomcTot.GetNbinsX()): 
        mcTot=histomcTot.GetBinContent(i)
        dataTot=histoTot.GetBinContent(i)
        mcHit=histomcHit.GetBinContent(i)
        dataHit=histoHit.GetBinContent(i)
        binXLo=histomcTot.GetBinLowEdge(i)
        binXHi=histomcTot.GetBinLowEdge(i)+histomcTot.GetBinWidth(i)
        if minX==default and mcTot>mintrks: 
            minX=binXLo
        if minX!=default and maxX==default and mcTot<maxtrksCutOff: 
            maxX=binXHi
        if dataTot>0 and mcTot>0 and mcHit>0:
            dataEff=dataHit/dataTot
            mcEff=mcHit/mcTot
#            print("filling " + str(dataEff)+" " +str(mcEff))
            r=dataEff/mcEff
            print(str(r))
            ratio.SetBinContent(i,r)
    ratio.Draw("histo")
    ratio.Print("V")    
    if(plotTitle == ""): ratio.SetTitle(ratio.GetTitle())
    else: ratio.SetTitle(plotTitle)
    ratio.GetXaxis().SetTitle(XaxisTitle)
    ratio.GetYaxis().SetTitle(YaxisTitle)
    ratio.GetYaxis().SetRangeUser(0.9,1.1)
#    ratio.GetYaxis().SetRangeUser(0.0,1.1)
    if minX==default: 
        print("Fixing minX:  new minX = "+str(minX))
        minX=histomcTot.GetXaxis().GetXmin()
    if minX!=default and maxX==default: 
        maxX=histomcTot.GetXaxis().GetXmax()
        print("Fixing maxX:  new maxX  = "+str(maxX))
    if maxX>minX: 
        print("xmin, xmax after fixing "+str(minX)+' '+str(maxX))
        ratio.GetXaxis().SetRangeUser(minX,maxX)
    line.SetX1(minX)
    line.SetX2(maxX)
    line.SetLineColor(2)
    line.SetLineWidth(3)
    line.Draw() 
    ratio.SetStats(stats)
    # parse the plotTitle to get the layer, top/bottom/axial/stereo/slot/hole
    # only look at the vs Channel data
    if not "Channel" in plotTitle: 
        return
    axSt="stereo"
    holeSlot="hole"
    topBot="foobar"
    layer=-1
    print(plotTitle)
    if "axial" in plotTitle:
        axSt="axial"
    if "slot" in plotTitle:
        holeSlot="slot"
    if re.search("\_L\d\w\_",plotTitle):
        print("getting layer and top/bottom")
        layerSide=re.search("\_L(\d)(\w)\_",plotTitle)
        print(layerSide.group(0))
        print(layerSide.group(1))
        layer=int(layerSide.group(1))
        topBot=layerSide.group(2)
    print("Layer="+str(layer)+"; topBot="+topBot+"; axSt="+axSt+"; holeSlot="+holeSlot)
    dumpRatios=False
    if layer==1 and "Ele" in plotTitle: 
        print("Found layer 1 Ele plots!")
        dumpRatios=True
    elif layer==6 and not "Ele" in plotTitle and not "Pos" in plotTitle:
        print("Found layer 6 All charges plots!")
        dumpRatios=True

    if not dumpRatios: 
        return
    if writeRatioFiles:
        outputFileName="RatioFiles/pass4b-hps2016_L"+str(layer)+topBot+"_"+axSt+"_"+holeSlot+".txt"
        outputFile=open(outputFileName,"w")
        minTracks=2
        for i in range(0,ratio.GetNbinsX()):
            mcTot=histomcTot.GetBinContent(i)
            dataTot=histoTot.GetBinContent(i)
            if dataTot>minTracks and mcTot>minTracks: 
                print(ratio.GetBinContent(i))
                outputFile.write(str(i)+"  "+str(ratio.GetBinContent(i))+"\n")
        outputFile.close()

def saveHisto(histo,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	drawHisto(histo,XaxisTitle,YaxisTitle,plotTitle,stats)
	canvas.Print(outfile+".pdf")

def saveTGraph(histo,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	drawTGraph(histo,XaxisTitle,YaxisTitle,plotTitle,stats)
	canvas.Print(outfile+".pdf")

def saveTGraphWithMC(histo,histomc,histomcTot,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	drawTGraphWithMC(histo,histomc,histomcTot,XaxisTitle,YaxisTitle,plotTitle,stats)
	canvas.Print(outfile+".pdf")


def saveRatioGraph(histoHit,histoTot,histomcHit,histomcTot,ratio,line,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	drawRatioGraph(histoHit,histoTot,histomcHit,histomcTot,ratio,line,XaxisTitle,YaxisTitle,plotTitle,stats)
	canvas.Print(outfile+".pdf")

def Plot(var,sensors,infile,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	openPDF(outfile,canvas)
	for i in range(len(sensors)):
		saveHisto(getHisto("{0} {1}".format(var,sensors[i]),infile),outfile,canvas,XaxisTitle,YaxisTitle,plotTitle,stats)
	closePDF(outfile,canvas)

def Fit(var,sensors,infile,outfile,canvas,top,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	ex = "Null Fit"
	volume = "Top"
	if(not top): volume = "Bottom"
	histoMean = TH1F("histoMean","histoMean",len(sensors),0,len(sensors))
	histoSigma = TH1F("histoSigma","histoSigma",len(sensors),0,len(sensors))
	openPDF(outfile,canvas)
	for i in range(len(sensors)):
		histo = getHisto("{0} {1}".format(var,sensors[i]),infile)
		histoFit = histo.Fit("gaus","S")
		saveHisto(histo,outfile,canvas,XaxisTitle,YaxisTitle,plotTitle,stats)
		mean = 0
		meanErr = 0
		sigma = 0
		sigmaErr = 0
		try:
			mean = histoFit.Parameter(1)
			meanErr = histoFit.ParError(1)
			sigma = histoFit.Parameter(2)
			sigmaErr = histoFit.ParError(2)
		except Exception as ex:
			print(ex)
		#for j in range(len(sensors)):
		histoMean.SetBinContent(i+1,mean)
		histoMean.SetBinError(i+1,meanErr)
		histoSigma.SetBinContent(i+1,sigma)
		histoSigma.SetBinError(i+1,sigmaErr)
		del histo
		del histoFit
	titleMean = plotTitle+" Mean "+volume
	titleSigma = plotTitle+" Sigma "+volume
	saveHisto(histoMean,outfile,canvas,"sensor ID","",titleMean)
	saveHisto(histoSigma,outfile,canvas,"sensor ID","",titleSigma)
	closePDF(outfile,canvas)
	del histoMean
	del histoSigma

def PlotVars(plotvars,sensors,infile,outfile,stats=0):
	c = TCanvas("c","c",800,600)
	for i in range(len(plotvars)):
		outputfile = outfile+"_"+plotvars[i]
		Plot("{0}".format(plotvars[i]),sensors,infile,outputfile,c,plotvars[i],"",plotvars[i],stats)	
	del c

def FitVars(fitvars,sensors,infile,outfile,top,stats=0):
	c = TCanvas("c","c",800,600)
	volume = "Top"
	if(not top): volume = "Bottom"
	for i in range(len(fitvars)):
		outputfile = outfile+"_"+fitvars[i]+"_fits_"+volume
		Fit("{0}".format(fitvars[i]),sensors,infile,outputfile,c,top,fitvars[i],"",fitvars[i],stats)	
	del c

def PlotEff(EffArr,sensors,infile,outfile,top,stats=0):
	c = TCanvas("c","c",800,600)
	volume = "Top"
	if(not top): volume = "Bottom"
	outputfile = outfile+"_"+"eff_"+volume
	openPDF(outputfile,c)	
	for i in range(len(EffArr)):
		histo = TH1F("{0} {1}".format(EffArr[i],volume),"{0} {1}".format(EffArr[i],volume),len(sensors),0,len(sensors))
		for j in range(len(sensors)):
			eff = getHisto("{0} {1}".format(EffArr[i],sensors[j]),infile)
			effErr = getHisto("{0} Error {1}".format(EffArr[i],sensors[j]),infile)
			histo.SetBinContent(j+1,eff.GetBinContent(1))
			histo.SetBinError(j+1,effErr.GetBinContent(1))
		saveHisto(histo,outputfile,c,"sensor ID","","{0} {1}".format(EffArr[i],volume),stats)
		del histo
	closePDF(outputfile,c)	
	del c

def PlotTGraphEff(trkArr,sensors,infile,outfile,top,stats=0):
    c = TCanvas("c","c",800,600)
    volume = "Top"
    if(not top): volume = "Bottom"
    outputfile = outfile+"_"+"TGraph_eff_"+volume
    openPDF(outputfile,c)	
    preList=["Number of Tracks ","Number of Tracks With Hit "]
    for i in range(len(trkArr)):
        for j in range(len(sensors)):
            numHist=getHisto(preList[1]+trkArr[i]+sensors[j],infile)
            denomHist=getHisto(preList[0]+trkArr[i]+sensors[j],infile)
            numHistMC=getHisto(preList[1]+trkArr[i]+sensors[j],mcfile)
            denomHistMC=getHisto(preList[0]+trkArr[i]+sensors[j],mcfile)
            print("Making TGraph for "+preList[1]+trkArr[i]+sensors[j])
            numHist.Print("V")
            denomHist.Print("V")
            eff=ROOT.TGraphAsymmErrors()
            effMC=ROOT.TGraphAsymmErrors()
            histName="TGraph Efficiency "+trkArr[i]+sensors[j]
            print(histName)
            eff.SetName(histName)
            eff.Divide(numHist,denomHist)
            effMC.Divide(numHistMC,denomHistMC)
#            saveTGraph(eff,outputfile,c,trkArr[i],"","{0} {1}".format(trkArr[i]+sensors[j],volume),stats)
#            saveTGraphWithMC(eff,effMC,outputfile,c,trkArr[i],"","{0} {1}".format(trkArr[i]+sensors[j],volume),stats)
            saveTGraphWithMC(eff,effMC,denomHistMC,outputfile,c,trkArr[i],"","{0} {1}".format(trkArr[i]+sensors[j],volume),stats)
            #need to declare this here so it persists to saving
            nbins=denomHist.GetNbinsX()
            xmin=denomHist.GetXaxis().GetXmin()
            xmax=denomHist.GetXaxis().GetXmax()
            ratio=ROOT.TH1D("Data/MC Ratio","",nbins,xmin,xmax)
            line=ROOT.TLine(xmin,1,xmax,1)
            saveRatioGraph(numHist,denomHist,numHistMC,denomHistMC,ratio,line,outputfile,c,trkArr[i],"","Data/MC Ratio {0} {1}".format(trkArr[i]+sensors[j],volume),stats)
            del eff
            del effMC
            del ratio
            del line
    closePDF(outputfile,c)	
    del c

def FitVars2D(fitvars2D,sensors,infile,outfile,stats=0):
	c = TCanvas("c","c",800,600)
	for i in range(len(fitvars2D)):
		outputfile = outfile+"_"+fitvars2D[i]+"_fits_"
		Fit2D("{0}".format(fitvars[i]),sensors,infile,outputfile,c,top,fitvars2D[i],"",fitvars2D[i],stats)	
	del c

def Fit2D(var,sensors,infile,outfile,canvas,top,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	ex = "Null Fit"
	histoMean = TH1F("histoMean","histoMean",len(sensors),0,len(sensors))
	histoSigma = TH1F("histoSigma","histoSigma",len(sensors),0,len(sensors))
	openPDF(outfile,canvas)
	for i in range(len(sensors)):
		histo = getHisto("{0} {1}".format(var,sensors[i]),infile)
		histoFit = histo.Fit("gaus","S")
		saveHisto(histo,outfile,canvas,XaxisTitle,YaxisTitle,plotTitle,stats)
		mean = 0
		meanErr = 0
		sigma = 0
		sigmaErr = 0
		try:
			mean = histoFit.Parameter(1)
			meanErr = histoFit.ParError(1)
			sigma = histoFit.Parameter(2)
			sigmaErr = histoFit.ParError(2)
		except Exception as ex:
			print(ex)
		#for j in range(len(sensors)):
		histoMean.SetBinContent(i+1,mean)
		histoMean.SetBinError(i+1,meanErr)
		histoSigma.SetBinContent(i+1,sigma)
		histoSigma.SetBinError(i+1,sigmaErr)
		del histo
		del histoFit
	titleMean = plotTitle+" Mean "+volume
	titleSigma = plotTitle+" Sigma "+volume
	saveHisto(histoMean,outfile,canvas,"sensor ID","",titleMean)
	saveHisto(histoSigma,outfile,canvas,"sensor ID","",titleSigma)
	closePDF(outfile,canvas)
	del histoMean
	del histoSigma

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

def buildSensorArrayTop(isL0):
	sensors = []
	if(not isL0):
		sensors.append("module_L1t_halfmodule_axial_sensor0")
		sensors.append("module_L1t_halfmodule_stereo_sensor0")
		sensors.append("module_L2t_halfmodule_axial_sensor0")
		sensors.append("module_L2t_halfmodule_stereo_sensor0")
		sensors.append("module_L3t_halfmodule_axial_sensor0")
		sensors.append("module_L3t_halfmodule_stereo_sensor0")
		sensors.append("module_L4t_halfmodule_axial_hole_sensor0")
		sensors.append("module_L4t_halfmodule_axial_slot_sensor0")
		sensors.append("module_L4t_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L4t_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L5t_halfmodule_axial_hole_sensor0")
		sensors.append("module_L5t_halfmodule_axial_slot_sensor0")
		sensors.append("module_L5t_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L5t_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L6t_halfmodule_axial_hole_sensor0")
		sensors.append("module_L6t_halfmodule_axial_slot_sensor0")
		sensors.append("module_L6t_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L6t_halfmodule_stereo_slot_sensor0")

	else:
		sensors.append("module_L1t_halfmodule_axial_hole_sensor0")
		sensors.append("module_L1t_halfmodule_axial_slot_sensor0")
		sensors.append("module_L1t_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L1t_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L2t_halfmodule_axial_sensor0")
		sensors.append("module_L2t_halfmodule_stereo_sensor0")
		sensors.append("module_L3t_halfmodule_axial_sensor0")
		sensors.append("module_L3t_halfmodule_stereo_sensor0")
		sensors.append("module_L4t_halfmodule_axial_sensor0")
		sensors.append("module_L4t_halfmodule_stereo_sensor0")
		sensors.append("module_L5t_halfmodule_axial_hole_sensor0")
		sensors.append("module_L5t_halfmodule_axial_slot_sensor0")
		sensors.append("module_L5t_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L5t_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L6t_halfmodule_axial_hole_sensor0")
		sensors.append("module_L6t_halfmodule_axial_slot_sensor0")
		sensors.append("module_L6t_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L6t_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L7t_halfmodule_axial_hole_sensor0")
		sensors.append("module_L7t_halfmodule_axial_slot_sensor0")
		sensors.append("module_L7t_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L7t_halfmodule_stereo_slot_sensor0")
	return sensors

def buildSensorArrayBot(isL0):
	sensors = []
	if(not isL0):
		sensors.append("module_L1b_halfmodule_axial_sensor0")
		sensors.append("module_L1b_halfmodule_stereo_sensor0")
		sensors.append("module_L2b_halfmodule_axial_sensor0")
		sensors.append("module_L2b_halfmodule_stereo_sensor0")
		sensors.append("module_L3b_halfmodule_axial_sensor0")
		sensors.append("module_L3b_halfmodule_stereo_sensor0")
		sensors.append("module_L4b_halfmodule_axial_hole_sensor0")
		sensors.append("module_L4b_halfmodule_axial_slot_sensor0")
		sensors.append("module_L4b_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L4b_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L5b_halfmodule_axial_hole_sensor0")
		sensors.append("module_L5b_halfmodule_axial_slot_sensor0")
		sensors.append("module_L5b_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L5b_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L6b_halfmodule_axial_hole_sensor0")
		sensors.append("module_L6b_halfmodule_axial_slot_sensor0")
		sensors.append("module_L6b_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L6b_halfmodule_stereo_slot_sensor0")

	else:
		sensors.append("module_L1b_halfmodule_axial_hole_sensor0")
		sensors.append("module_L1b_halfmodule_axial_slot_sensor0")
		sensors.append("module_L1b_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L1b_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L2b_halfmodule_axial_sensor0")
		sensors.append("module_L2b_halfmodule_stereo_sensor0")
		sensors.append("module_L3b_halfmodule_axial_sensor0")
		sensors.append("module_L3b_halfmodule_stereo_sensor0")
		sensors.append("module_L4b_halfmodule_axial_sensor0")
		sensors.append("module_L4b_halfmodule_stereo_sensor0")
		sensors.append("module_L5b_halfmodule_axial_hole_sensor0")
		sensors.append("module_L5b_halfmodule_axial_slot_sensor0")
		sensors.append("module_L5b_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L5b_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L6b_halfmodule_axial_hole_sensor0")
		sensors.append("module_L6b_halfmodule_axial_slot_sensor0")
		sensors.append("module_L6b_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L6b_halfmodule_stereo_slot_sensor0")
		sensors.append("module_L7b_halfmodule_axial_hole_sensor0")
		sensors.append("module_L7b_halfmodule_axial_slot_sensor0")
		sensors.append("module_L7b_halfmodule_stereo_hole_sensor0")
		sensors.append("module_L7b_halfmodule_stereo_slot_sensor0")
	return sensors

def buildVariableArray():
	plotvars = []
	plotvars.append("D0 Error")
	plotvars.append("Z0 Error")
	plotvars.append("Omega Error")
	plotvars.append("TanLambda Error")
	plotvars.append("Phi0 Error")
	plotvars.append("Error U")
	plotvars.append("Error U Electron")
	plotvars.append("Error U Positron")
	plotvars.append("Error U vs V")
	plotvars.append("Error U vs V Electron")
	plotvars.append("Error U vs V Positron")
	plotvars.append("Error U vs U")
	plotvars.append("Error U vs U Electron")
	plotvars.append("Error U vs U Positron")
	plotvars.append("Residual U")
	plotvars.append("Residual U Electron")
	plotvars.append("Residual U Positron")
	plotvars.append("Residual U vs V")
	plotvars.append("Residual U vs V Electron")
	plotvars.append("Residual U vs V Positron")
	plotvars.append("Residual U vs U")
	plotvars.append("Residual U vs U Electron")
	plotvars.append("Residual U vs U Positron")
	plotvars.append("U Pulls")
	plotvars.append("U Pulls Electron")
	plotvars.append("U Pulls Positron")
	plotvars.append("U Pulls vs V")
	plotvars.append("U Pulls vs V Electron")
	plotvars.append("U Pulls vs V Positron")
	plotvars.append("U Pulls vs U")
	plotvars.append("U Pulls vs U Electron")
	plotvars.append("U Pulls vs U Positron")
	plotvars.append("HitEfficiency Channel Corrected")
	plotvars.append("HitEfficiency Channel Corrected Ele")
	plotvars.append("HitEfficiency Channel Corrected Pos")
	plotvars.append("HitEfficiency P Corrected")
	plotvars.append("HitEfficiency P Corrected Ele")
	plotvars.append("HitEfficiency P Corrected Pos")
	plotvars.append("HitEfficiency Y Corrected")
	plotvars.append("HitEfficiency Y Corrected Ele")
	plotvars.append("HitEfficiency Y Corrected Pos")
	plotvars.append("HitEfficiency Channel")
	plotvars.append("HitEfficiency Channel Ele")
	plotvars.append("HitEfficiency Channel Pos")
	plotvars.append("HitEfficiency P")
	plotvars.append("HitEfficiency P Ele")
	plotvars.append("HitEfficiency P Pos")
	plotvars.append("HitEfficiency Y")
	plotvars.append("HitEfficiency Y Ele")
	plotvars.append("HitEfficiency Y Pos")
	return plotvars

def buildTracksArray():
    varList=["Channel","Y","P"]
    partList=["","Ele ","Pos "]
    trackvars=[]
    for var in varList:
        for part in partList:
            trackvars.append(var+" "+part)
    return trackvars

def buildFitArray():
	fitvars = []
	fitvars.append("Residual U")
	fitvars.append("Residual U Electron")
	fitvars.append("Residual U Positron")
	fitvars.append("U Pulls")
	fitvars.append("U Pulls Electron")
	fitvars.append("U Pulls Positron")
	return fitvars

def buildFit2DArray():
	fitvars2D = []
	fitvars2D.append("Residual U vs V")
	fitvars2D.append("Residual U vs V Electron")
	fitvars2D.append("Residual U vs V Positron")
	fitvars2D.append("Residual U vs U")
	fitvars2D.append("Residual U vs U Electron")
	fitvars2D.append("Residual U vs U Positron")
	fitvars2D.append("U Pulls vs V Electron")
	fitvars2D.append("U Pulls vs V Positron")
	fitvars2D.append("U Pulls vs U")
	fitvars2D.append("U Pulls vs U Electron")
	fitvars2D.append("U Pulls vs U Positron")
	return fitvars2D

def buildEffArray():
	EffArr = []
	EffArr.append("Total Eff")
	EffArr.append("Total Eff Ele")
	EffArr.append("Total Eff Pos")
	EffArr.append("Total Corrected Eff")
	EffArr.append("Total Corrected Eff Ele")
	EffArr.append("Total Corrected Eff Pos")
	return EffArr

sensors = buildSensorArray(isL0)
sensorsTop = buildSensorArrayTop(isL0)
sensorsBot = buildSensorArrayBot(isL0)
plotvars = buildVariableArray()
fitvars = buildFitArray()
fitvars2D = buildFit2DArray()
EffArr = buildEffArray()
trackvars=buildTracksArray()

#PlotVars(plotvars,sensors,infile,outfile,1)
#FitVars(fitvars,sensorsTop,infile,outfile,True,1)
#FitVars(fitvars,sensorsBot,infile,outfile,False,1)
#PlotEff(EffArr,sensorsTop,infile,outfile,True)
#PlotEff(EffArr,sensorsBot,infile,outfile,False)
PlotTGraphEff(trackvars,sensorsTop,infile,outfile,True)
PlotTGraphEff(trackvars,sensorsBot,infile,outfile,False)
#FitVars2D(fitvars2D,sensors,infile,outfile,1)
