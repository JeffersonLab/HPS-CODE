#include <stdhep.h>
#include <vector>
using namespace std;

struct stdhep_entry {
	int isthep;     /* status code */
	int idhep;      /* The particle id */
	int jmohep[2];    /* The position of the mother particle */
	int jdahep[2];    /* Position of the first daughter... */
	double phep[5];    /* 4-Momentum, mass */
	double vhep[4];    /* Vertex information */
};

void read_stdhep(vector<stdhep_entry> *new_event);
void write_stdhep(vector<stdhep_entry> *new_event, int nevhep);
