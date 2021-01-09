#!/usr/bin/env bash

# Example code for heudiconv and pydeface. This will get your data ready for analyses.
# This code will convert DICOMS to BIDS (PART 1). Will also deface (PART 2) and run MRIQC (PART 3).
 
# usage: bash prepdata.sh sub nruns
# example: bash prepdata.sh 104 3

# Notes: 
# 1) containers live under /data/tools on local computer. should these relative paths and shared? YODA principles would suggest so.
# 2) other projects should use Jeff's python script for fixing the IntendedFor 
# 3) aside from containers, only absolute path in whole workflow (transparent to folks who aren't allowed to access to raw data)
sourcedata=/data/sourcedata/srndna


sub=$1
nruns=$2


# set up input and output directories.
dsroot=`pwd` # assume you are running from the root
codedir=$dsroot/code


# make bids folder if it doesn't exist
if [ ! -d $dsroot/bids ]; then
	mkdir -p $dsroot/bids
fi

# overwrite existing
rm -rf $dsroot/bids/sub-${sub}


# PART 1: running heudiconv and fixing fieldmaps
if [ $sub -gt 121 ]; then
  singularity run --cleanenv -B $dsroot:/out -B $sourcedata:/sourcedata \
  /data/tools/heudiconv-0.5.4.simg -d /sourcedata/dicoms/SMITH-AgingDM-{subject}/*/DICOM/*.dcm -s $sub \
  -f /out/code/heuristics.py -c dcm2niix -b --minmeta -o /out/bids
else
  singularity run --cleanenv -B $dsroot:/out -B $sourcedata:/sourcedata \
  /data/tools/heudiconv-0.5.4.simg -d /sourcedata/dicoms/SMITH-AgingDM-{subject}/scans/*/DICOM/*.dcm -s $sub \
  -f /out/code/heuristics.py -c dcm2niix -b --minmeta -o /out/bids
fi

# run Jeff's code to fix field map, but first correct permissions
chmod -R ug+rw $dsroot/bids/sub-$sub
python $codedir/addIntendedFor.py


# PART 2: Defacing anatomicals to ensure compatibility with data sharing.

# note that pydeface.py should be in your path
bidsroot=$dsroot/bids
pydeface ${bidsroot}/sub-${sub}/anat/sub-${sub}_T1w.nii.gz
mv -f ${bidsroot}/sub-${sub}/anat/sub-${sub}_T1w_defaced.nii.gz ${bidsroot}/sub-${sub}/anat/sub-${sub}_T1w.nii.gz
pydeface ${bidsroot}/sub-${sub}/anat/sub-${sub}_T2w.nii.gz
mv -f ${bidsroot}/sub-${sub}/anat/sub-${sub}_T2w_defaced.nii.gz ${bidsroot}/sub-${sub}/anat/sub-${sub}_T2w.nii.gz



# PART 3: Run MRIQC on subject

# make derivatives folder if it doesn't exist. 
# let's keep this out of bids for now
if [ ! -d $dsroot/derivatives/mriqc ]; then
	mkdir -p $dsroot/derivatives/mriqc
fi


# make scratch
scratch=/data/scratch/`whoami`
if [ ! -d $scratch ]; then
	mkdir -p $scratch
fi

singularity run --cleanenv \
-B $dsroot/bids:/data \
-B $dsroot/derivatives/mriqc:/out \
-B $scratch:/scratch \
/data/tools/mriqc-0.15.1.simg \
/data /out \
participant --participant_label $sub -w /scratch


