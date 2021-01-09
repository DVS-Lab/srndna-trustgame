###SRNDNA
###shared reward, block design

from psychopy import visual, core, event, gui, data, sound, logging
import csv
import datetime
import random
import numpy
import os

#parameters
useFullScreen = True
useDualScreen=1
DEBUG = False

frame_rate=1
decision_dur=3
outcome_dur=0.25
fileSuffix = 'UG'

responseKeys=('2','3','z')

#get subjID
subjDlg=gui.Dlg(title="Bargaining Task")
subjDlg.addField('Enter Subject ID: ') #0
subjDlg.addField('Enter Gender (0 for male, 1 for female): ') #1
subjDlg.addField('Enter Ethnicity (0 for Caucasian, 1 for Other): ') #2
subjDlg.addField('Full Screen? (Enter lowercase: y or n):') #3
subjDlg.show()

if gui.OK:
    subj_id=subjDlg.data[0]
    subj_gen=subjDlg.data[1]
    subj_eth=subjDlg.data[2]
else:
    sys.exit()

run_data = {
    'Participant ID': subj_id,
    'Date': str(datetime.datetime.now()),
    'Description': 'SRNDNA Pilot - UG Task',
    'Participant Gender': subj_gen,
    'Participant Ethnicity': subj_eth
    }

#window setup
win = visual.Window([800,600], monitor="testMonitor", units="deg", fullscr=useFullScreen, allowGUI=False, screen=useDualScreen)

#checkpoint
print "got to check 1"

#define fixation
fixation = visual.TextStim(win, text="+", height=2)

#waiting for trigger
ready_screen = visual.TextStim(win, text="Please wait for the block of trials to begin. \n\nRemember to keep your head still!", height=1.5)


#decision screen
pictureStim =  visual.ImageStim(win, pos=(0,3.5),size=(6.65,5))
resp_text_reject = visual.TextStim(win,text="Reject Offer", pos =(-7,-4.8), height=1, alignHoriz="center")
resp_text_accept = visual.TextStim(win,text="Accept Offer", pos =(7,-4.8), height=1, alignHoriz="center")
offer_text = visual.TextStim(win,pos = (0,-1.5),alignHoriz="center", text='')

#outcome screen
outcome_stim = visual.TextStim(win, pos = (0,-2.5),text='')

#instructions
instruct_screen = visual.TextStim(win, text='Welcome to the bargaining game.\n\nIn this task you will interacting with a few different partners.\n\nOn every trial, your partner will have $20, which s/he can propose to divide in any way between the two of you.\n\nYour task is to choose to either accept or reject the proposed split of money.', pos = (0,1), wrapWidth=20, height = 1.2)
instruct_screen2 = visual.TextStim(win, text='Press Button 2 to accept the offer. Press Button 3 to reject the offer.\n\nIf you choose to reject the offer, you and your partner will both receive $0 for that trial.', pos = (0,1), wrapWidth=20, height = 1.2)

#exit
exit_screen = visual.TextStim(win, text='Thanks for playing! Please wait for instructions from the experimenter.', pos = (0,1), wrapWidth=20, height = 1.2)

#logging
expdir = os.getcwd()
subjdir = '%s/logs/%s' % (expdir, subj_id)
if not os.path.exists(subjdir):
    os.makedirs(subjdir)
log_file = os.path.join(subjdir,'sub{}_task-ultimatum_raw.csv')


globalClock = core.Clock()
logging.setDefaultClock(globalClock)

timer = core.Clock()

#trial handler
trial_data = [r for r in csv.DictReader(open('UG_design_test2DF.csv','rU'))]
trials = data.TrialHandler(trial_data, 1, method="sequential") #change to [] for full run


stim_map = {
    '3': 'olderadultMale_C',
    '2': 'youngadultMale_C',
    '1': 'computer',
    }

outcome_map = {
  #3: 'You have accepted the offer.\n\nYou: $%s.00\nPartner: $%s.00',
  #2: 'You have rejected the offer.\n\nYou: $0.00\nPartner: $0.00',
  'NA': 'You have 3 seconds to respond.'
  }

#checkpoint
print "got to check 2"

'''
runs=[]
for run in range(1):
    run_data = []
    for t in range(8):
        sample = random.sample(range(len(trial_data)),1)[0]
        run_data.append(trial_data.pop(sample))
    runs.append(run_data)
'''

# main task loop
# Instructions
instruct_screen.draw()
win.flip()
event.waitKeys(keyList=('space'))

instruct_screen2.draw()
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
        imagepath = os.path.join(expdir,'Images')
        image = os.path.join(imagepath, "%s.png") % condition_label
        pictureStim.setImage(image)

        #ITI
        logging.log(level=logging.DATA, msg='ITI') #send fixation log event
        timer.reset()
        ITI_onset = globalClock.getTime()
        iti_for_trial = float(trial['ITI'])
        fixation.draw()
        win.flip()
        core.wait(iti_for_trial)

        trials.addData('ITIonset', ITI_onset)


        #decision phase
        timer.reset()
        event.clearEvents()
        decision_onset = globalClock.getTime()
        trials.addData('decision_onset', decision_onset)

        resp_val=None
        resp_onset=None


        while timer.getTime() < decision_dur:
            resp_text_accept.draw()
            resp_text_reject.draw()
            pictureStim.draw()

            partner_offer = trial['Offer']
            partnerOffer = 'Proposal: $%s.00 out of $20.00' % partner_offer
            offer_text.setText(partnerOffer)
            offer_text.draw()
            win.flip()

            resp = event.getKeys(keyList = responseKeys)

            if len(resp)>0:
                if resp == ['z']:
                    #trials.saveAsText(fileName=log_file.format(subj_id),delim=',',dataOut='all_raw')
                    os.chdir(subjdir)
                    trials.saveAsWideText(fileName)
                    os.chdir(expdir)
                    win.close()
                    core.quit()
                resp_val = float(resp[0])
                resp_onset = globalClock.getTime()
                if resp_val == 2:
                    resp_text_reject.setColor('red')
                    core.wait(.25)
                if resp_val == 3:
                    resp_text_accept.setColor('red')
                    core.wait(.25)
                trials.addData('resp', resp_val)
                trials.addData('resp_onset', resp_onset)

                if resp == 0:
                    resp_val='NA'
                    print "got here"
                    outcome_txt = outcome_map[resp_val]
                    outcome_stim.setText(outcome_txt)
                    #win.flip()
                    outcome_stim.draw()
                    core.wait(.25)
                    trials.addData('resp', resp_val)


        #reset rating number color
        resp_text_accept.setColor('#FFFFFF')
        resp_text_reject.setColor('#FFFFFF')

        '''
        #outcome phase
        timer.reset()
        #win.flip()
        outcome_onset = globalClock.getTime()

        pictureStim.draw()
        #win.flip()
        subjectReceives = trial['Offer']
        partnerKeeps = trial['PartnerKeeps']
        if resp_val == 3:
            outcome_txt = outcome_map[resp_val] % (subjectReceives, partnerKeeps)
        elif resp_val==2:
            outcome_txt = outcome_map[resp_val]
        else:
            outcome_txt = outcome_map[resp_val]

        outcome_stim.setText(outcome_txt)
        outcome_stim.draw()
        #trials.addData('outcome_txt', outcome_txt)
        trials.addData('outcome_onset', outcome_onset)
        win.flip()
        core.wait(outcome_dur)
        outcome_offset = globalClock.getTime()
        trials.addData('outcome_offset', outcome_offset)

        fixation.draw()
        win.flip()
        core.wait(.75)
        '''
        trial_offset = globalClock.getTime()
        duration = trial_offset - decision_onset
        trials.addData('trialDuration', duration)
        event.clearEvents()
        print "got to check 3"


    #trials.saveAsText(fileName=log_file.format(subj_id),delim=',',dataOut='all_raw')
    os.chdir(subjdir)
    trials.saveAsWideText(fileName)
    os.chdir(expdir)
    if globalClock.getTime() < 850:
        endTime = (850 - globalClock.getTime())
    else:
        endTime = 10
        core.wait(endTime)
        print globalClock.getTime()

do_run(trial_data,1)

#final ITI
fixation.draw()
win.flip()
core.wait(10)

# Exit
exit_screen.draw()
win.flip()
event.waitKeys(keyList=('space'))
