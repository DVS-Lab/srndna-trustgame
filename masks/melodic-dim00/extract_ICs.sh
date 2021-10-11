#!/usr/bin/env bash

# this script prepares the melodic-114 (auto dim, or d=0) output for the nppi
# analyses. we only care about the maps that match the smith09 maps used in the
# main analyses.

# note: smith09_02 is also correlated IC05 (r=0.44) and IC31 (r=0.46), and
# IC31 is also correlated with smith09_03, so use IC05 for smith09_02.

fslsplit melodic_IC_dim-114.nii.gz melodic_ICs_ -t
smith09=0
for ic in 27 5 31 48 50 13 43 16 19 26; do # replacing second element with 5 to avoid  duplication
  let ic_n=$ic-1 #account for zero-indexing
  ic_pad=`zeropad $ic_n 4`
  cp melodic_ICs_${ic_pad}.nii.gz ../melodic-114_smith09_net${smith09}.nii.gz
  let smith09=$smith09+1
done
