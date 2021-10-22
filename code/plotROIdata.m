clear; close all;

% set up dirs
codedir = pwd; % must run from code, so this is not a good solution
T = readtable('participants.csv');
addpath(codedir);
cd ..
maindir = pwd;
roidir = fullfile(maindir,'derivatives','imaging');

% loop through rois for activation
rois = {'func_ECN-insula', 'func_DMN-tpj'};
types = {'melodic-nppi-ecn','melodic-nppi-dmn'};
for r = 1:length(rois)
    for t = 1:length(types)
        roi = rois{r};
        type = types{t};
        
        c4 = load(fullfile(roidir,[roi '_type-' type '_cope-04.txt']));
        c5 = load(fullfile(roidir,[roi '_type-' type '_cope-05.txt']));
        c6 = load(fullfile(roidir,[roi '_type-' type '_cope-06.txt']));
        c7 = load(fullfile(roidir,[roi '_type-' type '_cope-07.txt']));
        c8 = load(fullfile(roidir,[roi '_type-' type '_cope-08.txt']));
        c9 = load(fullfile(roidir,[roi '_type-' type '_cope-09.txt']));

        computer = [c4 c5]; % defect recip
        friend = [c6 c7];
        stranger = [c8 c9];

        figure, barweb_dvs2([mean(computer); mean(stranger); mean(friend)],[std(computer)/sqrt(length(computer)); std(stranger)/sqrt(length(stranger)); std(friend)/sqrt(length(friend)) ])
        axis square
        outname = fullfile(maindir,'derivatives','imaging',['plot_roi-' roi '_type-' type '_cope']);
        cmd = ['print -depsc ' outname];
        eval(cmd);
        
        T.C_def = c4;
        T.C_rec = c5;
        T.F_def = c6;
        T.F_rec = c7;
        T.S_def = c8;
        T.S_rec = c9;
        
        writetable(T,fullfile(roidir,['summary_ROI-' roi '_type-' type '.csv']))
    end
end
