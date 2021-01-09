#### trust game practice script, trustee role ####

# edited by Dominic Fareri, 6/2018

#import modules


from psychopy import visual, core, event, gui, data, sound, logging
import os
import sys
import csv
import datetime
import random

#parameters
DEBUG = False

frame_rate=1
decision_dur=3
instruct_dur=3
outcome_dur=1

responseKeys=('2','3','z')

#get subjID

subjDlg=gui.Dlg(title="Trust Game Task")
subjDlg.addField('Enter Subject ID: ') #0
subjDlg.addField('Enter Friend Name: ') #1
subjDlg.addField('Enter Partner Name: ') #NOTE: PARTNER IS THE CONFEDERATE/STRANGER #2
subjDlg.addField('Full Screen? (Enter lowercase: y or n):') #4
subjDlg.show()

if gui.OK:
    subj_id=subjDlg.data[0]
    friend_id=subjDlg.data[1]
    stranger_id=subjDlg.data[2]
    screen=subjDlg.data[3]
    if (not subj_id == False):
        run = 1
else:
    sys.exit()

run_data = {
    'Participant ID': subj_id,
    'Date': str(datetime.datetime.now()),
    'Description': 'SRNDNA Pilot - Trust Game Practice'
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
ready_screen = visual.TextStim(win, text="Please wait for the practice round to begin.", height=1.5)
waiting = visual.TextStim(win, text="Waiting...", height=1.5)


#decision screen
shareStim =  visual.TextStim(win, pos=(0,1.5), height=1, alignHoriz='center')
pictureStim =  visual.ImageStim(win, pos=(0,8.0), size=(6.65,6.65))
investedStim = visual.TextStim(win,pos=(0,0), height=1, alignHoriz='center')
resp_text_left = visual.TextStim(win, pos =(-7,-4.8), height=1, alignHoriz="center")
resp_text_right = visual.TextStim(win, pos =(7,-4.8), height=1, alignHoriz="center")


# instruction screen #
instruct_screen = visual.TextStim(win, text='Decide how much money to share \n- press 2 for left \n- press 3 for right', pos = (0,1), wrapWidth=20, height = 1.2)

#exit
exit_screen = visual.TextStim(win, text='Thanks for playing! Please wait for instructions from the experimenter.', pos = (0,1), wrapWidth=20, height = 1.2)

#miss screen
miss = visual.TextStim(win,text = '')

#logging
expdir = os.getcwd()
subjdir = '%s/logs/%s' % (expdir, subj_id)
if not os.path.exists(subjdir):
    os.makedirs(subjdir)
log_file = os.path.join(subjdir,'sub{}_task-trustee_practice.csv')

# double check that friend and stranger photos are created
imgdir = '%s/Images/friend.png' % (expdir)
if not os.path.isfile(imgdir):
    print 'Please create participant images and folders (see protocol).'
    sys.exit()

# Initialize timers
globalClock = core.Clock()
timer = core.Clock()

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

trustee_map = {
  '0': 'zero',
  '1': 'half',
  }

'''
miss_map = {
  'NA': 'You have 3 seconds to respond'
  }
'''

#read in stimuli
trial_data = [r for r in csv.DictReader(open('params/trustee_design_practice_DF.csv','rU'))]
#set up trial handlers
trials = data.TrialHandler(trial_data[:], 1, method="sequential") #change to [] for full run


#present instructions
curTime=globalClock.getTime()
startTime=curTime
if not DEBUG:
    while timer.getTime()<instruct_dur:
        instruct_screen.draw()
        win.flip()
        curTime=globalClock.getTime()

    print 'Got to check 1'

#main task loop
def do_run(run, trials):
    resp = []
    fileName=log_file.format(subj_id, run)
    #wait for trigger from scanner (= key press)
    ready_screen.draw()
    win.flip()
    event.waitKeys(keyList=('equal'))
    globalClock.reset()
    studyStart = globalClock.getTime()

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
        resp_left = trustee_map[trial['cLeft']]
        respcLeft = 'Share %s' % resp_left
        resp_text_left.setText(respcLeft)
        resp_right = trustee_map[trial['cRight']]
        respcRight = 'Share %s' % resp_right
        resp_text_right.setText(respcRight)


        #Wait for Partner Response Screen
        trial_onset=globalClock.getTime()
        wait_onset=globalClock.getTime()
        trials.addData('wait_onset', wait_onset)
        timer.reset()
        wait_dur = float(trial['ISI'])

        waiting.draw()
        win.flip()
        core.wait(wait_dur)

        #decision phase
        timer.reset()

        event.clearEvents()

        resp = []
        resp_val=None
        resp_onset=None

        while timer.getTime() < .5:
            shareStim.draw()
            pictureStim.draw()
            win.flip()

        while timer.getTime() < decision_dur:

            if (int(trial['AmtInvested']) == 0):
                shareStim.draw()
                pictureStim.draw()
                partner_invest = trial['AmtInvested']
                partnerInvest = 'Shared $%s.00 with you' % partner_invest
                investedStim.setText(partnerInvest)
                investedStim.draw()
                win.flip()
                core.wait(decision_dur)
            else:
                shareStim.draw()
                pictureStim.draw()
                resp_text_left.draw()
                resp_text_right.draw()
                partner_invest = trial['AmtInvested']
                partnerInvest = 'Shared $%s.00 with you' % partner_invest
                investedStim.setText(partnerInvest)
                investedStim.draw()
                win.flip()

                resp = event.getKeys(keyList = responseKeys)

                if len(resp) > 0:
                    if resp[0] == 'z':
                        os.chdir(subjdir)
                        trials.saveAsWideText(fileName)
                        os.chdir(expdir)
                        win.close()
                        core.quit()
                    resp_val = int(resp[0])
                    resp_onset = globalClock.getTime()
                    rt = resp_onset - trial_onset
                    if resp_val == 2:
                        resp_text_left.setColor('red')
                        response = resp_left
                    if resp_val == 3:
                        resp_text_right.setColor('red')
                        response = resp_right
                    shareStim.draw()
                    pictureStim.draw()
                    resp_text_left.draw()
                    resp_text_right.draw()
                    investedStim.draw()
                    win.flip()
                    core.wait(.5)
                    break
                #else:
                #    resp_val = 'NA'
                #    miss_txt = miss_map[resp_val]
                #    miss.setText(miss_txt)

        resp_text_left.setColor('#FFFFFF')
        resp_text_right.setColor('#FFFFFF')
        resp_text_left.setText()
        resp_text_right.setText()

    os.chdir(subjdir)
    trials.saveAsWideText(fileName)
    os.chdir(expdir)        
do_run(trial_data,trials)

#exit_screen
exit_screen.draw()
win.flip()
event.waitKeys()
