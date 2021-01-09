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
initial_fixation_dur = 4
#final_fixation_dur = 2
decision_dur=3
#outcome_dur=0.25
fileSuffix = 'UG'

responseKeys=('2','3','z')

#get subjID
subjDlg=gui.Dlg(title="Bargaining Task")
subjDlg.addField('Enter Subject ID: ') #0
subjDlg.addField('Enter Gender (0 for male, 1 for female): ') #1
subjDlg.addField('Enter Ethnicity (0 for Caucasian, 1 for Other): ') #2
subjDlg.addField('Enter Age: ') #3
subjDlg.addField('Full Screen? (Enter lowercase: y or n):') #4
subjDlg.show()

if gui.OK:
    subj_id=subjDlg.data[0]
    subj_gen=subjDlg.data[1]
    subj_eth=subjDlg.data[2]
    subj_age=subjDlg.data[3]
else:
    sys.exit()

run_data = {
    'Participant ID': subj_id,
    'Date': str(datetime.datetime.now()),
    'Description': 'SRNDNA Pilot - UG Task',
    'Participant Gender': subj_gen,
    'Participant Ethnicity': subj_eth,
    'Participant Age': subj_age
    }

#window setup
win = visual.Window([800,600], monitor="testMonitor", units="deg", fullscr=useFullScreen, allowGUI=False, screen=useDualScreen)

#checkpoint
print "got to check 1"

#define fixation
fixation = visual.TextStim(win, text="+", height=2)

#waiting for trigger
ready_screen = visual.TextStim(win, text="Please wait for Lets Make a Deal to begin! \n\nRemember to keep your head still!", height=1.5)


#decision screen
pictureStim =  visual.ImageStim(win, pos=(0,3.5),size=(6.65,6.65))
resp_text_reject = visual.TextStim(win,text="Reject Offer", pos =(-7,-4.8), height=1, alignHoriz="center")
resp_text_accept = visual.TextStim(win,text="Accept Offer", pos =(7,-4.8), height=1, alignHoriz="center")
offer_text = visual.TextStim(win,pos = (0,-1.5),alignHoriz="center", text='')

#outcome screen
outcome_stim = visual.TextStim(win, pos = (0,-2.5),text='')

#instructions
instruct_screen = visual.TextStim(win, text='Welcome to Lets Make a Deal!\n\nIn this task you will interacting with a few different partners.\n\nOn every trial, your partner will have $20, which s/he can propose to divide in any way between the two of you.\n\nYour task is to choose to either accept or reject the proposed split of money.', pos = (0,1), wrapWidth=20, height = 1.2)
instruct_screen2 = visual.TextStim(win, text='Press Button 2 to reject the offer. Press Button 3 to accept the offer.\n\nIf you choose to reject the offer, you and your partner will both receive $0 for that trial.', pos = (0,1), wrapWidth=20, height = 1.2)

#exit
exit_screen = visual.TextStim(win, text='Thanks for playing! Please wait for instructions from the experimenter.', pos = (0,1), wrapWidth=20, height = 1.2)

#logging
expdir = os.getcwd()
subjdir = '%s/logs/%s' % (expdir, subj_id)
if not os.path.exists(subjdir):
    os.makedirs(subjdir)
log_file = os.path.join(subjdir,'sub-{}_task-ultimatum_run-{}_raw.csv')


globalClock = core.Clock()
logging.setDefaultClock(globalClock)

timer = core.Clock()

#trial handler
trial_data_1 = [r for r in csv.DictReader(open('params/UG_blocks/sub-' + subj_id + '/sub-'+ subj_id + '_run-01_design.csv','rU'))]
trial_data_2  = [r for r in csv.DictReader(open('params/UG_blocks/sub-' + subj_id + '/sub-'+ subj_id + '_run-02_design.csv','rU'))]

trials_run1 = data.TrialHandler(trial_data_1[:], 1, method="sequential") #change to [] for full run
trials_run2 = data.TrialHandler(trial_data_2[:], 1, method="sequential") #change to [] for full run


subj_gen = int(subj_gen)
subj_eth = int(subj_eth)
subj_age = int(subj_age)

if subj_gen==0 and subj_eth==0 and subj_age > 35:
    stim_map = {
    '3': 'olderadultMale_C',
    '2': 'youngadultMale_C',
    '1': 'computer',
    }

elif subj_gen==0 and subj_eth==0 and subj_age <= 35:
    stim_map = {
    '3': 'youngadultMale_C',
    '2': 'olderadultMale_C',
    '1': 'computer',
    }

elif subj_gen==0 and subj_eth==1 and subj_age > 35:
    stim_map = {
    '3': 'olderadultMale_M',
    '2': 'youngadultMale_M',
    '1': 'computer',
    }

elif subj_gen==0 and subj_eth==1 and subj_age <= 35:
    stim_map = {
    '3': 'youngadultMale_M',
    '2': 'olderadultMale_M',
    '1': 'computer',
    }

elif subj_gen==1 and subj_eth==0 and subj_age > 35:
    stim_map = {
    '3': 'olderadultFemale_C',
    '2': 'youngadultFemale_C',
    '1': 'computer',
    }
elif subj_gen==1 and subj_eth==0 and subj_age <= 35:
    stim_map = {
    '3': 'youngadultFemale_C',
    '2': 'olderadultFemale_C',
    '1': 'computer',
    }
elif subj_gen==1 and subj_eth==1 and subj_age > 35:
    stim_map = {
    '3': 'olderadultFemale_M',
    '2': 'youngadultFemale_M',
    '1': 'computer',
    }
elif subj_gen==1 and subj_eth==1 and subj_age <= 35:
    stim_map = {
    '3': 'youngadultFemale_M',
    '2': 'olderadultFemale_M',
    '1': 'computer',
    }

outcome_map = {
  #3: 'You have accepted the offer.\n\nYou: $%s.00\nPartner: $%s.00',
  #2: 'You have rejected the offer.\n\nYou: $0.00\nPartner: $0.00',
  999: 'You have 3 seconds to respond.'
  }

#checkpoint
print "got to check 2"

# main task loop
# Instructions
instruct_screen.draw()
win.flip()
event.waitKeys(keyList=('space'))

instruct_screen2.draw()
win.flip()
event.waitKeys(keyList=('space'))


def do_run(run, trials):
    resp=[]
    fileName=log_file.format(subj_id,run)

    #wait for trigger
    ready_screen.draw()
    win.flip()
    event.waitKeys(keyList=('equal'))
    globalClock.reset()
    studyStart = globalClock.getTime()

    #Initial Fixation screen
    fixation.draw()
    win.flip()
    core.wait(initial_fixation_dur)

    for trial in trials:
        condition_label = stim_map[trial['Partner']]
        imagepath = os.path.join(expdir,'Images')
        image = os.path.join(imagepath, "%s.png") % condition_label
        pictureStim.setImage(image)

        #decision phase
        timer.reset()
        event.clearEvents()

        decision_onset = globalClock.getTime()
        trials.addData('decision_onset', decision_onset)

        #while timer.getTime() < decision_dur:
        while timer.getTime() < 1:
            partner_offer = trial['Offer']
            partnerOffer = 'Proposal: $%s.00 out of $20.00' % partner_offer
            offer_text.setText(partnerOffer)
            offer_text.draw()
            offer_text.draw()
            pictureStim.draw()
            win.flip()

        resp_val=None
        resp_onset=None

        while timer.getTime() < (decision_dur):
            resp_text_accept.draw()
            resp_text_reject.draw()
            pictureStim.draw()
            offer_text.setText(partnerOffer)
            offer_text.draw()
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
                rt = resp_onset - decision_onset
                if resp_val == 2:
                    resp_text_reject.setColor('darkorange')
                if resp_val == 3:
                    resp_text_accept.setColor('darkorange')
                resp_text_accept.draw()
                resp_text_reject.draw()
                pictureStim.draw()
                offer_text.setText(partnerOffer)
                offer_text.draw()
                win.flip()
                core.wait((decision_dur - rt)+.5)
                decision_offset = globalClock.getTime()
                break
            else:
                resp_val = 999
                rt = 999
                resp_onset = 999
                outcome_txt = outcome_map[resp_val]
                decision_offset = globalClock.getTime()

        trials.addData('resp', resp_val)
        trials.addData('rt',rt)
        trials.addData('resp_onset',resp_onset)
        trials.addData('decision_offset',decision_offset)
                #win.flip()

        timer.reset()
        if resp_val == 999:
            outcome_stim.setText(outcome_txt)
            outcome_stim.draw()
            win.flip()
            missFB_onset = globalClock.getTime()
            core.wait(.5)
            missFB_offset = globalClock.getTime()



        #reset rating number color
        resp_text_accept.setColor('#FFFFFF')
        resp_text_reject.setColor('#FFFFFF')

        trial_offset = globalClock.getTime()
        duration = trial_offset - decision_onset
        trials.addData('trialDuration', duration)
        event.clearEvents()
        print "got to check 3"

        #ITI
        logging.log(level=logging.DATA, msg='ITI') #send fixation log event
        timer.reset()
        ITI_onset = globalClock.getTime()
        iti_for_trial = float(trial['ITI'])
        fixation.draw()
        win.flip()
        core.wait(iti_for_trial)
        ITI_offset = globalClock.getTime()

        trials.addData('ITIonset', ITI_onset)
        trials.addData('ITIoffset', ITI_offset)


    # Final Fixation screen after trials completed
    fixation.draw()
    win.flip()
    #core.wait(final_fixation_dur)
    os.chdir(subjdir)
    trials.saveAsWideText(fileName)
    os.chdir(expdir)
    endTime = 0.01 # not sure if this will take a 0, so giving it 0.01 and making sure it is defined
    expected_dur = 398
    buffer_dur = 10
    total_dur = expected_dur + buffer_dur
    if globalClock.getTime() < total_dur:
        endTime = (total_dur - globalClock.getTime())
    else:
        endTime = buffer_dur
    core.wait(endTime)
    print globalClock.getTime()

for run, trials in enumerate([trials_run1, trials_run2]):
    do_run(run, trials)

# Exit
exit_screen.draw()
win.flip()
event.waitKeys(keyList=('space'))
