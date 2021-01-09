#!/bin/bash

# This run_* script is a wrapper for L3stats.sh, so it will loop over several
# copes and models. Note that Contrast N for PPI is always PHYS in these models.


# ensure paths are correct irrespective from where user runs the script
scriptdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
maindir="$(dirname "$scriptdir")"


# this loop defines the different types of analyses that will go into the group comparisons
for analysis in act ppi_seed-VS nppi-dmn nppi-ecn ppi_seed-VMPFC; do
	analysistype=type-${analysis}

	# these define the cope number (copenum) and cope name (copename)
	for copeinfo in "1 c_C" "2 c_F" "3 c_S" "4 C_def" "5 C_rec" "6 F_def" "7 F_rec" "8 S_def" "9 S_rec" "10 rec-def" "11 face" "12 rec-def_F-S" "13 F-S" "14 F-C" "15 S-C" "16 rec_SocClose" "17 def_SocClose" "18 rec-def_SocClose" "19 phys"; do

		# split copeinfo variable
		set -- $copeinfo
		copenum=$1
		copename=$2

		# skip non-existent contrast for activation analysis
		if [ "${analysistype}" == "type-act" ] && [ "${copeinfo}" == "19 phys" ]; then
			echo "skipping phys for activation since it does not exist..."
			continue
		fi

		NCORES=12 # per script; each script will launch 3 feat or randomise processes
		SCRIPTNAME=${maindir}/code/L3stats.sh
		while [ $(ps -ef | grep -v grep | grep $SCRIPTNAME | wc -l) -ge $NCORES ]; do
			sleep 1s
		done
		bash $SCRIPTNAME $copenum $copename $analysistype &

	done
done
