#include "Carbon.h"
#include "CrossSectionUtil.h"
#include "omniheader.h"

void DrawCarbonXS(){
  double ebeams[] = {1.056, 2.306};
  for(int i = 0; i<2; i++){
    TCanvas* c = new TCanvas();
    CarbonElastic * ele = new CarbonElastic(ebeams[i]);
    CarbonInelastic2Plus * ine2p = new CarbonInelastic2Plus(ebeams[i]);
    CarbonInelastic3Minus * ine3m = new CarbonInelastic3Minus(ebeams[i]);

    TH1* h_ele = generate_histogram_from_xs(ele);
    h_ele->SetName(Form("h_ele_%d", ebeams[i]));
    TH1* h_ine2p =  generate_histogram_from_xs(ine2p);
    h_ine2p->SetName(Form("h_ine2p", ebeams[i]));
    TH1* h_ine3m =  generate_histogram_from_xs(ine3m);
    h_ine3m->SetName(Form("h_ine3m", ebeams[i]));

    h_ele->SetFillColor(kGreen);
    h_ine2p->SetFillColor(kBlue);
    h_ine3m->SetFillColor(kRed);
    c->SetLogy(1);
    h_ele->Draw("E4");
    h_ine2p->Draw("SAME,E4");
    h_ine3m->Draw("SAME,E4");
    
    //cout << ele->get_xs_per_mott(.100) << endl;
    //cout << ine2p->get_xs_per_mott(.100) << endl;
    //cout << ine3m->get_xs_per_mott(.100) << endl;
  }
}
