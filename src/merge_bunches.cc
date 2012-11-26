#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdhep_mcfio.h>
#include <string.h>
#include <stdhep_util.hh>

// takes input stdhep file, merges a fixed number of events, and writes to a new stdhep file
int main(int argc,char** argv)
{
	int nevhep;             /* The event number */
	vector<stdhep_entry> new_event;

	if (argc!=4) 
	{
		printf("<input stdhep filename> <output stdhep filename> <number of events per event>\n");
		return 1;
	}
	int n_events;
	int istream = 0;
	int ostream = 1;
	int ilbl;
	StdHepXdrReadInit(argv[1],n_events,istream);
	printf("Reading %d events from %s\n",n_events,argv[1]);

	int n_merge = atoi(argv[3]);
	printf("Writing to %s, %d events per event\n",argv[2],n_merge);
	StdHepXdrWriteOpen(argv[2],argv[2],n_events,ostream);
	StdHepXdrWrite(100,ostream);

	nevhep = 0;

	while (true) {
		for (int i=0;i<n_merge;i++)
		{
			do {
				if (StdHepXdrRead(&ilbl,istream)!=0) {
					printf("End of file\n");
					StdHepXdrEnd(istream);

					StdHepXdrWrite(200,ostream);
					StdHepXdrEnd(ostream);
					return(0);
				}
				if (ilbl!=1)
					printf("ilbl = %d\n",ilbl);
			} while (ilbl!=1);

			read_stdhep(&new_event);
		}

		write_stdhep(&new_event,nevhep);
		StdHepXdrWrite(ilbl,ostream);
		nevhep++;
	}
}

