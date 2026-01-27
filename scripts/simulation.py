import subprocess
################## Description ##################
"""
This script run a simple simulation of a mutation that suppresses recombniation in a region around it.
It has the following parameters:
n = the population size (n = 1000 is 2000 chromosomes)
n_intro = how many individuals should the mutation occur in, most of the time you wnat this to be 1
l = the length of the chormosome you want to simulate
sup_pos = the position along the genome where you want the mutation to hit
sup_start = the start position of the suppression
sup_end = the end position of the supression
clade_size = int or NULL, if int this will be the minimum size of the clade when the simualtion is stopped, if null the simuation wil run for 2*n generations
alpha = the suppression factor, if the reduction factor is 0.10 there will only be 90% of the recombiniation events inside of the suppressed region for the individuals that are affected by the mutation
h = the dominance of the mutation, so if h != 0 or 1, then heterozygotes will have the 1-(h*alpha) of the recombination rate within the region homozygotes will alway have 1-alpha
outfile = the output file 

the requirements for the script to run is, pyslim, msprime, slim, tskit, numpy
"""

################## Run SLIM ##################

n = int(1000)
seed = int(795526450) # delete seed information if you ever want it to give other outputs or random generate it here directly (probably the better option)
n_intro = int(1)
l = int(1000000) 
sup_pos = int(l/2)
sup_start = int(sup_pos-100000)
sup_end = int(sup_pos+100000)
clade_size = 'NULL'
alpha = 0.9999
h = 1.0
uni_rec_rate = 1e-6
outfile = 'recomb_suppressor_example.trees'

subprocess.call(['slim',
                       '-seed', f'{seed}',
                       '-d', f'n={n}',
                       '-d', f'n_intro={n_intro}',
                       '-d', f'l={l}',
                       '-d', f'sup_pos={sup_pos}',
                       '-d', f'sup_start={sup_start}',
                       '-d', f'sup_end={sup_end}',
                       '-d', f'clade_size={clade_size}',
                       '-d', f'alpha={alpha}',
                       '-d', f'h={h}',
                       '-d', f'exp_r={uni_rec_rate}',
                       '-d', f'outfile="{outfile}"',
                       '../scripts/rec_suppression_script.slim'])

################## Recapitate ##################

infile = 'recomb_suppressor_example.trees'
recap_outfile = '../example.trees'
ancestral_ne = 1000
recomb_rate = 1e-6

subprocess.call(['python',
                 '../scripts/rec_suppression_recapitation.py',
                 f'{infile}',
                 f'{ancestral_ne}',
                 f'{recomb_rate}',
                 f'{recap_outfile}',
                 f'{seed}'])


################## Run dolores ##################

subprocess.call([
    'python',
    '-m', 'run-dolores',
    '-C', 'chr1',
    '-n', 'example',
    '-t', '..', 
    '-g', '../uniform_recmap.txt',
    '-M', '0', 
    '-m', '0',
    '-c', '0',
    '-u', '0'
])