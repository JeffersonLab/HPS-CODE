#!/usr/bin/env python
import sys
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TLegend, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph
#gStyle.SetOptFit(1)

ebeam=2.3
#THIS CLUSTER TIME IS FOR rotaionFix MC!
#clusterT = 43.0
#THIS CLUSTER TIME IS FOR MG_alphaFixMC!
#clusterT = 52.0
#THIS CLUSTER TIME IS FOR DATA!
clusterT = 56.0
targetZ = 0.5


inFile = TFile(sys.argv[2])
#outFile = TFile(sys.argv[1]+".root","RECREATE")
events = inFile.Get("ntuple")
#events.AddFriend("cut",sys.argv[3])

c = TCanvas("c","c",1200,900);
c.Print(sys.argv[1]+".pdf[")

#outfile = TFile(sys.argv[1]+".root","RECREATE")

events.SetLineColor(1)
events.Draw("eleTrkChisq>>(200,0,60)","","")
events.SetLineColor(2)
events.Draw("eleTrkChisq","max(eleTrkChisq,posTrkChisq)<15","same")
events.SetLineColor(3)
events.Draw("eleTrkChisq","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85","same")
events.SetLineColor(4)
events.Draw("eleTrkChisq","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85&&((tarVX-0.0113)**2/0.04)+((tarVY-0.003324)**2/0.0025)<1&&tarChisq<10","same")
events.SetLineColor(5)
events.Draw("eleTrkChisq","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85&&((tarVX-0.0113)**2/0.04)+((tarVY-0.003324)**2/0.0025)<1&&tarChisq<10&&tarP>0.8","same")
c.Print(sys.argv[1]+".pdf","Title:eleTrkChisq")

events.SetLineColor(1)
events.Draw("posTrkChisq>>(200,0,60)","","")
events.SetLineColor(2)
events.Draw("posTrkChisq","max(eleTrkChisq,posTrkChisq)<15","same")
events.SetLineColor(3)
events.Draw("posTrkChisq","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85","same")
events.SetLineColor(4)
events.Draw("posTrkChisq","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85&&((tarVX-0.0113)**2/0.04)+((tarVY-0.003324)**2/0.0025)<1&&tarChisq<10","same")
events.SetLineColor(5)
events.Draw("posTrkChisq","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85&&((tarVX-0.0113)**2/0.04)+((tarVY-0.003324)**2/0.0025)<1&&tarChisq<10&&tarP>0.8","same")
c.Print(sys.argv[1]+".pdf","Title:posTrkChisq")

events.SetLineColor(1)
events.Draw("eleP>>(200,0,1.6)","","")
events.SetLineColor(2)
events.Draw("eleP","max(eleTrkChisq,posTrkChisq)<15","same")
events.SetLineColor(3)
events.Draw("eleP","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85","same")
events.SetLineColor(4)
events.Draw("eleP","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85&&((tarVX-0.0113)**2/0.04)+((tarVY-0.003324)**2/0.0025)<1&&tarChisq<10","same")
events.SetLineColor(5)
events.Draw("eleP","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85&&((tarVX-0.0113)**2/0.04)+((tarVY-0.003324)**2/0.0025)<1&&tarChisq<10&&tarP>0.8","same")
c.Print(sys.argv[1]+".pdf","Title:eleP")

events.SetLineColor(1)
events.Draw("posP>>(200,0,1.6)","","")
events.SetLineColor(2)
events.Draw("posP","max(eleTrkChisq,posTrkChisq)<15","same")
events.SetLineColor(3)
events.Draw("posP","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85","same")
events.SetLineColor(4)
events.Draw("posP","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85&&((tarVX-0.0113)**2/0.04)+((tarVY-0.003324)**2/0.0025)<1&&tarChisq<10","same")
events.SetLineColor(5)
events.Draw("posP","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85&&((tarVX-0.0113)**2/0.04)+((tarVY-0.003324)**2/0.0025)<1&&tarChisq<10&&tarP>0.8","same")
c.Print(sys.argv[1]+".pdf","Title:posP")

events.SetLineColor(1)
events.Draw("tarVX>>(200,-0.5,0.5)","","")
events.SetLineColor(2)
events.Draw("tarVX","max(eleTrkChisq,posTrkChisq)<15","same")
events.SetLineColor(3)
events.Draw("tarVX","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85","same")
events.SetLineColor(4)
events.Draw("tarVX","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85&&((tarVX-0.0113)**2/0.04)+((tarVY-0.003324)**2/0.0025)<1&&tarChisq<10","same")
events.SetLineColor(5)
events.Draw("tarVX","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85&&((tarVX-0.0113)**2/0.04)+((tarVY-0.003324)**2/0.0025)<1&&tarChisq<10&&tarP>0.8","same")
c.Print(sys.argv[1]+".pdf","Title:tarVX")

events.SetLineColor(1)
events.Draw("tarVY>>(200,-0.1,0.1)","","")
events.SetLineColor(2)
events.Draw("tarVY","max(eleTrkChisq,posTrkChisq)<15","same")
events.SetLineColor(3)
events.Draw("tarVY","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85","same")
events.SetLineColor(4)
events.Draw("tarVY","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85&&((tarVX-0.0113)**2/0.04)+((tarVY-0.003324)**2/0.0025)<1&&tarChisq<10","same")
events.SetLineColor(5)
events.Draw("tarVY","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85&&((tarVX-0.0113)**2/0.04)+((tarVY-0.003324)**2/0.0025)<1&&tarChisq<10&&tarP>0.8","same")
c.Print(sys.argv[1]+".pdf","Title:tarVY")

events.SetLineColor(1)
events.Draw("tarP>>(200,0,1.6)","","")
events.SetLineColor(2)
events.Draw("tarP","max(eleTrkChisq,posTrkChisq)<15","same")
events.SetLineColor(3)
events.Draw("tarP","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85","same")
events.SetLineColor(4)
events.Draw("tarP","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85&&((tarVX-0.0113)**2/0.04)+((tarVY-0.003324)**2/0.0025)<1&&tarChisq<10","same")
events.SetLineColor(5)
events.Draw("tarP","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85&&((tarVX-0.0113)**2/0.04)+((tarVY-0.003324)**2/0.0025)<1&&tarChisq<10&&tarP>0.8","same")
c.Print(sys.argv[1]+".pdf","Title:tarP")

#events.SetLineColor(1)
#events.Draw("tarM>>(200,0,0.1)","","")
#events.SetLineColor(2)
#events.Draw("tarM","max(eleTrkChisq,posTrkChisq)<15","same")
#events.SetLineColor(3)
#events.Draw("tarM","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85","same")
#events.SetLineColor(4)
#events.Draw("tarM","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85&&((tarVX-0.0113)**2/0.04)+((tarVY-0.003324)**2/0.0025)<1&&tarChisq<10","same")
#events.SetLineColor(5)
#events.Draw("tarM","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85&&((tarVX-0.0113)**2/0.04)+((tarVY-0.003324)**2/0.0025)<1&&tarChisq<10&&tarP>0.8","same")
#c.Print(sys.argv[1]+".pdf)","Title:tarM")


#events.SetWeight(500e-6/((10e4/0.08193e6)*10*99)) # 5mrad RAD
#events.SetWeight(500e-6/((10e4/1.416e6)*10*98)) # 5mrad tritrig
#events.SetWeight(500e-6/((10e4/1.1416e6)*900)) # tritrig-WBT
#events.SetWeight(500e-6/((10e4/181.7e6)*10000)) # 5mrad wab low peak
#events.SetWeight(500e-6/((10e4/220.4e6)*10*990)) # 5mrad wab high peak
events.SetWeight(1)

#events.SetWeight(500e-6/((10e4/0.0667e6)*10*10)) #RAD reg 5mrad XS
#events.SetWeight(500e-6/((10e4/0.08193e6)*10)) #RAD angleScan 5mrad XS
#events.SetWeight(500e-6/((10e4/1.1416e6)*1000)) #tritrig reg 5mrad XS
#events.SetWeight(500e-6/((10e4/1.416e6)*1000)) #tritrig angleScan 5mrad XS

#massVar = "uncM"
massVar = "mRefitUnc"

#pair1 = ""
pair1 = "isPair1&&eleTrkEcalY*posTrkEcalY<0"
#pair1 = "isPair1&&eleClY*posClY<0"
#pair1 = "isPair1&&eleSlope*posSlope<0"
L1L1 = "&&eleHasL1&&posHasL1"
#Chi2 = "&&max(eleMatchChisq,posMatchChisq)<10&&bscChisq<10&&bscChisq-uncChisq<5&&max(eleTrkChisq,posTrkChisq)<30"
Chi2 = "&&bscChisq<10&&bscChisq-uncChisq<5&&max(eleTrkChisq,posTrkChisq)<30"
#time = "&&max(abs(eleClT-eleTrkT-52),abs(posClT-posTrkT-52))<4&&abs(eleClT-posClT)<2"
time = "&&max(abs(eleClT-eleTrkT)-10000,abs(posClT-posTrkT)-10000)<4&&abs(eleClT-posClT)<2"
#isolation = "&&min(eleMinPositiveIso+0.5*(eleTrkZ0+0*elePY/eleP)*sign(elePY),posMinPositiveIso+0.5*(posTrkZ0+0*posPY/posP)*sign(posPY))>0"
isolation = "&&min(eleMinPositiveIso+0.5*(eleTrkZ0+0.5*elePY/eleP)*sign(elePY),posMinPositiveIso+0.5*(posTrkZ0+0.5*posPY/posP)*sign(posPY))>0"
asymmetry = "&&abs(eleP-posP)/(eleP+posP)<0.4"
#doca = "&&posTrkD0+0*posPX/posP<1.5"
doca = "&&posTrkD0+0.5*posPX/posP<1.5"
energy = "&&eleP<2.3*0.75&&uncP<2.3*1.15"
rad = "&&uncP>0.8*2.3"

leg = TLegend(0.5,0.5,0.9,0.9)
#leg = TLegend(0.1,0.5,0.5,0.9)

# pair1 + opposite volume
events1 = events.Clone("")
events1.SetLineColor(1)
events1.Draw(massVar+">>(200,0,0.3)",pair1,"")
#events1.Draw(massVar+">>(200,0,0.2)",pair1,"")
#events1.Draw("max(abs(eleClT-eleTrkT),abs(posClT-posTrkT))>>(200,9990,10010)","","")
leg.AddEntry(events1,"Pair1 + opposite volume")
leg.Draw("")

# elastics/FEE
events2 = events.Clone("")
events2.SetLineColor(2)
events2.Draw(massVar,pair1+energy,"same")
leg.AddEntry(events2,"+ elastics/FEE")
leg.Draw("same")

#L1L1 cut
events3 = events.Clone("")
events3.SetLineColor(3)
events3.Draw(massVar,pair1+energy+L1L1,"same")
leg.AddEntry(events3,"+ L1L1")
leg.Draw("same")

# +Timing cuts
events4 = events.Clone("")
events4.SetLineColor(4)
events4.Draw(massVar,pair1+energy+L1L1+time,"same")
leg.AddEntry(events4,"+ timing")
leg.Draw("same")

# +isolation cut
events5 = events.Clone("")
events5.SetLineColor(5)
events5.Draw(massVar,pair1+energy+L1L1+time+isolation,"same")
leg.AddEntry(events5,"+ isolation")
leg.Draw("same")

# +momentum asymmetry
events6 = events.Clone("")
events6.SetLineColor(6)
events6.Draw(massVar,pair1+energy+L1L1+time+isolation+asymmetry,"same")
leg.AddEntry(events6,"+ momentum asymmetry")
leg.Draw("same")

# +positron DOCA
events7 = events.Clone("")
events7.SetLineColor(7)
events7.Draw(massVar,pair1+energy+L1L1+time+isolation+asymmetry+doca,"same")
leg.AddEntry(events7,"+ positron DOCA")
leg.Draw("same")

# +Chi2
events8 = events.Clone("")
events8.SetLineColor(8)
events8.Draw(massVar,pair1+energy+L1L1+time+isolation+asymmetry+doca+Chi2,"same")
leg.AddEntry(events8,"+ Chi2 cuts")
leg.Draw("same")

# +radiative cut
events9 = events.Clone("")
events9.SetLineColor(9)
events9.Draw(massVar,pair1+energy+L1L1+time+isolation+asymmetry+doca+Chi2+rad,"same")
leg.AddEntry(events9,"+ radiative cut")
leg.Draw("same")


#gStyle.SetXaxisTitle("pair invariant mass [GeV]")
#events9.GetXaxis().SetTitle("pair invariant mass [GeV]")
#events9.GetYaxis().SetTitle("cross-section [mb/GeV]")

c.Print(sys.argv[1]+".pdf)","Title:"+massVar)
outfile = TFile(sys.argv[1]+".root","RECREATE")
#events.SetLineColor(1)
#events.Draw("triM>>mass(200,0,0.2)","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85&&((tarVX-0.0113)**2/0.04)+((tarVY-0.003324)**2/0.0025)<1&&tarChisq<10&&tarP>0.8","same")
#massHist = gDirectory.Get("mass")
#massHist.Write()
outfile.Write()
outfile.Close()
