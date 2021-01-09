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
outcome_dur=.75
fileSuffix = 'UG'

responseKeys=('1','2')

#get subjID
subjDlg=gui.Dlg(title="Bargaining Task")
subjDlg.addField('Enter Subject ID: ')
subjDlg.show()

if gui.OK:
    subj_id=subjDlg.data[0]
else:
    sys.exit()

run_data = {
    'Participant ID': subj_id,
    'Date': str(datetime.datetime.now()),
    'Description': 'SRNDNA Pilot - UG Task'
    }

#window setup
win = visual.Window([800,600], monitor="testMonitor", units="deg", fullscr=useFullScreen, allowGUI=False, screen=useDualScreen)

#checkpoint
print "got to check 1"

#define fixation
fixation = visual.TextStim(win, text="+", height=2)

#waiting for trigger
ready_screen = visual.TextStim(win, text="Ready? \n\nPlease remember to keep your head still!", height=1.5)


#decision screen
pictureStim =  visual.ImageStim(win, pos=(0,3.5))
resp_text_reject = visual.TextStim(win,text="Reject Offer", pos =(-7,-4.8), height=1, alignHoriz="center")
resp_text_accept = visual.TextStim(win,text="Accept Offer", pos =(7,-4.8), height=1, alignHoriz="center")
offer_text = visual.TextStim(win,pos = (0,-1.5),alignHoriz="center", text='')

#outcome screen
outcome_stim = visual.TextStim(win, pos = (0,-2.5),text='')

#instructions
instruct_screen = visual.TextStim(win, text='Welcome to the bargaining game.\n\nIn this task you will interacting with a few different partners.\n\nOn every trial, your partner will have $20, which s/he can propose to divide in any way between the two of you.\n\nYour task is to choose to either accept or reject the proposed split of money.\n\nPress spacebar to continue', pos = (0,1), wrapWidth=20, height = 1.2)
instruct_screen2 = visual.TextStim(win, text='Press Button 1 to accept the offer. Press Button 2 to reject the offer.\n\nIf you choose to reject the offer, you and your partner will both receive $0 for that trial.', pos = (0,1), wrapWidth=20, height = 1.2)

#exit 
exit_screen = visual.TextStim(win, text='Thanks for playing! Please wait for instructions from the experimenter.', pos = (0,1), wrapWidth=20, height = 1.2)

#logging
log_file = os.path.join(maindir,'{}_run_{}.csv')

globalClock = core.Clock()
logging.setDefaultClock(globalClock)

timer = core.Clock()

#trial handler
trial_data = [r for r in csv.DictReader(open('UG_design_test2DF.csv','rU'))]
trials = data.TrialHandler(trial_data[:8], 1, method="sequential") #change to [] for full run

stim_map = {
  '3': 'olderadult',
  '2': 'youngeradult',
  '1': 'computer',
  }

outcome_map = {
  2: 'You have chosen to accept the offer.\n\nYou: $%s.00\nPartner: $%s.00',
  1: 'You have chosen to reject the offer.\n\nYou: $0.00\nPartner: $0.00',
  None: 'You have two seconds to choose.'
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
event.waitKeys()

instruct_screen2.draw()
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
        image = "Images/%s.png" % condition_label
        pictureStim.setImage(image)
        print 'image'
        
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
            resp_text_accept.draw()
            resp_text_reject.draw()
            pictureStim.draw()
            
            partner_offer = trial['Offer']
            partnerOffer = 'Your partner has offered you $%s.00 out of $20.00' % partner_offer
            offer_text.setText(partnerOffer)
            offer_text.draw()
            win.flip()
           
            resp = event.getKeys(keyList = responseKeys)
    
            if len(resp)>0:
                resp_val = float(resp[0])
                resp_onset = globalClock.getTime()
                if resp_val == 1:
                    resp_text_reject.setColor('red')
                if resp_val == 2:
                    resp_text_accept.setColor('red')
                trials.addData('resp', resp_val)
                trials.addData('resp_onset', resp_onset)


        trials.addData('decision_onset', decision_onset)
        trials.addData('ITIonset', ITI_onset)
        
        #reset rating number color
        resp_text_accept.setColor('#FFFFFF')
        resp_text_reject.setColor('#FFFFFF')
        
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
            pictureStim.draw()
            #win.flip()
            subjectReceives = trial['Offer']
            partnerKeeps = trial['PartnerKeeps']
            if resp_val == 2:
                outcome_txt = outcome_map[resp_val] % (subjectReceives, partnerKeeps)
            elif resp_val==1:
                outcome_txt = outcome_map[resp_val]
            else:
                outcome_txt = outcome_map[resp_val]
            
            outcome_stim.setText(outcome_txt)
            outcome_stim.draw()
            #trials.addData('outcome_txt', outcome_txt)
            trials.addData('outcome_onset', outcome_onset)
            win.flip()
            core.wait(.75)
            outcome_offset = globalClock.getTime()
            trials.addData('outcome_offset', outcome_offset)
            
            
            duration = outcome_offset - decision_onset
            trials.addData('trialDuration', duration)
            event.clearEvents()
        print "got to check 3"

    trials.saveAsText(fileName=log_file.format('UG_'+ subj_id, run_num),delim = ',', dataOut='all_raw')
do_run(trial_data,1)

#final ITI
fixation.draw()
win.flip()
core.wait(12)

# Exit
exit_screen.draw()
win.flip()
event.waitKeys()
