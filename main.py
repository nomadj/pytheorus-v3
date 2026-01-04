from utils import *

treble_notes = [('C', 1), ('E4', 1), ('G4', 2), ('rest', 4)]
bass_notes = [('C2', 4.0), ('B2', 4.0)]
# bass_notes = []
display_grandstaff(treble_notes, bass_notes, key_sig=0, time_sig='4/4')
