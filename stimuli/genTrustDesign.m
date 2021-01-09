
%{

simulatePayments([0 2 4 8],1000)

ans =

      mean: 25.5760
    twostd: 14.9474
       max: 48

%}

maindir = pwd;
outfiles = fullfile(maindir,'psychopy','params','TG_designs');
mkdir(outfiles);

subs = [101:299 999];
for s = subs
    subout = fullfile(outfiles,sprintf('sub-%03d',s));
    mkdir(subout);
    for r = 1:6
        
        ntrials = 36;
        choice_dur = 3;
        ISI_list = [repmat(2,1,20) repmat(3.5,1,10) repmat(5,1,6)];
        ISI_list = ISI_list(randperm(length(ISI_list)));
        ISI_list = ISI_list - 1.5; %shaving 1.5 seconds to account for "WAITING" screen
        ITI_list = [repmat(2,1,18) repmat(4,1,10) repmat(6,1,5) repmat(8,1,3)];
        ITI_list = ITI_list(randperm(length(ITI_list)));
        
        choice_pairs = combnk([0 2 4 8],2);
        trial_mat = [choice_pairs ones(6,1)*3 ones(6,1);
            choice_pairs ones(6,1)*3 zeros(6,1);
            choice_pairs ones(6,1)*2 ones(6,1);
            choice_pairs ones(6,1)*2 zeros(6,1);
            choice_pairs ones(6,1)*1 ones(6,1);
            choice_pairs ones(6,1)*1 zeros(6,1)];
        
        fname = fullfile(subout,sprintf('sub-%03d_run-%02d_design.csv',s,r));
        
        fid = fopen(fname,'w');
        fprintf(fid,'Trial,cLeft,cRight,Partner,Reciprocate,ISI,ITI\n');
        % Partner is Friend=3, Stranger=2, Computer=1
        % Reciprocate is Yes=1, No=0
        % cLeft is the left option
        % cRight is the right option
        % high/low value option will randomly flip between left/right
        
        rand_trials = randperm(ntrials);
        for i = 1:ntrials
            if rand < .5
                fprintf(fid,'%d,%d,%d,%d,%d,%d,%d\n',i,trial_mat(rand_trials(i),1),trial_mat(rand_trials(i),2),trial_mat(rand_trials(i),3:4),ISI_list(rand_trials(i)),ITI_list(rand_trials(i)));
            else
                fprintf(fid,'%d,%d,%d,%d,%d,%d,%d\n',i,trial_mat(rand_trials(i),2),trial_mat(rand_trials(i),1),trial_mat(rand_trials(i),3:4),ISI_list(rand_trials(i)),ITI_list(rand_trials(i)));
            end
        end
        fclose(fid);
        
    end
end
