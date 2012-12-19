#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <stdhep_util.hh>

void rotate_entry(stdhep_entry *entry, double theta)
{
	double px = entry->phep[0];
	double pz = entry->phep[2];
	double vx = entry->vhep[0];
	double vz = entry->vhep[2];
	entry->phep[0] = px*cos(theta) - pz*sin(theta);
	entry->phep[2] = px*sin(theta) + pz*cos(theta);
	entry->vhep[0] = vx*cos(theta) - vz*sin(theta);
	entry->vhep[2] = vx*sin(theta) + vz*cos(theta);
}

// takes input stdhep file, merges a fixed number of events, and writes to a new stdhep file
int main(int argc,char** argv)
{
	int nevhep;             /* The event number */
	vector<stdhep_entry> new_event;

	if (argc!=4) 
	{
		printf("<input stdhep filename> <output stdhep filename> <rotation around Y in radians>\n");
		return 1;
	}
	int n_events;
	int istream = 0;
	int ostream = 1;

	n_events = open_read(argv[1],istream);

	open_write(argv[2],ostream,n_events);

	double theta = atof(argv[3]);
	printf("Rotating by %f radians\n",theta);

	nevhep = 0;

	while (true) {
		if (!read_next(istream)) {
			close_read(istream);
			close_write(ostream);
			return(0);
		}
		read_stdhep(&new_event);

		for (int i=0;i<new_event.size();i++)
			rotate_entry(&(new_event[i]),theta);

		write_stdhep(&new_event,nevhep+1);
		write_file(ostream);
		nevhep++;
	}
}

