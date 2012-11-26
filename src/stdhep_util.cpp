#include <stdhep_util.hh>


void read_stdhep(vector<stdhep_entry> *new_event)
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
}

void write_stdhep(vector<stdhep_entry> *new_event, int nevhep)
{
	hepevt_.nhep = new_event->size();
	hepevt_.nevhep = nevhep;
	vector<stdhep_entry>::iterator it;
	for (int i = 0; i<new_event->size(); i++)
	{
		struct stdhep_entry temp = new_event->front();
		hepevt_.isthep[i] = temp.isthep;
		hepevt_.idhep[i] = temp.idhep;
		for (int j=0;j<2;j++) hepevt_.jmohep[i][j] = temp.jmohep[j];
		for (int j=0;j<2;j++) hepevt_.jdahep[i][j] = temp.jdahep[j];
		for (int j=0;j<5;j++) hepevt_.phep[i][j] = temp.phep[j];
		for (int j=0;j<4;j++) hepevt_.vhep[i][j] = temp.vhep[j];
	}
	new_event->clear();
}
