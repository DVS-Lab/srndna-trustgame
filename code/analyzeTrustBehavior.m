function output = analyzeTrustBehavior(subj)
maindir = pwd;

try
    
    [onsets,trial_type,RT,trust_value] = deal([]);
    for r = 1:5
        
        
        fname = sprintf('sub-%03d_task-trust_run-%02d_events.tsv',subj,r);
        input = fullfile(maindir,'bids',['sub-' num2str(subj)],'func');
        infile = fullfile(input,fname);
        if exist(infile,'file')
            fid = fopen(infile,'r');
            C = textscan(fid,'%f%f%s%f%s%s%d%d','Delimiter','\t','HeaderLines',1,'EmptyValue', NaN);
            fclose(fid);
        end
        
        onsets = [onsets; C{1}];
        trial_type = [trial_type; C{3}];
        RT = [RT; C{4}];
        trust_value = [trust_value; C{5}];
        
        % get friend trials and adjust for recip/defect on previous trial
        friend_trials = trial_type(startsWith(trial_type(:),'outcome_friend'));
        friend_trials(end) = [];
        friend_values = str2num(cell2mat(trust_value(startsWith(trial_type(:),'outcome_friend'))));
        friend_values(1) = [];
        
        % get stranger trials and adjust for recip/defect on previous trial
        stranger_trials = trial_type(startsWith(trial_type(:),'outcome_stranger'));
        stranger_trials(end) = [];
        stranger_values = str2num(cell2mat(trust_value(startsWith(trial_type(:),'outcome_stranger'))));
        stranger_values(1) = [];
        
        
        % get computer trials and adjust for recip/defect on previous trial
        computer_trials = trial_type(startsWith(trial_type(:),'outcome_computer'));
        computer_trials(end) = [];
        computer_values = str2num(cell2mat(trust_value(startsWith(trial_type(:),'outcome_computer'))));
        computer_values(1) = [];
        
        
        
    end
    
    output.computer_defect = mean(computer_values(endsWith(computer_trials(:),'defect')));
    output.computer_recip = mean(computer_values(endsWith(computer_trials(:),'recip')));
    
    output.stranger_defect = mean(stranger_values(endsWith(stranger_trials(:),'defect')));
    output.stranger_recip = mean(stranger_values(endsWith(stranger_trials(:),'recip')));
    
    output.friend_defect = mean(friend_values(endsWith(friend_trials(:),'defect')));
    output.friend_recip = mean(friend_values(endsWith(friend_trials(:),'recip')));
    
catch ME
    keyboard
end