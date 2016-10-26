# cut tuning
* makeTrainingTrees.py: takes a tuple as input, and outputs "good" and "bad" subsets of events (e.g. in-time and out-of-time clusters, or vertices reconstructed near the target and out in the +Z tail).
* tmva.py: uses TMVA to train a classifier. Doesn't work very well.
* cut_utils.py: utility methods for making ROC plots.
* bumphunt_cuts.py: makes ROC plots for the loose bumphunt cuts.
* vertex_cuts.py: makes ROC plots for vertex cuts.
* moller_cuts.py: makes ROC plots for Moller cuts.

# cut testing
* base_cuts_data.py: makes plots showing the effect of loose bumphunt cuts on the cluster delta-t distribution: `./base_cuts_data.py plots 5772_nocuts_tri.root`.
* vertex_cuts_data.py: makes plots showing the effect of vertex cuts on the vertex Z distribution: `./vertex_cuts_data.py plots golden_loosetri.root`.
* vertex_cuts_truth.py: makes plots showing the effect of vertex cuts on displaced A' Monte Carlo: `./vertex_cuts_truth.py plots apsignal_displaced_40_dq_tri.root`.
