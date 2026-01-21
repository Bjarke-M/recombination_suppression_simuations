import tskit as ts
import pyslim 
import sys
import numpy as np

file = sys.argv[1]
ancestral_pop_size = int(sys.argv[2])
recomb_rate = float(sys.argv[3])
outfile = sys.argv[4]

orig_ts = ts.load(file)
rts = pyslim.recapitate(orig_ts,
            recombination_rate=recomb_rate,
            ancestral_Ne=ancestral_pop_size)

rts.dump(outfile)

## for testing 


rng = np.random.default_rng(seed=3342)
alive_inds = pyslim.individuals_alive_at(rts, 0)
keep_indivs = rng.choice(alive_inds, 100, replace=False)
keep_nodes = []
for i in keep_indivs:
  keep_nodes.extend(rts.individual(i).nodes)

sts = rts.simplify(keep_nodes, keep_input_roots=True)
sts.dump('../reduced_samples.trees')  