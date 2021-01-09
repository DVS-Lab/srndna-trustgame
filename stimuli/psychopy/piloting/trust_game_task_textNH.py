#### trust game task ####

# ebeard
# 5/30/18

# edited by Dominic Fareri, 6/2018


### specs ###
# add task description here

### timing ###
# add timing info here

#import modules

from psychopy import visual, core, event, gui, data, sound, logging
import os
import sys
import csv
import datetime
import random

#maindir = os.getcwd()

#parameters
DEBUG = False

frame_rate=1
decision_dur=3
instruct_dur=3
outcome_dur=1

responseKeys=('2','3','z')

#get subjID
if DEBUG:
    subj_id='test_2' #change with specific test number/as needed
    friend_id='pal'
    stranger_id='stranger'
    specific_run='1'
    run = int(specific_run)
    screen='n'
    
else:
    subjDlg=gui.Dlg(title="Trust Game Task")
    subjDlg.addField('Enter Subject ID: ') #0
    subjDlg.addField('Enter Friend Name: ') #1
    subjDlg.addField('Enter Partner Name: ') #NOTE: PARTNER IS THE CONFEDERATE/STRANGER #2
    subjDlg.addField('Select Run (Leave empty if all!):') #3
    subjDlg.addField('Full Screen? (Enter lowercase: y or n):') #4
    subjDlg.show()
    
    if gui.OK:
        subj_id=subjDlg.data[0]
        friend_id=subjDlg.data[1]
        stranger_id=subjDlg.data[2]
        specific_run=subjDlg.data[3]
        screen=subjDlg.data[4]
        if (not subj_id == False):
            if (not specific_run):
                run = range(0,5)
            elif len(specific_run) == 1: #if user enters an ONLY run - run only the specified run
                run = int(specific_run);
                print 'Running Run %s' %int(specific_run)
            else:
                print 'Somthing went wrong. Here are your options: \n1) Run all runs: Leave the Select Run field empty. \n2) Run a single run: Enter run number (1-5) in Select Run Field. Please try again.'
        else:
            print 'Please enter subject ID. Consult the particiant folder for the correct ID'
            sys.exit()
    else:
        sys.exit()

run_data = {
    'Participant ID': subj_id,
    'Date': str(datetime.datetime.now()),
    'Description': 'SRNDNA Pilot - Trust Game Task'
    }

#window setup
if screen == 'y':
    useFullScreen=True
    useDualScreen=0
if screen == 'n':
    useFullScreen=False
    useDualScreen=0
if (screen != 'y') and (screen != 'n'):
    print 'Please specify how you want to present this task. Please enter y (yes) or n (no).'

win = visual.Window([800,600], monitor="testMonitor", units="deg", fullscr=useFullScreen, allowGUI=False, screen=useDualScreen) #set screen to 1 for dual monitor

#define stimulus
fixation = visual.TextStim(win, text="+", height=2)
ready_screen = visual.TextStim(win, text="Please wait for the block of trials to begin. \n\nRemember to keep your head still!", height=1.5)
waiting = visual.TextStim(win, text="Waiting...", height=1.5)

#decision screen
shareStim =  visual.TextStim(win, pos=(0,1.5), height=1, alignHoriz='center')
pictureStim =  visual.ImageStim(win, pos=(0,8.0))
resp_text_left = visual.TextStim(win, pos =(-7,-4.8), height=1, alignHoriz="center")
resp_text_right = visual.TextStim(win, pos =(7,-4.8), height=1, alignHoriz="center")

# outcome screen
outcome_stim = visual.TextStim(win, text='')

outcome_map = {
    1: 'You have chosen to keep the money',
    2: {0:'{} has chosen to share $0', 1:'{} has chosen to share money'},
    'NA': 'You have three seconds to choose'
    }

# instruction screen #
instruct_screen = visual.TextStim(win, text='Decide how much money to share \n- press 2 for left \n- press 3 for right', pos = (0,1), wrapWidth=20, height = 1.2)

#logging
expdir = os.getcwd()
subjdir = '%s/logs/%s' % (expdir, subj_id)
if not os.path.exists(subjdir):
    os.makedirs(subjdir)
log_file = os.path.join(subjdir,'sub{}_task-trust_run{}_raw.csv')

# double check that friend and stranger photos are created
imgdir = '%s/Images/friend.png' % (expdir)
if not os.path.isfile(imgdir):
    print 'Please create participant images and folders (see protocol).'
    sys.exit()

#timing
globalClock = core.Clock()
timer = core.Clock()

#read in stimuli
trial_data_1 = [r for r in csv.DictReader(open('params/run-01_design.csv','rU'))]
trial_data_2 = [r for r in csv.DictReader(open('params/run-02_design.csv','rU'))]
trial_data_3 = [r for r in csv.DictReader(open('params/run-03_design.csv','rU'))]
trial_data_4 = [r for r in csv.DictReader(open('params/run-04_design.csv','rU'))]
trial_data_5 = [r for r in csv.DictReader(open('params/run-05_design.csv','rU'))]
trial_data_6 = [r for r in csv.DictReader(open('params/run-06_design.csv','rU'))]

#set up trial handlers
trials_run1 = data.TrialHandler(trial_data_1[:], 1, method="sequential") #change to [] for full run
trials_run2 = data.TrialHandler(trial_data_2[:], 1, method="sequential") #change to [] for full run
trials_run3 = data.TrialHandler(trial_data_3[:], 1, method="sequential") #change to [] for full run
trials_run4 = data.TrialHandler(trial_data_4[:], 1, method="sequential") #change to [] for full run
trials_run5 = data.TrialHandler(trial_data_5[:], 1, method="sequential") #change to [] for full run
trials_run6 = data.TrialHandler(trial_data_6[:], 1, method="sequential") #change to [] for full run

# condition to stim mapping
# might need to edit this with text logic
stim_map = {
  '3': friend_id,
  '2': stranger_id,
  '1': 'Computer',
  }

image_map = {
  '3': 'friend',
  '2': 'stranger',
  '1': 'computer',
  }

#### TASK ####

#reset globalClock for beginning of task
globalClock.reset()

#present instructions
curTime=globalClock.getTime()
startTime=curTime
if not DEBUG:
    while timer.getTime()<instruct_dur:
        instruct_screen.draw()
        win.flip()
        curTime=globalClock.getTime()

# main task loop
def do_run(run, trials):
    resp = []
    
    #wait for trigger from scanner (= key press)
    
    ready_screen.draw()
    win.flip()
    event.waitKeys(keyList=('equal'))
    globalClock.reset()
        
    for trial in trials:
        
        # add trial logic
        # i.e. show stimuli
        # get resp
        # add data to 'trial'
        
        condition_label = stim_map[trial['Partner']]
        shareStim.setText(condition_label)
        image_label = image_map[trial['Partner']]
        imagepath = os.path.join(expdir,'Images')
        image = os.path.join(imagepath, "%s.png") % image_label
        pictureStim.setImage(image)
        resp_left = trial['cLeft']
        respcLeft = 'Share $%s.00' % resp_left
        resp_text_left.setText(respcLeft)
        resp_right = trial['cRight']
        respcRight = 'Share $%s.00' % resp_right
        resp_text_right.setText(respcRight)
        
        if resp == ['z']:
            trials.saveAsText(fileName=log_file.format(subj_id, run),delim=',',dataOut='all_raw')
            core.quit()
        
        #decision phase
        timer.reset()
        
        event.clearEvents()
        
        resp = []
        resp_val=None
        resp_onset=None
        #answer=0
        trial_onset=globalClock.getTime()
        ISI_pad = []
        
        while timer.getTime() < .5:
            shareStim.draw()
            pictureStim.draw()
            win.flip()
        
        while timer.getTime() < decision_dur:
            shareStim.draw()
            pictureStim.draw()
            resp_text_left.draw()
            resp_text_right.draw()
            win.flip()
            
            #if answer == 0:
            resp = event.getKeys(keyList = responseKeys)
                        
            if len(resp) > 0:
                resp_val = int(resp[0])
                resp_onset = globalClock.getTime()
                rt = resp_onset - trial_onset
                ISI_pad = decision_dur-rt
                #answer = 1
                if resp_val == 2:
                    resp_text_left.setColor('red')
                    response = resp_left
                    if resp_left < resp_right:
                        highlow = 'low'
                    else:
                        highlow = 'high'
                if resp_val == 3:
                    resp_text_right.setColor('red')
                    response = resp_right
                    if resp_left < resp_right:
                        highlow = 'high'
                    else:
                        highlow = 'low'
                shareStim.draw()
                pictureStim.draw()
                resp_text_left.draw()
                resp_text_right.draw()
                win.flip()  
                core.wait(.5)
                #win.flip()
                break
            else:
                resp_val = 'NA'
                response = 'NA'
                resp_onset = globalClock.getTime()
                highlow = 'NA'
                rt = 0
                ISI_pad = decision_dur-0
                
                
        trials.addData('onset', trial_onset)
        trials.addData('bpress', resp_val)
        trials.addData('resp', response)
        trials.addData('resp_onset', resp_onset)
        trials.addData('highlow', highlow)
        trials.addData('rt', rt)
        trials.addData('ISIpad', ISI_pad)
        
        #reset rating number and amount
        resp_text_left.setColor('#FFFFFF')
        resp_text_right.setColor('#FFFFFF')
        resp_text_left.setText()
        resp_text_right.setText()
        
        #ISI
        #logging.log(level=logging.DATA, msg='ISI') #send fixation log event
        ISI_onset=globalClock.getTime()
        trials.addData('ISI_onset', ISI_onset)
        timer.reset()
        isi_for_trial = float(trial['ISI'])
        
        #ANTHONY CHANGED THIS, SORRY THANKS!
        fixation.draw()
        win.flip()
        core.wait(ISI_pad)
        
        waiting.draw()
        win.flip()
        core.wait(isi_for_trial)
            
        #outcome phase
        partner_resp=float(trial['Reciprocate'])
        
        if len(resp) > 0:
            if (int(trial['cLeft']) == 0 and resp_val == 2) or (int(trial['cRight']) == 0 and resp_val == 3):
                core.wait(.5)
                outcome_onset = 'NA'
            else:
                outcome_txt = outcome_map[2][partner_resp].format(condition_label)
                outcome_stim.setText(outcome_txt)
                outcome_stim.draw()
                win.flip()
                core.wait(2)
                outcome_onset=globalClock.getTime()
        else:
            outcome_txt = outcome_map[resp_val]
            outcome_stim.setText(outcome_txt)
            outcome_stim.draw()
            win.flip()
            core.wait(2)
            outcome_onset='NA'
        
        trials.addData('outcome_onset', outcome_onset)
        trial_duration=globalClock.getTime()
        trials.addData('duration', trial_duration-trial_onset)
        
        #ITI
        #logging.log(level=logging.DATA, msg='ITI') #send fixation log event
        timer.reset()
        iti_for_trial = float(trial['ITI'])
        ITI_onset = globalClock.getTime()
        while timer.getTime() < iti_for_trial:
            fixation.draw()
            win.flip()
        trials.addData('ITI_onset', ITI_onset)
    trials.saveAsText(fileName=log_file.format(subj_id, run),delim=',',dataOut='all_raw',appendFile=True)
#### just do specific run if needed

if len (specific_run)==1:
    if run == 1:
        do_run(0, trials_run1)
    elif run == 2:
        do_run(1, trials_run2)
    elif run == 3:
        do_run(2, trials_run3)
    elif run == 4:
        do_run(3, trials_run4)
    elif run == 5:
        do_run(4, trials_run5)
    elif run == 6:
        do_run(5, trials_run6)
    else: 'Run index is not permissible.'
else:
    for run, trials in enumerate([trials_run1, trials_run2, trials_run3, trials_run4, trials_run5, trials_run6]):
        do_run(run, trials)