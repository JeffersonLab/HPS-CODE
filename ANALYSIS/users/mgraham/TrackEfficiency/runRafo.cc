void runRafo(){
  
  gROOT->ProcessLine(".L rafosNtuple.C++");

  // data by default
  //  g=rafosNtuple();
  //g.Loop("plots/");


  // tritrig
  
  TFile f("tr_and_cl_Root_tri_trig_1000.root");
  TTree* tree=(TTree*) f.Get("tr1");
  g=rafosNtuple(tree);
  g.Loop("plots-mc-superFid-ECalEnergyPositionCut/");
  
  /*  
    TFile f("tr_and_cl_Root__5772.root");
    TTree* tree=(TTree*) f.Get("tr1");
    g=rafosNtuple(tree);
    g.Loop("plots-nonskimmed/");
  */
  /*
    TFile f("tr_and_cl_Root__5772.root");
    TTree* tree=(TTree*) f.Get("tr1");
    g=rafosNtuple(tree);
    g.Loop("plots-nonskimmed-superFid-ECalEnergyPositionCut/");
  */ 
  /*
    gROOT->ProcessLine(".L rafosNtupleWABs.C++");
    TFile f("tr_and_cl_Root__5772.root");
    TTree* tree=(TTree*) f.Get("tr1");
    g=rafosNtupleWABs(tree);
    g.Loop("plots-WABs-nonskimmed/");
  */
  /*
  TFile f("tr_and_cl_Root_tri_trig_1000.root");
  TTree* tree=(TTree*) f.Get("tr1");
  g=rafosNtupleWABs(tree);
  g.Loop("plots-WABs-mc/");
  */
}
