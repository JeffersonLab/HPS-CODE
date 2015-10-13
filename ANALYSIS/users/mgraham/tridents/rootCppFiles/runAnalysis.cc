void runAnalysis(int runtype=1,int runNumber=5643){
  gROOT->ProcessLine(".L tridentAnalysis.C");  
  TChain* myntp=new TChain("HPS_Event","HPS_Event");
  if(runtype==0){
    tridentAnalysis test;
    test.Loop();
  }    else if(runtype==1) { //data    
    TString infile="/nfs/slac/g/hps3/users/mgraham/EngRun2015/pass1/dst/hps_00";
    infile+=runNumber;infile+=".*";
    cout<<infile<<endl;
    myntp->Add(infile);
    tridentAnalysis test(myntp);
    TString outfile="data";outfile+=runNumber;outfile+=".root";
    test.Loop(outfile,1);
  } else if(runtype==2){//tritrig-beam-tri
    TString infile="/nfs/slac/g/hps3/users/mgraham/EngRun2015/mc/tritrig-beam-tri/dst/*pairs1*.root";
    myntp->Add(infile);
    tridentAnalysis test(myntp);
    test.Loop("tritrig-beam-tri.root",0);
  } else if(runtype==3){//tritrig
    TString infile="/nfs/slac/g/hps3/users/mgraham/EngRun2015/mc/tritrig/dst/*20150805*pairs1*.root";
    myntp->Add(infile);
    tridentAnalysis test(myntp);
    test.Loop("tritrig.root",0);
  } else if(runtype==4){//beam-tri
    TString infile="/nfs/slac/g/hps3/users/mgraham/EngRun2015/mc/beam-tri/dst/*pairs1*.root";
    myntp->Add(infile);
    tridentAnalysis test(myntp);
    test.Loop("beamtri.root",0);
  }

  cout<<".....done...."<<endl;

}
