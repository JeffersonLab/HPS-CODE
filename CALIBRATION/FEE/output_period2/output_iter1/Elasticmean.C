void Elasticmean()
{
//=========Macro generated from canvas: scr/xxxx
//=========  (Fri Feb 25 18:52:18 2022) by ROOT version 6.24/06
   TCanvas *scr = new TCanvas("scr", "xxxx",0,0,1200,800);
   gStyle->SetOptFit(1);
   gStyle->SetOptStat(0);
   scr->Range(-26.9375,-0.1875,23.9375,1.6875);
   scr->SetFillColor(0);
   scr->SetBorderMode(0);
   scr->SetBorderSize(2);
   scr->SetFrameBorderMode(0);
   scr->SetFrameBorderMode(0);
   
   TMultiGraph *multigraph = new TMultiGraph();
   multigraph->SetName("");
   multigraph->SetTitle("Elastic Peak Position");
   
   Double_t grp0_fx1[25] = {
   -16,
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
   1,
   2,
   3,
   4,
   6,
   7,
   8,
   9,
   10,
   11,
   12};
   Double_t grp0_fy1[25] = {
   1.139955,
   1.093925,
   1.118862,
   1.094905,
   1.065374,
   1.058802,
   1.115152,
   1.072232,
   1.078047,
   1.056879,
   0.8975353,
   1.024731,
   1.07254,
   1.105433,
   1.089544,
   1.06949,
   1.129968,
   1.0944,
   1.089333,
   1.105796,
   1.100084,
   1.119268,
   1.154264,
   1.155928,
   1.15449};
   TGraph *graph = new TGraph(25,grp0_fx1,grp0_fy1);
   graph->SetName("grp0");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineWidth(3);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp01 = new TH1F("Graph_grp01","",100,-18.8,14.8);
   Graph_grp01->SetMinimum(0.871696);
   Graph_grp01->SetMaximum(1.181767);
   Graph_grp01->SetDirectory(0);
   Graph_grp01->SetStats(0);

   Int_t ci;      // for color index setting
   TColor *color; // for color definition with alpha
   ci = TColor::GetColor("#000099");
   Graph_grp01->SetLineColor(ci);
   Graph_grp01->GetXaxis()->SetLabelFont(42);
   Graph_grp01->GetXaxis()->SetTitleOffset(1);
   Graph_grp01->GetXaxis()->SetTitleFont(42);
   Graph_grp01->GetYaxis()->SetLabelFont(42);
   Graph_grp01->GetYaxis()->SetTitleFont(42);
   Graph_grp01->GetZaxis()->SetLabelFont(42);
   Graph_grp01->GetZaxis()->SetTitleOffset(1);
   Graph_grp01->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_grp01);
   
   multigraph->Add(graph,"LP");
   
   Double_t grp1_fx2[37] = {
   -20,
   -19,
   -18,
   -17,
   -16,
   -15,
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
   5,
   6,
   7,
   8,
   9,
   10,
   11,
   12,
   13,
   14,
   15,
   16,
   17};
   Double_t grp1_fy2[37] = {
   1.26332,
   1.115941,
   1.106483,
   1.151586,
   1.175306,
   1.105526,
   1.09226,
   1.045017,
   1.087564,
   1.102857,
   1.109138,
   1.100026,
   1.104193,
   1.114794,
   1.119582,
   1.099027,
   1.114091,
   1.106412,
   1.095409,
   1.079972,
   1.096921,
   1.099233,
   1.116922,
   1.101469,
   1.09979,
   1.103261,
   1.121947,
   1.107225,
   1.097705,
   1.095383,
   1.098764,
   1.118548,
   1.140359,
   1.147897,
   1.159357,
   1.224516,
   1.467888};
   graph = new TGraph(37,grp1_fx2,grp1_fy2);
   graph->SetName("grp1");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(2);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(2);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp12 = new TH1F("Graph_grp12","",100,-23.7,20.7);
   Graph_grp12->SetMinimum(1.00273);
   Graph_grp12->SetMaximum(1.510175);
   Graph_grp12->SetDirectory(0);
   Graph_grp12->SetStats(0);

   ci = TColor::GetColor("#000099");
   Graph_grp12->SetLineColor(ci);
   Graph_grp12->GetXaxis()->SetLabelFont(42);
   Graph_grp12->GetXaxis()->SetTitleOffset(1);
   Graph_grp12->GetXaxis()->SetTitleFont(42);
   Graph_grp12->GetYaxis()->SetLabelFont(42);
   Graph_grp12->GetYaxis()->SetTitleFont(42);
   Graph_grp12->GetZaxis()->SetLabelFont(42);
   Graph_grp12->GetZaxis()->SetTitleOffset(1);
   Graph_grp12->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_grp12);
   
   multigraph->Add(graph,"LP");
   
   Double_t grp2_fx3[35] = {
   -20,
   -19,
   -18,
   -17,
   -16,
   -15,
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
   5,
   6,
   8,
   9,
   10,
   11,
   12,
   13,
   14,
   15,
   16};
   Double_t grp2_fy3[35] = {
   1.242252,
   1.15189,
   1.10269,
   1.090969,
   1.063206,
   1.037441,
   1.078001,
   1.08631,
   1.080631,
   1.09306,
   1.103151,
   1.088981,
   1.122991,
   1.133074,
   1.108801,
   1.111917,
   1.111555,
   1.103319,
   1.087743,
   1.087495,
   1.098164,
   1.085189,
   1.093024,
   1.087292,
   1.05967,
   1.114668,
   1.15148,
   1.099301,
   1.093066,
   1.096628,
   1.089432,
   1.156655,
   1.175609,
   1.155464,
   1.253347};
   graph = new TGraph(35,grp2_fx3,grp2_fy3);
   graph->SetName("grp2");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(3);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(3);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp23 = new TH1F("Graph_grp23","",100,-23.6,19.6);
   Graph_grp23->SetMinimum(1.015851);
   Graph_grp23->SetMaximum(1.274937);
   Graph_grp23->SetDirectory(0);
   Graph_grp23->SetStats(0);

   ci = TColor::GetColor("#000099");
   Graph_grp23->SetLineColor(ci);
   Graph_grp23->GetXaxis()->SetLabelFont(42);
   Graph_grp23->GetXaxis()->SetTitleOffset(1);
   Graph_grp23->GetXaxis()->SetTitleFont(42);
   Graph_grp23->GetYaxis()->SetLabelFont(42);
   Graph_grp23->GetYaxis()->SetTitleFont(42);
   Graph_grp23->GetZaxis()->SetLabelFont(42);
   Graph_grp23->GetZaxis()->SetTitleOffset(1);
   Graph_grp23->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_grp23);
   
   multigraph->Add(graph,"LP");
   
   Double_t grp3_fx4[35] = {
   -20,
   -19,
   -18,
   -17,
   -16,
   -15,
   -14,
   -13,
   -12,
   -11,
   -10,
   -9,
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
   5,
   6,
   7,
   8,
   9,
   10,
   11,
   12,
   13,
   14,
   15,
   16,
   17};
   Double_t grp3_fy4[35] = {
   1.237328,
   1.205868,
   1.108798,
   1.086785,
   1.118772,
   1.086862,
   1.048133,
   1.076907,
   1.090405,
   1.096484,
   1.108147,
   1.107448,
   1.206114,
   1.152585,
   1.137439,
   1.109361,
   1.098114,
   1.09792,
   1.104125,
   1.096032,
   1.087422,
   1.116874,
   1.105463,
   1.067452,
   1.122888,
   1.104944,
   1.095131,
   1.095494,
   1.11034,
   1.106324,
   1.161807,
   1.182268,
   1.152452,
   1.220874,
   1.197124};
   graph = new TGraph(35,grp3_fx4,grp3_fy4);
   graph->SetName("grp3");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(4);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(4);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp34 = new TH1F("Graph_grp34","",100,-23.7,20.7);
   Graph_grp34->SetMinimum(1.029213);
   Graph_grp34->SetMaximum(1.256248);
   Graph_grp34->SetDirectory(0);
   Graph_grp34->SetStats(0);

   ci = TColor::GetColor("#000099");
   Graph_grp34->SetLineColor(ci);
   Graph_grp34->GetXaxis()->SetLabelFont(42);
   Graph_grp34->GetXaxis()->SetTitleOffset(1);
   Graph_grp34->GetXaxis()->SetTitleFont(42);
   Graph_grp34->GetYaxis()->SetLabelFont(42);
   Graph_grp34->GetYaxis()->SetTitleFont(42);
   Graph_grp34->GetZaxis()->SetLabelFont(42);
   Graph_grp34->GetZaxis()->SetTitleOffset(1);
   Graph_grp34->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_grp34);
   
   multigraph->Add(graph,"LP");
   
   Double_t grp4_fx5[7] = {
   -18,
   -1,
   7,
   8,
   9,
   10,
   11};
   Double_t grp4_fy5[7] = {
   1.389879,
   1.303191,
   1.156558,
   1.141707,
   1.136626,
   1.126222,
   1.17988};
   graph = new TGraph(7,grp4_fx5,grp4_fy5);
   graph->SetName("grp4");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(5);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(5);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp45 = new TH1F("Graph_grp45","",100,-20.9,13.9);
   Graph_grp45->SetMinimum(1.099856);
   Graph_grp45->SetMaximum(1.416245);
   Graph_grp45->SetDirectory(0);
   Graph_grp45->SetStats(0);

   ci = TColor::GetColor("#000099");
   Graph_grp45->SetLineColor(ci);
   Graph_grp45->GetXaxis()->SetLabelFont(42);
   Graph_grp45->GetXaxis()->SetTitleOffset(1);
   Graph_grp45->GetXaxis()->SetTitleFont(42);
   Graph_grp45->GetYaxis()->SetLabelFont(42);
   Graph_grp45->GetYaxis()->SetTitleFont(42);
   Graph_grp45->GetZaxis()->SetLabelFont(42);
   Graph_grp45->GetZaxis()->SetTitleOffset(1);
   Graph_grp45->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_grp45);
   
   multigraph->Add(graph,"LP");
   
   Double_t grp5_fx6[5] = {
   -14,
   9,
   10,
   11,
   12};
   Double_t grp5_fy6[5] = {
   1.19873,
   1.146798,
   1.208192,
   1.125866,
   1.153188};
   graph = new TGraph(5,grp5_fx6,grp5_fy6);
   graph->SetName("grp5");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(6);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(6);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp56 = new TH1F("Graph_grp56","",100,-16.6,14.6);
   Graph_grp56->SetMinimum(1.117633);
   Graph_grp56->SetMaximum(1.216425);
   Graph_grp56->SetDirectory(0);
   Graph_grp56->SetStats(0);

   ci = TColor::GetColor("#000099");
   Graph_grp56->SetLineColor(ci);
   Graph_grp56->GetXaxis()->SetLabelFont(42);
   Graph_grp56->GetXaxis()->SetTitleOffset(1);
   Graph_grp56->GetXaxis()->SetTitleFont(42);
   Graph_grp56->GetYaxis()->SetLabelFont(42);
   Graph_grp56->GetYaxis()->SetTitleFont(42);
   Graph_grp56->GetZaxis()->SetLabelFont(42);
   Graph_grp56->GetZaxis()->SetTitleOffset(1);
   Graph_grp56->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_grp56);
   
   multigraph->Add(graph,"LP");
   
   Double_t grp6_fx7[35] = {
   -20,
   -19,
   -18,
   -17,
   -16,
   -15,
   -14,
   -13,
   -12,
   -11,
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
   5,
   6,
   7,
   8,
   9,
   10,
   11,
   12,
   13,
   14,
   15,
   16,
   17};
   Double_t grp6_fy7[35] = {
   1.175074,
   1.193915,
   1.083098,
   1.099515,
   1.09578,
   1.089142,
   1.086011,
   1.089835,
   1.071557,
   1.071935,
   1.115234,
   1.105389,
   1.126244,
   1.113354,
   1.09695,
   1.079185,
   1.07624,
   1.080628,
   1.156688,
   1.097279,
   1.102843,
   1.103836,
   1.099631,
   1.098862,
   1.098144,
   1.08665,
   1.092914,
   1.088439,
   1.096399,
   1.088656,
   1.113552,
   1.156653,
   1.189602,
   1.167757,
   1.199684};
   graph = new TGraph(35,grp6_fx7,grp6_fy7);
   graph->SetName("grp6");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(7);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(7);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp67 = new TH1F("Graph_grp67","",100,-23.7,20.7);
   Graph_grp67->SetMinimum(1.058745);
   Graph_grp67->SetMaximum(1.212497);
   Graph_grp67->SetDirectory(0);
   Graph_grp67->SetStats(0);

   ci = TColor::GetColor("#000099");
   Graph_grp67->SetLineColor(ci);
   Graph_grp67->GetXaxis()->SetLabelFont(42);
   Graph_grp67->GetXaxis()->SetTitleOffset(1);
   Graph_grp67->GetXaxis()->SetTitleFont(42);
   Graph_grp67->GetYaxis()->SetLabelFont(42);
   Graph_grp67->GetYaxis()->SetTitleFont(42);
   Graph_grp67->GetZaxis()->SetLabelFont(42);
   Graph_grp67->GetZaxis()->SetTitleOffset(1);
   Graph_grp67->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_grp67);
   
   multigraph->Add(graph,"LP");
   
   Double_t grp7_fx8[36] = {
   -20,
   -19,
   -18,
   -17,
   -16,
   -15,
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
   5,
   6,
   7,
   8,
   9,
   10,
   11,
   12,
   13,
   14,
   15,
   16};
   Double_t grp7_fy8[36] = {
   1.151047,
   1.08702,
   1.090479,
   1.084751,
   1.091887,
   1.077439,
   1.114796,
   1.086687,
   1.081376,
   1.065913,
   1.087007,
   1.131146,
   1.079605,
   1.075519,
   1.080436,
   1.077351,
   1.083856,
   1.085063,
   1.070513,
   1.071612,
   1.089234,
   1.080082,
   1.094702,
   1.088788,
   1.09835,
   1.097677,
   1.09703,
   1.093706,
   1.087132,
   1.096154,
   1.098903,
   1.097309,
   1.144809,
   1.148217,
   1.177637,
   1.162814};
   graph = new TGraph(36,grp7_fx8,grp7_fy8);
   graph->SetName("grp7");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(8);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(8);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp78 = new TH1F("Graph_grp78","",100,-23.6,19.6);
   Graph_grp78->SetMinimum(1.054741);
   Graph_grp78->SetMaximum(1.188809);
   Graph_grp78->SetDirectory(0);
   Graph_grp78->SetStats(0);

   ci = TColor::GetColor("#000099");
   Graph_grp78->SetLineColor(ci);
   Graph_grp78->GetXaxis()->SetLabelFont(42);
   Graph_grp78->GetXaxis()->SetTitleOffset(1);
   Graph_grp78->GetXaxis()->SetTitleFont(42);
   Graph_grp78->GetYaxis()->SetLabelFont(42);
   Graph_grp78->GetYaxis()->SetTitleFont(42);
   Graph_grp78->GetZaxis()->SetLabelFont(42);
   Graph_grp78->GetZaxis()->SetTitleOffset(1);
   Graph_grp78->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_grp78);
   
   multigraph->Add(graph,"LP");
   
   Double_t grp8_fx9[36] = {
   -20,
   -19,
   -18,
   -17,
   -16,
   -15,
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
   5,
   6,
   7,
   8,
   9,
   10,
   11,
   12,
   13,
   14,
   15,
   16};
   Double_t grp8_fy9[36] = {
   1.175177,
   1.097523,
   1.100501,
   1.088992,
   1.092366,
   1.134132,
   1.087065,
   1.101267,
   1.079691,
   1.08808,
   1.08947,
   1.085747,
   1.081947,
   1.091666,
   1.090779,
   1.078178,
   1.087663,
   1.075733,
   1.089296,
   1.080326,
   1.089894,
   1.099903,
   1.127859,
   1.114708,
   1.107356,
   1.092243,
   1.105408,
   1.102804,
   1.091005,
   1.090123,
   1.096338,
   1.091154,
   1.109187,
   1.158623,
   1.162775,
   1.131601};
   graph = new TGraph(36,grp8_fx9,grp8_fy9);
   graph->SetName("grp8");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(9);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(9);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp89 = new TH1F("Graph_grp89","",100,-23.6,19.6);
   Graph_grp89->SetMinimum(1.065789);
   Graph_grp89->SetMaximum(1.185121);
   Graph_grp89->SetDirectory(0);
   Graph_grp89->SetStats(0);

   ci = TColor::GetColor("#000099");
   Graph_grp89->SetLineColor(ci);
   Graph_grp89->GetXaxis()->SetLabelFont(42);
   Graph_grp89->GetXaxis()->SetTitleOffset(1);
   Graph_grp89->GetXaxis()->SetTitleFont(42);
   Graph_grp89->GetYaxis()->SetLabelFont(42);
   Graph_grp89->GetYaxis()->SetTitleFont(42);
   Graph_grp89->GetZaxis()->SetLabelFont(42);
   Graph_grp89->GetZaxis()->SetTitleOffset(1);
   Graph_grp89->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_grp89);
   
   multigraph->Add(graph,"LP");
   
   Double_t grp9_fx10[26] = {
   -16,
   -15,
   -14,
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
   4,
   5,
   6,
   7,
   8,
   9,
   10,
   11,
   12};
   Double_t grp9_fy10[26] = {
   1.138898,
   1.157398,
   1.128593,
   1.085668,
   1.070163,
   1.06754,
   1.110948,
   0.9335439,
   1.064927,
   1.142817,
   1.031443,
   1.002093,
   1.03385,
   1.008075,
   1.060184,
   1.125642,
   1.112022,
   1.11027,
   1.123358,
   1.086211,
   1.094512,
   1.114705,
   1.137355,
   1.108562,
   1.115017,
   1.170102};
   graph = new TGraph(26,grp9_fx10,grp9_fy10);
   graph->SetName("grp9");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(11);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(11);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp910 = new TH1F("Graph_grp910","",100,-18.8,14.8);
   Graph_grp910->SetMinimum(0.9098881);
   Graph_grp910->SetMaximum(1.193758);
   Graph_grp910->SetDirectory(0);
   Graph_grp910->SetStats(0);

   ci = TColor::GetColor("#000099");
   Graph_grp910->SetLineColor(ci);
   Graph_grp910->GetXaxis()->SetLabelFont(42);
   Graph_grp910->GetXaxis()->SetTitleOffset(1);
   Graph_grp910->GetXaxis()->SetTitleFont(42);
   Graph_grp910->GetYaxis()->SetLabelFont(42);
   Graph_grp910->GetYaxis()->SetTitleFont(42);
   Graph_grp910->GetZaxis()->SetLabelFont(42);
   Graph_grp910->GetZaxis()->SetTitleOffset(1);
   Graph_grp910->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_grp910);
   
   multigraph->Add(graph,"LP");
   multigraph->Draw("A");
   multigraph->GetXaxis()->SetLimits(-21.85, 18.85);
   multigraph->GetXaxis()->SetTitle("x crystal index, viewed from back of calorimeter");
   multigraph->GetXaxis()->SetLabelFont(42);
   multigraph->GetXaxis()->SetTitleOffset(1);
   multigraph->GetXaxis()->SetTitleFont(42);
   multigraph->GetYaxis()->SetTitle("MC Elastic Peak / Data Elastic Peak");
   multigraph->GetYaxis()->SetLabelFont(42);
   multigraph->GetYaxis()->SetTitleFont(42);
   multigraph->SetMinimum(0);
   multigraph->SetMaximum(1.5);
   
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
