#ifndef __ROOT_UTIL_HH__
#define __ROOT_UTIL_HH__

#if !defined(__CINT__) || defined(__MAKECINT__)
#include "TChain.h"
#include "TLine.h"
#include "TPad.h"
#include "TMarker.h"
#include "TCanvas.h"
#include "TLatex.h"
#include "TDirectory.h"
#include "TKey.h"
#include "TGraph.h"
#include "TGraphErrors.h"
#include "TGraph2D.h"
#include "TGraph2DErrors.h"
#include "TH1.h"
#include "TH2.h"
#include "TH3.h"
#include "TF1.h"
#include "TF2.h"
#include "TFile.h"
#include "TLegend.h"
#include "TSystem.h"
#include "TRegexp.h"
#endif

#include "GetRunNumber.C"

void TH2AxisLabels(TH2* h,const float lx=-1,const float ly=1,
                          const int nx=-1,const int ny=-1)
{
    if (lx>=0) h->GetXaxis()->SetLabelSize(lx);
    if (ly>=0) h->GetYaxis()->SetLabelSize(ly);
    if (nx>=0) h->GetXaxis()->SetNdivisions(nx);
    if (ny>=0) h->GetYaxis()->SetNdivisions(ny);
}
void TH3Title(TH1* h,const char* x,const char* y=NULL,const char* z=NULL,const char* t=NULL,const float ox=-1,const float oy=-1,const float oz=-1,const float dx=-1,const float dy=-1,const float dz=-1)
{
    if (h==NULL) return;
    if (t!=NULL) h->SetTitle(t);
    h->GetXaxis()->SetTitle(x);
    h->GetYaxis()->SetTitle(y);
    h->GetZaxis()->SetTitle(z);
//    h->GetYaxis()->SetTitleOffset(1.5);
    if (dx>=0) h->GetXaxis()->SetTitleSize(dx);
    if (dy>=0) h->GetYaxis()->SetTitleSize(dy);
    if (dz>=0) h->GetZaxis()->SetTitleSize(dz);
    if (ox>=0) h->GetXaxis()->SetTitleOffset(ox);
    if (oy>=0) h->GetYaxis()->SetTitleOffset(oy);
    if (oz>=0) h->GetZaxis()->SetTitleOffset(oz);
    h->GetXaxis()->CenterTitle();
    h->GetYaxis()->CenterTitle();
}
void TH3Title(TH3* h,const char* x,const char* y=NULL,const char* z=NULL,const char* t=NULL,const float ox=-1,const float oy=-1,const float oz=-1,const float dx=-1,const float dy=-1,const float dz=-1)
{
    TH3Title((TH1*)h,x,y,z,t,ox,oy,oz,dx,dy,dz);
}
void TH2Title(TH2 *h,const char* x,const char* y,const char* t=NULL,const float ox=-1,const float oy=-1,const float dx=-1,const float dy=-1)
{
    TH3Title((TH1*)h,x,y,NULL,t,ox,oy,-1,dx,dy,-1);
}
void TH2Title(TH1 *h,const char* x,const char* y,const char* t=NULL,const float ox=-1,const float oy=-1,const float dx=-1,const float dy=-1)
{
    TH3Title(h,x,y,NULL,t,ox,oy,-1,dx,dy,-1);
}
void TH1Title(TH1 *h,const char* x,const char* y,const char* t=NULL,const float ox=-1,const float oy=-1,const float dx=-1,const float dy=-1)
{
    TH3Title(h,x,y,NULL,t,ox,oy,-1,dx,dy,-1);
}
void SetupTGraph(TGraph *g,const int& lc=-1,const int& ls=-1,const int& lw=-1,const int& ms=-1,const int& mc=-1,const int& mw=-1)
{
    if (g==NULL) return;
    if (lc>=0) g->SetLineColor(lc);
    if (ls>=0) g->SetLineStyle(ls);
    if (lw>=0) g->SetLineWidth(lw);
    if (ms>=0) g->SetMarkerStyle(ms);
    if (mc>=0) g->SetMarkerColor(mc);
    if (mw>=0) g->SetMarkerSize(mw);
}
void SetupTGraphErrors(TGraphErrors *g,
        const int& lc=-1,
        const int& ls=-1,
        const int& lw=-1,
        const int& ms=-1,
        const int& mc=-1,
        const float& mw=-1)
{
    if (g==NULL) return;
    if (lc>=0) g->SetLineColor(lc);
    if (ls>=0) g->SetLineStyle(ls);
    if (lw>=0) g->SetLineWidth(lw);
    if (ms>=0) g->SetMarkerStyle(ms);
    if (mc>=0) g->SetMarkerColor(mc);
    if (mw>=0) g->SetMarkerSize(mw);
}
void SetupTH1Line(TH1* h,const int& lc,const int& lw,const int& ls)
{
    if (h==NULL) return;
    h->SetLineColor(lc);
    h->SetLineWidth(lw);
    h->SetLineStyle(ls);
}
TLine* DrawLine(const float& x0,const float& y0,const float& x1,const float& y1,const int& color=kRed,const int& width=-1,const int& style=-1)
{
    TLine *l=new TLine(x0,y0,x1,y1);
    if (color>0) l->SetLineColor(color);
    if (width>0) l->SetLineWidth(width);
    if (style>0) l->SetLineStyle(style);
    l->Draw();
    return l;
}
TLine* DrawLine(const float& slope,const float& yint,const int color=kRed,const int width=-1,const int style=-1)
{
    gPad->Update();
    float x0=gPad->GetUxmin();
    float x1=gPad->GetUxmax();
    float y0=slope*x0+yint;
    float y1=slope*x1+yint;
    if      (y0 > gPad->GetUymax())  y0=gPad->GetUymax();
    else if (y0 < gPad->GetUymin())  y0=gPad->GetUymin();
    if      (y1 > gPad->GetUymax())  y1=gPad->GetUymax();
    else if (y1 < gPad->GetUymin())  y1=gPad->GetUymin();
    x0=(y0-yint)/slope;
    x1=(y1-yint)/slope;
    return DrawLine(x0,y0,x1,y1,color,width,style);
//    DrawLine(gPad->GetUxmin(),slope*gPad->GetUxmin()+yint,
//             gPad->GetUxmax(),slope*gPad->GetUxmax()+yint,
//             color,width,style);
}
TLine* DrawLineY(const float& y,const int& color=kRed,const int& width=-1,const int& style=-1)
{
    gPad->Update();
    const float xmin=gPad->GetUxmin();
    const float xmax=gPad->GetUxmax();
    return DrawLine(xmin,y,xmax,y,color,width,style);
}
TLine* DrawLineX(const float& x,const int& color=kRed,const int& width=-1,const int& style=-1)
{
    gPad->Update();
    const float ymin=gPad->GetUymin();
    const float ymax=gPad->GetUymax();
    return DrawLine(x,ymin,x,ymax,color,width,style);
}
TMarker MakeMarker(const float& x,const float& y,const int& color,const int& style,const int& size)
{
    TMarker mark(x,y,style);
    mark.SetMarkerColor(color);
    mark.SetMarkerSize(size);
    mark.DrawClone();
    return mark;
}
TLegend* MakeLegend(vector <TObject*> o,const char* symbol,const float& x1=0.65,const float& y1=0.65,const float& x2=0.89,const float& y2=0.89)
{
    TLegend *leg=new TLegend(x1,y1,x2,y2);
    leg->SetFillColor(kWhite);
    leg->SetFillStyle(0);
    leg->SetBorderSize(1);
    for (unsigned int ii=0; ii<o.size(); ii++)
        leg->AddEntry(o[ii],o[ii]->GetTitle(),symbol);
    leg->Draw();
    return leg;
}
TLegend* MakeLegend(vector <TObject*> o,vector <const char*> symbol,const float& x1=0.65,const float& y1=0.65,const float& x2=0.89,const float& y2=0.89)
{
    TLegend *leg=new TLegend(x1,y1,x2,y2);
    leg->SetFillColor(kWhite);
    leg->SetFillStyle(1);
    leg->SetBorderSize(1);
    for (unsigned int ii=0; ii<o.size(); ii++)
        leg->AddEntry(o[ii],o[ii]->GetTitle(),symbol[ii]);
    leg->Draw();
    return leg;
}
vector <TObject*> MakeObjectVector(TObject *o1,TObject *o2,TObject *o3=NULL,TObject *o4=NULL)
{
    vector <TObject*> o;
    o.push_back(o1);
    o.push_back(o2);
    if (o3) o.push_back(o3);
    if (o4) o.push_back(o4);
    return o;
}
vector <const char*> MakeStringVector(const char *o1,const char *o2,const char *o3=NULL,const char *o4=NULL)
{
    vector <const char*> o;
    o.push_back(o1);
    o.push_back(o2);
    if (o3) o.push_back(o3);
    if (o4) o.push_back(o4);
    return o;
}
void DrawLatex(const float& x,const float& y,const float& s,const char* c,const int& color=1,const short a=11)
{
    TLatex l;
    l.SetNDC(kTRUE);
    l.SetTextSize(s);
    l.SetTextColor(color);
    l.SetTextAlign(a);
    l.DrawLatex(x,y,c);
}
void Print(TH1* h)
{
    cout<<"NX:  "<<h->GetNbinsX()<<endl;
    if (h->InheritsFrom("TH2") || h->InheritsFrom("TH3")) cout<<"NY:  "<<h->GetNbinsY()<<endl;
    if (h->InheritsFrom("TH3")) cout<<"NZ:  "<<h->GetNbinsZ()<<endl;
    cout<<"T:  "<<h->GetTitle()<<endl;
    cout<<"X:  "<<h->GetXaxis()->GetTitle()<<endl;
    if (h->InheritsFrom("TH2") || h->InheritsFrom("TH3")) cout<<"Y:  "<<h->GetYaxis()->GetTitle()<<endl;
    if (h->InheritsFrom("TH3")) cout<<"Z:  "<<h->GetZaxis()->GetTitle()<<endl;
}
double TGraphMinimum(TGraphErrors *g)
{
    double min=9999999,x,y;
    for (int ii=0; ii<g->GetN(); ii++) {
        g->GetPoint(ii,x,y);
        const double e=g->GetErrorY(ii);
        if (y<min && e/y<0.1) min=y;
    }
    return min;
}
double TGraphMaximum(TGraphErrors *g)
{
    double max=-9999999,x,y;
    for (int ii=0; ii<g->GetN(); ii++) {
        g->GetPoint(ii,x,y);
        const double e=g->GetErrorY(ii);
        if (y>max && e/y<0.1) max=y;
    }
    return max;
}
double TGraphMaximum(TGraph *g)
{
    double max=-1,x,y;
    for (int ii=0; ii<g->GetN(); ii++) {
        g->GetPoint(ii,x,y);
        if (y>max) max=y;
    }
    return max;
}
double TGraphMaximum(vector<TGraph*> g)
{
    double max=-1;
    for (unsigned int ii=0; ii<g.size(); ii++) {
        double y=TGraphMaximum(g[ii]);
        if (y>max) max=y;
    }
    return max;
}
double TGraphMaximum(vector<TGraphErrors*> g)
{
    double max=-9999999;
    for (unsigned int ii=0; ii<g.size(); ii++) {
        double y=TGraphMaximum(g[ii]);
        if (y>max) max=y;
    }
    return max;
}
double TGraphMinimum(vector<TGraphErrors*> g1,vector <TGraphErrors*> g2)
{
    double min=9999999;
    for (unsigned int ii=0; ii<g1.size(); ii++) {
        double y=TGraphMinimum(g1[ii]);
        if (y<min) min=y;
    }
    for (unsigned int ii=0; ii<g2.size(); ii++) {
        double y=TGraphMinimum(g2[ii]);
        if (y<min) min=y;
    }
    return min;
}
double TGraphMaximum(vector<TGraphErrors*> g1,vector <TGraphErrors*> g2)
{
    double max=-9999999;
    for (unsigned int ii=0; ii<g1.size(); ii++) {
        double y=TGraphMaximum(g1[ii]);
        if (y>max) max=y;
    }
    for (unsigned int ii=0; ii<g2.size(); ii++) {
        double y=TGraphMaximum(g2[ii]);
        if (y>max) max=y;
    }
    return max;
}
double TGraphMinimum(vector<TGraphErrors*> g)
{
    double min=9999999;
    for (unsigned int ii=0; ii<g.size(); ii++) {
        double y=TGraphMinimum(g[ii]);
        if (y<min) min=y;
    }
    return min;
}
void FillHistFromVector(TH1* h,vector<double>* x)
{
    for (unsigned int ii=0; ii<x->size(); ii++) h->Fill(x->at(ii));
}
void SetHistosSameMax(vector <TH1*> h)
{
    float max=0;
    for (unsigned int ii=0; ii<h.size(); ii++) 
        if (h[ii]->GetMaximum()>max) max=h[ii]->GetMaximum();
    for (unsigned int ii=0; ii<h.size(); ii++) 
        h[ii]->SetMaximum(max);
}
void TH2EqualMinMax(TH2* h1,TH2* h2,TH2* h3=NULL)
{
    if (h1==NULL || h2==NULL) return;
    double min=999999,max=-9999999;
    if (h1->GetMaximum()>max) max=h1->GetMaximum();
    if (h1->GetMinimum()<min) min=h1->GetMinimum();
    if (h2->GetMaximum()>max) max=h2->GetMaximum();
    if (h2->GetMinimum()<min) min=h2->GetMinimum();
    if (h3) {
        if (h3->GetMaximum()>max) max=h3->GetMaximum();
        if (h3->GetMinimum()<min) min=h3->GetMinimum();
    }
    h1->SetMaximum(max);
    h1->SetMinimum(min);
    h2->SetMaximum(max);
    h2->SetMinimum(min);
    if (h3) {
        h3->SetMaximum(max);
        h3->SetMinimum(min);
    }
}
const char* FindUnits(const char* c)
{
    string s=c;
    if (s.find("GeV/c^2")!=string::npos) return "GeV/c^2";
    if (s.find("GeV/c")  !=string::npos) return "GeV/c";
    if (s.find("GeV")    !=string::npos) return "GeV";
    if (s.find("degrees")!=string::npos) return "#circ";
    if (s.find("deg")    !=string::npos) return "#circ";
    return "";
}
void SaveCanvas(TCanvas* can=NULL,char* filename=NULL,const bool gv=0)
{
    TString s;
    if (filename==NULL) {
        if (can==NULL) s=Form("%s.eps",gPad->GetName());
        else           s=Form("%s.eps",can->GetName());
    }
    else s=filename;
    s.ReplaceAll(" ","");
    if (can==NULL) gPad->SaveAs(s);
    else           can->SaveAs(s);
    if (gv) gSystem->Exec("gv "+s+" &");
    /*
    if (c==NULL || name==NULL) return;
    string s=name;
    if ( s.find(".eps")!=string::npos ||
         s.find(".jpg")!=string::npos ||
         s.find(".png")!=string::npos ||
         s.find(".pdf")!=string::npos ||
         s.find(".gif")!=string::npos ||
         s.find(".ps") != string::npos ) {
        c->SaveAs(name); 
    } else {
        c->SaveAs(Form("%s.eps",name));
        c->SaveAs(Form("%s.png",name));
    }
    */
}
/*
   void SetupROOT()
{
    gRandom->SetSeed(0);
    gStyle->SetOptStat(0);
    gStyle->SetFillStyle(0);
    gStyle->SetFillColor(0);
    gStyle->SetTitleBorderSize(0);
    gStyle->SetTitleFillColor(0);
    gStyle->SetLegendBorderSize(0);
}
*/
TH1* FindHisto(const char* name,TFile *f=NULL)
{
    TDirectory *g = (f==NULL) ? gDirectory : (TDirectory*)f;
    TH1* h=(TH1*)g->Get(name);
    TKey *key;
    TObject *obj;
    TIter nextkey(g->GetListOfKeys());
    while (h==NULL && (key=(TKey*)nextkey()))
    {
        obj=(TObject*)key->ReadObj();
        if (obj->IsA()->InheritsFrom("TDirectory"))
            h=(TH1*)((TDirectory*)obj)->Get(name);
    }
    return h;
}
TChain* ChainTrees(const char* clistfile,const char* treename)
{
    TChain *chain=new TChain("doggy","");
    char crootfile[1000];
    FILE *fin=fopen(clistfile,"r");
    while (fscanf(fin,"%s",crootfile)==1) 
        chain->AddFile(crootfile,-1,treename);
    return chain;
}
TH2* Projection3D(TH3* h3,const int& zlo,const int& zhi)
{
    TH2* h2=(TH2*)h3->Project3D("yx");
    h2->Reset();
    h2->SetName(Form("%s___proZ_%d_%d",h3->GetName(),zlo,zhi));
    for (int ix=1; ix<=h3->GetNbinsX(); ix++)
    {
        for (int iy=1; iy<=h3->GetNbinsY(); iy++)
        {
            for (int iz=zlo; iz<=zhi; iz++)
            {
                h2->AddBinContent(h2->GetBin(ix,iy),
                                  h3->GetBinContent(ix,iy,iz));
            }
        }
    }
    return h2;
}




// Don't call this, call one of the "MyColors" below
Int_t MyColors(const Int_t delta,const Int_t restart)
{
    static Int_t stepsize=15;
    static Int_t firstcolor=925;
    static Int_t nextcolor=firstcolor;
    if (delta==0 && restart==0 && stepsize==240) return 1;
    if      (delta!=0)   stepsize=delta;
    if      (restart>0)  nextcolor=firstcolor=restart;
    else if (restart<0)  nextcolor=firstcolor;
    const Int_t thiscolor=nextcolor;
    nextcolor += stepsize;
    return thiscolor;
}

// Call this one with # of colors you will use (and get the first color):
Int_t MyColors(const int ncolors) { return ncolors==0?1:MyColors((int)240/ncolors,924); }

// Then call this to get successive colors:
Int_t MyColors() { return MyColors(0,0); }



void SetTF2TGraph2D(TF2 *f,TGraph2D* g)
{
    f->SetRange(
        g->GetXmin(),g->GetYmin(),g->GetZmin(),
        g->GetXmax(),g->GetYmax(),g->GetZmax());
}

TF2 *__g__TF2;
TGraph2D *__g__TGraph2D;
double Residual(double *x,double *p)
{
    cout<<p[0]<<endl;
    const double g=__g__TGraph2D->Interpolate(x[0],x[1]);
    const double f=__g__TF2->Eval(x[0],x[1]);
    return (g-f)/g;
}
TF2* Residual(TF2* f,TGraph2D *g)
{
    static int ncalls=0;
    __g__TF2=f;
    __g__TGraph2D=g;
    TF2 *f2=new TF2(Form("f_residual__%d",ncalls++),Residual,f->GetXmin(),f->GetXmax(),f->GetYmin(),f->GetYmax(),0);
    f2->SetRange(g->GetXmin(),g->GetYmin(),g->GetZmin(),g->GetXmax(),g->GetYmax(),g->GetZmax());
    return f2;
}
TH2* Residual(TF2 *f,TH2 *h)
{
    static int ncalls=0;
    TH2* hr=(TH2*)h->Clone(Form("hResidual_%d",ncalls++));
    hr->Reset();
    for (int ix=0; ix<h->GetNbinsX(); ix++)
    {
        for (int iy=0; iy<h->GetNbinsX(); iy++)
        {
            if (fabs(h->GetBinContent(ix,iy))<1e-5) continue;
            double xx=h->GetXaxis()->GetBinCenter(ix);
            double yy=h->GetYaxis()->GetBinCenter(iy);
            double rr=h->GetBinContent(ix,iy)-f->Eval(xx,yy);
            hr->SetBinContent(ix,iy,rr);
        }
    }
    return hr;
}
TFile *GetMyFile(const char* basename)
{
    const int ndirs=2;
    const char* cdirs[ndirs]={"/disks/1/nbaltzell",
                              "/home/baltzell"};
    for (int ii=0; ii<ndirs; ii++)
    {
        const char* cfile=Form("%s/%s",cdirs[ii],basename);
        if (!gSystem->AccessPathName(cfile)) 
        {
            cout<<"Reading "<<cfile<<endl;
            return new TFile(cfile,"READ");
        }
    }
    cerr<<"MyRootUtil::GetFile Error: Missing File: "<<basename<<endl;
    return NULL;
}
void SetRangeTH2(TH2* h)
{
    float min=99999999;
    float max=-99999999;
    for (int ix=1; ix<=h->GetNbinsX(); ix++) {
        for (int iy=1; iy<=h->GetNbinsY(); iy++) {
            const float bc=h->GetBinContent(ix,iy);
            if (bc > max) max=bc;
            if (bc < min && bc > 0) min=bc;
        }
    }
    h->SetMinimum(min);
    h->SetMaximum(max);
}
void MyRebin(TH1 *h,int rx,int ry=-1,int rz=-1)
{
    if (ry<=0) ry=rx;
    if (rz<=0) rz=ry;

    if (h->InheritsFrom(TH3::Class()))
    {
        cerr<<"MyRebin not ready to rebin TH3"<<endl;
    }
    else if (h->InheritsFrom(TH2::Class()))
    {
        ((TH2*)h)->Rebin2D(rx,ry);
    }
    else
    {
        h->Rebin(rx);
    }
}
/*
//template <typename T>
template <typename T> void Print2(const int n,T t)
{
    cout<<"dog"<<endl;
}
*/
void Print(const int n,const vector <int> x[])
{
    for (int ii=0; ii<n; ii++)
    {
        cout<<ii<<" ";
        for (unsigned int jj=0; jj<x[ii].size(); jj++) cout<<x[ii][jj]<<" ";
        cout<<endl;
    }
}
void Print(const int n,const vector <double> x[])
{
    for (int ii=0; ii<n; ii++)
    {
        cout<<ii<<" ";
        for (unsigned int jj=0; jj<x[ii].size(); jj++) cout<<x[ii][jj]<<" ";
        cout<<endl;
    }
}
/*
TGraph* GetGraph(TPad *p=NULL)
{
//    if (!p) p=(TPad*)gPad;
//    if (!p) return NULL;
    TKey *k;
    TIter nextkey(p->GetListOfPrimitives());
    cerr<<"DOG"<<endl;
    while ((k=(TKey*)nextkey()))
    {
    cerr<<"CAT1"<<endl;
        TObject *o=k->ReadObj();
        if (!o) continue;
    cerr<<"CAT2 "<<o->GetName()<<endl;
        if (o->IsA()->InheritsFrom(TGraph::Class()))
            return (TGraph*)o;
    }
    return NULL;
}
*/

int GetTreeInt(TTree *t,const char* v,const int n)
{
    int f; TBranch *b;
    t->SetBranchAddress(v,&f,&b);
    b->GetEntry(n);
    return f;
}
float GetTreeFloat(TTree *t,const char* v,const int n)
{
    float f; TBranch *b;
    t->SetBranchAddress(v,&f,&b);
    b->GetEntry(n);
    return f;
}
double GetTreeDouble(TTree *t,const char* v,const int n)
{
    double f; TBranch *b;
    t->SetBranchAddress(v,&f,&b);
    b->GetEntry(n);
    return f;
}
void WriteRemainingHistos(const bool filledonly=0)
{
    TObject *oo;
    TIter noo(gDirectory->GetList());
    while ((oo=(TObject*)noo()))
    {
        if (!oo) continue;
        if (!oo->IsA()->InheritsFrom(TH1::Class())) continue;
        if (filledonly && ((TH1*)oo)->GetEntries()<=0) continue;
        oo->Write();
    }
}
#endif
