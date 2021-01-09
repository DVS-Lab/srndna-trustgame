#### trust game task practice ####

#ebeard
#06/04/18

#import modules
from psychopy import visual, core, event, gui, data, sound, logging
import os
import sys
import csv
import datetime
import random

reload(sys)  
sys.setdefaultencoding('utf8')

#parameters
frame_rate = 1
decision_dur = 3
instruct_dur = 3
outcome_dur = 1

responseKeys = ('2', '3', 'z')

#gui
subjDlg = gui.Dlg(title='Investment Game Practice')
subjDlg.addField('Enter Subject ID: ') #0
subjDlg.addField('Enter Friend Name: ') #1
subjDlg.addField('Enter Partner Name: ') #2
subjDlg.addField('Full Screen? (Enter lowercase: y or n):') #3
subjDlg.show()

if gui.OK:
    subj_id = subjDlg.data[0]
    friend_id=subjDlg.data[1]
    stranger_id=subjDlg.data[2]
    screen = subjDlg.data[3]
else:
    print 'please enter task info'
    sys.exit()

#windowsetup
if screen == 'y':
    useFullScreen = True
    useDualScreen = 1
if screen == 'n':
    useFullScreen = False
    useDualScreen = 0
if (screen != 'y') and (screen != 'n'):
    print 'please specify how you want to present the task'

win = visual.Window([800,600], monitor='testMonitor', units='deg', fullscr=useFullScreen, allowGUI=False, screen=useDualScreen)

#define stimuli
fixation = visual.TextStim(win, text="+", height=2)
ready_screen = visual.TextStim(win, text="Ready? \n\nPlease remember to keep your head still! \n (press space to continue)", height=1.5)
waiting = visual.TextStim(win, text="Waiting...", height=1.5)

#decision screen
shareStim =  visual.TextStim(win, pos=(0,1.5), height=1, alignHoriz='center')
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
log_file = 'logs/{}/{}_practice.csv'

#timing
globalClock = core.Clock()
timer = core.Clock()

#read in stimuli
trial_data = [r for r in csv.DictReader(open('params/trust_design_practice.csv','rU'))]

#set up trial handler
trials = data.TrialHandler(trial_data[:3], 1, method='random')

#condition to stim mapping
stim_map = {
  '1': friend_id,
  '2': stranger_id,
  '3': 'Computer',
}

#### TASK ####
#reset globalClock for beginning of task
globalClock.reset()

#present instructions
curTime = globalClock.getTime()
startTime = curTime

while timer.getTime()<instruct_dur:
    instruct_screen.draw()
    win.flip()
    curTime=globalClock.getTime()

# main task loop
def do_run(trials):
    resp = []
    
    #wait for button press from RA ('spacebar' key press)
    
    ready_screen.draw()
    win.flip()
    event.waitKeys(keyList=('space'))
    globalClock.reset()
        
    for trial in trials:
        
        # add trial logic
        # i.e. show stimuli
        # get resp
        # add data to 'trial'
        
        condition_label = stim_map[trial['Partner']]
        shareStim.setText(condition_label)
        resp_left = trial['cLeft']
        respcLeft = 'Share $%s.00' % resp_left
        resp_text_left.setText(respcLeft)
        resp_right = trial['cRight']
        respcRight = 'Share $%s.00' % resp_right
        resp_text_right.setText(respcRight)
        
        if resp == ['z']:
            core.quit()
        
        #decision phase
        timer.reset()
        
        event.clearEvents()
        
        resp = []
        resp_val=None
        resp_onset=None
        answer=0
        trial_onset=globalClock.getTime()
        ISI_pad = []
        
        while timer.getTime() < .5:
            shareStim.draw()
            win.flip()
        
        while timer.getTime() < decision_dur:
            shareStim.draw()
            resp_text_left.draw()
            resp_text_right.draw()
            win.flip()
            
            if answer == 0:
                resp = event.getKeys(keyList = responseKeys)
            
            if len(resp) == 0:
                resp_val = 'NA'
                response = 'NA'
                resp_onset = globalClock.getTime()
                highlow = 'NA'
                ISI_pad = decision_dur-resp_onset
            
            if answer == 0 and len(resp) > 0:
                resp_val = int(resp[0])
                resp_onset = globalClock.getTime()
                ISI_pad = decision_dur-resp_onset
                answer = 1
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
                resp_text_left.draw()
                resp_text_right.draw()
                win.flip()  
                core.wait(.5)
                break

        trials.addData('onset', trial_onset)
        trials.addData('bpress', resp_val)
        trials.addData('resp', response)
        trials.addData('resp_onset', resp_onset)
        trials.addData('highlow', highlow)
        trials.addData('rt', resp_onset-trial_onset) 
        
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
        while timer.getTime() < isi_for_trial+ISI_pad:
            waiting.draw()
            win.flip()
            
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
        
    trials.saveAsWideText(fileName=log_file.format(subj_id, subj_id), delim=',', appendFile=True)

do_run(trials)

