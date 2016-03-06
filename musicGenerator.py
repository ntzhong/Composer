import pygame
import time
import pygame.midi

#initiate
pygame.midi.init()
player = pygame.midi.Output(0)
player.set_instrument(48, 1)

#Set dynamic values
#PP =
#p
#MP = 
#N =
#MF =
#F =
#FF =

#TO ADJUST:
ROOT = 48
BPM = 90
TIME_SIGNATURE = 4 #will not do compound. all in 4
NUM_MEASURES = 16
MAJORKEY = True
#DYNAMIC = N #start dynamic. not static. will change over piece

#set range of notes
minRange = 0 #A0 = 21, lowest on piano
maxRange = 108 #C8 = 108, highest on piano


#change octave values here
OCTAVE = 0
octInc = OCTAVE * 12


OCTAVE_SIZE = 12
C4 = 48

#Associate midi values
tonic = 0 #+ octInc
second = 2 #+ octInc
minThird 3 #+ octInc
majThird = 4 #+ octInc
fourth = 5 #+ octInc
fifth = 7 #+ octInc
minSixth = 8 #+ octInc
majSixth = 9 #+ octInc
minSev = 10 #+ octInc
majSev = 11 #+ octInc


#scales
majScale = [tonic, second, majThird, fourth, fifth, majSixth, majSev, tonic+OCTAVE_SIZE]
minScale = [tonic, second, minThird, fourth, fifth, minSixth, minSev, tonic+OCTAVE_SIZE]

#construct basic chords based off of root.
def constructMajTriad(root):
	return [root, root+majThird, root+fifth]

def constructMinTriad(root):
	return [root, root+minThird, root+fifth]

#takes in an array of notes and returns a chord
def invChord(triad):


#inversions?

#generates and plays harmony+melody
def play(root=ROOT, major=MAJORKEY, measures=NUM_MEASURES, timeSig=TIME_SIGNAURE, bpm=BPM):
	melody = constructMelody()
	harmony = constructHarmony()

def constructHarmony(root=ROOT, major=MAJORKEY, measures=NUM_MEASURES, timeSig=TIME_SIGNAURE, bpm=BPM):
	#if chord progressions are similar, then just swap scales
	#curScale = majScale/minScale
	#construct Harmony based on major scale
	if major:

	#construct harmony based on minor scale
	else:

def constructMelody(root=ROOT, major=MAJORKEY, measures=NUM_MEASURES, timeSig=TIME_SIGNAURE, bpm=BPM):
	#construct Melody based on major scale
	if major==1:

	#construct harmony based on minor scale
	else:



#the backend

#Returns the amount of ms to alot per beat. input allowed incase of differing bpm
def getMsPerBeat(bpm=BPM):
	msPerMin = 60000
	msPerBeat = msPerMin/bpm
	return msPerBeat


#EX of playing note
#def go(note):
    #player.note_on(note, 127,1)
    #time.sleep(1)
    #player.note_off(note,127,1)