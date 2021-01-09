% convert all trust
 sublist = [104 105 106 107 108 109 110 111 112 113 115 116 ...
    117 118 120 121 122 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 140 141 142 ... 
    143 144 145 147 149:159];

%sublist = [130 131 132];

% no 139?
for s = 1:length(sublist)
    if sublist(s) == 143
        copyfile psychopy/logs/sub-143/func/*.tsv ../bids/sub-143/func/
        % don't redo since we had to remake ultimatum by hand
    else
        convertTrust_BIDS(sublist(s)); % scanner participant
        %convertUG_BIDS(sublist(s)); % scanner outside
        if sublist(s) == 129 || sublist(s) == 138
            pay_subject(sublist(s));
            continue
        else
            %this will break the bids directory?
            %should the 200s even be in the participants.tsv?
            %could add them to the .bidsignore file
            convertTrust_BIDS(sublist(s) + 100); % friend outside
            %convertUG_BIDS(sublist(s) + 100); % friend outside
        end
        
    end
end

% notes
% 229 only has one run for trust. looks like it was sstarted and stopped. technical issue?
% 238 -- STOPPED RESPONDED afer about 10 trials on run 5. why?


