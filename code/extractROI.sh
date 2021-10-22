#!/usr/bin/env bash

# ensure paths are correct irrespective from where user runs the script
scriptdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
maindir="$(dirname "$scriptdir")"

# DMN-TPJ
# ECN-Insula

# ROI name and other path information
for TYPE in melodic-nppi-dmn melodic-nppi-ecn; do
	for ROI in func_ECN-insula func_DMN-tpj; do
		MASK=${maindir}/masks/${ROI}.nii.gz
		TASK=trust
		outputdir=${maindir}/derivatives/imaging
		mkdir -p $outputdir

		for COPENUM in 4 5 6 7 8 9; do
			cnum_padded=`zeropad ${COPENUM} 2`
			MAINOUTPUT=${maindir}/derivatives/fsl/L3_model-01_task-trust_n48_flame1+2_retest
			DATA=`ls -1 ${MAINOUTPUT}/L3_task-${TASK}_type-${TYPE}_cnum-${cnum_padded}_*onegroup_new.gfeat/cope1.feat/filtered_func_data.nii.gz`
			fslmeants -i $DATA -o ${outputdir}/${ROI}_type-${TYPE}_cope-${cnum_padded}.txt -m ${MASK}
		done
	done
done
