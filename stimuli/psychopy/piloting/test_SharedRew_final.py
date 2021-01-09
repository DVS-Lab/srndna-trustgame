###SRNDNA
###shared reward, block design

from psychopy import visual, core, event, gui, data, sound, logging
import csv
import datetime
import random
import numpy
import os

maindir = os.getcwd()


#parameters
useFullScreen = True
DEBUG = False

frame_rate=1
decision_dur=2.5
outcome_dur=0.75

responseKeys=('1','2')

#get subjID
subjDlg=gui.Dlg(title="Shared Reward Task")
subjDlg.addField('Enter Subject ID: ')
subjDlg.show()

if gui.OK:
    subj_id=subjDlg.data[0]
else:
    sys.exit()

run_data = {
    'Participant ID': subj_id,
    'Date': str(datetime.datetime.now()),
    'Description': 'SRNDNA Pilot - SharedReward Task'
    }

#window setup
win = visual.Window([800,600], monitor="testMonitor", units="deg", fullscr=useFullScreen, allowGUI=False, screen=useDualScreen)

#checkpoint
print "got to check 1"

#define stimulus
fixation = visual.TextStim(win, text="+", height=2)

#waiting for trigger
ready_screen = visual.TextStim(win, text="Ready? \n\nPlease remember to keep your head still!", height=1.5)

#decision screen
#pictureStim =  visual.ImageStim(win, pos=(0,8.0))
nameStim = visual.TextStim(win=win, name='text',text='?',font='Arial',pos=(0, 8.0), height=1, wrapWidth=None, ori=0, color='white', colorSpace='rgb', opacity=1,depth=-1.0);
cardStim = visual.Rect(win=win, name='polygon', width=(8.0,8.0)[0], height=(10.0,10.0)[1], ori=0, pos=(0, 0),lineWidth=5, lineColor=[1,1,1], lineColorSpace='rgb',fillColor=[0,0,0], fillColorSpace='rgb',opacity=1, depth=0.0, interpolate=True)
question = visual.TextStim(win=win, name='text',text='?',font='Arial',pos=(0, 0), height=1, wrapWidth=None, ori=0, color='white', colorSpace='rgb', opacity=1,depth=-1.0);

#outcome screen
outcome_cardStim = visual.Rect(win=win, name='polygon', width=(8.0,8.0)[0], height=(10.0,10.0)[1], ori=0, pos=(0, 0),lineWidth=5, lineColor=[1,1,1], lineColorSpace='rgb',fillColor=[0,0,0], fillColorSpace='rgb',opacity=1, depth=0.0, interpolate=True)
outcome_text = visual.TextStim(win=win, name='text',text='',font='Arial',pos=(0, 0), height=2, wrapWidth=None, ori=0, color='white', colorSpace='rgb', opacity=1,depth=-1.0);
outcome_money = visual.TextStim(win=win, name='text',text='',font='Wingdings 3',pos=(0, 2.0), height=2, wrapWidth=None, ori=0, colorSpace='rgb', opacity=1,depth=-1.0);

#instructions
instruct_screen = visual.TextStim(win, text='Welcome to the experiment.\n\nIn this task you will be guessing the numerical value of a card.\n\nPress Button 1 to guess low and press Button 2 to guess high.\n\nCorrect responses will result in a monetary gain of $4, and incorrect responses will result in a monetary loss of $2.00.\n\nRemember, you will be sharing monetary outcomes on each trial with the partner displayed at the top of the screen.', pos = (0,1), wrapWidth=20, height = 1.2)

#exit
exit_screen = visual.TextStim(win, text='Thanks for playing! Please wait for instructions from the experimenter.', pos = (0,1), wrapWidth=20, height = 1.2)

#logging
log_file = os.path.join(maindir,'{}_run_{}.csv')

globalClock = core.Clock()
logging.setDefaultClock(globalClock)

timer = core.Clock()

#trial handler
trial_data = [r for r in csv.DictReader(open('SharedReward_design.csv','rU'))]
trials = data.TrialHandler(trial_data[:4], 1, method="sequential") #change to [] for full run

stim_map = {
  '3': 'friend',
  '2': 'stranger',
  '1': 'computer',
  }

outcome_map = {
  '3': 'reward',
  '2': 'neutral',
  '1': 'punish',
  }

'''
#parsing out file data
blocks=[]
runs=[]
for run in range(2):
    run_data=[]
    for block in range(12):
        block_data = []
        for t in range(8):
            sample = random.sample(range(len(trial_data)),1)[0]
            run_data.append(trial_data.pop(sample))
            runs.append(run_data)
            blocks.append(block_data)
         
'''

#checkpoint
print "got to check 2"

runs=[]
for run in range(1):
    run_data = []
    for t in range(8):
        sample = random.sample(range(len(trial_data)),1)[0]
        run_data.append(trial_data.pop(sample))
    runs.append(run_data)

# main task loop
# Instructions
instruct_screen.draw()
win.flip()
event.waitKeys()


def do_run(trial_data, run_num):
    resp=[]
    
    #wait for trigger
    ready_screen.draw()
    win.flip()
    event.waitKeys(keyList=('equal'))
    globalClock.reset()
    
    
    for trial in trials:
        condition_label = stim_map[trial['Partner']]
        #image = "Images/%s.png" % condition_label
        name = condition_label
        nameStim.setText(name)
        #pictureStim.setImage(image)
        #print 'image'
        
        #ITI
        logging.log(level=logging.DATA, msg='ITI') #send fixation log event
        timer.reset()
        ITI_onset = globalClock.getTime()
        iti_for_trial = float(trial['ITI'])
        while timer.getTime() < iti_for_trial:
            fixation.draw()
            win.flip()
            
        #decision phase   
        timer.reset()
        event.clearEvents()
        decision_onset = globalClock.getTime()

        resp_val=None
        resp_onset=None
        
        while timer.getTime() < decision_dur:
            cardStim.draw()
            question.draw()
            #pictureStim.draw()
            nameStim.draw()
            win.flip()
           
        resp = event.getKeys(keyList = responseKeys)
        resp_onset = globalClock.getTime()

        if len(resp)>0:
            resp_val = int(resp[0])
        else:
            resp_val = 0
            
        trials.addData('resp', int(resp_val))
        trials.addData('resp_onset', resp_onset)
        trials.addData('decision', decision_onset)
        trials.addData('ITIonset', ITI_onset)
        
#ISI
#this section of code was intended to move to a fixation if subjects respond before 2 seconds is up, but currently is not functional
        #if resp_val > 0 and timer.getTime() < decision_dur:
        #    logging.log(level=logging.DATA, msg='ISI') #send ISI log event
        #    isi_for_trial = float(trial['ISI'])
        #    while timer.getTime() < decision_dur:
        #       fixation.draw()
        #       win.flip()

#outcome phase
        timer.reset()
        #win.flip()
        outcome_onset = globalClock.getTime()
        
        while timer.getTime() < outcome_dur:
            outcome_cardStim.draw()
            #pictureStim.draw()
            nameStim.draw()
            #win.flip()
    
            if trial['Feedback'] == '3' and resp_val == 1:
                outcome_txt = int(random.randint(1,4))
                outcome_moneyTxt= 'h'
                outcome_color='green'
                trials.addData('outcome_val', int(outcome_txt))
            elif trial['Feedback'] == '3' and resp_val == 2:
                outcome_txt = int(random.randint(6,9))
                outcome_moneyTxt= 'h'
                outcome_color='green'
                trials.addData('outcome_val', int(outcome_txt))
            elif trial['Feedback'] == '2' and resp_val == 1:
                outcome_txt = int(5)
                outcome_moneyTxt= 'n'
                outcome_color='white'
                trials.addData('outcome_val', int(outcome_txt))
            elif trial['Feedback'] == '2' and resp_val == 2:
                outcome_txt = int(5)
                outcome_moneyTxt= 'n'
                outcome_color='white'
                trials.addData('outcome_val', int(outcome_txt))
            elif trial['Feedback'] == '1' and resp_val == 1:
                outcome_txt = int(random.randint(6,9))
                outcome_moneyTxt= 'i'
                outcome_color='red'
                trials.addData('outcome_val', int(outcome_txt))
            elif trial['Feedback'] == '1' and resp_val == 2:
                outcome_txt = int (random.randint(1,4))
                outcome_moneyTxt= 'i'
                outcome_color='red'
                trials.addData('outcome_val', int(outcome_txt))
            elif resp_val == 0: 
                outcome_txt='#'
                outcome_moneyTxt = ''
                outcome_color='white'
                
            
            print outcome_txt
            outcome_text.setText(outcome_txt)
            outcome_money.setText(outcome_moneyTxt)
            outcome_money.setColor(outcome_color)
            outcome_text.draw()
            outcome_money.draw()
            win.flip()
            core.wait(.75)
            #trials.addData('outcome_val', outcome_txt)
            trials.addData('outcome_onset', outcome_onset)
            
            outcome_offset = globalClock.getTime()
            trials.addData('outcome_offset', outcome_offset)

            duration = outcome_offset - decision_onset
            trials.addData('trialDuration', duration)
            event.clearEvents()
        print "got to check 3"

    trials.saveAsText(fileName=log_file.format('SR_'+ subj_id, run_num),delim = ',',dataOut='all_raw')
do_run(trial_data,1)

#final ITI
fixation.draw()
win.flip()
core.wait(12)

# Exit
exit_screen.draw()
win.flip()
event.waitKeys()
