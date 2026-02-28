void Elasticmean()
{
//=========Macro generated from canvas: scr/xxxx
//=========  (Wed Jul 22 17:59:01 2020) by ROOT version 6.18/04
   TCanvas *scr = new TCanvas("scr", "xxxx",0,0,1200,800);
   gStyle->SetOptFit(1);
   gStyle->SetOptStat(0);
   scr->Range(-16.1875,-0.1875,7.1875,1.6875);
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
   
   Double_t grp1_fx2[14] = {
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
   2};
   Double_t grp1_fy2[14] = {
   0.9944027,
   0.998735,
   0.9909386,
   0.9967934,
   0.9944923,
   0.9947188,
   0.9980841,
   0.9987792,
   1.001783,
   0.9989621,
   0.9947577,
   0.9979984,
   0.9984029,
   0.9983434};
   graph = new TGraph(14,grp1_fx2,grp1_fy2);
   graph->SetName("grp1");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(2);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(2);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp12 = new TH1F("Graph_grp12","",100,-13.4,3.4);
   Graph_grp12->SetMinimum(0.9898541);
   Graph_grp12->SetMaximum(1.002868);
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
   
   Double_t grp2_fx3[15] = {
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
   3};
   Double_t grp2_fy3[15] = {
   0.9917802,
   0.9997981,
   1.004469,
   0.9983196,
   1.001714,
   0.9933594,
   1.001039,
   1.001742,
   0.9987715,
   1.001853,
   1.002168,
   1.002454,
   0.9988253,
   0.9929571,
   0.9949523};
   graph = new TGraph(15,grp2_fx3,grp2_fy3);
   graph->SetName("grp2");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(3);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(3);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp23 = new TH1F("Graph_grp23","",100,-13.5,4.5);
   Graph_grp23->SetMinimum(0.9905113);
   Graph_grp23->SetMaximum(1.005738);
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
   
   Double_t grp3_fx4[17] = {
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
   4};
   Double_t grp3_fy4[17] = {
   0.9942156,
   0.9926618,
   1.007571,
   1.000142,
   0.9990098,
   0.9874473,
   1.012145,
   0.9921616,
   1.004188,
   1.000144,
   0.9933442,
   0.9986821,
   1.003935,
   0.9926521,
   1.006063,
   0.9955206,
   0.9918978};
   graph = new TGraph(17,grp3_fx4,grp3_fy4);
   graph->SetName("grp3");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(4);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(4);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp34 = new TH1F("Graph_grp34","",100,-14.7,5.7);
   Graph_grp34->SetMinimum(0.9849776);
   Graph_grp34->SetMaximum(1.014615);
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
   
   Double_t grp6_fx7[13] = {
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
   4};
   Double_t grp6_fy7[13] = {
   0.9982202,
   0.9986898,
   0.99727,
   1.000503,
   1.001444,
   0.9976942,
   1.001341,
   0.9989966,
   1.002463,
   0.997246,
   0.9983839,
   0.9949708,
   0.9921198};
   graph = new TGraph(13,grp6_fx7,grp6_fy7);
   graph->SetName("grp6");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(7);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(7);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp67 = new TH1F("Graph_grp67","",100,-13.6,5.6);
   Graph_grp67->SetMinimum(0.9910854);
   Graph_grp67->SetMaximum(1.003498);
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
   
   Double_t grp7_fx8[14] = {
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
   3};
   Double_t grp7_fy8[14] = {
   0.9871586,
   1.00339,
   0.9913871,
   1.000686,
   1.002455,
   1.000347,
   1.00065,
   0.9984112,
   1.000831,
   1.001112,
   0.9997516,
   1.002331,
   1.003408,
   0.9896486};
   graph = new TGraph(14,grp7_fx8,grp7_fy8);
   graph->SetName("grp7");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(8);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(8);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp78 = new TH1F("Graph_grp78","",100,-13.5,4.5);
   Graph_grp78->SetMinimum(0.9855337);
   Graph_grp78->SetMaximum(1.005033);
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
   
   Double_t grp8_fx9[13] = {
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
   2};
   Double_t grp8_fy9[13] = {
   0.9951404,
   0.9972537,
   0.9938824,
   0.9944988,
   1.000669,
   0.9957702,
   0.9949633,
   1.000459,
   0.9965558,
   0.9935704,
   0.9976436,
   0.9871634,
   0.9986817};
   graph = new TGraph(13,grp8_fx9,grp8_fy9);
   graph->SetName("grp8");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(9);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(9);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp89 = new TH1F("Graph_grp89","",100,-12.3,3.3);
   Graph_grp89->SetMinimum(0.9858128);
   Graph_grp89->SetMaximum(1.00202);
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
