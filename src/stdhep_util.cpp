#include <stdhep_util.hh>
#include <stdhep_mcfio.h>
#include <math.h>
#include <stdhep.h>
#include <stdio.h>

//hepevt hepevt_;
bool xdr_init_done = false;

int read_stdhep(vector<stdhep_entry> *new_event)
{
	int offset = new_event->size();
	for (int i = 0;i<hepevt_.nhep;i++)
	{
		struct stdhep_entry *temp = new struct stdhep_entry;
		temp->isthep = hepevt_.isthep[i];
		temp->idhep = hepevt_.idhep[i];
		for (int j=0;j<2;j++) temp->jmohep[j] = hepevt_.jmohep[i][j]+offset;
		for (int j=0;j<2;j++) temp->jdahep[j] = hepevt_.jdahep[i][j]+offset;
		for (int j=0;j<5;j++) temp->phep[j] = hepevt_.phep[i][j];
		for (int j=0;j<4;j++) temp->vhep[j] = hepevt_.vhep[i][j];
		new_event->push_back(*temp);
	}
	return hepevt_.nevhep;
}

void write_stdhep(vector<stdhep_entry> *new_event, int nevhep)
{
	hepevt_.nhep = new_event->size();
	hepevt_.nevhep = nevhep;
	vector<stdhep_entry>::iterator it;
	for (int i = 0; i<new_event->size(); i++)
	{
		struct stdhep_entry temp = new_event->at(i);
		hepevt_.isthep[i] = temp.isthep;
		hepevt_.idhep[i] = temp.idhep;
		for (int j=0;j<2;j++) hepevt_.jmohep[i][j] = temp.jmohep[j];
		for (int j=0;j<2;j++) hepevt_.jdahep[i][j] = temp.jdahep[j];
		for (int j=0;j<5;j++) hepevt_.phep[i][j] = temp.phep[j];
		for (int j=0;j<4;j++) hepevt_.vhep[i][j] = temp.vhep[j];
	}
	new_event->clear();
}

void add_filler_particle(vector<stdhep_entry> *new_event) //add a 10 MeV photon in the beam direction
{
	struct stdhep_entry *temp = new struct stdhep_entry;
	temp->isthep = 0; //stable particle
	temp->idhep = 22; //photon
	for (int j=0;j<2;j++) temp->jmohep[j] = 0;
	for (int j=0;j<2;j++) temp->jdahep[j] = 0;
	for (int j=0;j<5;j++) temp->phep[j] = 0.0;
	temp->phep[0]+=0.1*sin(0.0305); //30.5 mrad in +x direction
	temp->phep[2]+=0.1*cos(0.0305);
	temp->phep[3]+=0.1;
	for (int j=0;j<4;j++) temp->vhep[j] = 0.0;
	temp->vhep[2]+=0.1; //0.1 mm after target
	new_event->push_back(*temp);
}

int open_read(char *filename, int istream, int n_events)
{
	printf("Reading from %s; expecting %d events\n",filename,n_events);
	if (xdr_init_done)
		StdHepXdrReadOpen(filename,n_events,istream);
	else
	{
		StdHepXdrReadInit(filename,n_events,istream);
		xdr_init_done = true;
	}
	return n_events;
}

void open_write(char *filename, int ostream, int n_events)
{
	printf("Writing to %s; expecting %d events\n",filename, n_events);
	if (xdr_init_done)
		StdHepXdrWriteOpen(filename,filename,n_events,ostream);
	else
	{
		StdHepXdrWriteInit(filename,filename,n_events,ostream);
		xdr_init_done = true;
	}
	StdHepXdrWrite(100,ostream);
}


bool read_next(int istream)
{
	int ilbl;
	do {
		if (StdHepXdrRead(&ilbl,istream)!=0) {
			printf("End of file\n");
			return false;
		}
		if (ilbl!=1)
			printf("ilbl = %d\n",ilbl);
	} while (ilbl!=1);
	return true;
}

void close_write(int ostream)
{
	StdHepXdrWrite(200,ostream);
	StdHepXdrEnd(ostream);
}

void write_file(int ostream)
{
	StdHepXdrWrite(1,ostream);
}

void close_read(int istream)
{
	StdHepXdrEnd(istream);
}

void print_entry(stdhep_entry entry)
{
	printf("isthep = %d\tidhep = %d\t",entry.isthep,entry.idhep);
	for (int i=0;i<2;i++) printf("jmohep[%d] = %d\t",i,entry.jmohep[i]);
	//	printf("\n");
	for (int i=0;i<2;i++) printf("jdahep[%d] = %d\t",i,entry.jdahep[i]);
	printf("\n");
	for (int i=0;i<5;i++) printf("phep[%d] = %f\t",i,entry.phep[i]);
	printf("\n");
	for (int i=0;i<4;i++) printf("vhep[%d] = %f\t",i,entry.vhep[i]);
	printf("\n");
}
