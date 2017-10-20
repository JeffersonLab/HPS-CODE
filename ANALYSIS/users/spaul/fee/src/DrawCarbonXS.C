#include "../include/xs_model/Carbon.h"
#include "../include/xs_model/CrossSectionUtil.h"
#include "../include/omniheader.h"

void DrawCarbonXS(){
  double ebeams[] = {1.056, 2.306};
  int labels[] = {2015, 2016};
  for(int i = 0; i<2; i++){
    TCanvas* c = new TCanvas();
    CarbonElastic * ele = new CarbonElastic(ebeams[i]);
    CarbonInelastic2Plus * ine2p = new CarbonInelastic2Plus(ebeams[i]);
    CarbonInelastic3Minus * ine3m = new CarbonInelastic3Minus(ebeams[i]);
    CarbonQuasielastic * qua = new CarbonQuasielastic(ebeams[i]);
    
    TH1* h_ele = generate_histogram_from_xs(ele);
    h_ele->SetName(Form("h_ele_%d", ebeams[i]));
    TH1* h_ine2p =  generate_histogram_from_xs(ine2p);
    h_ine2p->SetName(Form("h_ine2p", ebeams[i]));
    TH1* h_ine3m =  generate_histogram_from_xs(ine3m);
    h_ine3m->SetName(Form("h_ine3m", ebeams[i]));
    TH1* h_qua =  generate_histogram_from_xs(qua);
    h_qua->SetName(Form("h_qua", ebeams[i]));

    TH1* h_tot = (TH1*) h_ele->Clone();
    h_tot->Add(h_ine2p);
    h_tot->Add(h_ine3m);
    h_tot->Add(h_qua);

    h_tot->SetFillColor(kRed);
    h_tot->SetTitle(Form("Cross Sections at %.3f GeV;#theta (rad);#sigma/#sigma_{Mott}", ebeams[i]));
    h_tot->SetTitleSize(.05, "XY");
    h_tot->SetLabelSize(.05, "XY");
    h_tot->GetYaxis()->SetRangeUser(.002,2);
    h_tot->SetStats(0);
    
    h_ele->SetFillColor(kOrange);
    h_ine2p->SetFillColor(kBlue);
    h_ine3m->SetFillColor(kGreen);
    h_qua->SetFillColor(kYellow+2);
    c->SetLogy(1);
    h_tot->Draw("E4");
    h_ele->Draw("SAME,E4");
    h_ine2p->Draw("SAME,E4");
    h_ine3m->Draw("SAME,E4");
    h_qua->Draw("SAME,E4");

    TLegend * legend = new TLegend(.7, .70, .95, .97);
    legend->AddEntry(h_tot, "total");
    legend->AddEntry(h_ele, "elastic");
    legend->AddEntry(h_qua, "quasielastic");
    legend->AddEntry(h_ine2p, "inelastic 2+");
    legend->AddEntry(h_ine3m, "inelastic 3-");

    legend->Draw();
    gPad->SaveAs(Form("out/img/%d/carbon_xs_model.pdf",labels[i]));
  }
}
