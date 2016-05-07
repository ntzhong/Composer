#Compose
from midiutil.MidiFile import MIDIFile #external package. For linux users: sudo apt-get install python-midiutil
from random import randint

#import pdb; pdb.set_trace() <- To debug: place this at breakpoints

#VALUES TO ADJUST
COMPOSE_SEPARATELY = True #chooses to construct parts indepndently
BPM = 90 #BPM
CHORDS_PER_MEASURE = 1 #standard is 1 or 2
PHRASE_LENGTH = 4 #in measures
SONG_LENGTH = PHRASE_LENGTH * 4 + 1 #in measures. +1 for resolution measure?
ROOT = 90 #Set tonic to middle C
TIME_SIGNATURE = 4 #no compound meter. in beats per measure
MAJORKEY = False #false => minor
NUM_TRACKS = 2 #number of tracks. only 1 or 2 for now.
QUALITY = 0
#set range of notes
minRange = 21 #A0 = 21, lowest on piano
maxRange = 108 #C8 = 108, highest on piano


#for octave changing (will need to modify to fit needs)
#OCTAVE = 0

#INIT STANDARD VALUES
OCTAVE_SIZE = 12
#octLocation = OCTAVE * OCTAVE_SIZE
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
minThird = 3 #+ octInc
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
	for i in range(0, len(a)):
		newArray.append(a[i]*b[i])
	return newArray

#returns array of reciprocals
def invertArray(array):
	newArray = []
	for value in array:
		#import pdb; pdb.set_trace()
		if (value != 0):
			newArray.append(1.0/value)
		else:
			newArray.append(value)
	return newArray

#takes array of items, with an associated distribution array, and returns an item based on distribution
#note that distrubtion does not have to be normalized
def sampleFromDist(itemArray, distribution):
	#take cumulative sum
	if (len(itemArray) == 1 and len(distribution) == 1):
		return itemArray[0]
	elif len(itemArray) == len(distribution):
		cumDist = []
		total = 0
		for p in distribution:
			total += p
			cumDist.append(total)

		#sample	and compare probability buckets
		sample = randint(0, total)
		i = 0
		for cumP in cumDist:
			if (sample <= cumP):
				return itemArray[i]
			i += 1

		print("distribution selection error")
	else:
		print ("array indices don't match up")
		print itemArray
		print distribution

#returns true with chance a, false w/ chance b
def coinFlip(a, b): 
	choices = [0, 1]
	dist = [a, b]
	return sampleFromDist(choices, dist)

#returns value of nearest note, and abs(distance)
def findNearestNote(curNote, noteInQuestion):
	dif1 = abs(curNote - noteInQuestion)
	dif2 = abs(curNote + OCTAVE_SIZE - noteInQuestion)
	dif3 = abs(curNote - OCTAVE_SIZE - noteInQuestion)
	minDif = min(dif1, dif2, dif3)
	if minDif == dif1:
		dist = dif1
		note = curNote
	elif minDif == dif2:
		dist = dif2
		note = noteInQuestion - OCTAVE_SIZE
	else:
		dist = dif3
		note = noteInQuestion + OCTAVE_SIZE
	return [note, dist]

#take the abs difference between two notes. If the difference is 6 higher, then lower
#if the difference is less than -6, then raise octave
#octave changes with chance. returns new note. chance is in [0, 1]
def flipOctWithDist(note, lastNote, threshold, chance): #note
	dist = note - lastNote
	octaves = [note - OCTAVE_SIZE, note, note + OCTAVE_SIZE]
	chanceInt = int(chance * 100)
	negChance = int(100 - chanceInt)
	rand = coinFlip(chanceInt, negChance)
	if rand:
		if (dist >= threshold):
			return octaves[0] #lower
		elif (dist <= -threshold):
			return octaves[2] #raise
	return note

#if beyond min/max threshold, move octave with chance. else keep going
def regulateRange(note, min, max, chance):
	chance = int(chance * 100)
	randChance = coinFlip(chance, 100-chance)
	if randChance:
		if note >= max:
			return note-OCTAVE_SIZE
		elif note <= min:
			return note+OCTAVE_SIZE
	return note


#Reweight distribution with regards to ascension and descension trends and returns distribution
#Chances of following trend increases up until a point, and decreases after that point
#ascension count represents number of consecutive descensions/ascensions. negative => descension. 
#count zeros as soon as trend is broken.
def reweightWithContext(notes, dist, curNote, ascensionCount):
	if ascensionCount == 0: #default
		return dist

	#else do teh calculamations
	trendCount = abs(ascensionCount)
	#this determines rate of diminish. higher offset => more gradual diminish (diminish by less than 1/(trendcount+offset))
	offset = 8
	#followChance is normalized to [0, 1]
	followChance = 0.85 * offset/(trendCount+offset-1)
	print followChance

	noteIndex = notes.index(curNote)
	if ascensionCount > 0: #ascension: amplify weights of higher notes by followChance
		for i in range(noteIndex+1, len(notes)): #problem: if note is at end of scale?
			dist[i] = int(round(dist[i] * (1+followChance)))

	else: #descension: amplify weights of those below curNote
		for i in range(0, noteIndex):
			dist[i] = int(round(dist[i] * (1 + followChance)))

	#need to cast to ints
	return dist


#updates ascension/descension counter.
#counter resets to zero if trend is broken
def determineAscensionCount(diff, curAscCount):
	ascCount = 0
	followsTrend = (diff * curAscCount) > 0

	if followsTrend: #follows trend
		ascCount = curAscCount + diff/abs(diff) #+/- 1 depending on sign of diff

	return ascCount



		
		


	
########################
##### MUSIC THEORY #####
########################

#takes in a MIDI value. returns 3-elem array of midi values
#quality = "min" or "maj"


#when using, want selected note to be on top => 2nd inversion triad of root

#build a chord according to chord scale on top of note
def constructTriadInScale(root, scale, inv=0):
	rootIndex = scale.index(root)
	thirdIndex = rootIndex+2
	fifthIndex = rootIndex+4

	first = scale[rootIndex]
	third = scale[(rootIndex+2)%8]
	fifth = scale[(rootIndex+4)%8]

	#handle wrap-around
	if third < first:
		third += OCTAVE_SIZE
	if fifth < first:
		fifth += OCTAVE_SIZE

	scale = [first, third, fifth]
	shift(scale, inv)
	return scale



def constructTriad(root, quality = 0):
	if quality == 0:
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
	return shift(triad, n)






#################################
##### COMPOSITION FUNCTIONS #####
#################################
#This is where the magic happens

#Qualities:
#0 = normal
#1 = lengthy and emotional
#2 = short, upbeat, fast, happy

#TO ADD: 2nd to last measure, high chance of eigth notes on last beat
#determines the rhythm for a measure (or phrase?) maybe an array of measure arrays?
#in comments, swing refers to .75, .25 beats in conjunction
#rest determined later (randomly turn notes on/off). Or can intentionally place them here, w/ duration=-1
def determineMelodicRhythm():
	print "constructing melodic rhythm ..."
	phrases_in_song = (SONG_LENGTH-1) / PHRASE_LENGTH
	rhythm = []
	lastBeat = TIME_SIGNATURE-1
	for phrase in range(0, phrases_in_song): #per phrase
		for measureNum in range(0, PHRASE_LENGTH): #per measure
			measure = []
			curBeat = 0.0 #measure= 0,1,2,3
			#determine rhythm of the measure with probability. Depends on location in phrase, possibly also on value of beatsLeft
			while curBeat < TIME_SIGNATURE: #per beat
				duration = 0.0
				duration2 = 0.0 #potential successive notes
				duration3 = 0.0
				#Determine next rhythm, note by note
				#arbitarily chosen style standard. Currently only style is QUALITY == 0. Create extension file for other options?
				if QUALITY == 0:
					#for end of the phrase, but not the song
					randomChance = [0, 1]
					randDist = [9, 1]
					chance = sampleFromDist(randomChance, randDist)

					#first beat of first measure
					if (curBeat + measureNum == 0):
						durations = [0.5, 1, 1.5, 2, 3, 3.5, 4]
						dist = [8, 8, 5, 1, 1, 1, 1]
						duration = sampleFromDist(durations, dist)
						if (duration == 1.5):
							durs = [0.5, 1.5]
							dist = [1, 1]
							duration2 = sampleFromDist(durs, dist)
						if (duration == 0.5):
							duration2 = 0.5

					#last measure of phrase
					elif (measureNum == PHRASE_LENGTH-1):
						if (curBeat == 0):
							durations = [0.5, 1, 2, 3, 3.5, 4]
							dist = [1, 2, 1, 4, 4, 1]
							duration = sampleFromDist(durations, dist)

							if (duration == 3): #two eigth notes to bridge into next phrase
								duration2 = duration3 = 0.5
							elif (duration == 3.5):
								duration2 = 0.5
							elif (duration == 0.5): #meh
								duration2 = 0.5
							elif (duration == 1):
								duration2 = 2 #also meh

						#4th beat. chance of 2 or 1 or no eigth-notes.
						elif (curBeat == lastBeat): 
							durations = [0.5, 0.75, 1]
							dist = [5, 5, 5]
							duration = sampleFromDist(durations, dist)
							if (duration == 0.5):
								duration2 = 0.5
							elif (duration == 0.75):
								duration2 = 0.25
						else:
							remaining_beats = TIME_SIGNATURE - curBeat
							 #higher chance of half-note if it is in 2nd beat
							options = [0.5, 1, 2]
							dist = [4, 3, 2]
							duration = sampleFromDist(options, dist)
							while duration > remaining_beats:
								duration = sampleFromDist(options, dist)

					elif (chance) and curBeat.is_integer():
						chance2 = sampleFromDist(randomChance, [1, 1])
						if chance2:
							duration = 0.25
							duration2 = 0.25
							duration3 = 0.5
						else:
							duration = 0.5
							duration2 = 0.25
							duration3 = 0.25

					#beginning of measure
					elif (curBeat == 0):
						durs = [0.5, 1, 1.5, 2, 3, 3.5, 4]
						dist = [10, 7, 5, 1, 1, 1, 1 ]
						duration = sampleFromDist(durs, dist)
						chance = coinFlip(1, 1)
						if (duration == 1.5 and chance):
							durs = [0.5, 1.5]
							dist = [1, 1]
							duration2 = sampleFromDist(durs, dist)
						elif (duration == 1.5):
							duration2 = 0.25
							duration3 = 0.25

					#last beat in normal measure. swings to bridge into next measure
					elif (curBeat == lastBeat): 
						durations = [0.5, 0.75, 1]
						dist = [5, 5, 5]
						duration = sampleFromDist(durations, dist)
						if (durations == 0.5):
							duration2 = 0.5
						elif (durations == 0.75):
							duration2 = 0.25

					else: #for everything else, sample psuedo-randomly.
						remaining_beats = TIME_SIGNATURE - curBeat
						options = [0.25, 0.5, 1, 1.5, 2, 3]
						dist = [2, 8, 4, 2, 1, 1]
						duration = sampleFromDist(options, dist)
						while duration > remaining_beats:
							if (len(options) > 1):
								index = options.index(duration) #narrow down choices
								options.pop(index)
								dist.pop(index)
							duration = sampleFromDist(options, dist)
						if (duration == 0.25) and (remaining_beats - duration > 0):
							duration2 = 0.25
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



def determineHarmonicRhythm(): #ONLY FOR TIME SIGNATURE = 4
	print "constructing harmonic rhythm"
	phrases_in_song = (SONG_LENGTH-1) / PHRASE_LENGTH
	rhythm = []
	for phrase in range(0, phrases_in_song): #per phrase
		for measureNum in range(0, PHRASE_LENGTH): #per measure
			measure = []
			curBeat = 0.0 #measure= 0,1,2,3
			duration = 0.0
			duration2 = 0.0 #potential successive note
			duration3 = 0.0
			#determine rhythm of the measure with probability. Depends on location in phrase, possibly also on value of beatsLeft
			while curBeat < TIME_SIGNATURE:
				#end of phrase
				if measureNum == PHRASE_LENGTH-1: #last measure of phrase
					if curBeat == 0:
						durs = [0.5, 1, 2, 4]
						dist = [5, 5, 5, 5]
					elif curBeat == 1:
						durs = [0.5, 1]
						dist = [5, 5]
					elif curBeat == 2: #beat 3
						durs = [2]
						dist = [1]
					elif curBeat == 3:
						durs = [1]
						dist = [1]
					else:
						durs = [0.5, 1]
						dist = [10, 1]

				elif (curBeat == 0 and measureNum == 0): #start of phrase
					durs = [0.5, 1]
					dist = [5, 5]

				#general everything
				elif curBeat == 0: #first beat higher chance of eigths
					durs = [0.5, 1, 2]
					dist = [10, 5, 1]

				elif curBeat == 1:#2nd beat: higer chance of quarter
					durs = [0.5, 1]
					dist = [1, 1]
				#other downbeats
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
	print "harmonic rhythm determined"
	#print rhythm
	return rhythm


#returns a chord progression for entirety of song. key_quality = "maj" or "min"
def constructChordProg(key_quality):
	#every chord gets equal amount of time, based on num chords per measure
	if key_quality == "maj":
		scale = majScale
	else:
		scale = minScale

	#Sets scale to octave range of root
	phrases_in_song = (SONG_LENGTH-1)/PHRASE_LENGTH
	
	chordProgression = []
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
					chord = sampleFromDist(notes, dist)
					chordProgression.append(chord)

				elif (measure == PHRASE_LENGTH-1): #end of phrase. high chance of dominant. can also be 4
					notes = [scale[3], scale[4]] #subDom, Dom
					dist = [1, 9]
					chord = sampleFromDist(notes, dist)
					chordProgression.append(chord)

				else: #probability. depends on previous, and like 1% chance of being tonic.
					notes = [scale[0], scale[2], scale[3], scale[4], scale[5]]
					dist = [1, 1, 1, 1, 1]
					chord = sampleFromDist(notes, dist)
					chordProgression.append(chord)

	for i in range (0, CHORDS_PER_MEASURE):
		chordProgression.append(scale[0]) #Resolve final measure w/ tonic
	return chordProgression



#JUST MAKE IT STOP JUMPING OCTAVES, OR DO IT HELLA RARELY
#ALSO DO THE ASCEND/DESCEND SHIT

#takes in a MIDIFile object and constructs composition
#constructs two independent lines, to be combined at the end, based on same chord progression
def constructMelody(file, chordProgression, track, channel):
	#melody starts at predefined normal vol
	print "constructing melody..."
	vol = N
	rhythm = determineMelodicRhythm() #array of measures, each measure contains durations summing to TIME_SIGNATURE
	phrases_in_song = (SONG_LENGTH-1)/ PHRASE_LENGTH
	measureNum = 0
	beatNum = 0.0
	note = 0
	baseNote = ROOT
	lastNote = 0 #scale note
	chordNum = 0
	#intervals of chord changes. e.g 2 chords per measure at 4/4: new chord at beat 3
	chordDiv = TIME_SIGNATURE/CHORDS_PER_MEASURE
	time = 0
	prevDuration = 4
	#negative => descend, positive => ascend
	asc = 0
	melody = []

	if MAJORKEY:
		scale = majScale
	else:
		scale = minScale

	cs = scale
	for measure in rhythm:
		durationIndex = 0 #track which note in measure
		curChord = chordProgression[chordNum]
		beatNum = 0.0
		for duration in measure:
			#MyMIDI.addNote(track,channel,pitch,time,duration,volume)
			if (measureNum + beatNum) == 0: #start of song excluding pickup
				#emphasis on 1, 3, 5
				dist = [10, 1, 8, 5, 9, 5, 5, 1]
				note = sampleFromDist(scale, dist)
			#very last measure
			if (measureNum == len(rhythm)-1):
				note = scale[0]
			#start of phrase
			elif ((measureNum % PHRASE_LENGTH) == 0) and (beatNum == 0):
				dist = [6, 1, 10, 5, 9, 5, 5, 1]
				note = sampleFromDist(scale, dist)

			#2nd to last note in song, force to be supertonic or leading
			elif (measureNum == SONG_LENGTH-1) and (durationIndex == len(measure)-1):
				notes = [scale[1], scale[6]] #supertonic or leading
				dist = [1, 1]
				note = sampleFromDist(notes, dist)

			#last measure of phrase. last note should be leading/supertonic of next chord
			elif ((measureNum)%PHRASE_LENGTH == 3) and (beatNum >= 3) and (coinFlip(1, 3)):#last measure
				nextChord = chordProgression[chordNum+1]
				nextScale = shift(scale, nextChord)
				notes = [nextScale[1], nextScale[6]]
				dist = [1, 1]
				note = sampleFromDist(notes, dist)				

			else:
				#favor smaller intervals, with max interval being w/in octive of previous note
				#construct new set of notes based on chord, following root scale
				chordIndex = scale.index(curChord)
				cs = shift(scale, chordIndex) #chordScale
				#downbeat of chord beginning (0, 3) (1,3,4-low,5, 6-low, 7-low)
				if (beatNum == 0): #first beat
					dist = [3, 2, 7, 4, 7, 4, 3, 2]
					note = sampleFromDist(cs, dist)
				elif beatNum.is_integer(): #all downbeats in general. #lower chance of tonic if not 1st note in measure
					dist = [2, 1, 2, 2, 2, 2, 1, 2]
					note = sampleFromDist(cs, dist)

				#upbeats. Closer notes more likely to be played, especially if eigth notes
				else:
					dist = [3, 4, 5, 5, 5, 5, 3, 1]
					distances = []
					notes = []
					for scaleNote in cs:
						if (scaleNote-lastNote != 0):
							#weight distances
							nearest = findNearestNote(scaleNote, lastNote) #[note, dist]
							distances.append(nearest[1])
							#get the correct octave version
							notes.append(nearest[0])
							
						else:
							distances.append(8) #low chance of repeating note
							notes.append(scaleNote)

					invDist = invertArray(distances) #gather the weights for cs distribution
					weightedDist = multiplyElems(invDist, dist)
					#squaring to give more weight, and eliminate negatives
					weightedDist = multiplyElems(weightedDist, invDist)
					#cube it to make sure there are almost no chance of jumps
					if prevDuration < 1.0:
						weightedDist = multiplyElems(weightedDist, invDist)
						weightedDist = multiplyElems(weightedDist, invDist)
					#need to convert dist into ints.
					weightedDist = [int(i*1000) for i in weightedDist]
					weightedDist = reweightWithContext(notes, weightedDist, lastNote, asc)
					note = sampleFromDist(notes, weightedDist)

			#chance of jumping octave, slim and depends on if prev note was eigth note?
			#add chance of rest

			#note obtained. Bring it to octave range.
			diff = note - lastNote #scale difference. negatve => lower than last
			lastNote = note
			#calculateAscensionValue()

			octaves = [note-OCTAVE_SIZE, note, note+OCTAVE_SIZE]
			#problem with flipping: diff no longer tracks positive/negative
			note = flipOctWithDist(note, lastNote, scale[5], 0.9 ) #note, distance, threshold, chance.

			#else: #randomly raise or lower octave
			if note != lastNote:
				octaveDist = [1, 14, 1] #in else
				note = sampleFromDist(octaves, octaveDist) #in else
			realNote = note + baseNote

			#regulate range: adjust realNote if it exceeds boundaries
			tmp = regulateRange(realNote, 60, 110, .8)
			if tmp > realNote: #implies tmp must then be +1 octave
				baseNote += OCTAVE_SIZE
			elif tmp < realNote:
				baseNote -= OCTAVE_SIZE
			realNote = tmp

			#update baseNote to new range
			if realNote < baseNote-2:
				baseNote -= OCTAVE_SIZE
			elif realNote > baseNote+OCTAVE_SIZE:
				baseNote += OCTAVE_SIZE

			#update values for next iteration
			asc = determineAscensionCount(diff, asc) #update asc count according to trend
			beatNum += duration
			prevDuration = duration
			if (beatNum > chordDiv) and (beatNum < TIME_SIGNATURE): #this only works for 2 chords in measure. abstract it further later to 4
				curChord = chordProgression[chordNum+1]
				cs = scale
			durationIndex += 1
			melody.append(note)
			file.addNote(track, channel, realNote, time, duration, vol)
			time += duration

		chordNum += CHORDS_PER_MEASURE
		measureNum += 1
	print "melody:"
	print melody

#REPETIVE AND ANNOYING. MAKE IT CLIMB
#ROUGH, FOCUS ONLY ON 1 CHORD PER MEASURE FOR NOW
def constructHarmony(file, chordProgression, track, channel):
	#make harmonic volume slightly lower than melody
	print "constructing harmony..."
	harmVol = N - 42
	rhythm = determineHarmonicRhythm()
	baseNote = ROOT - 2*OCTAVE_SIZE

	phrases_in_song = (SONG_LENGTH-1)/ PHRASE_LENGTH
	measureNum = 0
	beatNum = 0
	note = 0
	lastNote = 0 #scale note
	chordNum = 0
	#intervals of chord changes. e.g 2 chords per measure at 4/4: new chord at beat 3
	chordDiv = TIME_SIGNATURE/CHORDS_PER_MEASURE
	time = 0
	harmony = []

	if MAJORKEY:
		scale = majScale
	else:
		scale = minScale
	chordScale = scale
	for measure in rhythm:
		durationIndex = 0 #track which note in measure
		curChord = chordProgression[chordNum]
		for duration in measure:
			#construct new set of notes based on chord, following root scale
			chordIndex = scale.index(curChord)
			cs = shift(scale, chordIndex) #chordScale
			#start of phrase
			
			#if (measureNum%(PHRASE_LENGTH) == 0) and (beatNum == 0):
			#	pass
			#very last measure, resolve on tonic
			if (measureNum == len(rhythm)-1): 
				notes = [scale[0], scale[0] - OCTAVE_SIZE]
				dist = [10, 3]
			
			#start of measure. chord tonic
			elif (beatNum == 0):
				notes = [cs[0], cs[7], cs[0]-OCTAVE_SIZE, cs[0] - 2*OCTAVE_SIZE]
				dist = [3, 5, 1, 1]
			

			#if start of chord e.g TIME/CHORDSPERMEASURE. tonic. always
			elif ((beatNum+1) % CHORDS_PER_MEASURE) == 0:
				notes = [cs[0]]
				dist = [1]

			#other downbeats will contain dominant/ tonic+12/ high chance, also 3rd
			elif beatNum.is_integer():
				notes = [cs[0], cs[2], cs[4], cs[7], cs[2]+OCTAVE_SIZE]
				dist = [0, 1, 2, 2, 2]

			#upbeats:dominant, 3rd, chance of just going up 1 if prev was tonic
			else:
				if lastNote == cs[0]:
					notes = [cs[2], cs[4], cs[7] - OCTAVE_SIZE, cs[7]]
					dist = [5, 5, 1, 1]
				elif lastNote == cs[4]:
					notes = [cs[0], cs[2], cs[4], cs[7], cs[2]+OCTAVE_SIZE]
					dist = [2, 5, 1, 5, 5]
				elif lastNote == cs[7]:
					notes = [cs[2]+OCTAVE_SIZE, cs[4]]
					dist = [5, 5]
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
			if (beatNum > chordDiv) and (len(chordProgression)-1 > chordNum): #this only works for 2 chords in measure. abstract it further later to 4
				curChord = chordProgression[chordNum+1]
				chordScale = scale
			durationIndex += 1

			harmVol = N - realNote/2
			harmony.append(note)
			file.addNote(track, channel, realNote, time, duration, harmVol)
			time += duration

		chordNum += CHORDS_PER_MEASURE
		measureNum += 1

	print "harmony:"
	print harmony


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

#Main function. Can decide to take arugments
#def main(argv)
def main():
	#Def tracks
	track1 = 0 #melody
	track2 = 1 #harmony
	channel = 0 #0-15
	#create midi file w/ NUM_TRACKS tracks
	MyMIDI = MIDIFile(NUM_TRACKS)
	# Init track(s). Add track name and tempo.
	MyMIDI.addTrackName(track1,time,"Melody")
	if NUM_TRACKS == 2:
		MyMIDI.addTrackName(track2, time, "Harmony")
	MyMIDI.addTempo(track1,time,BPM)
	MyMIDI.addTempo(track2,time,BPM)
	print "constructing chord progression..."
	if MAJORKEY:
		chordProg = constructChordProg("maj")
	else:
		chordProg = constructChordProg("min")

	if COMPOSE_SEPARATELY:
		constructMelody(MyMIDI, chordProg, track1, channel)
		constructHarmony(MyMIDI, chordProg, track2, channel)
	else:
		compose(MyMIDI, chordProg)
	print "writing to disk..."	
	#write to disk
	binfile = open("out.mid", 'wb')
	MyMIDI.writeFile(binfile)
	binfile.close()
	print "Done!"

if __name__ == "__main__":
	main()
	#main(sys.argv)