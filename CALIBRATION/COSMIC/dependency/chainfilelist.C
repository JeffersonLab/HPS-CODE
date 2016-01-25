#include <fstream>
#include <string>
#include <iostream>
#include "TChain.h"
#include "TSystem.h"
#include "TTime.h"
#include "TString.h"
#include "ProgressMeter.C"

//#define __CHAINTMPDIR__ "/tmp"
#define __CHAINTMPDIR__ "/home/holly/scratch"

TChain *chainfilelist(const char* fname,const char* tname="h10",TChain *c=NULL,int nfiles=-1)
{
    string line;
    ifstream f;
    f.open(fname);
    if (!f.is_open()) return NULL;
    bool newchain=0;
    if (!c)
    {
        newchain=1;
        c=new TChain("chain","");
    }
    int nn=0;
    while ( f.good() )
    {
        getline(f,line);
        if (f.eof()) break;
        nn++;
        if (nfiles>0 && nn>=nfiles) break;
    }
    if (newchain) cout<<"Chaining "<<nn<<" Files...."<<endl;
    else          cout<<"Adding "<<nn<<" Files to chain...."<<endl; 
    f.clear();
    f.seekg(0);
    nfiles=nn;
    nn=0;
    while ( f.good() )
    {
        getline(f,line);
        if (f.eof()) break;
        if (c->AddFile(line.c_str(),-1,tname)) nn++;
        if (nn%100 == 0) ProgressMeter(nfiles,nn);
        if (nfiles>0 && nn>=nfiles) break;
    }

    f.close();
    cout<<"Chain now has "<<c->GetNtrees()<<" Files and "<<c->GetEntriesFast()<<" Entries"<<endl;
    return c;
}



TChain *chainfiledir(const char* dir=".",const char* tname="h10",TChain *c=NULL,const int nfiles=-1)
{
    // need to make this recusive so filelist can contain list of directories

    static int ncalls=0;
    TTime time=gSystem->Now();
    const TString tmpdir=__CHAINTMPDIR__;
    const TString tmpfile=Form("%s/tchain_%s_%d.tmp",tmpdir.Data(),time.AsString(),ncalls++); 
    gSystem->Exec(Form("/bin/ls %s/*.root > %s",dir,tmpfile.Data()));
    return chainfilelist(tmpfile.Data(),tname,c,nfiles);
}

TChain *chainfilematch(const char* dir,const char* match,const char* tname="h10",TChain *c=NULL,const int nfiles=-1)
{
    static int ncalls=0;
    TTime time=gSystem->Now();
    const TString tmpdir=__CHAINTMPDIR__;
    const TString tmpfile=Form("%s/tchain_%s_%d.tmp",tmpdir.Data(),time.AsString(),ncalls++); 
    gSystem->Exec(Form("/bin/ls %s/*%s*.root > %s",dir,match,tmpfile.Data()));
    return chainfilelist(tmpfile.Data(),tname,c,nfiles);
}
