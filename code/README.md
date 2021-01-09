# Analysis Code

## Overview and disclaimers
- run_* scripts loop through a list of subjects for a given script; e.g., run_L1stats.sh loops all subjects through the L1stats.sh script.
- paths to input/output data should work without error, but check package/software installation

## Scripts used to generate public data
Some files cannot be shared publicly. And some raw source data are in non-standard format. The scripts below helped us go from the raw source data to the standardized public data:
- `prepdata.sh` -- runs [heudiconv](https://github.com/nipy/heudiconv) to convert dicoms to BIDS, defaces structural scans with pydeface, and runs [mriqc](https://mriqc.readthedocs.io/en/latest/index.html)
  - [heuristics.py](https://github.com/DVS-Lab/srndna-trust/blob/main/code/heuristics.py) sets the heuristics for heudiconv
  - [addIntendedFor.py](https://github.com/DVS-Lab/srndna-trust/blob/main/code/addIntendedFor.py) adds the "IntendedFor" field for the fmap files
- Code for stimuli control/presentation and conversion of raw behavioral data to BIDS are in [stimuli](https://github.com/DVS-Lab/srndna-trust/tree/main/stimuli)

## Behavioral analyses  
- [analyzeTrustBehavior.m](https://github.com/DVS-Lab/srndna-trust/blob/main/code/analyzeTrustBehavior.m): examines how choice behavior changes as a function of feedback on the previous trial
- more from Dominic?

## Imaging analyses  
1. Run [fmriprep][fmriprep] using and `bash fmriprep.sh $sub`.
1. Convert `*_events.tsv` files to 3-column files (compatible with FSL) using Tom Nichols' [BIDSto3col.sh](https://github.com/INCF/bidsutils) script. This script is wrapped into our pipeline using `bash gen_3col_files.sh $sub $nruns`
1. Run analyses in FSL. Analyses in FSL consist of three stages, which we call "Level 1" (L1) and "Level 2" (L2).
  - `L1stats.sh` -- initial time series analyses, relating brain responses to the task conditions in each run
  - `L2stats.sh` -- combines data across runs
  - `L3stats.sh` -- combines data across subjects



[fmriprep]: http://fmriprep.readthedocs.io/en/latest/index.html
