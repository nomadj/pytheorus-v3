from pytheorus import display_grandstaff, quarter_note, half_note, whole_note, eighth_note

a, b, c, d, e, f, g = ("a", "b", "c", "d", "e", "f", "g")
qn, hn, wn, en = (quarter_note, half_note, whole_note, eighth_note)

treble_notes = [qn(c), qn(b), en(f), en(e), ('rest', 4)]
bass_notes = [('d', 4.0), ('B2', 4.0)]
# bass_notes = []
display_grandstaff(treble_notes, bass_notes, key_sig=0, time_sig='4/4')
