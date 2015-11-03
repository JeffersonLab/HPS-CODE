#!/usr/bin/env python
import sys, array
import getopt
from ROOT import gROOT, TCanvas, TF1, TFile, gStyle, TFormula, TGraph, TGraphErrors, TH1D, TCutG, TH2D

def makeplots(files,path,name,c):
	c.Clear()
	color=1
	for f in files:
	    h=f.Get(path)
	    h.SetLineColor(color)
	    if color==1:
		    h.Draw("")
	    else:
		    h.Draw("same")
	    color+=1
	c.SaveAs(sys.argv[1]+"-"+name+".png")

def makedivplots(files,path1,path2,name,c):
	c.Clear()
	color=1
	for f in files:
	    h1=f.Get(path1)#.Clone()
	    #h1.SetDirectory(0)
	    h2=f.Get(path2)
	    h1.Divide(h2)
	    h1.SetLineColor(color)
	    if color==1:
		    h1.Draw("")
	    else:
		    h1.Draw("same")
	    color+=1
	c.SaveAs(sys.argv[1]+"-"+name+".png")

def makenormplots(files,path,name,c):
	c.Clear()
	color=1
	for f in files:
	    h=f.Get(path).Clone("blah")
	    #h.SetDirectory(0)
	    h.SetLineColor(color)
	    h.Scale(1/h.Integral())
	    if color==1:
		    h.DrawCopy("")
	    else:
		    h.DrawCopy("same")
	    color+=1
	c.SaveAs(sys.argv[1]+"-"+name+".png")

scale_factor = 1
lumi_total = 1240

massres_a = 0.032 #sigma = a*mass + b
massres_b = 0.001 #units of GeV

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'l:h', ['luminosity','help',])

for opt, arg in options:
    if opt in ('-l', '--luminosity'):
        lumi = float(arg)
        scale_factor = lumi/lumi_total
    elif opt in ('-h', '--help'):
        print "\nUsage: "+sys.argv[0]+" <output basename> <root files>"
        print "Arguments: "
        print "\t-l, --luminosity: luminosity for normalization"
        print "\n"
        sys.exit(0)


if (len(remainder)!=3):
        print sys.argv[0]+' <output basename> <root files>'
        sys.exit()

c = TCanvas("c","c",800,600);
outfile = TFile(remainder[0]+"-plots.root","RECREATE")
totalH = None
files=[]
keylists=[]
for filename in remainder[1:]:
    f=TFile(filename)
    files.append(f)

makeplots(files,"sigma","sigma",c)
makeplots(files,"zcut","zcut",c)
makeplots(files,"mass","mass",c)
makenormplots(files,"mass","massnorm",c)
c.SetLogy(1)
makedivplots(files,"hightails","mass","hightails",c)
makedivplots(files,"lowtails","mass","lowtails",c)

    #keylists.append(f.GetListOfKeys())
    #print filename
    #print f.GetListOfKeys()
    #for blah in  f.GetListOfKeys():
	#    print blah
    #if totalH is None:
        #totalH=TH2D(h)
        #totalH.SetDirectory(outfile)
    #else:
        #totalH.Add(h)
#for key in files[0].GetListOfKeys():
	#print key
	#print key.GetName()
	#files[0].GetObjectUnchecked(key.GetName()).Draw()
	#	print 

sys.exit(0)

