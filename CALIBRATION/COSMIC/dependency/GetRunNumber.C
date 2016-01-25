#include "TString.h"
#include "TRegexp.h"
int GetRunNumber(const char* filename)
{
    TString ss=filename;
    TRegexp rr="[0-9][0-9][0-9][0-9][0-9]";  // any five numbers in a row will match!
    Ssiz_t ind=ss.Index(rr);
    if ((size_t)ind==std::string::npos) return -1;
    ss.Remove(0,ind);
    ss.Resize(5);
    return ss.Atoi();
}
