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
                print "blah"
                masses = array.array('d')
                zcuts = array.array('d')
                test = [
                         [0.015, 39.072],
                          [0.016, 39.9379],
                           [0.017, 40.6044],
                            [0.018, 41.1243],
                             [0.019, 41.5353],
                              [0.02, 41.874],
                               [0.021, 42.1671],
                                [0.022, 42.4281],
                                 [0.023, 42.6634],
                                  [0.024, 42.8838],
                                   [0.025, 43.095],
                                    [0.026, 43.303],
                                     [0.027, 43.5116],
                                      [0.028, 43.7343],
                                       [0.029, 43.961],
                                        [0.03, 43.9266],
                                         [0.031, 43.8693],
                                          [0.032, 43.5257],
                                           [0.033, 43.1753],
                                            [0.034, 42.8188],
                                             [0.035, 42.4538],
                                              [0.036, 42.0865],
                                               [0.037, 41.7118],
                                                [0.038, 41.3287],
                                                 [0.039, 40.9453],
                                                  [0.04, 40.5619],
                                                   [0.041, 40.1773],
                                                    [0.042, 39.7911],
                                                     [0.043, 39.4081],
                                                      [0.044, 39.0268],
                                                       [0.045, 38.648],
                                                        [0.046, 38.2636],
                                                         [0.047, 37.8759],
                                                          [0.048, 37.4939],
                                                           [0.049, 37.1126],
                                                            [0.05, 36.7295],
                                                             [0.051, 36.3433],
                                                              [0.052, 35.9514],
                                                               [0.053, 35.571],
                                                                [0.054, 35.1847],
                                                                 [0.055, 34.873],
                                                                  [0.056, 34.633],
                                                                   [0.057, 34.3992],
                                                                    [0.058, 34.1682],
                                                                     [0.059, 33.9416],
                                                                      [0.06, 33.7158],
                                                                      ]
                for l in test:
                    masses.append(l[0])
                    zcuts.append(l[1])
                zcutgraph = TGraph(len(masses),masses,zcuts)
                zcutgraph.SetLineColor(4)
                zcutgraph.Draw("same")
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

