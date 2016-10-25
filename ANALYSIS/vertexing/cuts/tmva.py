#!/usr/bin/env python
import sys,os
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, TMVA, TCut
print sys.argv[1]
#tree = TTree("ntuple","data from text tuple "+sys.argv[2])
print sys.argv[2:]
chain = TChain("ntuple")
for i in sys.argv[2:]:
	chain.Add(i)
#chain.Merge(sys.argv[1])

#goodEvents = chain.CopyTree("")
events = chain.CopyTree("uncM>0.03&&uncM<0.04")
#goodEvents = chain.CopyTree("uncM>0.03&&uncM<0.04&&eleP<1.05*0.85&&posP<1.05*0.85&&elePY*posPY<0&&eleP>1.05*0.05&&posP>1.05*0.05&&nPos==1&&uncP<1.05*1.25&&abs(eleClT-posClT)<2&&eleHasL1&&posHasL1&&max(eleMatchChisq,posMatchChisq)<10&&uncP>1.05*0.8&&uncVZ<15")
#badEvents = chain.CopyTree("uncM>0.03&&uncM<0.04&&eleP<1.05*0.85&&posP<1.05*0.85&&elePY*posPY<0&&eleP>1.05*0.05&&posP>1.05*0.05&&nPos==1&&uncP<1.05*1.25&&abs(eleClT-posClT)<2&&eleHasL1&&posHasL1&&max(eleMatchChisq,posMatchChisq)<10&&uncP>1.05*0.8&&uncVZ>15")


TMVA.Tools.Instance()
outFile = TFile(sys.argv[1],"RECREATE")
#factory = TMVA.Factory("TMVAClassification", outFile,":".join(["!V","!Silent","Color","DrawProgressBar","Transformations=I;D;P;G,D","AnalysisType=Classification"]))
factory = TMVA.Factory("TMVAClassification", outFile,":".join(["!V","!Silent","Color","DrawProgressBar","Transformations=I;G,D","AnalysisType=Classification"]))
factory.AddVariable("bscChisq","F")
#factory.AddVariable("min(minL1Iso,20.0)","F")
factory.AddVariable("1/minL1Iso","F")
#factory.AddVariable("abs(uncPY/uncP)","F")
#factory.AddVariable("abs(uncPX/uncP)","F")
#factory.AddVariable("eleTrkChisq","F")
#factory.AddVariable("posTrkChisq","F")
#factory.AddVariable("max(eleTrkChisq,posTrkChisq)","F")
#factory.AddVariable("eleTrkChisq+posTrkChisq","F")
sigCut=TCut("abs(uncVZ)<10")
bkgCut=TCut("uncVZ>15")
#factory.AddSignalTree(events)
#factory.AddBackgroundTree(events)
factory.SetInputTrees(events,sigCut,bkgCut)

#factory.AddSignalTree(goodEvents)
#factory.AddBackgroundTree(badEvents)

factory.BookMethod(TMVA.Types.kCuts,"Cuts","FitMethod=GA:VarProp=FMin")
#factory.BookMethod(TMVA.Types.kCuts,"Cuts","FitMethod=GA:VarProp=FMin:CutRangeMin[4]=5:CutRangeMax[4]=100:Steps=100")
#factory.BookMethod(TMVA.Types.kCuts,"Cuts","FitMethod=GA:VarProp=FMin:VarTransform=N_Background")
factory.BookMethod(TMVA.Types.kFisher,"Fisher","")
#factory.BookMethod(TMVA.Types.kFisher,"FisherG","VarTransform=G_Background")
factory.BookMethod(TMVA.Types.kFisher,"FisherGD","VarTransform=G_Background,D_Background")
#factory.BookMethod(TMVA.Types.kLikelihood,"Likelihood","")
#factory.BookMethod(TMVA.Types.kLikelihood,"LikelihoodG","VarTransform=G_Background")
#factory.BookMethod(TMVA.Types.kLikelihood,"LikelihoodGD","VarTransform=G_Background,D_Background")
#factory.BookMethod(TMVA.Types.kKNN,"kNN","")
#factory.BookMethod(TMVA.Types.kLD,"LD","")
#factory.BookMethod(TMVA.Types.kFisher,"FisherM","Method=Mahalanobis")
#factory.BookMethod(TMVA.Types.kFDA,"FDA","Formula=(0)+(1)*x0+(2)*x1+(3)*x2+(4)*x3+(5)*x4:ParRanges=(-2,2);(-1,1);(-1,1);(-10,1);(-10,1);(-1,1):FitMethod=GA:Converger=MINUIT")
#factory.BookMethod(TMVA.Types.kFDA,"FDA","Formula=(0)+(1)*x0+(2)*x1+(3)*x2+(4)*x3+(5)*x4:ParRanges=(-2,2);(-1,1);(-1,1);(-10,1);(-10,1);(-1,1):FitMethod=MINUIT:UseImprove:FitStrategy=2:UseMinos:MaxCalls=1000:Tolerance=0.00000001")
factory.BookMethod(TMVA.Types.kFDA,"FDA","Formula=(0)+(1)*x0+(2)*x1:ParRanges=(-2,2);(-1,1);(-1,1):FitMethod=MINUIT")
#factory.BookMethod(TMVA.Types.kFDA,"FDA2","Formula=(0)+(1)*x0^(3)+(2)*x1^(4):ParRanges=(-2,2);(-1,1);(-1,1);(0,5);(0,5):FitMethod=SA")
#factory.BookMethod(TMVA.Types.kFDA,"FDA","Formula=(0)+(1)*x0^(6)+(2)*x1^(7)+(3)*x2^(8)+(4)*x3^(9)+(5)*x4^(10):ParRanges=(-2,2);(-1,1);(-1,1);(-10,1);(-10,1);(-1,1);(0,3);(0,3);(0,3);(0,3);(0,3):FitMethod=MINUIT")
#factory.BookMethod(TMVA.Types.kSVM,"SVM","")
#factory.BookMethod(TMVA.Types.kBDT,"BDT","")
factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()
#sys.exit(0)
outFile.Close()
os._exit(1)

#print tree.ReadFile(sys.argv[2])
#tree.Write()

