#!/usr/bin/env bash

# This script will run melodic on all of the good runs from the trus task.
# It will also calculate the similarity (correlation) with the Smith09 maps.

# ensure paths are correct irrespective from where user runs the script
scriptdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
maindir="$(dirname "$scriptdir")"

task=trust
outdir=${maindir}/derivatives/fsl

# run melodic (auto-dim) and dual regression
melodic -i ${scriptdir}/melodic_filelist.txt \
-o ${outdir}/melodic-concat_dim-00_task-${task}.ica -v \
--nobet --bgimage=${outdir}/mean_func \
--report --guireport=report.html -d 0 \
--mmthresh=0.5 --Ostats -a concat

# dual regression with 1 -1 1 0 (des_norm, no design inputs, 1 permutations, and 0 thresholding)
dual_regression ${outdir}/melodic-concat_dim-00_task-${task}.ica/melodic_IC \
1 -1 1 \
${outdir}/melodic-concat_dim-00_task-${task}.ica/DR \
`cat ${scriptdir}/melodic_filelist.txt`


# run melodic (25 components) and dual regression
melodic -i ${scriptdir}/melodic_filelist.txt \
-o ${outdir}/melodic-concat_dim-25_task-${task}.ica -v \
--nobet --bgimage=${outdir}/mean_func \
--report --guireport=report.html -d 25 \
--mmthresh=0.5 --Ostats -a concat

# dual regression with 1 -1 1 0 (des_norm, no design inputs, 1 permutations, and 0 thresholding)
dual_regression ${outdir}/melodic-concat_dim-25_task-${task}.ica/melodic_IC \
1 -1 1 \
${outdir}/melodic-concat_dim-25_task-${task}.ica/DR \
`cat ${scriptdir}/melodic_filelist.txt`

# tar output and transfer to google drive
tar -zcvf melodic_task-trust.tar.gz ${outdir}/melodic-concat_dim-25_task-${task}.ica ${outdir}/melodic-concat_dim-00_task-${task}.ica
rclone copy melodic_task-trust.tar.gz dvs-temple:projects/
