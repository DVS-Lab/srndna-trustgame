#!/bin/bash

# ensure paths are correct irrespective from where user runs the script
scriptdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
maindir="$(dirname "$scriptdir")"

# setting inputs and common variables
sm=6
sub=$1
nruns=$2
type=$3
MAINOUTPUT=${maindir}/derivatives/fsl/sub-${sub}

# exceptions and conditionals for the task; need to exclude bad/missing runs
if [ $sub -eq 145 ] || [ $sub -eq 152 ]; then # bad data
	echo "skipping sub-${sub} for task-trust"
else
	if [ $sub -eq 129 ] || [ $sub -eq 138 ]; then # bad data
		nruns=2
		INPUT1=${MAINOUTPUT}/L1_task-trust_model-01_type-${type}_run-01_sm-${sm}.feat
		INPUT2=${MAINOUTPUT}/L1_task-trust_model-01_type-${type}_run-02_sm-${sm}.feat
	elif [ $sub -eq 118 ]; then # bad data
		nruns=4
		INPUT1=${MAINOUTPUT}/L1_task-trust_model-01_type-${type}_run-01_sm-${sm}.feat
		INPUT2=${MAINOUTPUT}/L1_task-trust_model-01_type-${type}_run-02_sm-${sm}.feat
		INPUT3=${MAINOUTPUT}/L1_task-trust_model-01_type-${type}_run-04_sm-${sm}.feat
		INPUT4=${MAINOUTPUT}/L1_task-trust_model-01_type-${type}_run-05_sm-${sm}.feat
	elif [ $sub -eq 111 ] || [ $sub -eq 128 ]; then # sub-111 (misses), sub-128 (bad registration)
		nruns=4
		INPUT1=${MAINOUTPUT}/L1_task-trust_model-01_type-${type}_run-02_sm-${sm}.feat
		INPUT2=${MAINOUTPUT}/L1_task-trust_model-01_type-${type}_run-03_sm-${sm}.feat
		INPUT3=${MAINOUTPUT}/L1_task-trust_model-01_type-${type}_run-04_sm-${sm}.feat
		INPUT4=${MAINOUTPUT}/L1_task-trust_model-01_type-${type}_run-05_sm-${sm}.feat
	elif [ $sub -eq 150 ]; then # bad data
		nruns=4
		INPUT1=${MAINOUTPUT}/L1_task-trust_model-01_type-${type}_run-01_sm-${sm}.feat
		INPUT2=${MAINOUTPUT}/L1_task-trust_model-01_type-${type}_run-03_sm-${sm}.feat
		INPUT3=${MAINOUTPUT}/L1_task-trust_model-01_type-${type}_run-04_sm-${sm}.feat
		INPUT4=${MAINOUTPUT}/L1_task-trust_model-01_type-${type}_run-05_sm-${sm}.feat
	elif [ $sub -eq 131 ]; then # bad data
		nruns=2
		INPUT1=${MAINOUTPUT}/L1_task-trust_model-01_type-${type}_run-01_sm-${sm}.feat
		INPUT2=${MAINOUTPUT}/L1_task-trust_model-01_type-${type}_run-04_sm-${sm}.feat
	else
		INPUT1=${MAINOUTPUT}/L1_task-trust_model-01_type-${type}_run-01_sm-${sm}.feat
		INPUT2=${MAINOUTPUT}/L1_task-trust_model-01_type-${type}_run-02_sm-${sm}.feat
		INPUT3=${MAINOUTPUT}/L1_task-trust_model-01_type-${type}_run-03_sm-${sm}.feat
		INPUT4=${MAINOUTPUT}/L1_task-trust_model-01_type-${type}_run-04_sm-${sm}.feat
		INPUT5=${MAINOUTPUT}/L1_task-trust_model-01_type-${type}_run-05_sm-${sm}.feat
	fi

	# check for existing output and re-do if missing/incomplete
	OUTPUT=${MAINOUTPUT}/L2_task-trust_model-01_type-${type}_sm-${sm}
	if [ -e ${OUTPUT}.gfeat/cope18.feat/cluster_mask_zstat1.nii.gz ]; then # check last (act) or penultimate (ppi) cope
		echo "skipping existing output"
	else
		echo "re-doing: ${OUTPUT}" >> re-runL2.log
		rm -rf ${OUTPUT}.gfeat

		# ppi has more contrasts than act (phys), so need a different L2 template
		if [ "${type}" == "act" ]; then
			ITEMPLATE=${maindir}/templates/L2_task-trust_model-01_type-act_nruns-${nruns}.fsf
			NCOPES=18
		else
			ITEMPLATE=${maindir}/templates/L2_task-trust_model-01_type-ppi_nruns-${nruns}.fsf
			NCOPES=19
		fi

		# set output template and run template-specific analyses
		OTEMPLATE=${MAINOUTPUT}/L2_task-trust_model-01_type-${type}.fsf
		if [ ${nruns} -eq 5 ]; then
			sed -e 's@OUTPUT@'$OUTPUT'@g' \
			-e 's@INPUT1@'$INPUT1'@g' \
			-e 's@INPUT2@'$INPUT2'@g' \
			-e 's@INPUT3@'$INPUT3'@g' \
			-e 's@INPUT4@'$INPUT4'@g' \
			-e 's@INPUT5@'$INPUT5'@g' \
			<$ITEMPLATE> $OTEMPLATE
		elif [ ${nruns} -eq 4 ]; then
			sed -e 's@OUTPUT@'$OUTPUT'@g' \
			-e 's@INPUT1@'$INPUT1'@g' \
			-e 's@INPUT2@'$INPUT2'@g' \
			-e 's@INPUT3@'$INPUT3'@g' \
			-e 's@INPUT4@'$INPUT4'@g' \
			<$ITEMPLATE> $OTEMPLATE
		elif [ ${nruns} -eq 3 ]; then
			sed -e 's@OUTPUT@'$OUTPUT'@g' \
			-e 's@INPUT1@'$INPUT1'@g' \
			-e 's@INPUT2@'$INPUT2'@g' \
			-e 's@INPUT3@'$INPUT3'@g' \
			<$ITEMPLATE> $OTEMPLATE
		elif [ ${nruns} -eq 2 ]; then
			sed -e 's@OUTPUT@'$OUTPUT'@g' \
			-e 's@INPUT1@'$INPUT1'@g' \
			-e 's@INPUT2@'$INPUT2'@g' \
			<$ITEMPLATE> $OTEMPLATE
		fi
		feat $OTEMPLATE

		# delete unused files
		for cope in `seq ${NCOPES}`; do
			rm -rf ${OUTPUT}.gfeat/cope${cope}.feat/stats/res4d.nii.gz
			rm -rf ${OUTPUT}.gfeat/cope${cope}.feat/stats/corrections.nii.gz
			rm -rf ${OUTPUT}.gfeat/cope${cope}.feat/stats/threshac1.nii.gz
			rm -rf ${OUTPUT}.gfeat/cope${cope}.feat/filtered_func_data.nii.gz
			rm -rf ${OUTPUT}.gfeat/cope${cope}.feat/var_filtered_func_data.nii.gz
		done

	fi
fi
