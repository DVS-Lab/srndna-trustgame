#!/bin/bash

# ensure paths are correct irrespective from where user runs the script
scriptdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
basedir="$(dirname "$scriptdir")"

for ppi in PCC rFFA tTPJ VMPFCface VMPFCwin VS; do # putting 0 first will indicate "activation"
	for subrun in "104 5" "105 5" "106 3" "107 5" "108 5" "109 2" "110 2" "111 5" "112 5" "113 5" "115 5" "116 5" "117 5" "118 5" "120 5" "121 5" "122 5" "124 5" "125 5" "126 5" "127 5" "128 5" "129 5" "130 5" "131 5" "132 5" "133 5" "134 4" "135 5" "136 2" "137 5" "138 4" "140 5" "141 4" "142 5" "143 3" "144 2" "145 2" "147 5" "149 4" "150 5" "151 5" "152 2" "153 5" "154 2" "155 5" "156 2" "157 5" "158 5" "159 5"; do

	  set -- $subrun
	  sub=$1
	  nruns=$2

	  for run in `seq $nruns`; do
	  	# Manages the number of jobs and cores
	  	SCRIPTNAME=${basedir}/code/L1stats.sh
	  	NCORES=15
	  	while [ $(ps -ef | grep -v grep | grep $SCRIPTNAME | wc -l) -ge $NCORES ]; do
	    		sleep 1s
	  	done
	  	bash $SCRIPTNAME $sub $run $ppi &
	  	sleep 1s
	  done

	done
done
