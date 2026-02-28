void Elasticmean()
{
//=========Macro generated from canvas: scr/xxxx
//=========  (Wed Jul 22 08:26:05 2020) by ROOT version 6.18/04
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
   0.9965133,
   0.9968734,
   0.9994247,
   0.9927355,
   0.9960707,
   0.9974374,
   0.9956666,
   1.000714,
   1.001672,
   1.000897,
   0.9935628,
   1.001301,
   1.000085,
   0.9997916};
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
   Graph_grp12->SetMinimum(0.9918418);
   Graph_grp12->SetMaximum(1.002566);
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
   
   Double_t grp2_fx3[16] = {
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
   Double_t grp2_fy3[16] = {
   1.002027,
   0.9993031,
   1.00287,
   0.9997714,
   1.000615,
   0.9931337,
   1.001871,
   1.002298,
   0.9989796,
   1.001897,
   1.002646,
   1.001502,
   1.000582,
   0.9956512,
   0.994692,
   0.8903078};
   graph = new TGraph(16,grp2_fx3,grp2_fy3);
   graph->SetName("grp2");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(3);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(3);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp23 = new TH1F("Graph_grp23","",100,-13.6,5.6);
   Graph_grp23->SetMinimum(0.8790516);
   Graph_grp23->SetMaximum(1.014126);
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
   1.001803,
   0.9837555,
   1.010109,
   0.9941797,
   1.005622,
   0.9945359,
   1.000765,
   0.9920052,
   1.00666,
   1.002035,
   0.9981974,
   0.9974071,
   1.002234,
   0.9900955,
   1.010396,
   0.9853988,
   0.9903417};
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
   Graph_grp34->SetMinimum(0.9810914);
   Graph_grp34->SetMaximum(1.013061);
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
   0.9978864,
   0.9999087,
   0.9960938,
   1.003447,
   1.003657,
   0.9958729,
   1.004051,
   0.9895248,
   1.001155,
   1.004209,
   0.9935332,
   0.9975951,
   0.999652};
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
   Graph_grp67->SetMinimum(0.9880565);
   Graph_grp67->SetMaximum(1.005677);
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
   0.9909826,
   0.9969541,
   0.9931631,
   1.000168,
   1.002053,
   1.000515,
   1.000996,
   0.9981971,
   0.999967,
   1.002331,
   1.000743,
   1.002189,
   1.000029,
   0.9976479};
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
   Graph_grp78->SetMinimum(0.9898477);
   Graph_grp78->SetMaximum(1.003466);
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
   
   Double_t grp8_fx9[15] = {
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
   Double_t grp8_fy9[15] = {
   0.8960657,
   0.9889548,
   0.9861403,
   0.9969729,
   0.997396,
   0.9987169,
   0.9956191,
   0.9971717,
   1.000556,
   0.9976659,
   0.9912215,
   0.9910452,
   0.9955818,
   0.9826091,
   0.8599773};
   graph = new TGraph(15,grp8_fx9,grp8_fy9);
   graph->SetName("grp8");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(9);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(9);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp89 = new TH1F("Graph_grp89","",100,-13.5,4.5);
   Graph_grp89->SetMinimum(0.8459195);
   Graph_grp89->SetMaximum(1.014614);
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
