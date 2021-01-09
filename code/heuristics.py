import os

def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')

    return template, outtype, annotation_classes

#0005: fmap/sub-<label>[_ses-<session_label>][_acq-<label>][_run-<run_index>]_magnitude1.nii[.gz]
#0006: fmap/sub-<label>[_ses-<session_label>][_acq-<label>][_run-<run_index>]_phasediff.nii[.gz]

def infotodict(seqinfo):

    t1w = create_key('sub-{subject}/anat/sub-{subject}_T1w')
    t2w = create_key('sub-{subject}/anat/sub-{subject}_T2w')
    mag = create_key('sub-{subject}/fmap/sub-{subject}_magnitude')
    phase = create_key('sub-{subject}/fmap/sub-{subject}_phasediff')
    trust = create_key('sub-{subject}/func/sub-{subject}_task-trust_run-{item:02d}_bold')
    
    # to be released later
    #ultimatum = create_key('sub-{subject}/func/sub-{subject}_task-ultimatum_run-{item:02d}_bold')
    #sharedreward = create_key('sub-{subject}/func/sub-{subject}_task-sharedreward_run-{item:02d}_bold')

    #info = {t1w: [], t2w: [], trust: [], ultimatum: [], mag: [], phase: [], sharedreward: []}
    info = {t1w: [], t2w: [], trust: [], mag: [], phase: []}
    
    for s in seqinfo:
        if (s.dim3 == 72) and ('gre_field' in s.protocol_name) and ('NORM' in s.image_type):
            info[mag] = [s.series_id]
        if (s.dim3 == 36) and ('gre_field' in s.protocol_name):
            info[phase] = [s.series_id]
        if (s.dim2 == 192) and ('T1w' in s.protocol_name) and ('NORM' in s.image_type):
            info[t1w] = [s.series_id]
        if (s.dim2 == 192) and ('T2w' in s.protocol_name) and ('NORM' in s.image_type):
            info[t2w] = [s.series_id]
        if (s.dim4 == 217) and ('trust' in s.protocol_name):
            info[trust].append({'item': s.series_id})
        #if (s.dim4 == 202) and ('reward' in s.protocol_name):
        #    info[sharedreward].append({'item': s.series_id})
        #if (s.dim4 == 200) and ('UG' in s.protocol_name):
        #    info[ultimatum].append({'item': s.series_id})


    return info
