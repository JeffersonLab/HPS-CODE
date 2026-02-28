void Elasticmean()
{
//=========Macro generated from canvas: scr/xxxx
//=========  (Thu Jul 23 12:34:58 2020) by ROOT version 6.18/04
   TCanvas *scr = new TCanvas("scr", "xxxx",0,0,1200,800);
   gStyle->SetOptFit(1);
   gStyle->SetOptStat(0);
   scr->Range(-17.5625,-0.1875,8.5625,1.6875);
   scr->SetFillColor(0);
   scr->SetBorderMode(0);
   scr->SetBorderSize(2);
   scr->SetFrameBorderMode(0);
   scr->SetFrameBorderMode(0);
   
   TMultiGraph *multigraph = new TMultiGraph();
   multigraph->SetName("");
   multigraph->SetTitle("Elastic Peak Position");
   
   TGraph *graph = new TGraph();
   graph->SetName("grp0");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineWidth(3);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   multigraph->Add(graph,"LP");
   
   Double_t grp1_fx2[16] = {
   -12,
   -11,
   -10,
   -9,
   -8,
   -7,
   -6,
   -5,
   -4,
   -3,
   -2,
   -1,
   1,
   2,
   3,
   4};
   Double_t grp1_fy2[16] = {
   0.9864082,
   0.985625,
   0.9917876,
   0.9841731,
   0.9769429,
   0.9796519,
   0.9885139,
   0.9977124,
   0.9946002,
   0.9880972,
   0.9767341,
   0.9879764,
   0.9837358,
   0.9873867,
   0.982826,
   0.9735682};
   graph = new TGraph(16,grp1_fx2,grp1_fy2);
   graph->SetName("grp1");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(2);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(2);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp12 = new TH1F("Graph_grp12","",100,-13.6,5.6);
   Graph_grp12->SetMinimum(0.9711538);
   Graph_grp12->SetMaximum(1.000127);
   Graph_grp12->SetDirectory(0);
   Graph_grp12->SetStats(0);

   Int_t ci;      // for color index setting
   TColor *color; // for color definition with alpha
   ci = TColor::GetColor("#000099");
   Graph_grp12->SetLineColor(ci);
   Graph_grp12->GetXaxis()->SetLabelFont(42);
   Graph_grp12->GetXaxis()->SetLabelSize(0.035);
   Graph_grp12->GetXaxis()->SetTitleSize(0.035);
   Graph_grp12->GetXaxis()->SetTitleOffset(1);
   Graph_grp12->GetXaxis()->SetTitleFont(42);
   Graph_grp12->GetYaxis()->SetLabelFont(42);
   Graph_grp12->GetYaxis()->SetLabelSize(0.035);
   Graph_grp12->GetYaxis()->SetTitleSize(0.035);
   Graph_grp12->GetYaxis()->SetTitleFont(42);
   Graph_grp12->GetZaxis()->SetLabelFont(42);
   Graph_grp12->GetZaxis()->SetLabelSize(0.035);
   Graph_grp12->GetZaxis()->SetTitleSize(0.035);
   Graph_grp12->GetZaxis()->SetTitleOffset(1);
   Graph_grp12->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_grp12);
   
   multigraph->Add(graph,"LP");
   
   Double_t grp2_fx3[19] = {
   -14,
   -13,
   -12,
   -11,
   -10,
   -9,
   -8,
   -7,
   -6,
   -5,
   -4,
   -3,
   -2,
   -1,
   1,
   2,
   3,
   4,
   5};
   Double_t grp2_fy3[19] = {
   0.9633917,
   0.981827,
   0.9954994,
   0.9928085,
   0.9954627,
   0.9901222,
   0.9959828,
   0.9853622,
   0.9960003,
   0.9999025,
   0.991999,
   0.9968337,
   0.998403,
   0.9987988,
   0.9849374,
   0.9891685,
   0.9851741,
   0.9840716,
   0.8745456};
   graph = new TGraph(19,grp2_fx3,grp2_fy3);
   graph->SetName("grp2");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(3);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(3);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp23 = new TH1F("Graph_grp23","",100,-15.9,6.9);
   Graph_grp23->SetMinimum(0.8620099);
   Graph_grp23->SetMaximum(1.012438);
   Graph_grp23->SetDirectory(0);
   Graph_grp23->SetStats(0);

   ci = TColor::GetColor("#000099");
   Graph_grp23->SetLineColor(ci);
   Graph_grp23->GetXaxis()->SetLabelFont(42);
   Graph_grp23->GetXaxis()->SetLabelSize(0.035);
   Graph_grp23->GetXaxis()->SetTitleSize(0.035);
   Graph_grp23->GetXaxis()->SetTitleOffset(1);
   Graph_grp23->GetXaxis()->SetTitleFont(42);
   Graph_grp23->GetYaxis()->SetLabelFont(42);
   Graph_grp23->GetYaxis()->SetLabelSize(0.035);
   Graph_grp23->GetYaxis()->SetTitleSize(0.035);
   Graph_grp23->GetYaxis()->SetTitleFont(42);
   Graph_grp23->GetZaxis()->SetLabelFont(42);
   Graph_grp23->GetZaxis()->SetLabelSize(0.035);
   Graph_grp23->GetZaxis()->SetTitleSize(0.035);
   Graph_grp23->GetZaxis()->SetTitleOffset(1);
   Graph_grp23->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_grp23);
   
   multigraph->Add(graph,"LP");
   
   Double_t grp3_fx4[19] = {
   -14,
   -13,
   -12,
   -11,
   -10,
   -9,
   -8,
   -7,
   -6,
   -5,
   -4,
   -3,
   -2,
   -1,
   1,
   2,
   3,
   4,
   5};
   Double_t grp3_fy4[19] = {
   0.9986517,
   0.9937465,
   0.970879,
   1.0009,
   0.9779325,
   0.9957039,
   0.984675,
   1.066524,
   0.9779772,
   0.9940945,
   0.9878716,
   0.9854118,
   0.9927074,
   1.00008,
   0.9677895,
   1.02138,
   0.9792632,
   0.976739,
   0.9642298};
   graph = new TGraph(19,grp3_fx4,grp3_fy4);
   graph->SetName("grp3");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(4);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(4);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp34 = new TH1F("Graph_grp34","",100,-15.9,6.9);
   Graph_grp34->SetMinimum(0.9540004);
   Graph_grp34->SetMaximum(1.076754);
   Graph_grp34->SetDirectory(0);
   Graph_grp34->SetStats(0);

   ci = TColor::GetColor("#000099");
   Graph_grp34->SetLineColor(ci);
   Graph_grp34->GetXaxis()->SetLabelFont(42);
   Graph_grp34->GetXaxis()->SetLabelSize(0.035);
   Graph_grp34->GetXaxis()->SetTitleSize(0.035);
   Graph_grp34->GetXaxis()->SetTitleOffset(1);
   Graph_grp34->GetXaxis()->SetTitleFont(42);
   Graph_grp34->GetYaxis()->SetLabelFont(42);
   Graph_grp34->GetYaxis()->SetLabelSize(0.035);
   Graph_grp34->GetYaxis()->SetTitleSize(0.035);
   Graph_grp34->GetYaxis()->SetTitleFont(42);
   Graph_grp34->GetZaxis()->SetLabelFont(42);
   Graph_grp34->GetZaxis()->SetLabelSize(0.035);
   Graph_grp34->GetZaxis()->SetTitleSize(0.035);
   Graph_grp34->GetZaxis()->SetTitleOffset(1);
   Graph_grp34->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_grp34);
   
   multigraph->Add(graph,"LP");
   
   graph = new TGraph();
   graph->SetName("grp4");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(5);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(5);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   multigraph->Add(graph,"LP");
   
   graph = new TGraph();
   graph->SetName("grp5");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(6);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(6);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   multigraph->Add(graph,"LP");
   
   Double_t grp6_fx7[16] = {
   -14,
   -13,
   -12,
   -11,
   -7,
   -6,
   -5,
   -4,
   -3,
   -2,
   -1,
   1,
   2,
   3,
   4,
   5};
   Double_t grp6_fy7[16] = {
   0.9186893,
   0.9837851,
   0.9967402,
   0.987173,
   0.9790433,
   0.9940332,
   0.9995963,
   0.9918069,
   0.9934933,
   0.9792218,
   0.9970032,
   0.9895632,
   0.9783366,
   0.9678863,
   0.974687,
   0.9897252};
   graph = new TGraph(16,grp6_fx7,grp6_fy7);
   graph->SetName("grp6");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(7);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(7);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp67 = new TH1F("Graph_grp67","",100,-15.9,6.9);
   Graph_grp67->SetMinimum(0.9105985);
   Graph_grp67->SetMaximum(1.007687);
   Graph_grp67->SetDirectory(0);
   Graph_grp67->SetStats(0);

   ci = TColor::GetColor("#000099");
   Graph_grp67->SetLineColor(ci);
   Graph_grp67->GetXaxis()->SetLabelFont(42);
   Graph_grp67->GetXaxis()->SetLabelSize(0.035);
   Graph_grp67->GetXaxis()->SetTitleSize(0.035);
   Graph_grp67->GetXaxis()->SetTitleOffset(1);
   Graph_grp67->GetXaxis()->SetTitleFont(42);
   Graph_grp67->GetYaxis()->SetLabelFont(42);
   Graph_grp67->GetYaxis()->SetLabelSize(0.035);
   Graph_grp67->GetYaxis()->SetTitleSize(0.035);
   Graph_grp67->GetYaxis()->SetTitleFont(42);
   Graph_grp67->GetZaxis()->SetLabelFont(42);
   Graph_grp67->GetZaxis()->SetLabelSize(0.035);
   Graph_grp67->GetZaxis()->SetTitleSize(0.035);
   Graph_grp67->GetZaxis()->SetTitleOffset(1);
   Graph_grp67->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_grp67);
   
   multigraph->Add(graph,"LP");
   
   Double_t grp7_fx8[16] = {
   -13,
   -12,
   -11,
   -10,
   -8,
   -7,
   -6,
   -5,
   -4,
   -3,
   -2,
   -1,
   1,
   2,
   3,
   4};
   Double_t grp7_fy8[16] = {
   0.9706588,
   0.992388,
   0.9888242,
   0.969559,
   0.9902579,
   0.9962068,
   0.994121,
   0.9964938,
   0.9897699,
   0.9927038,
   0.9943615,
   0.9963478,
   0.9956013,
   0.9991814,
   0.984201,
   0.9902785};
   graph = new TGraph(16,grp7_fx8,grp7_fy8);
   graph->SetName("grp7");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(8);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(8);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp78 = new TH1F("Graph_grp78","",100,-14.7,5.7);
   Graph_grp78->SetMinimum(0.9665967);
   Graph_grp78->SetMaximum(1.002144);
   Graph_grp78->SetDirectory(0);
   Graph_grp78->SetStats(0);

   ci = TColor::GetColor("#000099");
   Graph_grp78->SetLineColor(ci);
   Graph_grp78->GetXaxis()->SetLabelFont(42);
   Graph_grp78->GetXaxis()->SetLabelSize(0.035);
   Graph_grp78->GetXaxis()->SetTitleSize(0.035);
   Graph_grp78->GetXaxis()->SetTitleOffset(1);
   Graph_grp78->GetXaxis()->SetTitleFont(42);
   Graph_grp78->GetYaxis()->SetLabelFont(42);
   Graph_grp78->GetYaxis()->SetLabelSize(0.035);
   Graph_grp78->GetYaxis()->SetTitleSize(0.035);
   Graph_grp78->GetYaxis()->SetTitleFont(42);
   Graph_grp78->GetZaxis()->SetLabelFont(42);
   Graph_grp78->GetZaxis()->SetLabelSize(0.035);
   Graph_grp78->GetZaxis()->SetTitleSize(0.035);
   Graph_grp78->GetZaxis()->SetTitleOffset(1);
   Graph_grp78->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_grp78);
   
   multigraph->Add(graph,"LP");
   
   Double_t grp8_fx9[16] = {
   -12,
   -11,
   -10,
   -9,
   -8,
   -7,
   -6,
   -5,
   -4,
   -3,
   -2,
   -1,
   1,
   2,
   3,
   4};
   Double_t grp8_fy9[16] = {
   0.9905556,
   0.9766043,
   0.9757444,
   0.9827021,
   0.975659,
   0.9867198,
   0.9751759,
   0.9826958,
   0.9894052,
   0.9830679,
   0.972734,
   0.9737142,
   0.985168,
   0.974926,
   0.9741426,
   0.9741039};
   graph = new TGraph(16,grp8_fx9,grp8_fy9);
   graph->SetName("grp8");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(9);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(9);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp89 = new TH1F("Graph_grp89","",100,-13.6,5.6);
   Graph_grp89->SetMinimum(0.9709518);
   Graph_grp89->SetMaximum(0.9923377);
   Graph_grp89->SetDirectory(0);
   Graph_grp89->SetStats(0);

   ci = TColor::GetColor("#000099");
   Graph_grp89->SetLineColor(ci);
   Graph_grp89->GetXaxis()->SetLabelFont(42);
   Graph_grp89->GetXaxis()->SetLabelSize(0.035);
   Graph_grp89->GetXaxis()->SetTitleSize(0.035);
   Graph_grp89->GetXaxis()->SetTitleOffset(1);
   Graph_grp89->GetXaxis()->SetTitleFont(42);
   Graph_grp89->GetYaxis()->SetLabelFont(42);
   Graph_grp89->GetYaxis()->SetLabelSize(0.035);
   Graph_grp89->GetYaxis()->SetTitleSize(0.035);
   Graph_grp89->GetYaxis()->SetTitleFont(42);
   Graph_grp89->GetZaxis()->SetLabelFont(42);
   Graph_grp89->GetZaxis()->SetLabelSize(0.035);
   Graph_grp89->GetZaxis()->SetTitleSize(0.035);
   Graph_grp89->GetZaxis()->SetTitleOffset(1);
   Graph_grp89->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_grp89);
   
   multigraph->Add(graph,"LP");
   
   graph = new TGraph();
   graph->SetName("grp9");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(11);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(11);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   multigraph->Add(graph,"LP");
   multigraph->Draw("A");
   multigraph->GetXaxis()->SetTitle("x crystal index, viewed from back of calorimeter");
   multigraph->GetXaxis()->SetLabelFont(42);
   multigraph->GetXaxis()->SetLabelSize(0.035);
   multigraph->GetXaxis()->SetTitleSize(0.035);
   multigraph->GetXaxis()->SetTitleOffset(1);
   multigraph->GetXaxis()->SetTitleFont(42);
   multigraph->GetYaxis()->SetTitle("MC Elastic Peak / Data Elastic Peak");
   multigraph->GetYaxis()->SetLabelFont(42);
   multigraph->GetYaxis()->SetLabelSize(0.035);
   multigraph->GetYaxis()->SetTitleSize(0.035);
   multigraph->GetYaxis()->SetTitleFont(42);
   
   TPaveText *pt = new TPaveText(0.3227759,0.94,0.6772241,0.995,"blNDC");
   pt->SetName("title");
   pt->SetBorderSize(0);
   pt->SetFillColor(0);
   pt->SetFillStyle(0);
   pt->SetTextFont(42);
   TText *pt_LaTex = pt->AddText("Elastic Peak Position");
   pt->Draw();
   
   TLegend *leg = new TLegend(0.8,0.65,0.95,0.95,NULL,"brNDC");
   leg->SetBorderSize(1);
   leg->SetLineColor(1);
   leg->SetLineStyle(1);
   leg->SetLineWidth(1);
   leg->SetFillColor(0);
   leg->SetFillStyle(1001);
   TLegendEntry *entry=leg->AddEntry("NULL","Row in y","h");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(42);
   entry=leg->AddEntry("grp9","y=5","lep");
   entry->SetLineColor(11);
   entry->SetLineStyle(1);
   entry->SetLineWidth(3);
   entry->SetMarkerColor(11);
   entry->SetMarkerStyle(31);
   entry->SetMarkerSize(2);
   entry->SetTextFont(42);
   entry=leg->AddEntry("grp8","y=4","lep");
   entry->SetLineColor(9);
   entry->SetLineStyle(1);
   entry->SetLineWidth(3);
   entry->SetMarkerColor(9);
   entry->SetMarkerStyle(31);
   entry->SetMarkerSize(2);
   entry->SetTextFont(42);
   entry=leg->AddEntry("grp7","y=3","lep");
   entry->SetLineColor(8);
   entry->SetLineStyle(1);
   entry->SetLineWidth(3);
   entry->SetMarkerColor(8);
   entry->SetMarkerStyle(31);
   entry->SetMarkerSize(2);
   entry->SetTextFont(42);
   entry=leg->AddEntry("grp6","y=2","lep");
   entry->SetLineColor(7);
   entry->SetLineStyle(1);
   entry->SetLineWidth(3);
   entry->SetMarkerColor(7);
   entry->SetMarkerStyle(31);
   entry->SetMarkerSize(2);
   entry->SetTextFont(42);
   entry=leg->AddEntry("grp5","y=1","lep");
   entry->SetLineColor(6);
   entry->SetLineStyle(1);
   entry->SetLineWidth(3);
   entry->SetMarkerColor(6);
   entry->SetMarkerStyle(31);
   entry->SetMarkerSize(2);
   entry->SetTextFont(42);
   entry=leg->AddEntry("grp4","y=-1","lep");
   entry->SetLineColor(5);
   entry->SetLineStyle(1);
   entry->SetLineWidth(3);
   entry->SetMarkerColor(5);
   entry->SetMarkerStyle(31);
   entry->SetMarkerSize(2);
   entry->SetTextFont(42);
   entry=leg->AddEntry("grp3","y=-2","lep");
   entry->SetLineColor(4);
   entry->SetLineStyle(1);
   entry->SetLineWidth(3);
   entry->SetMarkerColor(4);
   entry->SetMarkerStyle(31);
   entry->SetMarkerSize(2);
   entry->SetTextFont(42);
   entry=leg->AddEntry("grp2","y=-3","lep");
   entry->SetLineColor(3);
   entry->SetLineStyle(1);
   entry->SetLineWidth(3);
   entry->SetMarkerColor(3);
   entry->SetMarkerStyle(31);
   entry->SetMarkerSize(2);
   entry->SetTextFont(42);
   entry=leg->AddEntry("grp1","y=-4","lep");
   entry->SetLineColor(2);
   entry->SetLineStyle(1);
   entry->SetLineWidth(3);
   entry->SetMarkerColor(2);
   entry->SetMarkerStyle(31);
   entry->SetMarkerSize(2);
   entry->SetTextFont(42);
   entry=leg->AddEntry("grp0","y=-5","lep");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(3);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(31);
   entry->SetMarkerSize(2);
   entry->SetTextFont(42);
   leg->Draw();
   scr->Modified();
   scr->cd();
   scr->SetSelected(scr);
}
