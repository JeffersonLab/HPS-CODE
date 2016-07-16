all: upperlimit.so SimpleExample
clean:
	rm upperlimit.so SimpleExample
upperlimit.so:
	f2py -c -m upperlimit UpperLim.pyf UpperLim.f y_vs_CLf.f CMaxinf.f ConfLev.f Cinf.f CERN_Stuff2.f
SimpleExample:
	f77 -o SimpleExample SimpleExample.f UpperLim.f CMaxinf.f ConfLev.f Cinf.f y_vs_CLf.f CERN_Stuff2.f
