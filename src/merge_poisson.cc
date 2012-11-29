#include <stdio.h>
#include <stdlib.h>
#include <math.h>
//#include <stdhep.h>
//#include <stdhep_mcfio.h>
#include <string.h>
#include <stdarg.h>
#include <stdhep_util.hh>

#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>

// takes input stdhep files, merges a Poisson-determined number of events per event into a new stdhep file
int main(int argc,char** argv)
{
	int nevhep;             /* The event number */
	vector<stdhep_entry> new_event;

	double poisson_mu = 1.0;
	int output_n = 500000;

	int c;

	while ((c = getopt(argc,argv,"hn:m:")) !=-1)
		switch (c)
		{
			case 'h':
				printf("-h: print this help\n");
				printf("-m: mean number of events in an event\n");
				return(0);
				break;
			case 'm':
				poisson_mu = atof(optarg);
				break;
			case 'n':
				output_n = atoi(optarg);
				break;
			case '?':
				printf("Invalid option or missing option argument; -h to list options\n");
				return(1);
			default:
				abort();
		}


	if ( argc-optind <2 )
	{
		printf("<input stdhep filenames> <output stdhep basename>\n");
		return 1;
	}

	//initialize the RNG
	const gsl_rng_type * T;
	gsl_rng * r;
	gsl_rng_env_setup();

	T = gsl_rng_mt19937;
	r = gsl_rng_alloc (T);
	gsl_rng_set(r,0);

	printf("Using mu=%f for Poisson\n",poisson_mu);

	int n_events;
	int istream = 0;
	int ostream = 1;
	int ilbl;

	open_read(argv[1],istream);

	open_write(argv[2],ostream,output_n);

	nevhep = 0;

	while (true) {
		for (int i=0;i<gsl_ran_poisson(r,poisson_mu);i++)
		{
			if (!read_next(istream)) {
				close_read(istream);
					close_write(ostream);
					return(0);
			}

			read_stdhep(&new_event);
		}

		write_stdhep(&new_event,nevhep);
		write_file(ostream);
		nevhep++;
	}
}

