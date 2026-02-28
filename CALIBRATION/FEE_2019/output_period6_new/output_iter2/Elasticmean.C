void Elasticmean()
{
//=========Macro generated from canvas: scr/xxxx
//=========  (Mon Jul 13 15:18:41 2020) by ROOT version 6.18/04
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
   
   Double_t grp0_fx1[20] = {
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
   Double_t grp0_fy1[20] = {
   0.9904742,
   0.9854503,
   0.979785,
   0.9788821,
   0.9963729,
   0.9830658,
   0.9887177,
   0.9841954,
   0.9440175,
   0.9848064,
   0.9884996,
   0.9932508,
   0.9973143,
   0.9865387,
   0.9837655,
   0.9984931,
   0.9859928,
   0.990873,
   0.973229,
   0.935093};
   TGraph *graph = new TGraph(20,grp0_fx1,grp0_fy1);
   graph->SetName("grp0");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineWidth(3);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp01 = new TH1F("Graph_grp01","",100,-15,9);
   Graph_grp01->SetMinimum(0.928753);
   Graph_grp01->SetMaximum(1.004833);
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
   
   Double_t grp1_fx2[31] = {
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
   Double_t grp1_fy2[31] = {
   1.0058,
   0.9824783,
   0.9813961,
   0.9781976,
   0.9989067,
   0.9922498,
   1.294155,
   1.000441,
   0.996733,
   0.9985867,
   0.9930909,
   0.9900847,
   0.9905645,
   1.003397,
   1.005872,
   1.012608,
   0.9986784,
   0.9877552,
   0.9958204,
   0.9943417,
   0.994436,
   0.9945694,
   1.002382,
   0.9835293,
   0.9991494,
   0.9831173,
   0.9761901,
   0.9889683,
   0.9945695,
   0.9868103,
   0.9785042};
   graph = new TGraph(31,grp1_fx2,grp1_fy2);
   graph->SetName("grp1");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(2);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(2);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp12 = new TH1F("Graph_grp12","",100,-22.1,15.1);
   Graph_grp12->SetMinimum(0.9443936);
   Graph_grp12->SetMaximum(1.325952);
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
   1.003365,
   0.9885895,
   0.9982874,
   1.002225,
   0.985679,
   0.9906945,
   0.9927247,
   0.9937416,
   1.001703,
   0.9908171,
   0.9971807,
   0.9868956,
   0.9971046,
   0.9989362,
   0.9924776,
   0.9986855,
   0.9997319,
   0.9995859,
   0.9879539,
   0.988704,
   0.9914787,
   0.9956929,
   0.9950067,
   0.9916525,
   1.03696,
   0.9831138,
   1.006323,
   0.9817327,
   1.000149,
   0.9980182};
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
   Graph_grp23->SetMinimum(0.97621);
   Graph_grp23->SetMaximum(1.042483);
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
   1.004256,
   1.003231,
   1.013266,
   0.9985162,
   0.9772715,
   1.005866,
   0.9832584,
   0.9993186,
   0.9938562,
   1.060559,
   0.9834698,
   0.9959211,
   0.9918508,
   0.9856802,
   0.9934106,
   1.004714,
   0.9702102,
   1.019175,
   0.9850916,
   0.9900462,
   0.9792136,
   1.004264,
   0.9777042,
   0.9807383,
   0.9941766,
   0.9850203,
   0.9765348,
   0.9802631};
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
   Graph_grp34->SetMinimum(0.9611753);
   Graph_grp34->SetMaximum(1.069594);
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
   
   Double_t grp4_fx5[6] = {
   -14,
   -13,
   -12,
   6,
   7,
   8};
   Double_t grp4_fy5[6] = {
   1.004321,
   0.9997632,
   0.9785286,
   0.9945594,
   0.933098,
   0.9312372};
   graph = new TGraph(6,grp4_fx5,grp4_fy5);
   graph->SetName("grp4");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(5);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(5);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp45 = new TH1F("Graph_grp45","",100,-16.2,10.2);
   Graph_grp45->SetMinimum(0.9239288);
   Graph_grp45->SetMaximum(1.011629);
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
   
   Double_t grp5_fx6[8] = {
   -12,
   -1,
   4,
   5,
   6,
   7,
   9,
   10};
   Double_t grp5_fy6[8] = {
   0.9772798,
   1.013429,
   0.9476113,
   0.9778996,
   0.986526,
   0.9476819,
   0.9392245,
   0.9962791};
   graph = new TGraph(8,grp5_fx6,grp5_fy6);
   graph->SetName("grp5");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(6);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(6);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp56 = new TH1F("Graph_grp56","",100,-14.2,12.2);
   Graph_grp56->SetMinimum(0.9318041);
   Graph_grp56->SetMaximum(1.02085);
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
   0.9922065,
   0.9910504,
   0.9988644,
   1.00138,
   0.9854751,
   0.9905196,
   0.9996744,
   0.999037,
   0.9847058,
   0.998933,
   1.00661,
   0.9924486,
   0.9927765,
   0.9838793,
   1.002248,
   0.9937879,
   0.9856386,
   0.9807033,
   0.9831376,
   1.013315,
   0.9939649,
   0.9908605,
   0.9945471,
   0.9883921,
   0.9573345,
   0.9800763,
   0.9691275};
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
   Graph_grp67->SetMinimum(0.9517365);
   Graph_grp67->SetMaximum(1.018913);
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
   
   Double_t grp7_fx8[30] = {
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
   11,
   12};
   Double_t grp7_fy8[30] = {
   1.015608,
   0.9892904,
   0.9840442,
   0.9865978,
   0.9941584,
   0.9989989,
   0.9819315,
   0.9955488,
   0.9902204,
   0.9761574,
   0.9955834,
   0.9971221,
   0.9953878,
   0.997475,
   0.9907567,
   0.9941268,
   0.9949176,
   0.9961771,
   0.9956344,
   0.9979053,
   0.9895027,
   0.9910708,
   0.9981304,
   0.9889591,
   0.9921451,
   0.9996359,
   0.9930336,
   1.006744,
   0.9966112,
   0.9505424};
   graph = new TGraph(30,grp7_fx8,grp7_fy8);
   graph->SetName("grp7");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(8);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(8);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp78 = new TH1F("Graph_grp78","",100,-22.1,15.1);
   Graph_grp78->SetMinimum(0.9440359);
   Graph_grp78->SetMaximum(1.022114);
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
   0.9910786,
   0.9653004,
   0.9854462,
   0.9892918,
   0.9905559,
   0.9944514,
   0.9858962,
   0.9869291,
   0.9950003,
   0.9913591,
   0.9991392,
   0.9908186,
   0.9967051,
   0.9903299,
   1.00014,
   1.004015,
   0.9919438,
   0.987789,
   0.9978467,
   1.000753,
   0.9896794,
   0.9834065,
   0.9851284,
   0.9766955,
   0.9967462,
   0.9825554,
   0.9826007,
   0.9928925,
   0.9946331,
   0.9846924,
   0.987743};
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
   Graph_grp89->SetMinimum(0.9614289);
   Graph_grp89->SetMaximum(1.007887);
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
   
   Double_t grp9_fx10[19] = {
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
   8};
   Double_t grp9_fy10[19] = {
   0.9158649,
   0.9183553,
   0.9728951,
   0.9898337,
   0.9689878,
   0.9853795,
   0.9872211,
   0.9919702,
   0.9901115,
   0.981065,
   0.9884283,
   0.9842701,
   0.985127,
   0.9994563,
   0.9842994,
   0.8773852,
   0.8990594,
   0.9328046,
   0.9227686};
   graph = new TGraph(19,grp9_fx10,grp9_fy10);
   graph->SetName("grp9");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(11);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(11);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp910 = new TH1F("Graph_grp910","",100,-15.1,10.1);
   Graph_grp910->SetMinimum(0.8651781);
   Graph_grp910->SetMaximum(1.011663);
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
