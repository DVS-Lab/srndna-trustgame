# example code for FMRIPREP
# runs FMRIPREP on input subject
# usage: bash run_fmriprep.sh sub
# example: bash run_fmriprep.sh 102

sub=$1

# set up input and output directories.
maindir=`pwd` # assume you are running from the root

# make derivatives folder if it doesn't exist.
# let's keep this out of bids for now
if [ ! -d $maindir/derivatives-test ]; then
	mkdir -p $maindir/derivatives-test
fi

scratchdir=/data/scratch/`whoami`
if [ ! -d $scratchdir ]; then
	mkdir -p $scratchdir
fi

singularity run --cleanenv -B $maindir:/base -B /data/tools/licenses:/opts -B $scratchdir:/scratch \
/data/tools/fmriprep-20.2.0.simg \
/base/bids /base/derivatives-test \
participant --participant_label $sub \
--cifti-output \
--output-spaces fsLR \
--stop-on-first-crash \
--fs-license-file /opts/fs_license.txt \
-w /scratch
