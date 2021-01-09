function convertTrust_BIDS(subj)
maindir = pwd;
cd ..
dsdir = pwd;
cd(maindir)

% Partner is Friend=3, Stranger=2, Computer=1
% Reciprocate is Yes=1, No=0
% cLeft is the left option
% cRight is the right option
% high/low value option will randomly flip between left/right
% 
% subj = subject number

try
    
    for r = 0:4
        fname = fullfile(maindir,'psychopy','logs',num2str(subj),sprintf('sub-%03d_task-trust_run-%d_raw.csv',subj,r));
        if exist(fname,'file')
            fid = fopen(fname,'r');
        else
            fprintf('sub-%d -- Investment Game, Run %d: No data found.\n', subj, r+1)
            continue;
        end
        
        C = textscan(fid,[repmat('%f',1,14) '%s' repmat('%f',1,9)],'Delimiter',',','HeaderLines',1,'EmptyValue', NaN);
        fclose(fid);
        
        outcomeonset = C{20}; % should be locked to the presentation of the partner cue (at least 500 ms before choice screen)
        choiceonset = C{11}; % should be locked to the presentation of the partner cue (at least 500 ms before choice screen)
        RT = C{16};
        Partner = C{4};
        reciprocate = C{3};
        response = C{15}; % high/low -- build in check below to check recording
        trust_val = C{13}; % 0-8 (with '999' for no response)
        cLeft = C{6};
        cRight = C{8};
        options = [cLeft cRight];
        
        fname = sprintf('sub-%03d_task-trust_run-%02d_events.tsv',subj,r+1);
        output = fullfile(dsdir,'bids',['sub-' num2str(subj)],'func');
        if ~exist(output,'dir')
            mkdir(output)
        end
        fid = fopen(fullfile(output,fname),'w');
        fprintf(fid,'onset\tduration\ttrial_type\tresponse_time\ttrust_value\tchoice\tcLow\tcHigh\n');
        for t = 1:length(choiceonset)
            
            % output check
            if trust_val(t) == 999
                if strcmp(response{t},'high') && (max(options(t,:)) ~= trust_val(t))
                    error('response output incorrectly recorded for trial %d', t)
                end
            end
            
            if (Partner(t) == 1)
                trial_type = 'computer';
            elseif (Partner(t) == 2)
                trial_type = 'stranger';
            elseif (Partner(t) == 3)
                trial_type = 'friend';
            end
            
            % "String values containing tabs MUST be escaped using double quotes.
            % Missing and non applicable values MUST be coded as "n/a"."
            % http://bids.neuroimaging.io/bids_spec.pdf
            
            %fprintf(fid,'onset\tduration\ttrial_type\tresponse_time\ttrust_value\tchoice\n');
            if trust_val(t) == 999
                fprintf(fid,'%f\t%f\t%s\t%f\t%s\t%s\t%d\t%d\n',choiceonset(t),3,'missed_trial',3,'n/a','n/a',min(options(t,:)),max(options(t,:)));
            else
                if trust_val(t) == 0
                    fprintf(fid,'%f\t%f\t%s\t%f\t%d\t%s\t%d\t%d\n',choiceonset(t),RT(t),['choice_' trial_type ],RT(t),0,response{t},min(options(t,:)),max(options(t,:))); %should always be 'low'
                else
                    if reciprocate(t) == 1
                        fprintf(fid,'%f\t%f\t%s\t%f\t%d\t%s\t%d\t%d\n',choiceonset(t),RT(t),['choice_' trial_type],RT(t),trust_val(t),response{t},min(options(t,:)),max(options(t,:)));
                        fprintf(fid,'%f\t%f\t%s\t%f\t%d\t%s\t%d\t%d\n',outcomeonset(t),1,['outcome_' trial_type '_recip'],RT(t),trust_val(t),response{t},min(options(t,:)),max(options(t,:)));
                    else
                        fprintf(fid,'%f\t%f\t%s\t%f\t%d\t%s\t%d\t%d\n',choiceonset(t),RT(t),['choice_' trial_type],RT(t),trust_val(t),response{t},min(options(t,:)),max(options(t,:)));
                        fprintf(fid,'%f\t%f\t%s\t%f\t%d\t%s\t%d\t%d\n',outcomeonset(t),1,['outcome_' trial_type '_defect'],RT(t),trust_val(t),response{t},min(options(t,:)),max(options(t,:)));
                    end
                end
            end
            
        end
        fclose(fid);
        rand_trial = randsample(1:36,1);
        if trust_val(rand_trial) == 999
            %fprintf('sub-%d -- Investment Game, Run %d: On trial %d, Participant did not respond.\n',subj, r+1, rand_trial);
        else
            if reciprocate(rand_trial)
                participant = (8 - trust_val(rand_trial)) + ((trust_val(rand_trial) * 3)/2);
                friend = (trust_val(rand_trial) * 3)/2;
            else
                participant = 8 - trust_val(rand_trial);
                friend = (trust_val(rand_trial) * 3);
            end
            if (Partner(rand_trial) == 1)
                trial_type = 'Computer';
            elseif (Partner(rand_trial) == 2)
                trial_type = 'Stranger';
            elseif (Partner(rand_trial) == 3)
                trial_type = 'Friend';
            end
            %fprintf('sub-%d -- Investment Game, Run %d: On trial %d, Participant WINS $%.2f and %s WINS $%.2f.\n', subj, r+1, rand_trial, participant, trial_type, friend);
        end
    end
    
catch ME
    disp(ME.message)
    msg = sprintf('check line %d', ME.stack.line);
    disp(msg);
    keyboard
end