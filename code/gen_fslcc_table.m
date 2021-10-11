% summarizes the fslcc output from the command below:
% fslcc -t -1 --noabs -m melodic_mask.nii.gz melodic_IC_dim-114.nii.gz rPNAS_Smith09.nii.gz > fslcc_output.txt
%
% goals are to a) identify the best-matching components with Smith09PNAS,
% b) collect descriptive stats for other components (mean corr, range of corrs),
% and c) output a table for the paper supplement

% set paths and output
codedir = pwd;
addpath(codedir);
cd ..
basedir = pwd;
outdir = fullfile(basedir,'derivatives','imaging');
if ~exist(outdir,'dir')
    mkdir(outdir);
end

% load in all pairwise spatial correlations (10 * 114)
% result is 1140 x 3 matrix (col1 is melodic_IC, col2 is Smith09 map, col3 is correlation
indata = load(fullfile(basedir,'masks','fslcc_output_dim-114.txt'));

% reshape into 25 x 10 matrix (this could just go into the supplement)
nICs = 114;
data_mat = zeros(nICs,10);
myrownames = cell(nICs,1);
mycolnames = cell(1,10);
for i = 1:nICs
    myrownames{i,1} = sprintf('melodicIC_%03d',i);
    for j = 1:10
        if i == 1
            mycolnames{1,j} = sprintf('smith09_%02d',j);
        end
        data_mat(i,j) = indata((indata(:,1)==i & indata(:,2)==j),3);
    end
end

[max_vals,i] = max(data_mat);
for x = 1:length(i)
    data_mat(i(x),x) = NaN; %replace with NaNs
end

%get descriptives for each smith09 map after removing max correlation
mean_corr = nanmean(data_mat);
std_corr = nanstd(data_mat);
min_corr = nanmin(data_mat);
max_corr = nanmax(data_mat);


corr_stats = [i; max_vals; mean_corr; std_corr; min_corr; max_corr];
rownames_corr = {'melodic_IC', 'corr with Smith09', 'mean corr (other)','std corr (other)','min corr (other)','max corr (other)'};

% convert corr_stats to table and output as a spreadsheet
output = fullfile(outdir,'corr_stats_dim-114.csv');
T = array2table(corr_stats,'VariableNames',mycolnames,'RowNames',rownames_corr);
writetable(T,output,'WriteRowNames',true)
% note: smith09_02 is also correlated IC05 (r=0.44) and IC31 (r=0.46), and
% IC31 is also correlated with smith09_03, so use IC05 for smith09_02.

% convert data_mat to table and output as a spreadsheet
output = fullfile(outdir,'component_correlations_dim-114.csv');
T = array2table(data_mat,'VariableNames',mycolnames,'RowNames',myrownames);
writetable(T,output,'WriteRowNames',true)
