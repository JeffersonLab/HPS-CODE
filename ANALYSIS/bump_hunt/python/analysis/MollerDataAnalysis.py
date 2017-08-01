
import MollerAnalysis

class MollerDataAnalysis(MollerAnalysis.MollerAnalysis): 

    def __init__(self): 

        self.trigger_count = 0
        self.svt_quality_count = 0
        
        MollerAnalysis.MollerAnalysis.__init__(self)

    def process(self, event): 

        # Only look at singles1 triggers
        if not event.isSingle1Trigger(): return
        self.trigger_count += 1

        # Only look at events with the SVT bias on
        if not event.isSvtBiasOn(): return

        # Only look at events where the SVT is closed.
        if not event.isSvtClosed(): return

        # Skip events that had busrt mode noise.
        if event.hasSvtBurstModeNoise(): return

        # Skip events that had SVT header errors
        if event.hasSvtEventHeaderErrors(): return
        self.svt_quality_count += 1

        # Use the base class to process the event.
        MollerAnalysis.MollerAnalysis.process(self, event)

    def finalize(self):

        print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'
        print '    Data Only    '
        print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'
        print 'Trigger count: %s' % self.trigger_count
        print 'SVT quality count: %s' % self.svt_quality_count
        print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'

        MollerAnalysis.MollerAnalysis.finalize(self)
