# Age-Related Differences in Social Closeness and Trust
This repository contains code related to our manuscript, tentatively titled "Neural Responses to Reciprocated Trust in Older and Younger Adults". All hypotheses and analysis plans were pre-registered on AsPredicted on 7/26/2018 and data collection commenced on 7/31/2018. Imaging data will be shared via [OpenNeuro][openneuro] when the manuscript is posted on bioRxiv.


## A few prerequisites and recommendations
- Understand BIDS and be comfortable navigating Linux
- Install [FSL](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation)
- Install [miniconda or anaconda](https://stackoverflow.com/questions/45421163/anaconda-vs-miniconda)
- Install PyDeface: `pip install pydeface`
- Make singularity containers for heudiconv (version: 0.5.4), mriqc (version: 0.15.1), and fmriprep (version: 20.1.0).


## Notes on repository organization and files
- Raw DICOMS (an input to heudiconv) are only accessible locally (Smith Lab Linux: /data/sourcedata)
- Some of the contents of this repository are not tracked (.gitignore) because the files are large and we do not yet have a nice workflow for datalad. These folders include: /data/sourcedata (dicoms), bids, and derivatives.
- Tracked folders and their contents:
  - `code`: analysis code
  - `templates`: fsf template files used for FSL analyses
  - `masks`: images used as masks, networks, and seed regions in analyses
  - `stimuli`: psychopy scripts and matlab scripts for delivering stimuli and organizing output


## Basic commands to reproduce our analyses
```
# get code and data (two options for data)
git clone https://github.com/DVS-Lab/srndna-trustgame
cd srndna-trustgame
rm -rf bids # remove bids subdirectory since it will be replaced below

# option 1 for data -- if outside of lab and reproducing/extending:
datalad clone https://github.com/OpenNeuroDatasets/ds003745.git bids
# the bids folder is a datalad dataset
# you can get all of the data with the command below:
datalad get sub-*

# option 2 for data -- if inside of lab and testing/training:
bash code/run_prepdata.sh
# this creates the bids data, but restrict to a few subjects to save diskspace

# run preprocessing and generate confounds and timing files for analyses
bash code/run_fmriprep.sh
python code/MakeConfounds.py --fmriprepDir="derivatives/fmriprep"
bash code/run_gen3colfiles.sh

# run statistics
bash code/run_L1stats.sh
bash code/run_L2stats.sh
bash code/run_L3stats.sh
```


## Acknowledgments
This work was supported, in part, by grants from the National Institutes of Health (R21-MH113917 and R03-DA046733 to DVS and R15-MH122927 to DSF) and a Pilot Grant from the Scientific Research Network on Decision Neuroscience and Aging [to DVS; Subaward of NIH R24-AG054355 (PI Gregory Samanez-Larkin)]. We thank Elizabeth Beard for assistance with task coding, Dennis Desalme, Ben Muzekari, Isaac Levy, Gemma Goldstein, and Srikar Katta for assistance with participant recruitment and data collection, and Jeffrey Dennison for assistance with data processing. DVS was a Research Fellow of the Public Policy Lab at Temple University during the preparation of the manuscript (2019-2020 academic year).

[openneuro]: https://openneuro.org/
