#!/usr/bin/env bash

# This script will run melodic on all of the good runs from the trus task.
# It will also calculate the similarity (correlation) with the Smith09 maps.

# ensure paths are correct irrespective from where user runs the script
scriptdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
maindir="$(dirname "$scriptdir")"

task=trust
outdir=${maindir}/derivatives/fsl

# run melodic: auto-dim
melodic -i ${scriptdir}/melodic_filelist.txt \
-o ${outdir}/melodic-concat_dim-00_task-${task}.ica -v \
--nobet --bgimage=${outdir}/mean_func \
--report --guireport=report.html -d 0 \
--mmthresh=0.5 --Ostats -a concat

# run melodic: 25 components
melodic -i ${scriptdir}/melodic_filelist.txt \
-o ${outdir}/melodic-concat_dim-25_task-${task}.ica -v \
--nobet --bgimage=${outdir}/mean_func \
--report --guireport=report.html -d 25 \
--mmthresh=0.5 --Ostats -a concat
