

// This removes the crystals in the electron hole
bool ishole(const int x,const int y)
{
    return (x>12 && x<22 && y>3 && y<6);
}
// Loads the initial ROOT file containing the raw data
struct fadc_t
{
  int adc[NX][NY][NSAMP]; // adc value for each time sample
  int pulse[NX][NY];      // adc integrated over first NSAMPINT samples
  float ped[NX][NY];      // pedestal
};
void InitTreeFADC(TTree *t,fadc_t &t_)
{
    if (!t) return;
    t->SetBranchAddress("adc",&t_.adc);
    t->SetBranchAddress("pulse",&t_.pulse);
    t->SetBranchAddress("ped",&t_.ped);
}
TChain *CHAIN=NULL;
fadc_t FADC;
void LoadTree()
{
    if (CHAIN) return;
    CHAIN=chainfiledir("cosmicInput","Tadc");
    InitTreeFADC((TTree*)CHAIN,FADC);
}

//input x in the range [0,45]
//returns x as crystals ix [-23,23]
int calcIX(int xx){
  int ix = xx-23;
  if (xx>=23) ix+=1;
  return ix;
}

//input Y in the range [0,9]
//returns y as crystal iy [-5,5]
int calcIY(int yy){
  int iy = yy-5;
  if (yy>=5) iy+=1;
  return iy;
}
int xy2dbid(int xx, int yy){
  //here, xx, and yy correspond to [0,45] and [0,9]
  int dbid;
  dbid = xx+2*23*(5*2-yy-1)+1;
  int ix = calcIX(xx);
  int iy = calcIY(yy);
  if (iy==1 && ix>-10) dbid -= 9;
  else if(iy==-1 && ix<-10) dbid -= 9;
  else if (iy<0) dbid -= 18;

  return dbid;
}

