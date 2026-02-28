void Elasticmean()
{
//=========Macro generated from canvas: scr/xxxx
//=========  (Fri Feb 25 15:37:40 2022) by ROOT version 6.24/06
   TCanvas *scr = new TCanvas("scr", "xxxx",0,0,1200,800);
   gStyle->SetOptFit(1);
   gStyle->SetOptStat(0);
   scr->Range(-28.125,-0.1875,24.125,1.6875);
   scr->SetFillColor(0);
   scr->SetBorderMode(0);
   scr->SetBorderSize(2);
   scr->SetFrameBorderMode(0);
   scr->SetFrameBorderMode(0);
   
   TMultiGraph *multigraph = new TMultiGraph();
   multigraph->SetName("");
   multigraph->SetTitle("Elastic Peak Position");
   
   Double_t grp0_fx1[24] = {
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
   5,
   6,
   7,
   8,
   9,
   10,
   11};
   Double_t grp0_fy1[24] = {
   0.9906667,
   0.9997104,
   1.002267,
   0.9944558,
   0.98913,
   1.001287,
   0.9878703,
   0.9959075,
   0.9896774,
   0.9449746,
   0.9886568,
   0.9951411,
   1.004514,
   1.001732,
   0.9878855,
   1.004466,
   0.9921672,
   0.9937733,
   0.9929951,
   0.9976912,
   0.992609,
   0.9990238,
   1.000858,
   1.00194};
   TGraph *graph = new TGraph(24,grp0_fx1,grp0_fy1);
   graph->SetName("grp0");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineWidth(3);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp01 = new TH1F("Graph_grp01","",100,-16.5,13.5);
   Graph_grp01->SetMinimum(0.9390207);
   Graph_grp01->SetMaximum(1.010468);
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
   
   Double_t grp1_fx2[35] = {
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
   15};
   Double_t grp1_fy2[35] = {
   1.020125,
   0.9896876,
   0.9919574,
   1.00463,
   1.012956,
   1.000574,
   0.9997191,
   0.9823306,
   0.9946952,
   0.9985209,
   0.9989235,
   0.9995161,
   0.9948703,
   0.9963925,
   1.012268,
   1.002232,
   1.010744,
   1.003896,
   0.9948104,
   0.9953082,
   0.9985494,
   0.9998946,
   0.9998067,
   1.001493,
   0.9978364,
   0.9966697,
   0.9988198,
   0.9953469,
   0.9921518,
   0.9929023,
   0.9881657,
   0.9939034,
   0.9935516,
   0.9941804,
   0.9993736};
   graph = new TGraph(35,grp1_fx2,grp1_fy2);
   graph->SetName("grp1");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(2);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(2);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp12 = new TH1F("Graph_grp12","",100,-23.5,18.5);
   Graph_grp12->SetMinimum(0.9785511);
   Graph_grp12->SetMaximum(1.023904);
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
   
   Double_t grp2_fx3[34] = {
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
   15};
   Double_t grp2_fy3[34] = {
   1.010968,
   0.9979518,
   0.9867105,
   0.9930014,
   0.9870892,
   0.9786934,
   0.9997886,
   0.9999583,
   0.9907687,
   1.001151,
   0.997992,
   0.9896719,
   1.001841,
   0.9979287,
   0.9894092,
   0.99523,
   0.9953527,
   0.996889,
   0.9998552,
   0.9962571,
   0.9982691,
   0.9966751,
   0.9971504,
   0.994442,
   0.9830818,
   0.998124,
   1.007116,
   0.9939113,
   0.991249,
   0.9957817,
   0.9851685,
   1.002862,
   0.998871,
   0.9846847};
   graph = new TGraph(34,grp2_fx3,grp2_fy3);
   graph->SetName("grp2");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(3);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(3);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp23 = new TH1F("Graph_grp23","",100,-23.5,18.5);
   Graph_grp23->SetMinimum(0.9754659);
   Graph_grp23->SetMaximum(1.014195);
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
   1.009488,
   1.012645,
   0.9847448,
   0.985413,
   1.002608,
   0.9909771,
   0.9780732,
   0.9897872,
   0.9977355,
   0.9998806,
   0.9961098,
   0.9967035,
   1.003386,
   0.9956911,
   0.9975512,
   0.9964936,
   0.9941368,
   0.9929649,
   0.9947836,
   0.9670869,
   0.9937958,
   0.9873871,
   0.9977099,
   0.9814107,
   0.9956631,
   0.986813,
   0.9918047,
   0.9927387,
   0.9931427,
   0.9867486,
   0.9978337,
   0.9965976,
   0.9830372,
   1.002067,
   0.9986079};
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
   Graph_grp34->SetMinimum(0.9625311);
   Graph_grp34->SetMaximum(1.017201);
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
   
   Double_t grp4_fx5[10] = {
   -16,
   -15,
   -14,
   5,
   6,
   7,
   8,
   9,
   10,
   11};
   Double_t grp4_fy5[10] = {
   1.007969,
   0.9918704,
   1.009656,
   1.011134,
   1.00436,
   0.999311,
   0.9997861,
   0.9985498,
   0.9892642,
   1.003871};
   graph = new TGraph(10,grp4_fx5,grp4_fy5);
   graph->SetName("grp4");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(5);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(5);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp45 = new TH1F("Graph_grp45","",100,-18.7,13.7);
   Graph_grp45->SetMinimum(0.9870773);
   Graph_grp45->SetMaximum(1.013321);
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
   
   Double_t grp5_fx6[2] = {
   -21,
   10};
   Double_t grp5_fy6[2] = {
   8.624359,
   1.008727};
   graph = new TGraph(2,grp5_fx6,grp5_fy6);
   graph->SetName("grp5");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(6);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(6);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp56 = new TH1F("Graph_grp56","",100,-24.1,13.1);
   Graph_grp56->SetMinimum(0.2471637);
   Graph_grp56->SetMaximum(9.385922);
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
   
   Double_t grp6_fx7[29] = {
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
   14};
   Double_t grp6_fy7[29] = {
   0.9964616,
   0.9983783,
   0.9961393,
   0.9930972,
   0.9961169,
   0.9904106,
   0.9896672,
   0.9969791,
   0.9942979,
   1.001255,
   0.9999403,
   0.9987642,
   0.9985156,
   0.9972631,
   0.9951975,
   0.9987541,
   0.9681875,
   0.9125283,
   0.990369,
   0.9983915,
   0.9923413,
   0.9933586,
   0.9969542,
   0.992033,
   0.9851232,
   0.9930214,
   0.9921924,
   0.9885318,
   0.9956027};
   graph = new TGraph(29,grp6_fx7,grp6_fy7);
   graph->SetName("grp6");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(7);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(7);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp67 = new TH1F("Graph_grp67","",100,-20.1,17.1);
   Graph_grp67->SetMinimum(0.9036556);
   Graph_grp67->SetMaximum(1.010128);
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
   
   Double_t grp7_fx8[32] = {
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
   14};
   Double_t grp7_fy8[32] = {
   0.9957246,
   0.992794,
   0.9993899,
   0.9985778,
   1.002735,
   0.9935937,
   0.9984326,
   0.9906784,
   0.9924927,
   1.00592,
   0.9937332,
   0.992004,
   0.9939658,
   0.995125,
   0.9979563,
   0.9988893,
   1.000563,
   0.9961966,
   0.9985962,
   0.9931308,
   0.9931667,
   0.990768,
   0.9960858,
   0.9934945,
   0.9970948,
   0.9968858,
   0.9884411,
   1.022589,
   0.9919139,
   0.9925718,
   1.002088,
   0.9926269};
   graph = new TGraph(32,grp7_fx8,grp7_fy8);
   graph->SetName("grp7");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(8);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(8);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp78 = new TH1F("Graph_grp78","",100,-21.2,17.2);
   Graph_grp78->SetMinimum(0.9850263);
   Graph_grp78->SetMaximum(1.026004);
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
   
   Double_t grp8_fx9[29] = {
   -17,
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
   13};
   Double_t grp8_fy9[29] = {
   0.9956126,
   1.009504,
   0.9997897,
   0.9969077,
   0.9973704,
   0.999218,
   0.997711,
   1.001055,
   1.001851,
   1.001022,
   1.000349,
   1.000412,
   1.011082,
   0.9992997,
   1.004877,
   0.9998626,
   0.995603,
   0.9957877,
   1.003886,
   0.9985604,
   0.9975239,
   0.9943751,
   0.998292,
   0.9978553,
   0.9919754,
   0.993944,
   0.9928402,
   0.9908755,
   0.9855287};
   graph = new TGraph(29,grp8_fx9,grp8_fy9);
   graph->SetName("grp8");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(9);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(9);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp89 = new TH1F("Graph_grp89","",100,-20,16);
   Graph_grp89->SetMinimum(0.9829734);
   Graph_grp89->SetMaximum(1.013637);
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
   
   Double_t grp9_fx10[21] = {
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
   4,
   5,
   6,
   7,
   8,
   9,
   10,
   11};
   Double_t grp9_fy10[21] = {
   0.9959416,
   0.9998854,
   0.9939323,
   0.9717097,
   1.00031,
   1.012435,
   0.9885629,
   0.9833589,
   1.000794,
   0.9855291,
   0.9950045,
   1.003253,
   0.9956151,
   0.99512,
   0.9997571,
   0.9937965,
   0.9930349,
   0.9938697,
   1.002569,
   0.9951776,
   0.9934017};
   graph = new TGraph(21,grp9_fx10,grp9_fy10);
   graph->SetName("grp9");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(11);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(11);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp910 = new TH1F("Graph_grp910","",100,-15.4,13.4);
   Graph_grp910->SetMinimum(0.9676371);
   Graph_grp910->SetMaximum(1.016508);
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
   multigraph->GetXaxis()->SetLimits(-22.9, 18.9);
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
