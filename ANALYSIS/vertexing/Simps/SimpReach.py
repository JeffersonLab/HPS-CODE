#Simp Rates
#author Matt Solt

import numpy as np
import sys
import array
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1, TH1F, TH2F, TF1, RooDataSet, RooWorkspace, RooFit, RooArgList
sys.argv = tmpargv

def openPDF(outfile,canvas):
	canvas.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	canvas.Print(outfile+".pdf]")

def drawHisto(histo,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
	histo.Draw("COLZ")
	#histo.GetXaxis().SetRangeUser(-5,150)
	#histo.GetYaxis().SetRangeUser(0,1.1)
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)

def saveContour(histo,outfile,canvas,limit,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0,logy=0,logx=0):
	limitLevels = array.array('d')
	limitLevels.append(limit)
	histo.SetContour(1,limitLevels)
	histo.SetTitle(plotTitle)
	histo.GetXaxis().SetTitle(XaxisTitle)
	histo.GetYaxis().SetTitle(YaxisTitle)
	histo.SetStats(stats)
	histo.Draw("cont1")
	canvas.SetLogx(logx)
	canvas.SetLogy(logy)
	canvas.Print(outfile+".pdf")

def saveHisto(histo,outfile,canvas,XaxisTitle="",YaxisTitle="",plotTitle="",stats=0,logy=0,logx=0):
	drawHisto(histo,XaxisTitle,YaxisTitle,plotTitle,stats)
	canvas.SetLogx(logx)
	canvas.SetLogy(logy)
	canvas.Print(outfile+".pdf")

def rate_Ap(m_Ap,eps,N_eff):
	alpha = 1/137.
	return N_eff * m_Ap * alpha * eps**2

def rate_2pi(m_Ap,m_pi,m_V,alpha_D):
	coeff = 2*alpha_D/3 * m_Ap
	pow1 = (1-4*m_pi**2/(m_Ap**2))**(3/2.)
	pow2 = (m_V**2/(m_Ap**2-m_V**2))**2
	return coeff * pow1 * pow2

def rate_Vpi(m_Ap,m_pi,m_V,alpha_D,f_pi,rho,phi):
	x = m_pi/m_Ap
	y = m_V/m_Ap
	pi = 3.14159
	coeff = alpha_D*Tv(rho,phi)/(192*pi**4)
	return coeff * 1/(x**2) * (y**2/(x**2)) * (m_pi/f_pi)**4 * m_Ap*Beta(x,y)**(3/2.)

def br_Vpi(m_Ap,m_pi,m_V,alpha_D,f_pi,rho,phi):
	rate = rate_Vpi(m_Ap,m_pi,m_V,alpha_D,f_pi,rho,phi) + rate_2pi(m_Ap,m_pi,m_V,alpha_D)
	if(2*m_V < m_Ap): rate = rate_Vpi(m_Ap,m_pi,m_V,alpha_D,f_pi,rho,phi) + rate_2pi(m_Ap,m_pi,m_V,alpha_D) + rate_2V(m_Ap,m_V,alpha_D)
	return rate_Vpi(m_Ap,m_pi,m_V,alpha_D,f_pi,rho,phi)/rate

def br_2V(m_Ap,m_pi,m_V,alpha_D,f_pi,rho,phi):
	if(2*m_V >= m_Ap): return 0.
	rate = rate_Vpi(m_Ap,m_pi,m_V1,alpha_D,f_pi,rho,phi) + rate_2pi(m_Ap,m_pi,m_V1,alpha_D) + rate_2V(m_Ap,m_V1,alpha_D)
	return rate_2V(m_Ap,m_V1,alpha_D)/rate

def Tv(rho,phi):
	if rho:
		return 3/4.
	elif phi:
		return 3/2.
	else:
		return 18

def Beta(x,y):
	return (1+y**2-x**2-2*y)*(1+y**2-x**2+2*y)

def rate_2V(m_Ap,m_V,alpha_D):
	r = m_V/m_Ap
	return alpha_D/6 * m_Ap * f(r)

def f(r):
	num = 1 + 16*r**2 - 68*r**4 - 48*r**6
	den = (1-r**2) ** 2
	return num/den * (1-4*r**2)**0.5

def rate_2l(m_Ap,m_pi,m_V,eps,alpha_D,f_pi,m_l,rho):
	alpha = 1/137.
	pi = 3.14159
	coeff = 16*pi*alpha_D*alpha*eps**2*f_pi**2/(3*m_V**2)
	term1 = (m_V**2/(m_Ap**2 - m_V**2))**2
	term2 = (1-4*m_l**2/m_V**2)**0.5
	term3 = 1+2*m_l**2/m_V**2
	const = 1
	if rho:
		const = 2
	return coeff * term1 * term2 * term3 * m_V * const

def ctau(m_Ap,m_pi,m_V,eps,alpha_D,f_pi,m_l,rho):
	hbar_c = 1.973e-13
	return hbar_c / rate_2l(m_Ap,m_pi,m_V,eps,alpha_D,f_pi,m_l,rho)

def Vdistribution(z,targZ,gammact):
	return np.exp(targZ/gammact-1/gammact*z)/gammact

def integrate(minZ,maxZ,n,targZ,gammact,mass,inputFile):
	tot = 0
	zwidth = (maxZ-minZ)/float(n)
	for i in range(0,n):
		z = minZ + (i + 0.5) * zwidth
		tot = tot + InterpolateFromFile(mass,z,inputFile) * Vdistribution(z,targZ,gammact) * zwidth
	return tot

#Function to plot efficiency tests of known masses
def Interpolate(Mass,Z,mass,z,eff):
    iMass = 0
    iZ = 0
    nMass = len(mass)
    nBins = len(z)
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

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input file name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-h: this help message'
    print

scale = 1.0
isL0 = False

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hs:l')

# Parse the command line arguments
for opt, arg in options:
		if opt=='-s':
			scale = float(arg)
		if opt=='-l':
			isL0 = True
		if opt=='-h':
			print_usage()
			sys.exit(0)

gStyle.SetOptStat(0)
gStyle.SetPalette(55)
c = TCanvas("c","c",800,600)

#alpha_D = 0.01
#hbar_c = 1.973e-13
m_l = 0.000000511
Ebeam = 2.3
gamma = 0.5
targetz = 0.5
maxZ = 80.
zcut_count = 0.5
masscut_nsigma = 2.80
masscut_eff = 0.838
reachlimit = 2.3

outfile = remainder[0]
efffile = remainder[1]
tailsfile = TFile(remainder[2])
infile = TFile(remainder[3])
massresfile = TFile(remainder[4])
#radfile = TFile(remainder[5])
promptfile = TFile(remainder[5])

NepsBins = 50
epsmin = -4
epsmax = -2
fpiArr = []
fpiArr.append(3.)
fpiArr.append(4.)
fpiArr.append(4*np.pi)
alphadArr = []
alphadArr.append(0.1)
alphadArr.append(0.01)
alphadArr.append(0.001)
nApMass = 50
massApmin = 0.07
massApmax = 0.139

fitfunc = TF1("fitfunc","[0]*exp( ((x-[1])<[3])*(-0.5*(x-[1])^2/[2]^2) + ((x-[1])>=[3])*(-0.5*[3]^2/[2]^2-(x-[1]-[3])/[4]))",-50,50)
fitfunc.SetParName(0,"Amplitude")
fitfunc.SetParName(1,"Mean")
fitfunc.SetParName(2,"Sigma")
fitfunc.SetParName(3,"Tail Z")
fitfunc.SetParName(4,"Tail length")


w = RooWorkspace("w")
w.factory("{0}[0,0.1]".format("uncM"))
w.factory("uncVZ[-100,100]")
w.factory("uncP[0,10]")
w.factory("cut[0,1]")

w.defineSet("myVars","{0},uncVZ".format("uncM"))

events = infile.Get("cut")
#eventsrad = radfile.Get("ntuple")
eventsprompt = promptfile.Get("cut")
dataset = RooDataSet("data","data",events,w.set("myVars"),"")

w.factory("Gaussian::vtx_model(uncVZ,mean[-50,50],sigma[0,50])")
gauss_pdf = w.pdf("vtx_model")
w.factory("EXPR::gaussExp('exp( ((@0-@1)<@3)*(-0.5*(@0-@1)^2/@2^2) + ((@0-@1)>=@3)*(-0.5*@3^2/@2^2-(@0-@1-@3)/@4))',uncVZ,gauss_mean[-5,-20,20],gauss_sigma[5,1,50],exp_breakpoint[10,0,50],exp_length[3,0.5,20])")
gaussexp_pdf = w.pdf("gaussExp")
w.defineSet("obs_1d","uncVZ")
obs=w.set("obs_1d")
uncVZ = w.var("uncVZ")
uncVZ.setBins(200)
gauss_params = gauss_pdf.getParameters(obs)
gaussexp_params = gaussexp_pdf.getParameters(obs)

Medges = array.array('d')
Epsedges = array.array('d')
for i in range(0,nApMass+1):
    Medges.append(massApmin+(i-0.5)*(massApmax-massApmin)/float(nApMass-1))
for j in range(0,NepsBins+1):
	Epsedges.append(10**(epsmin+(j-0.5)*(epsmax-epsmin)/float(NepsBins-1)))

ZRes = TH1F("ZRes","ZRes",nApMass,massApmin*0.6,massApmax*0.6)
ZCut = TH1F("ZCut","ZCut",nApMass,massApmin*0.6,massApmax*0.6)


#Make more intermediate plots
#Cut on A' tuples
#Figure out cuts
#Fix Generate Efficiency Code.
#Obtain Mass Resolution
#Calculate gamma correctly
#Normalize properly
#Radiative Fraction
#Cleanup Code
#Cleanup Plots


zresArr = []
zcutArr = []
openPDF(outfile,c)
for i in range(0,len(fpiArr)):
	for j in range(0,len(alphadArr)):
		alphaD = alphadArr[j]
		ApProduced = TH2F("ApProduced","ApProduced",nApMass,Medges,NepsBins,Epsedges)
		VProducedRho = TH2F("VProducedRho","VProducedRho",nApMass,Medges,NepsBins,Epsedges)
		detectableRho = TH2F("detectableRho","detectableRho",nApMass,Medges,NepsBins,Epsedges)
		VProducedPhi = TH2F("VProducedPhi","VProducedPhi",nApMass,Medges,NepsBins,Epsedges)
		detectablePhi = TH2F("detectablePhi","detectablePhi",nApMass,Medges,NepsBins,Epsedges)
		for k in range(0,nApMass):
			massAp = (massApmax - massApmin)/float(nApMass - 1) * k + massApmin
			massV = 0.6*massAp
			massPi = massAp/3.
			fPi = massPi/fpiArr[i]
			massVres = massresfile.Get("mres").GetFunction("pol1").Eval(massV)
			breakz = tailsfile.Get("breakz").GetFunction("pol3").Eval(massV)
			length = tailsfile.Get("length").GetFunction("pol3").Eval(massV)

			frame = uncVZ.frame()
			dataInRange = dataset.reduce(obs,"abs({0}-{1})<{2}/2*{3}".format("uncM",massV,masscut_nsigma,massVres))
			binnedData = dataInRange.binnedClone()
			binnedData.plotOn(frame)
			mean = binnedData.mean(uncVZ)
			sigma = binnedData.sigma(uncVZ)
			uncVZ.setRange("fitRange",mean-2*sigma,mean+2*sigma)
			gauss_params.setRealValue("mean",mean)
			gauss_params.setRealValue("sigma",sigma)
			gauss_pdf.fitTo(binnedData,RooFit.Range("fitRange"),RooFit.PrintLevel(-1))
			mean = gauss_params.getRealValue("mean")
			sigma = gauss_params.getRealValue("sigma")
			gaussexp_params.setRealValue("gauss_mean",mean)
			gaussexp_params.setRealValue("gauss_sigma",sigma)
			gaussexp_params.setRealValue("exp_breakpoint",breakz)
			gaussexp_params.setRealValue("exp_length",length)
			w.var("gauss_mean").setConstant(True)
			w.var("gauss_sigma").setConstant(True)
			w.var("exp_breakpoint").setConstant(True)
			w.var("exp_length").setConstant(True)
			func = gaussexp_pdf.createCdf(obs).asTF(RooArgList(obs),RooArgList(gaussexp_params))
			zcut_frac = zcut_count/(dataInRange.sumEntries()*scale)
			zcut = func.GetX(1-zcut_frac,0,50)
			if(isL0): zcut = zcut * 0.5
			ZRes.SetBinContent(k+1,sigma)
			ZCut.SetBinContent(k+1,zcut)
			for l in range(0,NepsBins):
				logeps = (epsmax - epsmin)/float(NepsBins - 1) * l + epsmin
				eps = 10**logeps
				ct = ctau(massAp,massPi,massV,eps,alphaD,fPi,m_l,False)
				gammact = ct * Ebeam * gamma/massV
				deltaM = 0.001
				eventsprompt.Draw("{0}>>MassAp(100,{1}-{2},{1}+{2})".format("tarM",massAp,0.5*deltaM),"abs({0}-{1})<{2}".format("tarM",massAp,0.5*deltaM),"")
				num_pairs = gDirectory.Get("MassAp").GetEntries() * scale
				rad_frac = 0.15
				num_rad = num_pairs * rad_frac
				#eventsrad.Draw("{0}>>massAp(100,{1}-{2},{1}+{2})".format("triPair1M",massAp,0.5*deltaM),"abs({0}-{1})<{2}".format("triPair1M",massAp,0.5*deltaM),"")
				#num_rad = gDirectory.Get("massAp").GetEntries() * 7089/(1.92 * 99) #* scale
				ap_yield = 3*np.pi/(2*(1/137.0))*num_rad*(massAp/deltaM)*eps**2
				brVpi_rho = br_Vpi(massAp,massPi,massV,alphaD,fPi,True,False)
				brVpi_phi = br_Vpi(massAp,massPi,massV,alphaD,fPi,False,True)
				rho_yield = brVpi_rho * ap_yield
				phi_yield = brVpi_phi * ap_yield
				ApProduced.Fill(massAp,eps,ap_yield)
				VProducedRho.Fill(massAp,eps,rho_yield)
				detectableRho.Fill(massAp,eps,rho_yield * integrate(zcut,maxZ,1000,targetz,gammact,massV,efffile))
				VProducedPhi.Fill(massAp,eps,phi_yield)
				detectablePhi.Fill(massAp,eps,phi_yield * integrate(zcut,maxZ,1000,targetz,gammact,massV,efffile))
		#Save Histos
		saveHisto(ApProduced,outfile,c,"A' mass [GeV]","eps","Number of A's Produced, alpha_d = {0}, mPi/fPi = {1}, mA':mV:mPi = 3:1.8:1".format(alphaD,fpiArr[i]),0,1,1)
		saveHisto(VProducedRho,outfile,c,"A' mass [GeV]","eps","Number of Dark Rhos Produced, alpha_d = {0}, mPi/fPi = {1}, mA':mV:mPi = 3:1.8:1".format(alphaD,fpiArr[i]),0,1,1)
		saveHisto(detectableRho,outfile,c,"A' mass [GeV]","eps","Number of Dark Rhos Detectable, alpha_d = {0}, mPi/fPi = {1}, mA':mV:mPi = 3:1.8:1".format(alphaD,fpiArr[i]),0,1,1)
		saveContour(detectableRho,outfile,c,reachlimit,"A' mass [GeV]","eps","Dark Rho Reach, alpha_d = {0}, mPi/fPi = {1}, mA':mV:mPi = 3:1.8:1".format(alphaD,fpiArr[i]),0,1,1)
		saveHisto(VProducedPhi,outfile,c,"A' mass [GeV]","eps","Number of Dark Phis Produced, alpha_d = {0}, mPi/fPi = {1}, mA':mV:mPi = 3:1.8:1".format(alphaD,fpiArr[i]),0,1,1)
		saveHisto(detectablePhi,outfile,c,"A' mass [GeV]","eps","Number of Dark Phis Detectable, alpha_d = {0}, mPi/fPi = {1}, mA':mV:mPi = 3:1.8:1".format(alphaD,fpiArr[i]),0,1,1)
		saveContour(detectablePhi,outfile,c,reachlimit,"A' mass [GeV]","eps","Dark Phi Reach, alpha_d = {0}, mPi/fPi = {1}, mA':mV:mPi = 3:1.8:1".format(alphaD,fpiArr[i]),0,1,1)
		del ApProduced
		del VProducedRho
		del detectableRho
		del VProducedPhi
		del detectablePhi

saveHisto(ZRes,outfile,c,"mass V [GeV]","z resolution [mm]""Vertex Z Resolution")
saveHisto(ZCut,outfile,c,"mass V [GeV]","z cut [mm]","Z Cut")

closePDF(outfile,c)