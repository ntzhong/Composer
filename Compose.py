#Compose
from midiutil.MidiFile import MIDIFile #external package. For linux users: sudo apt-get install python-midiutil
from random import randint

#VALUES TO ADJUST
COMPOSE_SEPARATELY = True #chooses to construct parts indepndently
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
#OCTAVE = 0

#INIT STANDARD VALUES
OCTAVE_SIZE = 12
octLocation = OCTAVE * OCTAVE_SIZE
C4 = 60


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
#durations = [0.25, 0.5, 0.75, 1, 1.5, 2, 3, 3.5, 4]



########################
##### MUSIC THEORY #####
########################

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

def constructMajMinSev(root):
	majTriad = constructMajTriad(root)
	return majTriad.append(root + minSev)

def constructMinSev(root):
	minTriad = constructMinTriad(root)
	return minTriad.append(root + minSev)

def constructMajSev(root):
	majTraid = constructMajTriad(root)
	return majTriad.append(root + majSev)

#takes in an array of notes and returns a random inversion (root, 1st, 2nd).
#chord can be any length, but max 4 inversions
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
	for i in range(0, n): #[0,2), so run 2 times
		root = triad.pop(0)
		triad.append(root)
	return root





#####################################
##### MATH AND HELPER FUNCTIONS #####
#####################################

#return true if curBeat lies within beat. e.g. if 2.5 beats left, then in 2nd beat. beat is a whole number. curBeat is float.
def withinBeat(curBeat, beat):
	return (curBeat >= beat) and (curBeat < beat+1)

#returns true if min <= value < max. i.e. [min, max)
def isBetween(value, minV, maxV):
	return (minV <= value) and (value < maxV) 

#shifts array by n to the left 
def shift(array, n):
	return array[n:] + array[:n]

#performs element-wise multiplication between 2 arrays
def multiplyElems(a, b):
	newArray = []
	for i in range(0, len(a)-1):
		newArray.append(a[i]*b[i])
	return newArray

#returns array of reciprocals
def invertArray(array):
	newArray = []
	for value in array:
		newArray.append(1/value)
	return newArray


#takes array of items, with an associated distribution array, and returns an item based on distribution
#note that distrubtion does not have to be normalized
def sampleFromDist(itemArray, distribution):
	#take cumulative sum
	cumDist = []
	total = 0
	i = 0
	for p in distribution:
		total += p
		cumDist[i] = total
		i += 1

	#sample	and compare probability buckets
	sample = random.randint(0, total)
	i = 0
	for cumP in cumDist:
		if (sample <= cumP):
			return itemArray[i]
		i += 1

	print("distribution selection error")





#################################
##### COMPOSITION FUNCTIONS #####
#################################

#0 = normal
#1 = lengthy and emotional
#2 = short, upbeat, fast, happy

#TO ADD: 2nd to last measure, high chance of eigth notes on last beat
#determines the rhythm for a measure (or phrase?) maybe an array of measure arrays?
#in comments, swing refers to .75, .25 beats in conjunction
#rest determined later (randomly turn notes on/off). Or can intentionally place them here, w/ duration=-1
def determineMelodicRhythm():
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
	measure = [TIME_SIGNATURE] #standard to end on last measure
	rhythm.append(measure)
	return rhythm

def determineHarmonicRhythm():
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
			while curBeat < TIME_SIGNATURE:
				if curBeat == 0: #first beat higher chance of eigths
					durs = [0.5, 1, 2]
					dist = [10, 3, 1]

				elif curBeat == 1:#2nd beat: higer chance of quarter
					durs = [0.5, 1]
					dist = [1, 1]
				
				elif curBeat.is_integer():
					durs = [0.5, 1, 2]#if downbeat: quarter or eigth
					dist = [10, 4/CHORDS_PER_MEASURE, 2]

				#if upbeat: high chance of eigth note
				else:
					durs = [0.5, 1]
					dist = [10, 2]

				duration = sampleFromDist(durs, dist)
				while duration+curBeat > TIME_SIGNATURE:
					duration = sampleFromDist(durs, dist)
				measure.append(duration)
				curBeat += duration

			rhythm.append(measure)
	#last note = whole note
	measure = [TIME_SIGNATURE]
	rhythm.append(measure)
	return rhythm



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
				#maybe create chance of separate branch, where harmony just walks down and back up
				randVal = randint(0, 20) #determines buckets for probabilities
				
				if (phrase + measure + chord == 0): #beginning of song
					chordProgression.append(scale[0]) #tonic, 100%

				elif (phrase == phrases_in_song-1) and (measure == PHRASE_LENGTH-1) and (chord == CHORDS_PER_MEASURE-1): #right before end of song
					#dominant = 100%
					chordProgression.append(scale[4])

				elif (phrase > 0) and (measure == 0) and (chord == 0): #start of phrase, but not song. small chance of relative minor
					#80% tonic, 20% relative minor
					notes = [scale[0], scale[5]]
					dist = [8, 2]
					sampleFromDist(notes, dist)

				elif (measure == PHRASE_LENGTH-1): #end of phrase. high chance of dominant. can also be 4
					#dominant 85%
					#subDom = 10%
					notes = [scale[3], scale[4]]
					dist = [1, 9]
					sampleFromDist(notes, dist)

				else: #probability. depends on previous, and like 1% chance of being tonic.
					options = [scale[0], scale[2], scale[3], scale[4], scale[5]]
					chordProgression.append(randint(0, len(options)))

	for i in range (0, CHORDS_PER_MEASURE):
		chordProgression.append(scale[0]) #Resolve final measure w/ tonic

	return chordProgression




#takes in a MIDIFile object and constructs composition
#constructs two independent lines, to be combined at the end, based on same chord progression
def constructMelody(file, chordProgression, track, channel):
	#melody starts at predefined normal vol
	vol = N
	rhythm = determineMelodicRhythm() #array of measures, each measure contains durations summing to TIME_SIGNATURE
	phrases_in_song = (SONG_LENGTH-1)/ PHRASE_LENGTH
	measureNum = 0
	beatNum = 0
	note = 0
	baseNote = ROOT
	lastNote = 0 #scale note
	chordNum = 0
	#intervals of chord changes. e.g 2 chords per measure at 4/4: new chord at beat 3
	chordDiv = TIME_SIGNATURE/CHORDS_PER_MEASURE
	chordScale = scale
	time = 0

	if MAJORKEY:
		scale = majScale
	else:
		scale = minScale
	
	for measure in rhythm:
		durationIndex = 0 #track which note in measure
		curChord = chordProgression[chordNum]
		for duration in measure:
			#MyMIDI.addNote(track,channel,pitch,time,duration,volume)
			if (measureNum + beatNum) == 0: #start of song excluding pickup
				#emphasis on 1, 3, 5
				dist = [10, 1, 8, 5, 9, 5, 5, 1]
				note = sampleFromDist(scale, dist)

			#2nd to last measure of song (where the dominant chord is)
			elif (measureNum == len(rhythm-1)):
				pass

			#start of phrase
			elif (measureNum%(PHRASE_LENGTH) == 0) and (beatNum == 0):
				dist = [10, 1, 8, 5, 9, 5, 5, 1]
				note = sampleFromDist(scale, dist)

			#last measure of phrase
			elif ((measureNum+1)%(PHRASE_LENGTH) == 0):
				pass

			#2nd to last note in song, force to be supertonic or leading
			elif (measureNum == SONG_LENGTH-1) and (durationIndex = len(duration)-1):
				notes = [scale[1], scale[6]] #supertonic or leading
				dist = [2, 1]
				note = sampleFromDist(notes, dist)
			
			#Last note in song. (remember extra appended measure)
			elif (measureNum == SONG_LENGTH) and (durationIndex == len(duration)-1) 
				note = scale[0] #w/ small chance of building a triad on this? so dominant

			else:
				#favor smaller intervals, with max interval being w/in octive of previous note
				#construct new set of notes based on chord, following root scale
				chordIndex = scale.index(chord)
				cs = shift(scale, chordIndex) #chordScale
				#downbeat of chord beginning (0, 3) (1,3,4-low,5, 6-low, 7-low)
				if (curBeat == 0) #first beat
					dist = [5, 2, 7, 4, 7, 5, 3, 0]
					note = sampleFromDist[cs, dist]
				elif curBeat.is_integer(): #all downbeats in general. #lower chance of tonic if not 1st note in measure
					dist = [2, 1, 2, 1, 3, 1, 1, 3]
					ntoe = sampleFromDist[cs, dist]

				#upbeats. Closer notes more likely to be played, especially if eigth notes
				else:
					dist = [3, 5, 5, 5, 5, 5, 3, 1]
					distances = []
					for scaleNote in cs:
						distances.append(scaleNote-lastNote) #positive implies above
					invDist = invertArray(distances) #gather the weights for cs distribution
					weightedDist = multiplyElems(invDist, dist)
					note = sampleFromDist(cs, weightedDist)


				#consecutive repeating rhythms should have relatively small variance
			
			#final edits to note
			#chance of jumping octave, slim and depends on if prev note was eigth note?
			#add chance of rest
			#dynamic change based on location in phrase and prev note (if ascending and in mid of phrase, louder)

			#note obtained. Bring it to octave range.
			lastNote = note #scale note
			diff = note - lastNote #scale difference

			octaves = [note-OCTAVE_SIZE, note, note+OCTAVE_SIZE]


			if diff >= scale[5]: #6+ jump up from prev note, slight chance of lowering octave
				octaveDist = [1, 1, 0]
				note = sampleFromDist(octaves, octaveDist)

			elif diff <= -(scale[5]): #6+ jump down from prev note, slight chance of raising octave
				#raise octave w/ chance
				octaveDist = [0, 1, 1]
				note = sampleFromDist(octaves, octaveDist)
			else: #randomly raise or lower octave
				dist = [1, 8, 1]
				note = sampleFromDist(octaves, octaveDist)

			realNote = note + baseNote

			#regulate range:
			if realNote <= 48:
				#remain, or bring back up 1
				octs = [realNote, realNote + OCTAVE_SIZE]
				octaveDist = [1, 2]
				tmp = sampleFromDist(octs, octaveDist)
				if tmp > realNote:
					baseNote += OCTAVE_SIZE
				realNote = tmp
			elif realNotes >= 110:
				#remain, or bring down 1
				octs = [realNote - OCTAVE_SIZE, realNote]
				octaveDist = [2, 1]
				tmp = sampleFromDist(octs, octaveDist)
				if tmp < realNote:
					baseNote -= OCTAVE_SIZE
				realNote = tmp

			#update baseNote to new range
			if realNote < baseNote-2:
				baseNote -= OCTAVE_RANGE
			elif realNote > baseNote+OCTAVE_RANGE:
				baseNote += OCTAVE_RANGE


			#update values for next iteration
			beatNum += duration
			if beatNum > chordDiv: #this only works for 2 chords in measure. abstract it further later to 4
				curChord = chordProgression[chordNum+1]
				chordScale = scale
			durationIndex += 1

			MyMIDI.addNote(track, channel, realNote, time, duration, vol)
			time += duration

		chordNum += CHORDS_PER_MEASURE
		measureNum += 1


#ROUGH, FOCUS ONLY ON 1 CHORD PER MEASURE FOR NOW
def constructHarmony(file, chordProgression, track, channel):
	#make harmonic volume slightly lower than melody
	harmVol = N - 5
	rhythm = determineHarmonicRhythm()
	baseNote = ROOT - 2*OCTAVE_SIZE

	phrases_in_song = (SONG_LENGTH-1)/ PHRASE_LENGTH
	measureNum = 0
	beatNum = 0
	note = 0
	baseNote = ROOT
	lastNote = 0 #scale note
	chordNum = 0
	#intervals of chord changes. e.g 2 chords per measure at 4/4: new chord at beat 3
	chordDiv = TIME_SIGNATURE/CHORDS_PER_MEASURE
	chordScale = scale
	time = 0

	if MAJORKEY:
		scale = majScale
	else:
		scale = minScale
	
	for measure in rhythm:
		durationIndex = 0 #track which note in measure
		curChord = chordProgression[chordNum]
		for duration in measure:
			#construct new set of notes based on chord, following root scale
			chordIndex = scale.index(chord)
			cs = shift(scale, chordIndex) #chordScale
			#start of phrase
			elif (measureNum%(PHRASE_LENGTH) == 0) and (beatNum == 0):


			#start of measure. chord tonic
			elif (beatNum == 0):
				notes = [cs[0], cs[0]-OCTAVE_SIZE, cs[0] - 2*OCTAVE_SIZE]
				dist = [3, 1, 1]

			#if start of chord e.g TIME/CHORDSPERMEASURE. tonic. always
			elif ((beatNum+1) % CHORDS_PER_MEASURE) == 0:
				notes = [cs[0]]
				dist = [1]

			#other downbeats will contain dominant/tonic w/ high chance, also 3rd
			elif beatNum.is_integer():
				notes = [cs[0], cs[2], cs[4], cs[7], cs[2]+OCTAVE_SIZE]
				dist = [0, 1, 2, 2, 2]

			#upbeats:dominant, 3rd, chance of just going up 1 if prev was tonic
			else:
				if lastNote == cs[0]:
					notes = [cs[2], cs[4], cs[7], lastNote+1]
					dist = [5, 5, 2 1]
				else:
					notes = [cs[2], cs[4], cs[7]]
					dist = [3, 3, 1]

			note = sampleFromDist(notes, dist)
			realNote = baseNote + note

			lastNote = note
			lastRealNote = realNote
			#handling octaves. 1st in chord/measure can be 1-2 octaves lower
			#med+octave if 2ndlast was octave+tonic
						#update values for next iteration
			beatNum += duration
			if beatNum > chordDiv: #this only works for 2 chords in measure. abstract it further later to 4
				curChord = chordProgression[chordNum+1]
				chordScale = scale
			durationIndex += 1

			MyMIDI.addNote(track, channel, realNote, time, duration, vol)
			time += duration

		chordNum += CHORDS_PER_MEASURE
		measureNum += 1


	#upbeats:dominant, 3rd, chance of just going up 1 if prev was tonic



#this constructs melody+harmony simultaneously, so relations can be considered
	#(easier to decide pick-ups, exceptions, etc)
	#file is a MIDIFile object. chordProgression is an array of base values
def compose(file, chordProgression):
	vol = N
	harmVol = vol-5
	
	pass





##############
#### MAIN ####
##############

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

	if MAJORKEY:
		chordProg = constructChordProg("maj")
	else:
		chordProg = constructChordProg("min")

	if COMPOSE_SEPARATELY:
		constructMelody(MyMIDI, chordProg, track1, channel)
		constructHarmony(MyMIDI, chordProg, track2, channel)
	else:
		compose(MyMIDI, chordProg)

	#write to disk
	binfile = open("out.mid", 'wb')
	MyMIDI.writeFile(binfile)
	binfile.close()

# Now add the note. 
MyMIDI.addNote(track,channel,pitch,time,duration,volume)
MyMIDI.addNote(track,channel,pitch,time+duration,duration,volume+5)
MyMIDI.addNote(track,channel,pitch,time+2*duration,duration,volume-25)
MyMIDI.addNote(track,channel,pitch,time+3*duration,duration,volume+25)





