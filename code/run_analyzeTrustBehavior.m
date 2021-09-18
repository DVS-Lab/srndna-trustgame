% analyze and aggregate trust task behavior across all subjects 
% make sure you run from the code directory so that paths are correct

% set paths and output
codedir = pwd;
addpath(codedir);
cd ..
basedir = pwd;
outdir = fullfile(basedir,'derivatives','behavioral');
if ~exist(outdir,'dir')
    mkdir(outdir);
end

sublist = [104 105 106 107 108 109 110 111 112 113 115 116 ...
    117 118 120 121 122 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 140 141 142 ...
    143 144 145 147 149:159];


fname = sprintf('summary_task-trust_desc-postOutcomeShifts-std.csv');
fid = fopen(fullfile(outdir,fname),'w');
fprintf(fid,'sub,computer_defect,computer_recip,stranger_defect,stranger_recip,friend_defect,friend_recip\n');
for s = 1:length(sublist)
    o = analyzeTrustBehavior(sublist(s));
    fprintf(fid,'sub-%d,%f,%f,%f,%f,%f,%f\n',sublist(s),o.computer_defect,o.computer_recip,o.stranger_defect,o.stranger_recip,o.friend_defect,o.friend_recip');
end
fclose(fid);
