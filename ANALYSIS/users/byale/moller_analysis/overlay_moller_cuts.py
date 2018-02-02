#!/usr/bin/env python
import sys, getopt, array
#from ROOT import gROOT, gStyle, TFile, TTree, TChain, TLegend, TMVA, TCut, TCanvas, gDirectory, TH1, TH2, TGraph
from ROOT import gROOT, TCanvas, TF1, TFile, gStyle, TFormula, TGraph, TGraphErrors, TH1D, TCutG, TH2D, gDirectory, TLegend
#gStyle.SetOptFit(1)

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'h', ['help',])

ebeam=2.3
#THIS CLUSTER TIME IS FOR rotaionFix MC!
#clusterT = 43.0
#THIS CLUSTER TIME IS FOR MG_alphaFixMC!
clusterT = 52.0
#THIS CLUSTER TIME IS FOR DATA!
#clusterT = 56.0
targetZ = 0.5

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600);
#c = TCanvas("c","c",2000,2000);

#inFile = TFile(sys.argv[2])
#inFileData = TFile(sys.argv[3])
inFile = TFile(remainder[1])
#inFileData = TFile(remainder[2])

events = inFile.Get("ntuple")
#eventsData = inFileData.Get("ntuple")

#events.AddFriend("cut",sys.argv[3])

#events.SetWeight(1000/(74*(2e6)*(2500)*(4.062e-4)*(6.306e-2)*1000)) # MC XS (mb)
events.SetWeight(1000*4097/(74*112.166690534e9)) # Data XS (mb)

#c.Print(sys.argv[1]+".pdf[")

#options, remainder = getopt.gnu_getopt(sys.argv[1:], 'tpolVvamwe:c:z:h')

#outfile = TFile(sys.argv[0]+".root","RECREATE")

c.Print(remainder[0]+".pdf[")
#outfile = TFile(remainder[0]+".root","RECREATE")

events.SetLineColor(1)
#events.Draw("eleTrkChisq>>(200,0,60)","","")
#events.Draw("max(abs(topClT-topTrkT-151.2),abs(botClT-botTrkT-151.2))>>(200,-10,10)","","")

events.SetLineColor(2)
#events.Draw("eleTrkChisq","max(eleTrkChisq,posTrkChisq)<15","same")
events.SetLineColor(3)
#events.Draw("eleTrkChisq","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85","same")
events.SetLineColor(4)
#events.Draw("eleTrkChisq","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85&&((tarVX-0.0113)**2/0.04)+((tarVY-0.003324)**2/0.0025)<1&&tarChisq<10","same")
events.SetLineColor(5)
#events.Draw("eleTrkChisq","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85&&((tarVX-0.0113)**2/0.04)+((tarVY-0.003324)**2/0.0025)<1&&tarChisq<10&&tarP>0.8","same")
c.Print(sys.argv[1]+".pdf","Title:eleTrkChisq")

events.SetLineColor(1)
events.Draw("abs(topTrkT-botTrkT)>>(200,0,5)","","")
#events.Draw("topClT>>(200,0,100)","","")
events.SetLineColor(2)
#events.Draw("posTrkChisq","max(eleTrkChisq,posTrkChisq)<15","same")
events.SetLineColor(3)
#events.Draw("posTrkChisq","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85","same")
events.SetLineColor(4)
#events.Draw("posTrkChisq","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85&&((tarVX-0.0113)**2/0.04)+((tarVY-0.003324)**2/0.0025)<1&&tarChisq<10","same")
events.SetLineColor(5)
#events.Draw("posTrkChisq","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85&&((tarVX-0.0113)**2/0.04)+((tarVY-0.003324)**2/0.0025)<1&&tarChisq<10&&tarP>0.8","same")
c.Print(sys.argv[1]+".pdf","Title:posTrkChisq")

#theta_theta = TH2("theta_theta", "", 200, 0, 0.1, 200, 0, 0.1)

events.SetLineColor(1)
#events.Draw("atan2(sqrt(topPX*topPX + topPY*topPY),topPZ)>>(200,0,0.1,200,0,2)","","")
events.Draw("atan2(sqrt(topPX*topPX + topPY*topPY),topPZ):atan2(sqrt(botPX*botPX + botPY*botPY),botPZ)>>(200,0.0,0.1,200,0.0,0.1)","","colz")
events.SetLineColor(2)
#events.Draw("eleP","max(eleTrkChisq,posTrkChisq)<15","same")
events.SetLineColor(3)
#events.Draw("eleP","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85","same")
events.SetLineColor(4)
#events.Draw("eleP","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85&&((tarVX-0.0113)**2/0.04)+((tarVY-0.003324)**2/0.0025)<1&&tarChisq<10","same")
events.SetLineColor(5)
#events.Draw("eleP","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85&&((tarVX-0.0113)**2/0.04)+((tarVY-0.003324)**2/0.0025)<1&&tarChisq<10&&tarP>0.8","same")
c.Print(sys.argv[1]+".pdf","Title:theta")

events.SetLineColor(1)
#events.Draw("topMatchChisq+botMatchChisq>>(200,0,50)","","")
events.Draw("topMatchChisq:botMatchChisq>>(200,0,30,200,0,30);botMatchChisq;topMatchChisq;","","")
events.SetLineColor(2)
#events.Draw("posP","max(eleTrkChisq,posTrkChisq)<15","same")
events.SetLineColor(3)
#events.Draw("posP","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85","same")
events.SetLineColor(4)
#events.Draw("posP","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85&&((tarVX-0.0113)**2/0.04)+((tarVY-0.003324)**2/0.0025)<1&&tarChisq<10","same")
events.SetLineColor(5)
#events.Draw("posP","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85&&((tarVX-0.0113)**2/0.04)+((tarVY-0.003324)**2/0.0025)<1&&tarChisq<10&&tarP>0.8","same")
c.Print(sys.argv[1]+".pdf","Title:match2D")

events.SetLineColor(1)
#events.Draw("tarVX>>(200,-0.5,0.5)","","")
events.Draw("topP>>(200,0.0,2.3)","","")
events.SetLineColor(2)
#events.Draw("tarVX","max(eleTrkChisq,posTrkChisq)<15","same")
events.SetLineColor(3)
#events.Draw("tarVX","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85","same")
events.SetLineColor(4)
#events.Draw("tarVX","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85&&((tarVX-0.0113)**2/0.04)+((tarVY-0.003324)**2/0.0025)<1&&tarChisq<10","same")
events.SetLineColor(5)
#events.Draw("tarVX","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85&&((tarVX-0.0113)**2/0.04)+((tarVY-0.003324)**2/0.0025)<1&&tarChisq<10&&tarP>0.8","same")
c.Print(sys.argv[1]+".pdf","Title:momentum")

events.SetLineColor(1)
events.Draw("topMatchChisq+botMatchChisq>>(200,0,15000)","","")
events.SetLineColor(2)
#events.Draw("tarVY","max(eleTrkChisq,posTrkChisq)<15","same")
events.SetLineColor(3)
#events.Draw("tarVY","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85","same")
events.SetLineColor(4)
#events.Draw("tarVY","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85&&((tarVX-0.0113)**2/0.04)+((tarVY-0.003324)**2/0.0025)<1&&tarChisq<10","same")
events.SetLineColor(5)
#events.Draw("tarVY","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85&&((tarVX-0.0113)**2/0.04)+((tarVY-0.003324)**2/0.0025)<1&&tarChisq<10&&tarP>0.8","same")
c.Print(sys.argv[1]+".pdf","Title:match")

events.SetLineColor(1)
#events.Draw("tarP>>(200,0,1.6)","","")
events.Draw("botClY-botTrkEcalY>>(200,-25,25)","","")
events.SetLineColor(2)
#events.Draw("tarP","max(eleTrkChisq,posTrkChisq)<15","same")
events.SetLineColor(3)
#events.Draw("tarP","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85","same")
events.SetLineColor(4)
#events.Draw("tarP","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85&&((tarVX-0.0113)**2/0.04)+((tarVY-0.003324)**2/0.0025)<1&&tarChisq<10","same")
events.SetLineColor(5)
#events.Draw("tarP","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85&&((tarVX-0.0113)**2/0.04)+((tarVY-0.003324)**2/0.0025)<1&&tarChisq<10&&tarP>0.8","same")
c.Print(sys.argv[1]+".pdf","Title:tarP")

events.SetLineColor(1)
#events.Draw("topClY-topTrkEcalY>>(200,-25,25)","","")
events.SetLineColor(2)
#events.Draw("tarM","max(eleTrkChisq,posTrkChisq)<15","same")
events.SetLineColor(3)
#events.Draw("tarM","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85","same")
events.SetLineColor(4)
#events.Draw("tarM","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85&&((tarVX-0.0113)**2/0.04)+((tarVY-0.003324)**2/0.0025)<1&&tarChisq<10","same")
events.SetLineColor(5)
#events.Draw("tarM","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85&&((tarVX-0.0113)**2/0.04)+((tarVY-0.003324)**2/0.0025)<1&&tarChisq<10&&tarP>0.8","same")
#c.Print(sys.argv[1]+".pdf)","Title:matching")


#events.SetWeight(500e-6/((10e4/0.08193e6)*10*99)) # 5mrad RAD
#events.SetWeight(500e-6/((10e4/1.416e6)*10*98)) # 5mrad tritrig
#events.SetWeight(500e-6/((10e4/1.1416e6)*900)) # tritrig-WBT
#events.SetWeight(500e-6/((10e4/181.7e6)*10000)) # 5mrad wab low peak
#events.SetWeight(500e-6/((10e4/220.4e6)*10*990)) # 5mrad wab high peak
#events.SetWeight(1)

#events.SetWeight(500e-6/((10e4/0.0667e6)*10*10)) #RAD reg 5mrad XS
#events.SetWeight(500e-6/((10e4/0.08193e6)*10)) #RAD angleScan 5mrad XS
#events.SetWeight(500e-6/((10e4/1.1416e6)*1000)) #tritrig reg 5mrad XS
#events.SetWeight(500e-6/((10e4/1.416e6)*1000)) #tritrig angleScan 5mrad XS

#outfile.cd()
#cut_mass=TH1D("cut_mass","cut_mass",1200,0.03,0.1)

#c.Print(remainder[0]+".pdf[")
#outfile = TFile(remainder[0]+".root","RECREATE")


###################### PREVIOUS ########################
massVar = "uncM"
#massVar = "bscM"
#massVar = "tarM"
#massVar = "mRefitUnc"

#pair1 = ""
#pair1 = "isSingle0&&topTrkLambda*botTrkLambda<0"
#pair1 = "topClY*botClY<0"
#pair1 = "isSingle0&&topClY*botClY<0"

#pair1 = "isSingle0&&topTrkLambda*botTrkLambda<0"
#pair1 = "topTrkLambda*botTrkLambda<0"
#L1L1 = "&&topHasL1&&botHasL1&&topHasL2&&botHasL2"
#Chi2 = "&&(topClY-topTrkEcalY)>-10&&(topClY-topTrkEcalY)<10&&(botClY-botTrkEcalY)<10&&(botClY-botTrkEcalY)>-10"
#Chi2 = ""
#Chi2 = "&&topMatchChisq+botMatchChisq<10"
#time=""
#time = "&&abs(topTrkT-botTrkT)<2"
#isolation = "&&min(topMinPositiveIso+0.5*(topTrkZ0+0.5*topPY/topP)*sign(topPY),botMinPositiveIso+0.5*(botTrkZ0+0.5*botPY/botP)*sign(botPY))>0"
#asymmetry = ""
#doca = "&&atan2(sqrt(topPX*topPX + topPY*topPY),topPZ)+atan2(sqrt(botPX*botPX + botPY*botPY),botPZ)>0.040&&atan2(sqrt(topPX*topPX + topPY*topPY),topPZ)+atan2(sqrt(botPX*botPX + botPY*botPY),botPZ)<0.048&&atan2(sqrt(topPX*topPX + topPY*topPY),topPZ)>0.016&&atan2(sqrt(topPX*topPX + topPY*topPY),topPZ)<0.028&&atan2(sqrt(botPX*botPX + botPY*botPY),botPZ)>0.016&&atan2(sqrt(botPX*botPX + botPY*botPY),botPZ)<0.028"
#energy = "&&topP<2.3*0.75&&botP<2.3*0.75"
#rad = "&&uncP>0.8*2.3&&uncP<2.3*1.15"

#################################################################################################

######################################### LATEST CUTS #########################################
pair1 = "topTrkLambda*botTrkLambda<0&&isSingle0"
#pair1 = "isPair1&&eleSlope*posSlope<0"
#L1L1 = "&&topHasL1&&botHasL1"
L1L1 = "&&(topHasL1&&botHasL1)&&(topHasL2||botHasL2)"
#Chi2 = "&&(topClY-topTrkEcalY)>-10&&(topClY-topTrkEcalY)<10&&(botClY-botTrkEcalY)<10&&(botClY-botTrkEcalY)>-10"
#Chi2 = ""
Chi2 = "&&topMatchChisq+botMatchChisq<10000"
#Chi2 = "&&topMatchChisq+botMatchChisq<30&&topTrkChisq+botTrkChisq<50"
#Chi2 = "&&topMatchChisq+botMatchChisq<40&&topTrkChisq+botTrkChisq<70"
#Chi2 = "&&max(topMatchChisq,botMatchChisq)<10&&bscChisq<10&&bscChisq-uncChisq<5&&max(topTrkChisq,botTrkChisq)<30"
#Chi2 = "&&bscChisq<10&&bscChisq-uncChisq<5&&max(eleTrkChisq,posTrkChisq)<30"
#time=""
time = "&&abs(topTrkT-botTrkT)<2"
#time = "&&abs(topClT-botClT)<2"
#time = "&&max(abs(topClT-topTrkT-151.2),abs(botClT-botTrkT-151.2))<4&&abs(topClT-botClT)<2"
#time = "&&max(abs(eleClT-eleTrkT)-10000,abs(posClT-posTrkT)-10000)<4&&abs(eleClT-posClT)<2"
#isolation = "&&min(eleMinPositiveIso+0.5*(eleTrkZ0+0*elePY/eleP)*sign(elePY),posMinPositiveIso+0.5*(posTrkZ0+0*posPY/posP)*sign(posPY))>0"
#isolation = ""
isolation = "&&min(topMinPositiveIso+0.5*(topTrkZ0+0.5*topPY/topP)*sign(topPY),botMinPositiveIso+0.5*(botTrkZ0+0.5*botPY/botP)*sign(botPY))>0"
asymmetry = ""
#asymmetry = "&&abs(topP-botP)/(topP+botP)<0.4"
#doca  = ""
#doca = "&&posTrkD0+0*posPX/posP<1.5"
#doca = "&&botTrkD0+0.5*botPX/botP<1.5"
#doca = "&&atan2(sqrt(topPX*topPX + topPY*topPY),topPZ)+atan2(sqrt(botPX*botPX + botPY*botPY),botPZ)>0.040&&atan2(sqrt(topPX*topPX + topPY*topPY),topPZ)+atan2(sqrt(botPX*botPX + botPY*botPY),botPZ)<0.048&&atan2(sqrt(topPX*topPX + topPY*topPY),topPZ)>0.016&&atan2(sqrt(topPX*topPX + topPY*topPY),topPZ)<0.028&&atan2(sqrt(botPX*botPX + botPY*botPY),botPZ)>0.016&&atan2(sqrt(botPX*botPX + botPY*botPY),botPZ)<0.028"
doca = "&&atan2(sqrt(topPX*topPX + topPY*topPY),topPZ)+atan2(sqrt(botPX*botPX + botPY*botPY),botPZ)<0.048&&atan2(sqrt(topPX*topPX + topPY*topPY),topPZ)+atan2(sqrt(botPX*botPX + botPY*botPY),botPZ)>0.030"
#energy = ""
energy = "&&topP<2.3*0.75&&botP<2.3*0.75"
rad = "&&bscP>0.75*2.3&&bscP<2.3*1.15"
########################################################################################################


leg = TLegend(0.5,0.5,0.9,0.9)
#leg = TLegend(0.1,0.5,0.5,0.9)

#outfile.cd()

# pair1 + opposite volume
events1 = events.Clone("")
events1.SetLineColor(1)
#events1.Draw(massVar+">>(200,0.03,0.1)",pair1,"")
events1.Draw(massVar+">>(200,0.03,0.1)",pair1,"")
#events1.Draw("max(abs(eleClT-eleTrkT),abs(posClT-posTrkT))>>(200,9990,10010)","","")
leg.AddEntry(events1,"opposite volume")
leg.Draw("")

#outfile.cd()

# elastics/FEE
events2 = events.Clone("")
events2.SetLineColor(2)
events2.Draw(massVar,pair1+energy,"same")
#events2.Draw(massVar,pair1+energy)
leg.AddEntry(events2,"+ FEE")
leg.Draw("same")

#L1L1 cut
events3 = events.Clone("")
events3.SetLineColor(3)
events3.Draw(massVar,pair1+energy+L1L1,"same")
#events3.Draw(massVar,pair1+energy+L1L1)
leg.AddEntry(events3,"+ L1L1")
leg.Draw("same")

# +Timing cuts
events4 = events.Clone("")
events4.SetLineColor(4)
#events4.Draw(massVar+">>(200,0.03,0.1)",pair1+energy+L1L1+time,"")
events4.Draw(massVar,pair1+energy+L1L1+time,"")
leg.AddEntry(events4,"+ timing")
leg.Draw("")

# +isolation cut
events5 = events.Clone("")
events5.SetLineColor(5)
events5.Draw(massVar,pair1+energy+L1L1+time+isolation,"same")
leg.AddEntry(events5,"+ isolation")
leg.Draw("same")

# +momentum asymmetry
#events6 = events.Clone("")
#events6.SetLineColor(6)
#events6.Draw(massVar,pair1+energy+L1L1+time+isolation+asymmetry,"same")
#leg.AddEntry(events6,"+ momentum asymmetry")
#leg.Draw("same")

# +theta-theta (formerly positron DOCA)
events6 = events.Clone("")
events6.SetLineColor(6)
events6.Draw(massVar,pair1+energy+L1L1+time+isolation+asymmetry+doca,"same")
leg.AddEntry(events6,"+ theta sum")
leg.Draw("same")

# +Chi2
events7 = events.Clone("")
events7.SetLineColor(7)
events7.Draw(massVar,pair1+energy+L1L1+time+isolation+asymmetry+doca+Chi2,"same")
leg.AddEntry(events7,"+ matching")
leg.Draw("same")

# +radiative cut
events8 = events.Clone("")
events8.SetLineColor(8)
#events9.GetXaxis().SetTitle("mass[GeV]")
events8.Draw(massVar,pair1+energy+L1L1+time+isolation+asymmetry+doca+Chi2+rad,"same")
#c.Print(remainder[0]+".pdf","Title:cutMass")
#events9.Write()
leg.AddEntry(events8,"+ momentum sum")
leg.Draw("same")
c.Print(sys.argv[1]+".pdf","Title:"+massVar)

cutEvents = events8.Clone("")
outfile = TFile(remainder[0]+".root","RECREATE")
cutEvents.Draw(massVar+">>cutMass(200,0.03,0.1)",pair1+energy+L1L1+time+isolation+asymmetry+doca+Chi2+rad,"")
cutHist = gDirectory.Get("cutMass")
cutHist.Draw("same")
cutHist.Write()

#outfile = TFile(remainder[0]+".root","RECREATE")

#inFileData = TFile(remainder[2])
#eventsData = inFileData.Get("ntuple")
#eventsData.SetWeight(1000/(112.166690534e9/74/4097)) # Data XS (mb)

#cutEventsData = eventsData.Clone("")
#cutEventsData.Draw("mRefitUnc>>cutMass2(200,0.03,0.1)",pair1+energy+L1L1+time+isolation+asymmetry+doca+Chi2+rad+"&&isSingle0","same")
#cutEventsData.Draw(massVar+">>cutMass2(200,0.03,0.1)",pair1+energy+L1L1+time+isolation+asymmetry+doca+Chi2+rad+"&&isSingle0","same")
#eventsData.Draw("mRefitUnc",pair1+energy+L1L1+time+isolation+asymmetry+doca+Chi2+rad+"&&isSingle0","same")
#eventsData.Draw(massVar,pair1+energy+L1L1+time+isolation+asymmetry+doca+Chi2+rad+"&&isSingle0","same")

#eventsData.Draw("mRefitUnc>>cutMass(200,0.03,0.1)",pair1+energy+L1L1+time+isolation+asymmetry+doca+Chi2+rad+"&&isSingle0","same")
#cutHistData = gDirectory.Get("cutMass")
#cutHistData.Draw("same")
#cutHistData.Write()
#cutHist.Write()
c.Print(sys.argv[1]+".pdf","Title:"+massVar)

#outfile = TFile(remainder[0]+".root","RECREATE")

#outfile.draw(events8,200,0.03,0.1)
#gStyle.SetXaxisTitle("pair invariant mass [GeV]")
#events9.GetXaxis().SetTitle("pair invariant mass [GeV]")
#events9.GetYaxis().SetTitle("cross-section [mb/GeV]")

#c.Print(sys.argv[1]+".pdf)","Title:"+massVar)
#outfile = TFile(sys.argv[1]+".root","RECREATE")
#outfile.cd()
#events.SetLineColor(1)
#events.Draw("triM>>mass(200,0,0.2)","max(eleTrkChisq,posTrkChisq)<15&&max(eleP,posP)<0.85&&((tarVX-0.0113)**2/0.04)+((tarVY-0.003324)**2/0.0025)<1&&tarChisq<10&&tarP>0.8","same")
#massHist = gDirectory.Get("mass")
#massHist.Write()
#print remainder[1:]
#print remainder[1:]
#chain = TChain("ntuple")
#for i in remainder[1:]:
#        chain.Add(i,0)
#print chain.GetEntries()
#outFile = TFile(remainder[0],"RECREATE")
#events = chain.CopyTree(events9)
#print events9.GetEntries()
#events9.Write("ntuple",TTree.kOverwrite)
#outfile.Write(events,TTree.kOverwrite)
#c.Print(remainder[1]+".pdf]")

#c.Print(sys.argv[0]+".pdf]","Title:"+massVar)
#c.Print(remainder[0]+".pdf","Title:"+massVar)
#outfile = TFile(sys.argv[1]+".root","RECREATE")
outfile.Write()
outfile.Close()
sys.exit(0)
