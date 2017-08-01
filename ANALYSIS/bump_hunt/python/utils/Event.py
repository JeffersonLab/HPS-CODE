
import ROOT as r

class Event(object):

    def __init__(self, config):
    
        # Get the path for the event lib
        print config['EventLib']
        r.gSystem.Load(config['EventLib'][0])
        
        self.rfile = None
        self.tree = None
        self.entry = 0
       
        self.event = r.HpsEvent()

    def load_file(self, rfile_path):
        self.rfile = r.TFile(rfile_path)
        
        self.tree = self.rfile.Get("HPS_Event")
        self.tree.SetBranchAddress("Event", r.AddressOf(self.event))

        self.entry = 0

    def close_file(self):
        if self.rfile: self.rfile.Close()

    def next_event(self):
        if self.entry >= self.tree.GetEntries(): return False
        
        if (self.entry)%10000 == 0 : print "Event %s" % (self.entry + 1)
        
        self.tree.GetEntry(self.entry)
        self.entry += 1
        return True
   
    def get_event(self):
       return self.event
