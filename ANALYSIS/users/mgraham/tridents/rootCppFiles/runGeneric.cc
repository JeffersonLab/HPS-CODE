void runGeneric(int runtype=2){
  gROOT->ProcessLine(".L lookAtHits.C");  
  TChain* myntp=new TChain("HPS_Event","HPS_Event");
    
  if(runtype==0){
    lookAtHits test;
    test.Loop();
  }    else if(runtype==1) { //data    
    TString infile="/nfs/slac/g/hps3/users/mgraham/EngRun2015/pass1/dst/hps_005772.*";
    myntp->Add(infile);
    lookAtHits test(myntp);
    test.Loop("data-hit-time.root",1);
  } else if(runtype==2){//tritrig-beam-tri
    TString infile="/nfs/slac/g/hps3/users/mgraham/EngRun2015/mc/tritrig-beam-tri/dst/*pairs1*.root";
    myntp->Add(infile);
    lookAtHits test(myntp);
    test.Loop("tritrig-beam-tri-hit-time.root",0);
  } else if(runtype==3){//tritrig
    TString infile="/nfs/slac/g/hps3/users/mgraham/EngRun2015/mc/tritrig/dst/*20150805*pairs1*.root";
    myntp->Add(infile);
    lookAtHits test(myntp);
    test.Loop("tritrig-hit-time.root",0);
  } else if(runtype==4){//beam-tri
    TString infile="/nfs/slac/g/hps3/users/mgraham/EngRun2015/mc/beam-tri/dst/*pairs1*.root";
    myntp->Add(infile);
    lookAtHits test(myntp);
    test.Loop("beamtri-hit-time.root",0);
  }

  cout<<".....done...."<<endl;

}
