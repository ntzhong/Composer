#Compose
from midiutil.MidiFile import MIDIFile
from random import randint

#VALUES TO ADJUST
COMPOSE_SEPARATELY = False #chooses to construct parts indepndently
BPM = 90 #BPM
CHORDS_PER_MEASURE = 1 #standard is 1 or 2
PHRASE_LENGTH = 4 #in measures
SONG_LENGTH = PHRASE_LENGTH * 4 + 1 #in measures. +1 for resolution measure?
ROOT = 60 #Set tonic to middle C
TIME_SIGNATURE = 4 #no compound meter. in beats per measure
MAJORKEY = True #false => minor
NUM_TRACKS = 2 #number of tracks. only 1 or 2 for now.

#set range of notes
minRange = 21 #A0 = 21, lowest on piano
maxRange = 108 #C8 = 108, highest on piano


#for octave changing (will need to modify to fit needs)
OCTAVE = 0

#INIT STANDARD VALUES
OCTAVE_SIZE = 12
octLocation = OCTAVE * OCTAVE_SIZE
C4 = 48


#Set dynamic values from 0-127
PP = 35
P = 50
MP = 65
N = 80 #standard
MF = 95
F = 110
FF = 125

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


time = 0 #in beats. Location in song. must increment

#scale construction
majScale = [tonic, second, majThird, fourth, fifth, majSixth, majSev, tonic+OCTAVE_SIZE]
minScale = [tonic, second, minThird, fourth, fifth, minSixth, minSev, tonic+OCTAVE_SIZE]

#establish rhythms. 1 = 1 beat
durations = [0.25, 0.5, 0.75, 1, 1.5, 2, 3, 3.5, 4]







#takes in a MIDI value. returns 3-elem array of midi values
#quality = "min" or "maj"
def constructTriad(root, quality = "maj"):
	if quality = "maj":
		return constructMajTriad(root)
	else:
		return constructMinTriad(root)


def constructMajTriad(root):
	return [root, root+majThird, root+fifth]

def constructMinTriad(root):
	return [root, root+minThird, root+fifth]
 

#takes in an array of notes and returns a random inversion (root, 1st, 2nd)
def invChordRand(triad):
	value = randint(0, 15) #0-10 inclusive
	if value < 4:
		return triad
	elif value < 8: 
		return inv(triad, 1)
	elif value < 12:
		return inv(triad, 2) 
	else: #between [12,15]
		if len(triad) < 4:
			return triad
		else:
			return inv(triad, 3)


#returns nth inversion of chord
def inv(triad, n):
	for i in range(0, inversion): #[0,2), so run 2 times
		root = triad.pop(0)
		triad.append(root)
	return root


#return true if curBeat lies within beat. e.g. if 2.5 beats left, then in 2nd beat. beat is a hole number. curBeat is float.
def withinBeat(curBeat, beat):
	return (curBeat >= beat) and (curBeat < beat+1)

#returns true if min <= value < max. i.e. [min, max)
def isBetween(value, minV, maxV):
	return (minV <= value) and (value < maxV) 


#0 = normal
#1 = lengthy and emotional
#2 = short, upbeat, fast, happy

#determines the rhythm for a measure (or phrase?) maybe an array of measure arrays?
#in comments, swing refers to .75, .25 beats in conjunction
#rest determined later (randomly turn notes on/off). Or can intentionally place them here, w/ duration=-1
def determineMelodicRhythm(quality):
	phrases_in_song = (SONG_LENGTH-1) / 
	rhythm = []
	for phrase in range(0, phrases_in_song): #per phrase
		for measureNum in range(0, PHRASE_LENGTH): #per measure
			measure = []
			curBeat = 0 #measure= 0,1,2,3
			duration = 0
			duration2 = 0 #potential successive note
			duration3 = 0

			#determine rhythm of the measure with probability. Depends on location in phrase, possibly also on value of beatsLeft
			while curBeat < TIME_SIGNATURE: #per beat
				randVal = randint(0,20)

				#Determine next rhythm, note by note

				#arbitarily chosen style standard
				if quality == 0:
					#for end of the phrase, but not the song
					if (measureNum = PHRASE_LENGTH-1):
						#1st beat: extremely high chance of whole note. Chances: whole note > eigth > quarter > half > swing.
						#does not end on upbeat
						if (curBeat == 0):
							if isBetween(randVal, 0, 4): #whole
								duration = 4
							elif isBetween(randVal, 4, 10): #eighth
								duration = 0.5
								duration2 = 0.5
							elif isBetween(randVal, 10, 15): #quarter
								duration = 1
								duration2 = 2
							elif isBetween(randVal, 15, 18): #dotted half
								duration = 3
							else: #swing into end
								duration = 0.75
								duration2 = 0.25
								duration3 = 2
						elif (curBeat == 3): #4th beat. chance of 2 or 1 or no eigth-notes.
							if isBetween(randVal, 0, 10):
								duration = 0.5
								duration2 = 0.5
							else:
								print measure
								measure[len(measure-1)] += 0.5 #increase previous note's duration by 0.5.
								curBeat += 0.5 #update to reflect forced change
								duration = 0.5
								print measure
						else:
							remaining_beats = TIME_SIGNATURE - 1 - curBeat
							options = [0.5, 1, 2, 2] #higher chance of half-note if it is in 2nd beat
							duration = options[randint(0, len(options))]
							while duration > remaining_beats:
								duration = options[randint(0, len(options))]


					#for everything else, sample psuedo-randomly. swing notes only allowed in set?
					else:
						remaining_beats = TIME_SIGNATURE - 1 - curBeat
						options = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 1, 1, 1.5, 1.5, 2, 3] #probability distribution
						duration = options[randint(0, len(options))]
						while duration > remaining_beats:
							duration = options[randint(0, len(options))]

				#rhythm of next note decided
				measure.append(duration)
				if duration2 > 0:
					measure.append(duration2)
				if duration3 > 0:
					measure.append(duration3)
				curBeat += (duration + duration2 + duration3)

			#full measure established. log it
			rhythm.append(measure)
	#exit loop over phrases
	#construct resolution for final measure here. 
	measure = []
	measure.append(4) #JUST A PLACEHOLDER
	rhythm.append(measure)


#returns a chord progression for entirety of song. key_quality = "maj" or "min"
def constructChordProg(key_quality):
	#every chord gets equal amount of time, based on num chords per measure
	if key_quality == "maj":
		scale = majScale
	else:
		scale = minScale

	#Sets scale to octave range of root
	scale = [x+root for x in scale]
	phrases_in_song = (SONG_LENGTH-1)/PHRASE_LENGTH
	
	chordProgression[]
	for phrase in range(0, phrases_in_song):
		for measure in range(0,PHRASE_LENGTH):
			for chord in range(0, CHORDS_PER_MEASURE):

				randVal = randint(0, 20) #determines buckets for probabilities
				
				if (phrase > 0) and (measure == 0) and (chord == 0): #start of phrase, but not song. small chance of relative minor
					#80% tonic, 20% relative minor
					if randVal < 16:
						chordProgression.append(scale[0])
					else:
						chordProgression.append(scale[5])

				elif (phrase==0) and (measure == 0) and (chord == 0): #beginning of song
					chordProgression.append(scale[0]) #tonic, 100%

				elif (phrase == phrases_in_song-1) and (measure == PHRASE_LENGTH-1) and (chord == CHORDS_PER_MEASURE-1): #right before end of song
					#dominant = 100%
					chordProgression.append(scale[4])

				elif (measure == PHRASE_LENGTH-1): #end of phrase. high chance of dominant. can also be 4
					#dominant 85%
					#subDom = 10%

				else: #probability. depends on previous, and like 1% chance of being tonic.

	chordProgression.append(scale[0]) #Resolve w/ tonic
	return chordProgression

#this constructs melody+harmony simultaneously, so relations can be considered
	#(easier to decide pick-ups, exceptions, etc)
def compose(file):
	vol = N
	harmVol = vol-5
	if MAJORKEY:
		chordProg = constructChordProg("maj")
	else:
		chordProg = constructChordProg("min")


#takes in a MIDIFile object and constructs composition
#constructs two independent lines, to be combined at the end
def constructMelody(file):

def constructHarmony(file):


#MAIN
if __name__ == "__main__":
	main(sys.argv)

#Main function. Can decide to take arugments
def main(argv):
	#Def tracks
	track1 = 0 #melody
	track2 = 1 #harmony
	channel = 0 #0-15
	#create midi file w/ NUM_TRACKS tracks
	MyMIDI = MIDIFile(NUM_TRACKS)
	# Init track(s). Add track name and tempo.
	MyMIDI.addTrackName(track1,time,"Melody")
	if NUM_TRACKS == 2:
		MyMIDI.addTrackNAme(track2, time, "Harmony")
	MyMIDI.addTempo(track1,time,BPM)
	MyMIDI.addTempo(track2,time,BPM)
	if COMPOSE_SEPARATELY:
		constructMelody(MyMIDI)
		constructHarmony(MyMIDI)
	else:
		compose(MyMIDI)
	#write to disk
	binfile = open("out.mid", 'wb')
	MyMIDI.writeFile(binfile)
	binfile.close()

# Now add the note. 
MyMIDI.addNote(track,channel,pitch,time,duration,volume)
MyMIDI.addNote(track,channel,pitch,time+duration,duration,volume+5)
MyMIDI.addNote(track,channel,pitch,time+2*duration,duration,volume-25)
MyMIDI.addNote(track,channel,pitch,time+3*duration,duration,volume+25)





