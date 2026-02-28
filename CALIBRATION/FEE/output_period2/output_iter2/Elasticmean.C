void Elasticmean()
{
//=========Macro generated from canvas: scr/xxxx
//=========  (Sat Feb 26 14:17:51 2022) by ROOT version 6.24/06
   TCanvas *scr = new TCanvas("scr", "xxxx",0,0,1200,800);
   gStyle->SetOptFit(1);
   gStyle->SetOptStat(0);
   scr->Range(-26.75,-0.1875,22.75,1.6875);
   scr->SetFillColor(0);
   scr->SetBorderMode(0);
   scr->SetBorderSize(2);
   scr->SetFrameBorderMode(0);
   scr->SetFrameBorderMode(0);
   
   TMultiGraph *multigraph = new TMultiGraph();
   multigraph->SetName("");
   multigraph->SetTitle("Elastic Peak Position");
   
   Double_t grp0_fx1[23] = {
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
   10};
   Double_t grp0_fy1[23] = {
   0.9920709,
   1.004724,
   1.00053,
   0.9911646,
   0.992753,
   1.003585,
   0.9948266,
   0.9979501,
   0.9931402,
   0.9481875,
   0.9891022,
   0.9980634,
   1.000428,
   1.001338,
   0.9909396,
   1.001256,
   0.9940454,
   1.000775,
   0.9979271,
   0.9969556,
   0.9895763,
   1.002585,
   1.002325};
   TGraph *graph = new TGraph(23,grp0_fx1,grp0_fy1);
   graph->SetName("grp0");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineWidth(3);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp01 = new TH1F("Graph_grp01","",100,-16.4,12.4);
   Graph_grp01->SetMinimum(0.9425339);
   Graph_grp01->SetMaximum(1.010377);
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
   
   Double_t grp1_fx2[34] = {
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
   Double_t grp1_fy2[34] = {
   0.9939779,
   0.9894808,
   1.00352,
   1.016453,
   0.9996887,
   0.9989808,
   0.9819741,
   0.9956511,
   0.9998034,
   0.9996794,
   0.9953393,
   0.9957248,
   1.000045,
   1.005847,
   1.003051,
   1.006028,
   1.000653,
   0.9969994,
   0.9912041,
   0.9978616,
   0.997404,
   0.9989913,
   0.9980111,
   0.9993315,
   0.9951718,
   0.9994345,
   0.992303,
   0.9922485,
   0.9912863,
   0.9952872,
   0.9945688,
   1.000147,
   1.001116,
   1.00314};
   graph = new TGraph(34,grp1_fx2,grp1_fy2);
   graph->SetName("grp1");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(2);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(2);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp12 = new TH1F("Graph_grp12","",100,-22.4,18.4);
   Graph_grp12->SetMinimum(0.9785262);
   Graph_grp12->SetMaximum(1.019901);
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
   
   Double_t grp2_fx3[33] = {
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
   Double_t grp2_fy3[33] = {
   0.9914787,
   0.9880065,
   0.993423,
   0.9859283,
   0.9834163,
   0.9975371,
   0.9994676,
   0.991104,
   0.995453,
   0.9961141,
   0.9910494,
   1.001077,
   0.9975683,
   0.9887037,
   0.9919074,
   0.994858,
   0.9958403,
   0.9929904,
   0.9947243,
   0.9972758,
   0.993263,
   0.9936219,
   0.9897883,
   0.9823648,
   1.004466,
   1.0035,
   0.9898781,
   0.9874422,
   0.9969478,
   0.986537,
   0.9982242,
   0.994822,
   0.9841776};
   graph = new TGraph(33,grp2_fx3,grp2_fy3);
   graph->SetName("grp2");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(3);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(3);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp23 = new TH1F("Graph_grp23","",100,-22.4,18.4);
   Graph_grp23->SetMinimum(0.9801546);
   Graph_grp23->SetMaximum(1.006676);
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
   
   Double_t grp3_fx4[32] = {
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
   15};
   Double_t grp3_fy4[32] = {
   1.011713,
   0.9806255,
   0.9879966,
   1.009953,
   0.9994842,
   0.9862268,
   0.996102,
   0.999835,
   0.9977949,
   0.9978982,
   1.002143,
   0.9967247,
   0.9953513,
   0.9960065,
   0.9964539,
   0.9934037,
   0.9916359,
   0.9976245,
   0.9963925,
   0.9965059,
   1.005911,
   1.001129,
   0.987347,
   0.9994473,
   0.9893129,
   0.9903252,
   0.9913412,
   0.9916652,
   0.9919368,
   1.007157,
   1.006264,
   0.9861026};
   graph = new TGraph(32,grp3_fx4,grp3_fy4);
   graph->SetName("grp3");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(4);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(4);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp34 = new TH1F("Graph_grp34","",100,-22.4,18.4);
   Graph_grp34->SetMinimum(0.9775167);
   Graph_grp34->SetMaximum(1.014822);
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
   
   Double_t grp5_fx6[1] = {
   10};
   Double_t grp5_fy6[1] = {
   1.013803};
   graph = new TGraph(1,grp5_fx6,grp5_fy6);
   graph->SetName("grp5");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(6);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(6);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp56 = new TH1F("Graph_grp56","",100,9.9,11.1);
   Graph_grp56->SetMinimum(0.9138032);
   Graph_grp56->SetMaximum(2.113803);
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
   
   Double_t grp6_fx7[31] = {
   -20,
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
   Double_t grp6_fy7[31] = {
   1.014959,
   0.989549,
   1.00328,
   1.002786,
   0.996159,
   0.9900802,
   0.9996349,
   0.9965396,
   0.9975862,
   0.998081,
   0.9952939,
   1.000853,
   0.9993484,
   0.9975501,
   0.9946991,
   0.9967638,
   0.9939113,
   0.9998885,
   0.9995032,
   1.000327,
   1.000255,
   0.9983923,
   0.994075,
   0.9919999,
   0.9868302,
   0.9908765,
   0.987787,
   0.9960699,
   1.001925,
   1.012428,
   1.001742};
   graph = new TGraph(31,grp6_fx7,grp6_fy7);
   graph->SetName("grp6");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(7);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(7);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp67 = new TH1F("Graph_grp67","",100,-23.6,19.6);
   Graph_grp67->SetMinimum(0.9840173);
   Graph_grp67->SetMaximum(1.017772);
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
   
   Double_t grp7_fx8[35] = {
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
   Double_t grp7_fy8[35] = {
   1.003058,
   0.9847484,
   0.9885585,
   0.9923618,
   0.9888957,
   0.9873435,
   1.000949,
   0.9925815,
   0.9968232,
   0.9923677,
   0.9943376,
   1.003815,
   0.9914934,
   0.9911065,
   0.9930501,
   0.9917384,
   0.9963241,
   0.9982924,
   0.994734,
   0.9923612,
   0.9939238,
   0.991484,
   0.9929921,
   0.9925585,
   0.9954921,
   0.9943658,
   0.9950493,
   0.9959749,
   0.9917135,
   0.9967169,
   0.9940194,
   0.9916002,
   0.9989883,
   0.9879571,
   0.999837};
   graph = new TGraph(35,grp7_fx8,grp7_fy8);
   graph->SetName("grp7");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(8);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(8);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp78 = new TH1F("Graph_grp78","",100,-23.5,18.5);
   Graph_grp78->SetMinimum(0.9828417);
   Graph_grp78->SetMaximum(1.005722);
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
   1.02372,
   0.9923999,
   0.9990053,
   0.99356,
   0.9867052,
   1.0042,
   0.990451,
   0.9985937,
   0.9959863,
   0.9978404,
   0.9963113,
   1.00085,
   1.001239,
   0.9999353,
   0.9990183,
   0.9990762,
   1.004606,
   0.9986878,
   1.004062,
   0.9987599,
   0.9962031,
   0.9959585,
   1.006346,
   0.9942609,
   0.9979675,
   0.9957152,
   0.9984432,
   0.9963807,
   0.9911652,
   0.9960014,
   0.9951721,
   0.9884619,
   0.9892376,
   1.001547,
   1.000508,
   1.003007};
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
   Graph_grp89->SetMinimum(0.9830037);
   Graph_grp89->SetMaximum(1.027421);
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
   
   Double_t grp9_fx10[20] = {
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
   5,
   6,
   7,
   8,
   9,
   10};
   Double_t grp9_fy10[20] = {
   0.993777,
   0.9980143,
   0.998259,
   0.9913769,
   0.9708485,
   1.000817,
   1.013086,
   0.9899128,
   0.9851477,
   0.9996485,
   0.9858395,
   0.9931549,
   1.008102,
   1.003979,
   1.002756,
   0.9874229,
   0.9980116,
   0.9973769,
   1.001689,
   0.9929296};
   graph = new TGraph(20,grp9_fx10,grp9_fy10);
   graph->SetName("grp9");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineColor(11);
   graph->SetLineWidth(3);
   graph->SetMarkerColor(11);
   graph->SetMarkerStyle(31);
   graph->SetMarkerSize(2);
   
   TH1F *Graph_grp910 = new TH1F("Graph_grp910","",100,-16.4,12.4);
   Graph_grp910->SetMinimum(0.9666247);
   Graph_grp910->SetMaximum(1.01731);
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
   multigraph->GetXaxis()->SetLimits(-21.8, 17.8);
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
