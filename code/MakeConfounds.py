# Extracts confound regressors for use in feat
# E.G. use
#$ python MakeConfounds.py --fmriprepDir="/data/projects/Tensor_game/Data/Raw/NARPS/derivatives/fmriprep"
#
# originally written by Jeff Dennison
# latest version here: https://github.com/DVS-Lab/general/blob/master/MakeConfounds.py


import numpy as np
import pandas as pd
import argparse
import os
import re

# check arg (input path)
parser = argparse.ArgumentParser(description='Give me a path to your fmriprep output')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--fmriprepDir',default=None, type=str,help="This is the full path to your fmriprep dir")
args = parser.parse_args()
fmriprep_path = args.fmriprepDir

#make list of confound tsvs
cons=[]
for root, dirs, files in os.walk(fmriprep_path):
    for f in files:
        if f.endswith('-confounds_regressors.tsv'): # note: newer versions of fmriprep end with -confounds_timeseries.tsv
            cons.append(os.path.join(root, f))

# loop through files
for f in cons:

    # parse key-value pairs and build variables
    sub=re.search('/func/(.*)_task', f).group(1)
    run=re.search('_run-(.*)_desc', f).group(1)
    task=re.search('_task-(.*)_run',f).group(1)
    derivatives_path=re.search('(.*)fmriprep/sub',f).group(1)

    #read in confound file and build matrix
    con_regs=pd.read_csv(f,sep='\t')
    # other=['csf','white_matter'] # use aCompCor instead
    aCompCor =['a_comp_cor_00','a_comp_cor_01','a_comp_cor_02','a_comp_cor_03','a_comp_cor_04','a_comp_cor_05'] # use aCompCor instead
    cosine = [col for col in con_regs if col.startswith('cosine')]
    NSS = [col for col in con_regs if col.startswith('non_steady_state')]
    # aroma_motion=[col for col in con_regs if col.startswith('aroma_motion_')] # skipping aroma due to reproducibility issues
    motion = ['trans_x','trans_y','trans_z','rot_x','rot_y','rot_z']
    fd = ['framewise_displacement']
    filter_col=np.concatenate([cosine,NSS,motion,fd,aCompCor])
    df_all=con_regs[filter_col]

    # generate output files
    outfile="%s_task-%s_run-%s_desc-fslConfounds.tsv"%(sub,task,run)
    outdir=derivatives_path+"fsl/confounds/%s/" %(sub)
    if not os.path.exists(outdir):
    	os.makedirs(outdir)
    output=outdir+outfile
    print(sub,run,task)
    df_all.to_csv(output,index=False,sep='\t',header=False)
