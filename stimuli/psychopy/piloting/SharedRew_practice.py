from psychopy import visual, core, event, gui, data, sound, logging
import csv
import datetime
import random
import numpy
import os

#maindir = os.getcwd()


#parameters
useFullScreen = True
useDualScreen=1
DEBUG = False

frame_rate=1
decision_dur=2.5
outcome_dur=1

responseKeys=('2','3','z')

#get subjID
subjDlg=gui.Dlg(title="Shared Reward Task")
subjDlg.addField('Enter Subject ID: ')
subjDlg.addField('Enter Friend Name: ') #1
subjDlg.addField('Enter Partner Name: ') #NOTE: PARTNER IS THE CONFEDERATE/STRANGER #2
subjDlg.show()

if gui.OK:
    subj_id=subjDlg.data[0]
    friend_id=subjDlg.data[1]
    stranger_id=subjDlg.data[2]

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
ready_screen = visual.TextStim(win, text="Please wait for the block of trials to begin. \n\nRemember to keep your head still!", height=1.5)

#decision screen
nameStim = visual.TextStim(win=win,font='Arial',pos=(0, 6.0), height=1, color='white', colorSpace='rgb', opacity=1,depth=-1.0);
cardStim = visual.Rect(win=win, name='polygon', width=(8.0,8.0)[0], height=(10.0,10.0)[1], ori=0, pos=(0, 0),lineWidth=5, lineColor=[1,1,1], lineColorSpace='rgb',fillColor=[0,0,0], fillColorSpace='rgb',opacity=1, depth=0.0, interpolate=True)
question = visual.TextStim(win=win, name='text',text='?',font='Arial',pos=(0, 0), height=1, wrapWidth=None, ori=0, color='white', colorSpace='rgb', opacity=1,depth=-1.0);
pictureStim =  visual.ImageStim(win, pos=(0,9.0), size=(6.65,6.65))

#outcome screen
outcome_cardStim = visual.Rect(win=win, name='polygon', width=(8.0,8.0)[0], height=(10.0,10.0)[1], ori=0, pos=(0, 0),lineWidth=5, lineColor=[1,1,1], lineColorSpace='rgb',fillColor=[0,0,0], fillColorSpace='rgb',opacity=1, depth=0.0, interpolate=True)
outcome_text = visual.TextStim(win=win, name='text',text='',font='Arial',pos=(0, 0), height=2, wrapWidth=None, ori=0, color='white', colorSpace='rgb', opacity=1,depth=-1.0);
outcome_money = visual.TextStim(win=win, name='text',text='',font='Wingdings 3',pos=(0, 2.0), height=2, wrapWidth=None, ori=0, colorSpace='rgb', opacity=1,depth=-1.0);

#instructions
instruct_screen = visual.TextStim(win, text='Welcome to the experiment.\n\nIn this task you will be guessing the numerical value of a card.\n\nPress Button 2 to guess low and press Button 3 to guess high.\n\nCorrect responses will result in a monetary gain of $4, and incorrect responses will result in a monetary loss of $2.00.\n\nRemember, you will be sharing monetary outcomes on each trial with the partner displayed at the top of the screen.', pos = (0,1), wrapWidth=20, height = 1.2)

#exit
exit_screen = visual.TextStim(win, text='Thanks for playing! Please wait for instructions from the experimenter.', pos = (0,1), wrapWidth=20, height = 1.2)

#logging
expdir = os.getcwd()
subjdir = '%s/logs/%s' % (expdir, subj_id)
if not os.path.exists(subjdir):
    os.makedirs(subjdir)
log_file = os.path.join(subjdir,'sub{}_task-sharedrewardPractice_raw.csv')

globalClock = core.Clock()
logging.setDefaultClock(globalClock)

timer = core.Clock()

#trial handler
trial_data = [r for r in csv.DictReader(open('SharedReward_practice_DF.csv','rU'))]
trials = data.TrialHandler(trial_data[:6], 1, method="sequential") #change to [] for full run

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

outcome_map = {
  '3': 'reward',
  '2': 'neutral',
  '1': 'punish',
  }

#checkpoint
print "got to check 2"

runs=[]
for run in range(1):
    run_data = []
    for t in range(6):
        sample = random.sample(range(len(trial_data)),1)[0]
        run_data.append(trial_data.pop(sample))
    runs.append(run_data)

# main task loop
# Instructions
instruct_screen.draw()
win.flip()
event.waitKeys(keyList=('space'))

def do_run(trial_data, run_num):
    resp=[]
    fileName=log_file.format(subj_id)

    #wait for trigger
    ready_screen.draw()
    win.flip()
    event.waitKeys(keyList=('equal'))
    globalClock.reset()


    for trial in trials:
        condition_label = stim_map[trial['Partner']]
        image_label = image_map[trial['Partner']]
        imagepath = os.path.join(expdir,'Images')
        image = os.path.join(imagepath, "%s.png") % image_label
        nameStim.setText(condition_label)
        pictureStim.setImage(image)


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

        resp=[]
        resp_val=None
        resp_onset=None

        trial_onset = globalClock.getTime()

        while timer.getTime() < decision_dur:
            cardStim.draw()
            question.draw()
            pictureStim.draw()
            nameStim.draw()
            win.flip()

        resp = event.getKeys(keyList = responseKeys)

        if len(resp)>0:
            if resp[0] == 'z':
                #trials.saveAsText(fileName=log_file.format(subj_id),delim=',',dataOut='all_raw')
                os.chdir(subjdir)
                trials.saveAsWideText(fileName)
                os.chdir(expdir)
                win.close()
                core.quit()
            resp_val = int(resp[0])
            resp_onset = globalClock.getTime()
            rt = resp_onset - trial_onset
        else:
            resp_val = 0
            resp_onset = 'NA'
            #rt = 'NA'

        trials.addData('resp', int(resp_val))
        trials.addData('resp_onset', resp_onset)
        trials.addData('onset', trial_onset)
        trials.addData('ITIonset', ITI_onset)
        trials.addData('rt', rt)


#outcome phase
        timer.reset()
        #win.flip()
        outcome_onset = globalClock.getTime()

        while timer.getTime() < outcome_dur:
            outcome_cardStim.draw()
            pictureStim.draw()
            nameStim.draw()
            #win.flip()

            if trial['Feedback'] == '3' and resp_val == 2:
                outcome_txt = int(random.randint(1,4))
                outcome_moneyTxt= 'h'
                outcome_color='green'
                trials.addData('outcome_val', int(outcome_txt))
            elif trial['Feedback'] == '3' and resp_val == 3:
                outcome_txt = int(random.randint(6,9))
                outcome_moneyTxt= 'h'
                outcome_color='green'
                trials.addData('outcome_val', int(outcome_txt))
            elif trial['Feedback'] == '2' and resp_val == 2:
                outcome_txt = int(5)
                outcome_moneyTxt= 'n'
                outcome_color='white'
                trials.addData('outcome_val', int(outcome_txt))
            elif trial['Feedback'] == '2' and resp_val == 3:
                outcome_txt = int(5)
                outcome_moneyTxt= 'n'
                outcome_color='white'
                trials.addData('outcome_val', int(outcome_txt))
            elif trial['Feedback'] == '1' and resp_val == 2:
                outcome_txt = int(random.randint(6,9))
                outcome_moneyTxt= 'i'
                outcome_color='red'
                trials.addData('outcome_val', int(outcome_txt))
            elif trial['Feedback'] == '1' and resp_val == 3:
                outcome_txt = int (random.randint(1,4))
                outcome_moneyTxt= 'i'
                outcome_color='red'
                trials.addData('outcome_val', int(outcome_txt))
            elif resp_val == 0:
                outcome_txt='#'
                outcome_moneyTxt = ''
                outcome_color='white'


            #print outcome_txt
            outcome_text.setText(outcome_txt)
            outcome_money.setText(outcome_moneyTxt)
            outcome_money.setColor(outcome_color)
            outcome_text.draw()
            outcome_money.draw()
            win.flip()
            core.wait(outcome_dur)
            #trials.addData('outcome_val', outcome_txt)
            trials.addData('outcome_onset', outcome_onset)

            outcome_offset = globalClock.getTime()
            trials.addData('outcome_offset', outcome_offset)

            duration = outcome_offset - trial_onset
            trials.addData('trialDuration', duration)
            event.clearEvents()
        print "got to check 3"

    os.chdir(subjdir)
    trials.saveAsWideText(fileName)
    os.chdir(expdir)
do_run(trial_data,1)

# Exit
exit_screen.draw()
win.flip()
event.waitKeys()
