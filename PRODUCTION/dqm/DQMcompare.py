#!/usr/bin/python
#
import sys, os, ROOT, re, argparse

#list of data: path to histogram and if it should be displayed with a logarithmic y/z-axis
data = [('EcalClusters/pairs1/EcalClusters Cluster Count per Event'                    , False),
        ('EcalClusters/pairs1/EcalClusters Cluster Size'                               , False),
        ('EcalClusters/pairs1/EcalClusters Cluster Energy'                             , False),
        ('EcalClusters/pairs1/EcalClusters Two Cluster Energy Sum'                     , False),
        ('EcalHits/pairs1/EcalCalHits Hit Count In Event'                              , False),
        ('FinalStateParticles/SeedTrack/pairs1/Electron Total P (GeV):  Bottom'        , False),
        ('FinalStateParticles/SeedTrack/pairs1/Electron Total P (GeV):  Top'           , False),
        ('FinalStateParticles/SeedTrack/pairs1/Positron Total P (GeV):  Bottom'        , False),
        ('FinalStateParticles/SeedTrack/pairs1/Positron Total P (GeV):  Top'           , False),
        ('FinalStateParticles/SeedTrack/pairs1/ECal T minus track T'                   , False),
        ('FinalStateParticles/SeedTrack/pairs1/Number of photons per event'            , False),
        ('FinalStateParticles/SeedTrack/pairs1/Number of unassociated tracks per event', True ),
        ('FinalStateParticles/GBLTrack/pairs1/Electron Total P (GeV):  Bottom'         , False),
        ('FinalStateParticles/GBLTrack/pairs1/Electron Total P (GeV):  Top'            , False),
        ('FinalStateParticles/GBLTrack/pairs1/Positron Total P (GeV):  Bottom'         , False),
        ('FinalStateParticles/GBLTrack/pairs1/Positron Total P (GeV):  Top'            , False),
        ('Tracks/GBLTracks/pairs1/Track Chi2'                                          , False),
        ('Tracks/GBLTracks/pairs1/Tracks per Event'                                    , False),
        ('Tracks/MatchedTracks/pairs1/Track Chi2'                                      , False),
        ('Tracks/MatchedTracks/pairs1/Tracks per Event'                                , False),
        ('TridentMonitoring/GBLTrack/pairs1/Trident: Vertex mass'                      , False),
        ('TridentMonitoring/GBLTrack/pairs1/Vertex: Vertex mass'                       , False),
        ('TridentMonitoring/GBLTrack/pairs1/Radiative vertex: Vertex Z'                , False),
        ('TridentMonitoring/GBLTrack/pairs1/Radiative vertex: Vertex X'                , False),
        ('TridentMonitoring/GBLTrack/pairs1/Radiative vertex: Vertex Y'                , False),
        ('TridentMonitoring/SeedTrack/pairs1/Trident: Vertex mass'                     , False),
        ('TridentMonitoring/SeedTrack/pairs1/Vertex: Vertex mass'                      , False),
        ('TridentMonitoring/SeedTrack/pairs1/Radiative vertex: Vertex Z'               , False),
        ('TridentMonitoring/SeedTrack/pairs1/Radiative vertex: Vertex X'               , False),
        ('TridentMonitoring/SeedTrack/pairs1/Radiative vertex: Vertex Y'               , False),
        ('V0Monitoring/GBLTrack/pairs1/BeamspotConstrainedV0Candidates/Chi2'           , False),
        ('V0Monitoring/GBLTrack/pairs1/BeamspotConstrainedV0Candidates/Mass (GeV)'     , False),
        ('V0Monitoring/GBLTrack/pairs1/BeamspotConstrainedV0Candidates/Vx (mm)'        , False),
        ('V0Monitoring/GBLTrack/pairs1/BeamspotConstrainedV0Candidates/Vy (mm)'        , False),
        ('V0Monitoring/GBLTrack/pairs1/BeamspotConstrainedV0Candidates/Vz (mm)'        , False),
        ('V0Monitoring/GBLTrack/pairs1/TargetConstrainedV0Candidates/Chi2'             , False),
        ('V0Monitoring/GBLTrack/pairs1/TargetConstrainedV0Candidates/Mass (GeV)'       , False),
        ('V0Monitoring/GBLTrack/pairs1/TargetConstrainedV0Candidates/Vx (mm)'          , False),
        ('V0Monitoring/GBLTrack/pairs1/TargetConstrainedV0Candidates/Vy (mm)'          , False),
        ('V0Monitoring/GBLTrack/pairs1/TargetConstrainedV0Candidates/Vz (mm)'          , False),
        ('V0Monitoring/GBLTrack/pairs1/UnconstrainedV0Candidates/Chi2'                 , False),
        ('V0Monitoring/GBLTrack/pairs1/UnconstrainedV0Candidates/Invariant Mass (GeV)' , False),
        ('V0Monitoring/GBLTrack/pairs1/UnconstrainedV0Candidates/Vx (mm)'              , False),
        ('V0Monitoring/GBLTrack/pairs1/UnconstrainedV0Candidates/Vy (mm)'              , False),
        ('V0Monitoring/GBLTrack/pairs1/UnconstrainedV0Candidates/Vz (mm)'              , False),     
        ('V0Monitoring/SeedTrack/pairs1/BeamspotConstrainedV0Candidates/Chi2'          , False),
        ('V0Monitoring/SeedTrack/pairs1/BeamspotConstrainedV0Candidates/Mass (GeV)'    , False),
        ('V0Monitoring/SeedTrack/pairs1/BeamspotConstrainedV0Candidates/Vx (mm)'       , False),
        ('V0Monitoring/SeedTrack/pairs1/BeamspotConstrainedV0Candidates/Vy (mm)'       , False),
        ('V0Monitoring/SeedTrack/pairs1/BeamspotConstrainedV0Candidates/Vz (mm)'       , False),
        ('V0Monitoring/SeedTrack/pairs1/TargetConstrainedV0Candidates/Chi2'            , False),
        ('V0Monitoring/SeedTrack/pairs1/TargetConstrainedV0Candidates/Mass (GeV)'      , False),
        ('V0Monitoring/SeedTrack/pairs1/TargetConstrainedV0Candidates/Vx (mm)'         , False),
        ('V0Monitoring/SeedTrack/pairs1/TargetConstrainedV0Candidates/Vy (mm)'         , False),
        ('V0Monitoring/SeedTrack/pairs1/TargetConstrainedV0Candidates/Vz (mm)'         , False),
        ('V0Monitoring/SeedTrack/pairs1/UnconstrainedV0Candidates/Chi2'                , False),
        ('V0Monitoring/SeedTrack/pairs1/UnconstrainedV0Candidates/Invariant Mass (GeV)', False),
        ('V0Monitoring/SeedTrack/pairs1/UnconstrainedV0Candidates/Vx (mm)'             , False),
        ('V0Monitoring/SeedTrack/pairs1/UnconstrainedV0Candidates/Vy (mm)'             , False),
        ('V0Monitoring/SeedTrack/pairs1/UnconstrainedV0Candidates/Vz (mm)'             , False)]

#a class that contains the method and data to compare 2 histograms and draw them
#in one canvas
class compared_histo1D:
    
    def __init__(self, histos, entries, log, colours = None):
        
        self.histos = histos
        self.entries = entries

        if colours is None:
            self.colours = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kMagenta,  ROOT.kPink, ROOT.kViolet, ROOT.kOrange, ROOT.kAzure, ROOT.kCyan, ROOT.kTeal, ROOT.kSpring]
        else:
            self.colours = colours
            
        self.set_colours()
        self.format_histo()
        self.log = log
    
    #sets the colours of the lines
    def set_colours(self):
        count = 0
        count2 = 0
        count3 = 0
        while count < len(self.histos):
            self.histos[count].SetLineColor(self.colours[count2] - count3)
            count += 1
            count2 += 1
            if count2 >= len(self.colours):
                count2 = 0
                count3 += 1
    
    #normalizes the histograms
    def format_histo(self):
        for i in range(1, len(self.entries)):
            ratio = self.entries[0]/self.entries[i]
            self.histos[i].Scale(ratio)
    
    #gives the canvas with the histograms in one grid
    def get_canvas(self):
        canvas = ROOT.TCanvas("Canvas", "Canvas", 1)
        if self.log:
            canvas.SetLogy()
        # self.histos[0].SetMaximum(self.get_max())
        maxi = self.get_max()
        for i in self.histos:
            if i.GetMaximum() > maxi:
                maxi = i.GetMaximum()
        self.histos[0].SetMaximum(maxi*1.05)
        self.histos[0].Draw()
        for i in self.histos[1:]:
            i.Draw('same')
        canvas.Update()
        return canvas

    #toggle the logarithmic y-axis
    def toggle_log(self):
        self.log = not self.log

    #get the highest y-axis
    def get_max(self):
        l = []
        for i in self.histos:
            l.append(i.GetMaximum())
        return max(l)

#object to compare the TH2D histograms
class compared_histo2D:

    def __init__(self, histos, log):
        self.histos = histos
        self.log = log

    #gives the histograms plotted next to eachother
    def get_canvas(self):
        canvas = ROOT.TCanvas ("Canvas", "Canvas", 1)
        length = len(self.histos)
        canvas.SetWindowSize(canvas.GetWindowWidth()*length, canvas.GetWindowHeight())
        canvas.Divide(length)
        for i in range(length):
            canvas.cd(i + 1)
            if self.log:
                canvas.cd(i + 1).SetLogz()
            self.histos[i].Draw("Colz")
        canvas.Update()
        return canvas

    #toggle the logarithmic z-axis
    def toggle_log(self):
        self.log = not self.log

#returns the right compared_histo object
def compare_histo(histos, entries, log):
    if histos[0].ClassName() == 'TH1D':
        return compared_histo1D(histos, entries, log)
    elif histos[0].ClassName() == 'TH2D':
        return compared_histo2D(histos, log)
    else:
        print >> sys.stderr, 'Histograms not recognized'
        return None

#returns a text file with a check if it exists
def get_file(filename):
    if not os.path.exists(filename):
        print >> sys.stderr, "file: " + filename + " does not exist"
        return True
    return open(filename, 'r')

#recursive algorithm that returns the right compared histo object        
def get_histo(f, path):

#    print("get_histo: "+str(f)+","+str(path))
    if type(f) is ROOT.TObject:
        return False
    if isinstance(f, ROOT.TH1):
        tdf = f.GetDirectory()
        f.SetTitle(tdf.GetTitle()+"/"+f.GetTitle())
        return f
    else:
        tmp = get_histo(f.Get(path[0]), path[1:len(path)])
        if not tmp:
            return False
        return tmp

#returns the amount of entries
def get_entries(f):
    return f.Get('EcalClusters/pairs1/EcalClusters Cluster Count per Event').GetEntries()

#gets a list of all the lines in a file (possible paths for within the root file)
def get_list_from_file(filename):
    try:
        f = get_file(filename)
        if f:
            return []
        data = f.readlines()
        f.close()
        return data
    except IOError:
        print >> sys.stderr, filename + " is missing"
        return []

#read out files for paths to root files
def read_files(files):
    fl = []
    fn = []
    for i in files:
        f = ROOT.TFile(i)
        if not os.path.exists(i):
            print >> sys.stderr, "Invalid file path"
            sys.exit(0)
        elif not i.endswith(".root"):
            print >> sys.stderr, "Invalid file type"
            sys.exit(0)
        elif i in fn:
            print >> sys.stderr, "Do not enter the same file"
        else:
            fl.append(f)
            fn.append(i)
    return fl

#check if none of the items in the list are None            
def get_lboolean(l):
    b = True
    for i in l:
        b &= bool(i)
    return b

#return the compare histo objects
def get_histos(data, files, bottomtop):
    dat = []
    bl = []
    for i in data:
        dat.append(i[0].rstrip('\n'))
        bl.append(i[1])
    r = []
    names = []
    
    for p in range(len(dat)):
        line = dat[p]
        path = filter(None, re.split('\\/', line))
        
        histos = []
        entries = []

        #optional putting Bottom and Top files together
        if bottomtop:
            if line.endswith("Bottom"):
                if (line[:-6] + "Top") in names:
                    continue
                elif not ((line[:-6] + "Top") in dat):
                    pass    
                else:
                    for i in files:
                        histos.append(get_histo(i, path[:-1] + [path[len(path) - 1][:-6] + "Top"]))
                        entries.append(get_entries(i))
                     
            if line.endswith("Top"):
                if (line[:-3] + "Bottom") in names:
                    continue
                elif not (line[:-3] + "Bottom" in dat):
                    pass
                else:
                    for i in files:
                        histos.append(get_histo(i, path[:-1] + [path[len(path) - 1][:-3] + "Bottom"]))
                        entries.append(get_entries(i))
                     
        for i in files:
            histos.append(get_histo(i, path))
            entries.append(get_entries(i))

        names.append(line)
        
        if get_lboolean(histos):
            r.append(compare_histo(histos, entries, bl[p]))
        else:
            print >> sys.stderr, '/'.join(path) + ' does not exist or is entered wrong'
    return r
    
#main program
def main(argv=None):
    global data

    #setup the argparser
    if argv is None:
        argv = sys.argv
    elif type(argv) is str:
        argv = argv.split()
        argv.insert(0,sys.argv[0])
    elif type(argv) is list:
        argv.insert(0,sys.argv[0])
    else:
        print("I don't understand the argument here.")

    parser = argparse.ArgumentParser(description='Compare two root files from the HPS DQM output.')
    parser.add_argument("filename1",type=str, help="Reference root file from DQM, will be shown in red.")
    parser.add_argument("filenameN",type=str,nargs="+", help="Root file(s) you want to compare, shown in blue and subsequent colors.")
    parser.add_argument("-f", "--filename", action="append", default=[], help="Optional extra files you want to add to the comparison. Colors vary. Give logarithmic scale with -@l directly after filename.")
    parser.add_argument("-n", "--rfilename", action="append", default=[], help="Possible extra file containing list of root files to compare written in the same style as in -f.")
    parser.add_argument("-d", "--data", action="append", default=[], help="Optional extra histograms (with path) to compare.")
    parser.add_argument("-t", "--rdata", action="append", default=[], help="Possible extra files containing extra histograms (with path) to compare.")
    parser.add_argument("-s", "--skipdata", action="store_true", default=False, help="Skip all standard histograms, only use what's specified with -d and -rd.")
    parser.add_argument("-o", "--bottomtop", action="store_true", default=False, help="Show bottom and top histograms in the same picture.")
    parser.add_argument("-p", "--savepdf", action="store_true", default=False, help="Save all histograms to result.pdf in stead of displaying them")
    parser.add_argument("-b", action="store_true", help="Bash only mode")
    args = parser.parse_args(argv[1:])

    #process data from argparse
    tmp = []
    for i in args.rdata:
        s = get_list_from_file(i)
        if s.endswith("-@l"):
            tmp.append((s[:-3], True))
        else:
            tmp.append((s, False))

    for i in args.data:
        if i.endswith("-@l"):
            tmp.append((i[:-3], True))
        else:
            tmp.append((i, False))
                   
    if args.skipdata:
        data = tmp
    else:
        data.extend(tmp)
                    
    tmp = []
    for i in args.rfilename:
        tmp.extend(get_list_from_file(i))

    filenames = [args.filename1]+ args.filenameN
    filenames.extend(tmp)
    filenames.extend(args.filename)
    
    files = read_files(filenames)

    #check if there are any files to compare
    if len(files) < 2:
        print >> stderr, "Too many invalid files"
        sys.exit(0)
    
    #retrieve and put the compared histo objects in a list with in the first
    #slot a 'pointer' to the current histogram to be displayed    
    histo_compare_obj = [1] + get_histos(data, files, args.bottomtop)

    #stop the program if there are no items in the histo compare obj list
    if len(histo_compare_obj) == 1:
        sys.exit(0)

    #save as pdf
    if args.savepdf:
        if os.path.exists("result.pdf"):
            os.remove("result.pdf")
        histo_compare_obj[1].get_canvas().Print("result.pdf(", "pdf")
        if len(histo_compare_obj) > 2:
            for i in range(2, len(histo_compare_obj)):
                histo_compare_obj[i].get_canvas().Print("result.pdf", "pdf")
            histo_compare_obj[-1].get_canvas().Print("result.pdf)", "pdf")
        return
    go_on = True
    
    #start command loop
    while go_on:
        canvas = histo_compare_obj[histo_compare_obj[0]].get_canvas()
        
        while True:
            command = raw_input()
            
            #command for next item in the list
            if command == '':
                if histo_compare_obj[0] < len(histo_compare_obj) - 1:
                    histo_compare_obj[0] += 1
                else:
                    histo_compare_obj[0] = 1
                break
            
            #command for previous item in the list
            elif command == 'p':
                if histo_compare_obj[0] > 1:
                    histo_compare_obj[0] -= 1
                else:
                    histo_compare_obj[0] = len(histo_compare_obj) - 1
                break
            
            #command to stop the program
            elif command == 'q':
                go_on = False
                break

            #command to display the histogram logarithmic
            elif command == 'log':
                histo_compare_obj[histo_compare_obj[0]].toggle_log()
                break
            
            #If the command was not recognized, an error message is displayed with the possible commands
            else:
                print >> sys.stderr, 'Command not recognized, please try again with the following commands:\n\'q\' to quit\n\'p\' for previous histogram\n\'enter\' for next histogram\n\'log\' for logarithmic scaling'
        try:
            canvas.Close()
        except:
            pass

if __name__ == '__main__': 
    sys.exit(main())
