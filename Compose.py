#Compose
from midiutil.MidiFile import MIDIFile
from random import randint

#VALUES TO ADJUST
COMPOSE_SEPARATELY = True #chooses to construct parts indepndently
BPM = 90 #BPM
CHORDS_PER_MEASURE = 1 #standard is 1 or 2
PHRASE_LENGTH = 4 #in measures
SONG_LENGTH = PHRASE_LENGTH * 4 + 1 #in measures. +1 for resolution measure?
ROOT = 60 #Set tonic to middle C
TIME_SIGNATURE = 4 #no compound meter. out of 4
MAJORKEY = True #false => minor
NUM_TRACKS = 2 #number of tracks

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
		if len(traid) < 4:
			return triad
		else:
			return inv(triad, 3)


#returns nth inversion of chord
def inv(triad, n):
	for i in range(0, inversion): #[0,2), so run 2 times
		root = triad.pop(0)
		triad.append(root)
	return root

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
				
				if (measure == 0) && (phrase > 0): #start of phrase, but not song. small chance of relative minor
					#90% tonic, 10% relative minor

				elif (measure == 0): #beginning of phrase:
					chordProgression.append(scale[0]) #tonic, 100%

				elif (measure == 3) && (phrase == phrases_in_song-1): #end of song
					#dominant = 100%
				elif (measure == 3): #end of phrase. high chance of dominant. can also be 4
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





