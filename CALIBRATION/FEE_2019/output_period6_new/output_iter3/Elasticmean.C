void Elasticmean()
{
//=========Macro generated from canvas: scr/xxxx
//=========  (Mon Jul 13 23:11:12 2020) by ROOT version 6.18/04
   TCanvas *scr = new TCanvas("scr", "xxxx",0,0,1200,800);
   gStyle->SetOptFit(1);
   gStyle->SetOptStat(0);
   scr->Range(-24.8125,-0.1875,17.8125,1.6875);
   scr->SetFillColor(0);
   scr->SetBorderMode(0);
   scr->SetBorderSize(2);
   scr->SetFrameBorderMode(0);
   scr->SetFrameBorderMode(0);
   
   TMultiGraph *multigraph = new TMultiGraph();
   multigraph->SetName("");
   multigraph->SetTitle("Elastic Peak Position");
   
   Double_t grp0_fx1[21] = {
   -17,
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
   7};
   Double_t grp0_fy1[21] = {
   0.9881603,
   0.9880844,
   0.989535,
   0.9962597,
   0.9918738,
   1.00312,
   0.9980291,
   0.9984171,
   0.9963125,
   0.9828328,
   0.9956303,
   1.000343,
   1.000215,
   0.9999138,
   0.9958064,
   0.9947733,
   0.9997599,
   0.9956567,
   1.000612,
   0.9967518,
   0.9805816};
   TGraph *graph = new TGraph(21,grp0_fx1,grp0_fy1);
   graph->SetName("grp0");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineWidth(3);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp01 = new TH1F("Graph_grp01","",100,-19.4,9.4);
   Graph_grp01->SetMinimum(0.9783278);
   Graph_grp01->SetMaximum(1.005374);
   Graph_grp01->SetDirectory(0);
   Graph_grp01->SetStats(0);

   Int_t ci;      // for color index setting
   TColor *color; // for color definition with alpha
   ci = TColor::GetColor("#000099");
   Graph_grp01->SetLineColor(ci);
   Graph_grp01->GetXaxis()->SetLabelFont(42);
   Graph_grp01->GetXaxis()->SetLabelSize(0.035);
   Graph_grp01->GetXaxis()->SetTitleSize(0.035);
   Graph_grp01->GetXaxis()->SetTitleOffset(1);
   Graph_grp01->GetXaxis()->SetTitleFont(42);
   Graph_grp01->GetYaxis()->SetLabelFont(42);
   Graph_grp01->GetYaxis()->SetLabelSize(0.035);
   Graph_grp01->GetYaxis()->SetTitleSize(0.035);
   Graph_grp01->GetYaxis()->SetTitleFont(42);
   Graph_grp01->GetZaxis()->SetLabelFont(42);
   Graph_grp01->GetZaxis()->SetLabelSize(0.035);
   Graph_grp01->GetZaxis()->SetTitleSize(0.035);
   Graph_grp01->GetZaxis()->SetTitleOffset(1);
   Graph_grp01->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_grp01);
   
   multigraph->Add(graph,"LP");
   
   Double_t grp1_fx2[30] = {
   -19,
   -18,
   -17,
   -16,
   -15,
   -14,
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
   12};
   Double_t grp1_fy2[30] = {
   1.004378,
   0.9932166,
   0.9963154,
   0.9905242,
   1.000184,
   0.9793102,
   0.9922143,
   0.9999492,
   1.002729,
   1.000048,
   1.000262,
   0.9990513,
   1.003856,
   1.004074,
   1.006284,
   1.000606,
   0.9969106,
   1.001068,
   1.00069,
   1.000904,
   0.9988942,
   1.003309,
   0.9952494,
   1.00475,
   0.9979383,
   0.9941394,
   0.9985305,
   1.001224,
   0.9978291,
   0.9914893};
   graph = new TGraph(30,grp1_fx2,grp1_fy2);
   graph->SetName("grp1");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(2);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(2);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp12 = new TH1F("Graph_grp12","",100,-22.1,15.1);
   Graph_grp12->SetMinimum(0.9766128);
   Graph_grp12->SetMaximum(1.008981);
   Graph_grp12->SetDirectory(0);
   Graph_grp12->SetStats(0);

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
   
   Double_t grp2_fx3[30] = {
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
   12};
   Double_t grp2_fy3[30] = {
   1.003113,
   0.9967134,
   1.003461,
   1.002273,
   0.990213,
   0.9892818,
   0.9984328,
   0.9991829,
   1.002688,
   0.9981467,
   1.000123,
   0.9936258,
   1.00055,
   1.001,
   0.9984363,
   1.001328,
   1.001383,
   1.001229,
   0.9989838,
   0.9974197,
   0.9993701,
   1.00126,
   0.9988706,
   0.9975509,
   1.01745,
   0.9939558,
   1.006602,
   0.9954829,
   1.005366,
   1.002417};
   graph = new TGraph(30,grp2_fx3,grp2_fy3);
   graph->SetName("grp2");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(3);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(3);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp23 = new TH1F("Graph_grp23","",100,-21,15);
   Graph_grp23->SetMinimum(0.986465);
   Graph_grp23->SetMaximum(1.020267);
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
   
   Double_t grp3_fx4[28] = {
   -18,
   -17,
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
   12};
   Double_t grp3_fy4[28] = {
   1.00247,
   1.002087,
   1.007881,
   1.000649,
   0.9930832,
   1.005387,
   0.9934682,
   1.000564,
   0.9940746,
   1.015893,
   0.9922851,
   1.004694,
   0.9994459,
   0.998426,
   0.9999322,
   1.003669,
   0.9888633,
   1.010098,
   0.9969387,
   0.9981326,
   0.9943268,
   1.005762,
   0.9976622,
   0.9993796,
   1.000397,
   0.9960993,
   0.9931648,
   0.9929317};
   graph = new TGraph(28,grp3_fx4,grp3_fy4);
   graph->SetName("grp3");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(4);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(4);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp34 = new TH1F("Graph_grp34","",100,-21,15);
   Graph_grp34->SetMinimum(0.9861604);
   Graph_grp34->SetMaximum(1.018596);
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
   
   Double_t grp4_fx5[4] = {
   -14,
   -12,
   7,
   8};
   Double_t grp4_fy5[4] = {
   0.9990171,
   0.9940999,
   0.9797088,
   0.9790645};
   graph = new TGraph(4,grp4_fx5,grp4_fy5);
   graph->SetName("grp4");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(5);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(5);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp45 = new TH1F("Graph_grp45","",100,-16.2,10.2);
   Graph_grp45->SetMinimum(0.9770692);
   Graph_grp45->SetMaximum(1.001012);
   Graph_grp45->SetDirectory(0);
   Graph_grp45->SetStats(0);

   ci = TColor::GetColor("#000099");
   Graph_grp45->SetLineColor(ci);
   Graph_grp45->GetXaxis()->SetLabelFont(42);
   Graph_grp45->GetXaxis()->SetLabelSize(0.035);
   Graph_grp45->GetXaxis()->SetTitleSize(0.035);
   Graph_grp45->GetXaxis()->SetTitleOffset(1);
   Graph_grp45->GetXaxis()->SetTitleFont(42);
   Graph_grp45->GetYaxis()->SetLabelFont(42);
   Graph_grp45->GetYaxis()->SetLabelSize(0.035);
   Graph_grp45->GetYaxis()->SetTitleSize(0.035);
   Graph_grp45->GetYaxis()->SetTitleFont(42);
   Graph_grp45->GetZaxis()->SetLabelFont(42);
   Graph_grp45->GetZaxis()->SetLabelSize(0.035);
   Graph_grp45->GetZaxis()->SetTitleSize(0.035);
   Graph_grp45->GetZaxis()->SetTitleOffset(1);
   Graph_grp45->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_grp45);
   
   multigraph->Add(graph,"LP");
   
   Double_t grp5_fx6[9] = {
   -12,
   -1,
   4,
   5,
   6,
   7,
   8,
   9,
   10};
   Double_t grp5_fy6[9] = {
   0.9966593,
   1.003734,
   0.9823613,
   0.9885723,
   1.001313,
   0.9830726,
   0.9743904,
   0.9809279,
   1.001207};
   graph = new TGraph(9,grp5_fx6,grp5_fy6);
   graph->SetName("grp5");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(6);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(6);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp56 = new TH1F("Graph_grp56","",100,-14.2,12.2);
   Graph_grp56->SetMinimum(0.9714561);
   Graph_grp56->SetMaximum(1.006669);
   Graph_grp56->SetDirectory(0);
   Graph_grp56->SetStats(0);

   ci = TColor::GetColor("#000099");
   Graph_grp56->SetLineColor(ci);
   Graph_grp56->GetXaxis()->SetLabelFont(42);
   Graph_grp56->GetXaxis()->SetLabelSize(0.035);
   Graph_grp56->GetXaxis()->SetTitleSize(0.035);
   Graph_grp56->GetXaxis()->SetTitleOffset(1);
   Graph_grp56->GetXaxis()->SetTitleFont(42);
   Graph_grp56->GetYaxis()->SetLabelFont(42);
   Graph_grp56->GetYaxis()->SetLabelSize(0.035);
   Graph_grp56->GetYaxis()->SetTitleSize(0.035);
   Graph_grp56->GetYaxis()->SetTitleFont(42);
   Graph_grp56->GetZaxis()->SetLabelFont(42);
   Graph_grp56->GetZaxis()->SetLabelSize(0.035);
   Graph_grp56->GetZaxis()->SetTitleSize(0.035);
   Graph_grp56->GetZaxis()->SetTitleOffset(1);
   Graph_grp56->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_grp56);
   
   multigraph->Add(graph,"LP");
   
   Double_t grp6_fx7[27] = {
   -18,
   -17,
   -16,
   -15,
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
   5,
   6,
   7,
   8,
   9,
   10,
   11,
   12};
   Double_t grp6_fy7[27] = {
   0.9961372,
   0.9959162,
   1.000045,
   1.001555,
   0.9975184,
   1.000792,
   1.001633,
   1.002508,
   0.9974893,
   0.9998727,
   1.001475,
   0.999182,
   1.000281,
   0.9950057,
   1.002078,
   0.99919,
   0.9962084,
   0.9964489,
   0.9993534,
   1.008498,
   1.000658,
   1.000634,
   1.001992,
   1.000941,
   0.9875401,
   0.9976864,
   0.9930339};
   graph = new TGraph(27,grp6_fx7,grp6_fy7);
   graph->SetName("grp6");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(7);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(7);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp67 = new TH1F("Graph_grp67","",100,-21,15);
   Graph_grp67->SetMinimum(0.9854442);
   Graph_grp67->SetMaximum(1.010594);
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
   
   Double_t grp7_fx8[29] = {
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
   11};
   Double_t grp7_fy8[29] = {
   1.008155,
   0.998664,
   0.9980152,
   0.9960696,
   0.998797,
   1.001848,
   0.9942987,
   1.002262,
   0.9993907,
   0.9926553,
   1.000168,
   1.001446,
   0.9994968,
   1.000034,
   0.998273,
   1.00059,
   1.001099,
   1.000473,
   1.000364,
   1.003044,
   0.9999694,
   1.002076,
   1.003727,
   0.9984409,
   1.00015,
   1.00236,
   1.00015,
   1.004718,
   1.001448};
   graph = new TGraph(29,grp7_fx8,grp7_fy8);
   graph->SetName("grp7");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(8);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(8);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp78 = new TH1F("Graph_grp78","",100,-22,14);
   Graph_grp78->SetMinimum(0.9911054);
   Graph_grp78->SetMaximum(1.009705);
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
   
   Double_t grp8_fx9[31] = {
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
   12};
   Double_t grp8_fy9[31] = {
   0.9964463,
   1.023487,
   0.9970735,
   0.9986885,
   0.9989876,
   1.000886,
   1.002428,
   1.003124,
   1.005259,
   1.000252,
   1.002873,
   0.9990001,
   1.000433,
   0.9982414,
   1.001598,
   1.004065,
   0.9996532,
   0.9989965,
   1.000902,
   1.001974,
   1.002305,
   1.006368,
   1.007264,
   0.9995517,
   1.002619,
   0.9975256,
   0.9992365,
   1.001168,
   1.000772,
   0.9955182,
   1.000192};
   graph = new TGraph(31,grp8_fx9,grp8_fy9);
   graph->SetName("grp8");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(9);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(9);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp89 = new TH1F("Graph_grp89","",100,-22.1,15.1);
   Graph_grp89->SetMinimum(0.9927213);
   Graph_grp89->SetMaximum(1.026284);
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
   
   Double_t grp9_fx10[21] = {
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
   9};
   Double_t grp9_fy10[21] = {
   0.975041,
   0.9753774,
   0.9970889,
   1.003456,
   0.9923837,
   0.9997327,
   0.9967813,
   0.9970216,
   0.9995294,
   0.9958891,
   1.004884,
   0.9987333,
   0.9984956,
   1.003838,
   1.005075,
   0.9625037,
   0.9802147,
   0.9856503,
   0.9254852,
   0.9744653,
   0.9620706};
   graph = new TGraph(21,grp9_fx10,grp9_fy10);
   graph->SetName("grp9");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(11);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(11);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp910 = new TH1F("Graph_grp910","",100,-15.2,11.2);
   Graph_grp910->SetMinimum(0.9175262);
   Graph_grp910->SetMaximum(1.013034);
   Graph_grp910->SetDirectory(0);
   Graph_grp910->SetStats(0);

   ci = TColor::GetColor("#000099");
   Graph_grp910->SetLineColor(ci);
   Graph_grp910->GetXaxis()->SetLabelFont(42);
   Graph_grp910->GetXaxis()->SetLabelSize(0.035);
   Graph_grp910->GetXaxis()->SetTitleSize(0.035);
   Graph_grp910->GetXaxis()->SetTitleOffset(1);
   Graph_grp910->GetXaxis()->SetTitleFont(42);
   Graph_grp910->GetYaxis()->SetLabelFont(42);
   Graph_grp910->GetYaxis()->SetLabelSize(0.035);
   Graph_grp910->GetYaxis()->SetTitleSize(0.035);
   Graph_grp910->GetYaxis()->SetTitleFont(42);
   Graph_grp910->GetZaxis()->SetLabelFont(42);
   Graph_grp910->GetZaxis()->SetLabelSize(0.035);
   Graph_grp910->GetZaxis()->SetTitleSize(0.035);
   Graph_grp910->GetZaxis()->SetTitleOffset(1);
   Graph_grp910->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_grp910);
   
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
