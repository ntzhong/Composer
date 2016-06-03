This program generates a piano piece complete with both melodic and harmonic lines.

The program requires MIDIUtil to run (sudo apt-get install python-midiutil). MIDIUtil runs best with python 2.x.

To run, enter the directory and run: python2 Composer.py
The composition should be written to a new MIDI file named out.mid. This can be played by any media player that supports midi, and can be imported into music editors and converted into sheet music.

Parameters at the beginning of the code can be changed. The following parameters can be safely changed:

	BPM (beats per minute)
	CHORDS_PER_MEASURE (how often a chord changes in a measure. Default is 1.)
	PHRASE_LENGTH (Determines how many measures are in a phrase. Any integer should work.)
	ROOT (Determines the starting octave and key signature. Value is a MIDI value.)
	MAJORKEY (True = compose in major key. False = compose in minor key)