#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdhep_mcfio.h>
#include <stdhep.h>
#include <TFile.h>
#include <TH2D.h>
#include <TCanvas.h>
#include <string.h>

// Reads one stdhep file and splits it into multiple files, each of a given length.
int main(int argc,char** argv)
{
	char outputname[200];
	if (argc!=4) 
	{
		printf("<input stdhep filename> <output stdhep filename> <number of events per file>\n");
		return 1;
	}
	int n_events = atoi(argv[3]);
	printf("Reading %d events from %s\n",n_events,argv[1]);
	int istream = 0;
	int ostream = 1;
	int ilbl;
	StdHepXdrReadInit(argv[1],n_events,istream);
	int j = 1;

	while (true) {
		sprintf(outputname,"%s_%d.stdhep",argv[2],j);
		printf("Writing to %s\n",outputname);
		StdHepXdrWriteOpen(outputname,outputname,n_events,ostream);
		StdHepXdrWrite(100,ostream);
		do {
			StdHepXdrRead(&ilbl,istream);
		} while (ilbl==100);

		for (int i=0;i<n_events;i++)
		{
			StdHepXdrRead(&ilbl,istream);
			if (ilbl!=1)
			{
				printf("End of file\n");
				return(0);
			}
			StdHepXdrWrite(ilbl,ostream);
		}
		StdHepXdrWrite(200,ostream);
		StdHepXdrEnd(ostream);
		j++;
	}
}
