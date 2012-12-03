#include <stdio.h>
#include <stdlib.h>
#include <stdhep_mcfio.h>
#include <stdhep.h>
#include <string.h>


// takes input stdhep files, merges one event from each file into a single event in a new stdhep file
int main(int argc,char** argv)
{
	int nevhep;             /* The event number */
	int nhep;               /* The number of entries in this event */
	int isthep[NMXHEP];     /* The Particle id */
	int idhep[NMXHEP];      /* The particle id */
	int jmohep[NMXHEP][2];    /* The position of the mother particle */
	int jdahep[NMXHEP][2];    /* Position of the first daughter... */
	double phep[NMXHEP][5];    /* 4-Momentum, mass */
	double vhep[NMXHEP][4];    /* Vertex information */

	if (argc<3) 
	{
		printf("<output stdhep filename> <input stdhep filenames>\n");
		return 1;
	}
	int n_events;
	int ostream = 0;
	printf("Writing to %s\n",argv[1]);
	StdHepXdrWriteInit(argv[1],argv[1],n_events,ostream);
	StdHepXdrWrite(100,ostream);

	int n_inputs = argc-2;
	for (int i=0;i<n_inputs;i++) {
		int istream = i+1;
		int ilbl;
		StdHepXdrReadOpen(argv[i+2],n_events,istream);
		printf("Reading %d events from %s\n",n_events,argv[i+2]);
	}

	nevhep = 0;

	while (true) {
		nhep = 0;
		for (int i=0;i<n_inputs;i++)
		{
			int istream = i+1;
			int ilbl;
			do {
				if (StdHepXdrRead(&ilbl,istream)!=0) {
					printf("End of file %s\n",argv[i+2]);
					StdHepXdrWrite(200,ostream);
					StdHepXdrEnd(ostream);
					for (int i=0;i<n_inputs;i++)
					{
						int istream = i+1;
						StdHepXdrEnd(istream);
					}
					return(0);
				}
				if (ilbl!=1)
					printf("ilbl = %d\n",ilbl);
			} while (ilbl!=1);

			//if (nevhep!=hepevt_.nevhep) printf("Expected nevhep = %d, got %d in file %s\n",nevhep,hepevt_.nevhep,argv[i+2]);

			for (int i = 0;i<hepevt_.nhep;i++)
			{
				isthep[nhep+i] = hepevt_.isthep[i];
				idhep[nhep+i] = hepevt_.idhep[i];
				for (int j=0;j<2;j++) jmohep[nhep+i][j] = hepevt_.jmohep[i][j];
				for (int j=0;j<2;j++) jdahep[nhep+i][j] = hepevt_.jdahep[i][j];
				for (int j=0;j<5;j++) phep[nhep+i][j] = hepevt_.phep[i][j];
				for (int j=0;j<4;j++) vhep[nhep+i][j] = hepevt_.vhep[i][j];
			}
			nhep += hepevt_.nhep;
		}


		hepevt_.nhep = nhep;
		hepevt_.nevhep = nevhep;

		for (int i = 0;i<nhep;i++)
		{
			hepevt_.isthep[i] = isthep[i];
			hepevt_.idhep[i] = idhep[i];
			for (int j=0;j<2;j++) hepevt_.jmohep[i][j] = jmohep[i][j];
			for (int j=0;j<2;j++) hepevt_.jdahep[i][j] = jdahep[i][j];
			for (int j=0;j<5;j++) hepevt_.phep[i][j] = phep[i][j];
			for (int j=0;j<4;j++) hepevt_.vhep[i][j] = vhep[i][j];
		}
		StdHepXdrWrite(1,ostream);
		nevhep++;
	}
}

