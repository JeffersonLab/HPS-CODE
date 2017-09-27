#!/usr/bin/env python
#Author Matt Solt mrsolt@slac.stanford.edu
import sys
import array, math
import ROOT
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph, gPad, TF1, TH1F, TLegend
import getopt

def print_usage():
    print "\nUsage: {0} <output file basename> <input recon tuple files list> <input recon truth tuple files list> <L1L1 input files list>".format(sys.argv[0])
    print "Arguments: "
    print '\t-e: use this beam energy <default 1.056 GeV>'
    print '\t-t: use this target position <default -5 mm>'
    print '\t-n: number of bins in histograms <default 50>'
    print '\t-z: total range in z covered <default 100 mm>'
    print '\t-T: plot Test plots'
    print '\t-N: number of bins from target to normalize to <default is 4>'
    print '\t-h: this help message'
    print

#Default Values
eBeam = 1.056
makeTestPlots = False
targZ = -5.
nBins = 50
zRange = 100
nNorm = 4

#Function to plot efficiency tests of known masses
def plotTest(iMass,inputFile,output,targZ,maxZ,canvas):
    inputfile = open(inputFile,"r")
    mass = []
    z = []
    result = []
    eff = []
    #Readlines from input file
    lines = inputfile.readlines()
    for x in lines:
        result.append(x.split())
    inputfile.close()
    nMass = len(result[0])
    nBins = len(result[1])
    #Grab Array of Masses
    for i in range(nMass):
        mass.append(float(result[0][i]))
    #Grab Array of z's
    for i in range(nBins):
        z.append(float(result[1][i]))
    #Convert the strings from input file into floats
    for i in range(nMass):
        dummy = []
        for j in range(nBins):
            dummy.append(float(result[i+2][j]))
        eff.append(dummy)
        del dummy
    #define histograms
    histo1 = TH1F("histo1","histo1",nBins-1,targZ,maxZ) #test histogram
    histo2 = TH1F("histo2","histo2",nBins,targZ,maxZ) #known histogram
    #Use the mass greater than and less than the mass of interest
    iMass1 = iMass - 1
    iMass2 = iMass + 1
    for i in range(nBins-1):
        iZ1 = i
        iZ2 = i + 1
        Q11 = eff[iMass1][iZ1]
        Q12 = eff[iMass2][iZ1]
        Q21 = eff[iMass1][iZ2]
        Q22 = eff[iMass2][iZ2]
        #Interpolate value
        interpolate = Bilinear(z[i],mass[iMass],z[iZ1],z[iZ2],mass[iMass1],mass[iMass2],Q11,Q12,Q21,Q22)
        histo1.SetBinContent(i+1,interpolate)
    for i in range(nBins):
        histo2.SetBinContent(i+1,eff[iMass][i])
    #Draw Histograms
    legend = TLegend(.68,.66,.92,.87)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.035)
    legend.AddEntry(histo1,"Interpolation","LP")
    legend.AddEntry(histo2,"MC","LP")
    maximum = histo1.GetMaximum()
    if(histo2.GetMaximum() > maximum): maximum = histo2.GetMaximum()
    histo1.Draw("")
    histo1.GetXaxis().SetTitle("z [mm]")
    histo1.SetTitle("A' Efficiency " + str(mass[iMass]) + " GeV")
    histo1.GetYaxis().SetRangeUser(0,maximum*1.2)
    histo2.Draw("same")
    histo2.SetLineColor(2)
    legend.Draw("")
    gStyle.SetOptStat(0)
    canvas.Print(output+".pdf")

#Function to plot efficiency tests of known masses
def Interpolate(Mass,Z,mass,z,eff):
    iMass = 0
    iZ = 0
    #Grab the index of mass and z
    for i in range(nMass):
        if(Mass < mass[i]):
	    iMass = i
	    break
    for i in range(nBins):
        if(Z < z[i]):
	    iZ = i
	    break
    #Check to make sure mass and z are not out of range
    if(iMass == 0):
        print "Mass is out of range!"
        return
    if(iZ == 0):
        print "Z is behind target!"
        return
    iMass1 = iMass - 1
    iMass2 = iMass
    iZ1 = iZ - 1
    iZ2 = iZ
    Q11 = eff[iMass1][iZ1]
    Q12 = eff[iMass2][iZ1]
    Q21 = eff[iMass1][iZ2]
    Q22 = eff[iMass2][iZ2]
    #Interpolate value
    interpolate = Bilinear(Z,Mass,z[iZ1],z[iZ2],mass[iMass1],mass[iMass2],Q11,Q12,Q21,Q22)
    return interpolate

#Function to plot efficiency tests of known masses directly from file
def InterpolateFromFile(Mass,Z,inputFile):
	mass = getMassArray(inputFile)
	z = getZArray(inputFile)
	eff = getEfficiency(inputFile)
	interpolate = Interpolate(Mass,Z,mass,z,eff)
	return interpolate

def getMassArray(inputFile):
 	inputfile = open(inputFile,"r")
	mass = []
	result = []
	#Readlines from input file
	lines = inputfile.readlines()
	for x in lines:
		result.append(x.split())
	inputfile.close()
	nMass = len(result[0])
	#Grab Array of Masses
	for i in range(nMass):
		mass.append(float(result[0][i]))
	return mass

def getZArray(inputFile):
 	inputfile = open(inputFile,"r")
	z = []
	result = []
	#Readlines from input file
	lines = inputfile.readlines()
	for x in lines:
		result.append(x.split())
	inputfile.close()
	nBins = len(result[1])
	#Grab Array of z's
	for i in range(nBins):
		z.append(float(result[1][i]))
	return z

def getEfficiency(inputFile):
	inputfile = open(inputFile,"r")
	result = []
	eff = []
	#Readlines from input file
	lines = inputfile.readlines()
	for x in lines:
 		result.append(x.split())
	inputfile.close()
        nMass = len(result[0])
        nBins = len(result[1])
	#Convert the strings from input file into floats
	for i in range(nMass):
		dummy = []
		for j in range(nBins):
	    		dummy.append(float(result[i+2][j]))
		eff.append(dummy)
		del dummy
	return eff

#Function for Bilinear interpolation
def Bilinear(x,y,x1,x2,y1,y2,Q11,Q12,Q21,Q22):
    denom = (x2-x1)*(y2-y1)
    t1 = (x2-x)*(y2-y)/denom*Q11
    t2 = (x-x1)*(y2-y)/denom*Q21
    t3 = (x2-x)*(y-y1)/denom*Q12
    t4 = (x-x1)*(y-y1)/denom*Q22
    return t1+t2+t3+t4

datafile=""
options, remainder = getopt.gnu_getopt(sys.argv[1:], 'e:t:n:z:Th')

# Parse the command line arguments
for opt, arg in options:
    if opt=='-e':
        eBeam=float(arg)
    if opt=='-t':
        targZ=float(arg)
    if opt=='-n':
        nBins=int(arg)
    if opt=='-z':
        zRange=float(arg)
    if opt=='-T':
        makeTestPlots = True
    if opt=='-N':
        nNorm = int(arg)
    if opt=='-h':
        print_usage()
        sys.exit(0)

if len(remainder)!=4:
    print_usage()
    sys.exit(0)

gROOT.SetBatch(True)
maxZ = targZ + zRange #Define Maximum Z

#Set outfile and grab infile
outfile = remainder[0]
inputfile = open(remainder[1],"r")
truthfile = open(remainder[2],"r")
L1L1file = open(remainder[3],"r")

reconFiles = []
truthFiles = []
L1L1Files = []

#Read files from input text file
for line in (raw.strip().split() for raw in inputfile):
            reconFiles.append(line[0])

#Read files from input text truth file
for line in (raw.strip().split() for raw in truthfile):
            truthFiles.append(line[0])

#Read files from L1L1 input text file
for line in (raw.strip().split() for raw in L1L1file):
            L1L1Files.append(line[0])

if (len(reconFiles) != len(L1L1Files) or len(reconFiles) != len(truthFiles)):
    print "The number of L1L1 files, input files, or truth files do not match!"
    print_usage()
    sys.exit(0)

mass = array.array('d')
z = array.array('d')
nMass = len(reconFiles)

#Grab values of mass from the truth in the tuple files
for i in range(nMass):
    inputReconFile = TFile(str(reconFiles[i]))
    inputReconFile.Get("cut").Draw("triM>>histoMass({0},{1},{2})".format(1000,0,1))
    histoMass = ROOT.gROOT.FindObject("histoMass")
    mass.append(histoMass.GetMean())
    del histoMass

#Build array of z values
for i in range(nBins):
    z.append(targZ+i*(maxZ-targZ)/float(nBins))

#Create text files to write to
textfile = open(outfile + ".eff","w")
textfileNorm = open(outfile + "_norm.eff","w")

#Write values of mass in the first row
for i in range(nMass):
    textfile.write(str(mass[i]) + " ")
    textfileNorm.write(str(mass[i]) + " ")
textfile.write("\n")
textfileNorm.write("\n")
#Write values of z in the 2nd row
for i in range(nBins):
    textfile.write(str(z[i]) + " ") 
    textfileNorm.write(str(z[i]) + " ")  
textfile.write("\n")
textfileNorm.write("\n")

#Loop over all values of mass
for i in range(nMass):
    inputReconFile = TFile(str(reconFiles[i])) #tuple files after cuts
    inputTruthFile = TFile(str(truthFiles[i])) #truth files
    inputL1L1ReconFile = TFile(str(L1L1Files[i])) #L1L1 tuple files after cuts
    inputReconFile.Get("cut").Draw("triEndZ>>histoRecon({0},{1},{2})".format(nBins,targZ,maxZ),"triP>0.8*{0}".format(eBeam))
    histoRecon = ROOT.gROOT.FindObject("histoRecon")
    inputTruthFile.Get("ntuple").Draw("triEndZ>>histoTruth({0},{1},{2})".format(nBins,targZ,maxZ),"triP>0.8*{0}".format(eBeam))
    histoTruth = ROOT.gROOT.FindObject("histoTruth")
    inputL1L1ReconFile.Get("cut").Draw("triEndZ>>histoL1L1Recon({0},{1},{2})".format(nBins,targZ,maxZ),"triP>0.8*{0}".format(eBeam))
    histoL1L1Recon = ROOT.gROOT.FindObject("histoL1L1Recon")
    #Find the normalization based on a certain number of bins
    norm = 0.0
    for j in range(nNorm):
        if (histoTruth.GetBinContent(j+1) != 0): 
            norm += histoL1L1Recon.GetBinContent(j+1)/histoTruth.GetBinContent(j+1)
        else: 
            norm = 0.0
            break
    norm = norm/nNorm
    #Write the efficiency for a given mass (row) as function of z
    for j in range(nBins):
        if (histoTruth.GetBinContent(j+1) == 0):
            textfile.write("0.0 ")
            textfileNorm.write("0.0 ")
        else:
            textfile.write(str(histoRecon.GetBinContent(j+1)/histoTruth.GetBinContent(j+1)) + " ")
            if(norm != 0):
                textfileNorm.write(str(histoRecon.GetBinContent(j+1)/(histoTruth.GetBinContent(j+1)*norm)) + " ")
            else:
                textfileNorm.write("0.0 ")
    textfile.write("\n")
    textfileNorm.write("\n")

textfile.close()
textfileNorm.close()

#Make test plots if desired
if(makeTestPlots):
    #Make Absolute Efficiency Plots
    c1 = TCanvas("c","c",1200,900)
    c1.Print(outfile+".pdf[")   

    for i in range(1,nMass-1):
        plotTest(i,outfile+".eff",outfile,targZ,maxZ,c1)

    c1.Print(outfile+".pdf]")

    del c1
    
    #Make Normalized Efficiency Plots
    outfileNorm = outfile+"_norm"
    c2 = TCanvas("c","c",1200,900)
    c2.Print(outfile+"_norm.pdf[")

    for i in range(1,nMass-1):
        plotTest(i,outfileNorm+".eff",outfileNorm,targZ,maxZ,c2)

    c2.Print(outfile+"_norm.pdf]")