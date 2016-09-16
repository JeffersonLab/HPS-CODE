#!/usr/bin/env python
import sys, array
import getopt
from ROOT import gROOT, TCanvas, TF1, TFile, gStyle, TFormula, TGraph, TGraphErrors, TH1D, TCutG, TH2D

def makeplots(files,path,name,c):
	c.Clear()
	color=1
	for f in files:
            print path
	    h=f.Get(path)
            #h.Print()
	    h.SetLineColor(color)
	    if color==1:
		    h.Draw("")
	    else:
		    h.Draw("same")
	    color+=1
	c.SaveAs(sys.argv[1]+"-"+name+".png")

def makenormplots(files,path,name,c):
	c.Clear()
	color=1
	for f in files:
	    h=f.Get(path)#.Clone()
	    #h.SetDirectory(0)
	    h.SetLineColor(color)
	    h.Scale(1/h.Integral())
	    if color==1:
                    #h.SetName("slice_36")
                    h.GetXaxis().SetTitle("Vertex Z [mm]")
                    h.GetYaxis().SetTitle("Arbitrary units")
		    h.DrawCopy("")
	    else:
                nbins = h.GetXaxis().GetNbins()
                shiftedH = TH1D("shiftedH","test",h.GetNbinsX(),h.GetXaxis().GetXmin(),h.GetXaxis().GetXmax())
                for i in range(0,nbins-1):
                    shiftedH.SetBinContent(i,h.GetBinContent(i+1))
                    shiftedH.SetBinError(i,h.GetBinError(i+1))
                shiftedH.SetLineColor(color)
                shiftedH.DrawCopy("same")
	    color+=1
	c.SaveAs(sys.argv[1]+"-"+name+".png")

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'h', ['help',])

for opt, arg in options:
    if opt in ('-h', '--help'):
        print "\nUsage: "+sys.argv[0]+" <output basename> <root files>"
        print "Arguments: "
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

makeplots(files,"zcut","zcut",c)
c.SetLogy(1)
makenormplots(files,"slice_36","slice-36",c)
c.SetLogy(0)
makeplots(files,"profile","profile",c)

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
outfile.Write()
outfile.Close()

sys.exit(0)

