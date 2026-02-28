#include "../util/utilities.h"

#define NX 46
#define NY 10
#define NCRY 442

int runPOST=10650;
int runZERO=10115;
int runMAX=10740;

int nGroups=30;

double slopes[442];
double gains[442];

double correctGain(double run,int id){
  double corr=1;
  double gain=gains[id-1];
  corr/=(1+slopes[id-1]*(run-runZERO));
  return corr*gain;
}

void produceGainsIncorporateSlope(){

  ifstream fileSlopes("../ecalSlopes.txt");
  string line,word;
  std::getline(fileSlopes,line);
  
  int id=0;
  while (std::getline(fileSlopes,line)){
   
    istringstream strm(line);
    int counter=0;
  
    double slope;
    while (strm){
      if (!getline( strm, word, ',' )) break;
      if (counter==0) id=atoi(word.c_str());
      if (counter==1) slope=atof(word.c_str());
      counter++;
    }
   
    slopes[id-1]=slope;
  }

  ifstream fileGains("cGlobal_4.txt");
  while (std::getline(fileGains,line)){
    
    istringstream strm(line);
    int counter=0;
   
    double gain;
    while (strm){
      if (!getline( strm, word, ',' )) break;
      if (counter==0) id=atoi(word.c_str());
      if (counter==1) gain=atof(word.c_str());
      counter++;
    }
    
    gains[id-1]=gain;
  }

  
  
  for (int iy=0; iy<NY; iy++) {
    // loop over crystal x
      for (int ix=0; ix<NX; ix++) {
	if (!ishole(ix,iy)){
	  int id = xy2dbid(ix,iy);
	  double gain1=correctGain(runZERO,id);
	  double gain2=correctGain(runMAX,id);
	  cout<<id<<" "<<gain1<<" "<<gain2<<" "<<gain2/gain1<<endl;
	  
	}
      }
  }

  
  
  int deltaRun=(runMAX-runZERO)/nGroups;
  cout<<runMAX-runZERO<<" "<<deltaRun<<endl;                       
  for (int iGroup=0;iGroup<nGroups;iGroup++){

    int firstRun=runZERO+deltaRun*iGroup;
    int lastRun=runZERO+(deltaRun)*(1+iGroup);
    if (iGroup==(nGroups-1)) lastRun=runMAX;

    double middleRun=(firstRun+lastRun)/2.;

    ofstream ofile(Form("%i_%i.txt",firstRun,lastRun));
    
    for (int iy=0; iy<NY; iy++) {
      // loop over crystal x
      for (int ix=0; ix<NX; ix++) {
	if (!ishole(ix,iy)){
	  int id = xy2dbid(ix,iy);
	  double gain=correctGain(middleRun,id);

	  if ((id==153)||(id==275)||(id==334)||(id==267)||(id==198)) gain=0;
	  if ((id==361)&&lastRun<1370) gain=0;
	  
	  ofile<<id<<","<<gain<<endl;
	}
      }
    }
    ofile.close();
  }
}
