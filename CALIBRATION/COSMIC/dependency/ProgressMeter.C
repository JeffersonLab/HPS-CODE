#ifndef __PROGRESSMETER__
#define __PROGRESSMETER__
#include "stdio.h"
void ProgressMeter(const double total,const double current)
{
    static const int maxdots=40;
    const double frac = current/total;
    int ii=0;  printf("%3.0f%% [",frac*100);
    for ( ; ii < frac*maxdots; ii++) printf("=");
    for ( ; ii < maxdots;      ii++) printf(" ");
    printf("]\r"); fflush(stdout);
}
#endif
