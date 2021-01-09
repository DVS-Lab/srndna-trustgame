#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.85.4),
    on April 13, 2018, at 15:41
If you publish work using this script please cite the PsychoPy publications:
    Peirce, JW (2007) PsychoPy - Psychophysics software in Python.2
        Journal of Neuroscience Methods, 162(1-2), 8-13.
    Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy.
        Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import absolute_import, division
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

# Store info about the experiment session
expName = 'Investment Game Ratings'  # from the Builder filename that created this script
expInfo = {'participant':'', 'session (change this accordingly; 1, 2)':''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=u'C:\\Users\\Jojo\\Downloads\\Psychopy\\set1_1.psyexp',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(
    size=(1280, 720), fullscr=True, screen=1,
    allowGUI=True, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True)
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# Initialize components for Routine "trust1"
trust1Clock = core.Clock()
q1 = visual.RatingScale(win=win, name='q1', marker='triangle', size=1.5, pos=[0.0, -0.55], low=0, high=100, leftKeys='1', rightKeys='3', acceptKeys='2', markerStart='5', scale='')
q1_ = visual.TextStim(win=win, name='q1_',
    text='How trustworthy do you feel this person is?',
    font='Arial',
    pos=(0,-0.1), height=0.1, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0);
image = visual.ImageStim(
    win=win, name='image',
    image='sin', mask=None,
    ori=0, pos=(0, 0.5), size=(0.4, 0.7),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)
not_trustworthy = visual.TextStim(win=win, name='not_trustworthy',
    text='Not at all',
    font='Arial',
    pos=(-0.45, -0.4), height=0.07, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-3.0);
neutral = visual.TextStim(win=win, name='neutral',
    text='Neutral',
    font='Arial',
    pos=(0, -0.4), height=0.07, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-4.0);
trustworthy = visual.TextStim(win=win, name='trustworthy',
    text='Very',
    font='Arial',
    pos=(0.45, -0.4), height=0.07, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-5.0);

# Initialize components for Routine "likeable"
likeableClock = core.Clock()
q1_4 = visual.RatingScale(win=win, name='q1_4', marker='triangle', size=1.5, pos=[0.0, -0.55], low=0, high=100, leftKeys='1', rightKeys='3', acceptKeys='2', markerStart='5', scale='')
q1__2 = visual.TextStim(win=win, name='q1__2',
    text='How likeable do you feel this person is?',
    font='Arial',
    pos=(0,-0.1), height=0.1, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0);
image_2 = visual.ImageStim(
    win=win, name='image_2',
    image='sin', mask=None,
    ori=0, pos=(0, 0.5), size=(0.4, 0.7),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)
not_trustworthy_4 = visual.TextStim(win=win, name='not_trustworthy_4',
    text='Not at all',
    font='Arial',
    pos=(-0.45, -0.4), height=0.07, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-3.0);
neutral_4 = visual.TextStim(win=win, name='neutral_4',
    text='Neutral',
    font='Arial',
    pos=(0, -0.4), height=0.07, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-4.0);
trustworthy_4 = visual.TextStim(win=win, name='trustworthy_4',
    text='Very',
    font='Arial',
    pos=(0.45, -0.4), height=0.07, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-5.0);

# Initialize components for Routine "approachable"
approachableClock = core.Clock()
q1_5 = visual.RatingScale(win=win, name='q1_5', marker='triangle', size=1.5, pos=[0.0, -0.55], low=0, high=100, leftKeys='1', rightKeys='3', acceptKeys='2', markerStart='5', scale='')
q1__3 = visual.TextStim(win=win, name='q1__3',
    text='How approachable do you feel this person is?',
    font='Arial',
    pos=(0,-0.1), height=0.1, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0);
image_3 = visual.ImageStim(
    win=win, name='image_3',
    image='sin', mask=None,
    ori=0, pos=(0, 0.5), size=(0.4, 0.7),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)
not_trustworthy_5 = visual.TextStim(win=win, name='not_trustworthy_5',
    text='Not at all',
    font='Arial',
    pos=(-0.45, -0.4), height=0.07, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-3.0);
neutral_5 = visual.TextStim(win=win, name='neutral_5',
    text='Neutral',
    font='Arial',
    pos=(0, -0.4), height=0.07, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-4.0);
trustworthy_5 = visual.TextStim(win=win, name='trustworthy_5',
    text='Very',
    font='Arial',
    pos=(0.45, -0.4), height=0.07, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=-5.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine

# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=1, method='sequential',
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('Trust.csv'),
    seed=None, name='trials')
thisExp.addLoop(trials)  # add the loop to the experiment
thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
if thisTrial != None:
    for paramName in thisTrial.keys():
        exec(paramName + '= thisTrial.' + paramName)

for thisTrial in trials:
    currentLoop = trials
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial.keys():
            exec(paramName + '= thisTrial.' + paramName)

    # ------Prepare to start Routine "trust1"-------
    t = 0
    trust1Clock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    q1.reset()
    image.setImage(trust)
    # keep track of which components have finished
    trust1Components = [q1, q1_, image, not_trustworthy, neutral, trustworthy]
    for thisComponent in trust1Components:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # -------Start Routine "trust1"-------
    while continueRoutine:
        # get current time
        t = trust1Clock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # *q1* updates
        if t >= 0.0 and q1.status == NOT_STARTED:
            # keep track of start time/frame for later
            q1.tStart = t
            q1.frameNStart = frameN  # exact frame index
            q1.setAutoDraw(True)
        continueRoutine &= q1.noResponse  # a response ends the trial

        # *q1_* updates
        if t >= 0.0 and q1_.status == NOT_STARTED:
            # keep track of start time/frame for later
            q1_.tStart = t
            q1_.frameNStart = frameN  # exact frame index
            q1_.setAutoDraw(True)

        # *image* updates
        if t >= 0.0 and image.status == NOT_STARTED:
            # keep track of start time/frame for later
            image.tStart = t
            image.frameNStart = frameN  # exact frame index
            image.setAutoDraw(True)

        # *not_trustworthy* updates
        if t >= 0.0 and not_trustworthy.status == NOT_STARTED:
            # keep track of start time/frame for later
            not_trustworthy.tStart = t
            not_trustworthy.frameNStart = frameN  # exact frame index
            not_trustworthy.setAutoDraw(True)

        # *neutral* updates
        if t >= 0.0 and neutral.status == NOT_STARTED:
            # keep track of start time/frame for later
            neutral.tStart = t
            neutral.frameNStart = frameN  # exact frame index
            neutral.setAutoDraw(True)

        # *trustworthy* updates
        if t >= 0.0 and trustworthy.status == NOT_STARTED:
            # keep track of start time/frame for later
            trustworthy.tStart = t
            trustworthy.frameNStart = frameN  # exact frame index
            trustworthy.setAutoDraw(True)

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in trust1Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "trust1"-------
    for thisComponent in trust1Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store data for trials (TrialHandler)
    trials.addData('q1.response', q1.getRating())
    trials.addData('q1.rt', q1.getRT())
    # the Routine "trust1" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()

# completed 1 repeats of 'trials'


# set up handler to look after randomisation of conditions etc
trials_2 = data.TrialHandler(nReps=1, method='sequential',
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('Trust.csv'),
    seed=None, name='trials_2')
thisExp.addLoop(trials_2)  # add the loop to the experiment
thisTrial_2 = trials_2.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTrial_2.rgb)
if thisTrial_2 != None:
    for paramName in thisTrial_2.keys():
        exec(paramName + '= thisTrial_2.' + paramName)

for thisTrial_2 in trials_2:
    currentLoop = trials_2
    # abbreviate parameter names if possible (e.g. rgb = thisTrial_2.rgb)
    if thisTrial_2 != None:
        for paramName in thisTrial_2.keys():
            exec(paramName + '= thisTrial_2.' + paramName)

    # ------Prepare to start Routine "likeable"-------
    t = 0
    likeableClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    q1_4.reset()
    image_2.setImage(likeable)
    # keep track of which components have finished
    likeableComponents = [q1_4, q1__2, image_2, not_trustworthy_4, neutral_4, trustworthy_4]
    for thisComponent in likeableComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # -------Start Routine "likeable"-------
    while continueRoutine:
        # get current time
        t = likeableClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # *q1_4* updates
        if t >= 0.0 and q1_4.status == NOT_STARTED:
            # keep track of start time/frame for later
            q1_4.tStart = t
            q1_4.frameNStart = frameN  # exact frame index
            q1_4.setAutoDraw(True)
        continueRoutine &= q1_4.noResponse  # a response ends the trial

        # *q1__2* updates
        if t >= 0.0 and q1__2.status == NOT_STARTED:
            # keep track of start time/frame for later
            q1__2.tStart = t
            q1__2.frameNStart = frameN  # exact frame index
            q1__2.setAutoDraw(True)

        # *image_2* updates
        if t >= 0.0 and image_2.status == NOT_STARTED:
            # keep track of start time/frame for later
            image_2.tStart = t
            image_2.frameNStart = frameN  # exact frame index
            image_2.setAutoDraw(True)

        # *not_trustworthy_4* updates
        if t >= 0.0 and not_trustworthy_4.status == NOT_STARTED:
            # keep track of start time/frame for later
            not_trustworthy_4.tStart = t
            not_trustworthy_4.frameNStart = frameN  # exact frame index
            not_trustworthy_4.setAutoDraw(True)

        # *neutral_4* updates
        if t >= 0.0 and neutral_4.status == NOT_STARTED:
            # keep track of start time/frame for later
            neutral_4.tStart = t
            neutral_4.frameNStart = frameN  # exact frame index
            neutral_4.setAutoDraw(True)

        # *trustworthy_4* updates
        if t >= 0.0 and trustworthy_4.status == NOT_STARTED:
            # keep track of start time/frame for later
            trustworthy_4.tStart = t
            trustworthy_4.frameNStart = frameN  # exact frame index
            trustworthy_4.setAutoDraw(True)

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in likeableComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "likeable"-------
    for thisComponent in likeableComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store data for trials_2 (TrialHandler)
    trials_2.addData('q1_4.response', q1_4.getRating())
    trials_2.addData('q1_4.rt', q1_4.getRT())
    # the Routine "likeable" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()

# completed 1 repeats of 'trials_2'


# set up handler to look after randomisation of conditions etc
trials_3 = data.TrialHandler(nReps=1, method='sequential',
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('Trust.csv'),
    seed=None, name='trials_3')
thisExp.addLoop(trials_3)  # add the loop to the experiment
thisTrial_3 = trials_3.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTrial_3.rgb)
if thisTrial_3 != None:
    for paramName in thisTrial_3.keys():
        exec(paramName + '= thisTrial_3.' + paramName)

for thisTrial_3 in trials_3:
    currentLoop = trials_3
    # abbreviate parameter names if possible (e.g. rgb = thisTrial_3.rgb)
    if thisTrial_3 != None:
        for paramName in thisTrial_3.keys():
            exec(paramName + '= thisTrial_3.' + paramName)

    # ------Prepare to start Routine "approachable"-------
    t = 0
    approachableClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    q1_5.reset()
    image_3.setImage(approach)
    # keep track of which components have finished
    approachableComponents = [q1_5, q1__3, image_3, not_trustworthy_5, neutral_5, trustworthy_5]
    for thisComponent in approachableComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # -------Start Routine "approachable"-------
    while continueRoutine:
        # get current time
        t = approachableClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # *q1_5* updates
        if t >= 0.0 and q1_5.status == NOT_STARTED:
            # keep track of start time/frame for later
            q1_5.tStart = t
            q1_5.frameNStart = frameN  # exact frame index
            q1_5.setAutoDraw(True)
        continueRoutine &= q1_5.noResponse  # a response ends the trial

        # *q1__3* updates
        if t >= 0.0 and q1__3.status == NOT_STARTED:
            # keep track of start time/frame for later
            q1__3.tStart = t
            q1__3.frameNStart = frameN  # exact frame index
            q1__3.setAutoDraw(True)

        # *image_3* updates
        if t >= 0.0 and image_3.status == NOT_STARTED:
            # keep track of start time/frame for later
            image_3.tStart = t
            image_3.frameNStart = frameN  # exact frame index
            image_3.setAutoDraw(True)

        # *not_trustworthy_5* updates
        if t >= 0.0 and not_trustworthy_5.status == NOT_STARTED:
            # keep track of start time/frame for later
            not_trustworthy_5.tStart = t
            not_trustworthy_5.frameNStart = frameN  # exact frame index
            not_trustworthy_5.setAutoDraw(True)

        # *neutral_5* updates
        if t >= 0.0 and neutral_5.status == NOT_STARTED:
            # keep track of start time/frame for later
            neutral_5.tStart = t
            neutral_5.frameNStart = frameN  # exact frame index
            neutral_5.setAutoDraw(True)

        # *trustworthy_5* updates
        if t >= 0.0 and trustworthy_5.status == NOT_STARTED:
            # keep track of start time/frame for later
            trustworthy_5.tStart = t
            trustworthy_5.frameNStart = frameN  # exact frame index
            trustworthy_5.setAutoDraw(True)

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in approachableComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "approachable"-------
    for thisComponent in approachableComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store data for trials_3 (TrialHandler)
    trials_3.addData('q1_5.response', q1_5.getRating())
    trials_3.addData('q1_5.rt', q1_5.getRT())
    # the Routine "approachable" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()

# completed 1 repeats of 'trials_3'

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
