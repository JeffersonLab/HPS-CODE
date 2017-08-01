#!usr/bin/env python

def getDetector(run):
    "This gets the detector name based on run number"
#mg...note we don't have a 3mmPre5216 detector yet
    if(run>5065 and run<5080):
        return "HPS-EngRun2015-2mmPreRun5216-v1"
    if(run>5149 and run<5181):
        return "HPS-EngRun2015-2mmPreRun5216-v1"
    if(run>5181 and run<5200):
        return "HPS-EngRun2015-2mmPreRun5216-v1"
    if(run>5149 and run<5181):
        return "HPS-EngRun2015-2mmPreRun5216-v1"
    if(run>5253 and run<5352):
        return "HPS-EngRun2015-1_5mm-v1"
    if(run>5379 and run<5388):
        return "HPS-EngRun2015-1_5mm-v1"
    if(run>5403 and run<5413):
        return "HPS-EngRun2015-1_5mm-v1"
    if(run>5539 and run<5580):
        return "HPS-EngRun2015-1_5mm-v1"
    if(run>5539 and run<5580):
        return "HPS-EngRun2015-1_5mm-v1"
    if(run>5596 and run<5612):
        return "HPS-EngRun2015-1_5mm-v1"
    if(run>5622 and run<5627):
        return "HPS-EngRun2015-Nominal-v1"
    if(run>5631 and run<5658):
        return "HPS-EngRun2015-Nominal-v1"
    if(run>5685 and run<5699):
        return "HPS-EngRun2015-Nominal-v1"
    if(run>5703 and run<5712):
        return "HPS-EngRun2015-Nominal-v1"
    if(run>5714 and run<5744):
        return "HPS-EngRun2015-Nominal-v1"
    if(run>5753 and run<5798):
        return "HPS-EngRun2015-Nominal-v1"
    return "FOOBAR"

