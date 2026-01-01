from music21 import stream, note, environment, metadata, clef, meter, key
import os
import subprocess
import threading

os.environ['QT_LOGGING_RULES'] = 'qt.qpa.xcb=false;*.warning=false'
os.environ['SKIP_LIBJACK'] = '1'
os.environ['LD_DEBUG'] = ''
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

env = environment.Environment()
env['musicxmlPath'] = '/usr/local/bin/musescore4portable'
env['musescoreDirectPNGPath'] = '/usr/local/bin/musescore4portable'

## key -- positive integer for sharps, negative for flats
def display_treble(pitches, filename='my_score', time_sig='4/4', key=0):
    # create a stream object
    s = stream.Stream()
    # add metadata
    s.insert(0, metadata.Metadata())
    s.insert(0, meter.TimeSignature(time_sig))
    s.insert(0, key.KeySignature(key))
             
    s.metadata.title = ""
    s.metadata.composer = ""

    # convert each string in notes list to a music21 note object
    for pitch in pitches:
        note_object = note.Note(pitch)
        s.append(note_object)

    xml_path = f"{filename}.musicxml"
    s.write('musicxml', fp=xml_path)

    musescore_path = '/usr/local/bin/musescore4portable'
    png_output = f"{filename}.png"
    
    print("Generating Image...")
    cmd = f"{musescore_path} {xml_path} -o {png_output} -T 10 -r 115 >/dev/null 2>&1"
    subprocess.run(cmd, shell=True)
    # subprocess.run([
    #     musescore_path,
    #     xml_path,
    #     '-o', png_output,
    #     '-T', '10', ## Trim border
    #     '-r', '115' ## Resolution
    # ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if os.path.exists(xml_path):
        os.remove(xml_path)

    final_png = f"{filename}-1.png"
    if os.path.exists(final_png):
        subprocess.run(f"feh {final_png} >/dev/null 2>&1", shell=True)
        # subprocess.run([ 'feh', final_png], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        

    else:
        print(f"Error: Could not find {final_png}")

def display_grandstaff(treble_data, bass_data, title="", composer="", time_sig='4/4', key_sig=0):
    main_score = stream.Score()
    main_score.insert(0, metadata.Metadata())
    main_score.metadata.title = title
    main_score.metadata.composer = composer

    ## Create treble
    treble_part = stream.Part()
    treble_part.insert(0, clef.TrebleClef())
    treble_part.insert(0, meter.TimeSignature(time_sig))
    treble_part.insert(0, key.KeySignature(key_sig))
    for n_str, dur in treble_data:
        if n_str.lower() == 'rest':
            new_note = note.Rest()
        else:
            new_note = note.Note(n_str)
        new_note.duration.quarterLength = dur
        treble_part.append(new_note)

    ## Create bass
    bass_part = stream.Part()
    bass_part.insert(0, clef.BassClef())
    bass_part.insert(0, meter.TimeSignature(time_sig))
    bass_part.insert(0, key.KeySignature(key_sig))
    for n_str, dur in bass_data:
        if n_str.lower() == 'rest':
            new_note = note.Rest()
        else:
            new_note = note.Note(n_str)
        new_note.duration.quarterLength = dur
        bass_part.append(new_note)
        new_note = note.Note(n_str)

    main_score.insert(0, treble_part)
    main_score.insert(0, bass_part)

    output_name = "grandstaff"
    xml_path = f"{output_name}.musicxml"
    main_score.write('musicxml', fp=xml_path)

    musescore_path = '/usr/local/bin/musescore4portable'
    png_output = f"{output_name}.png"
    cmd = f"{musescore_path} {xml_path} -o {png_output} -T 10 -r 115 >/dev/null 2>&1"
    subprocess.run(cmd, shell=True)
    threading.Thread(target=play_audio, args=(xml_path,), daemon=True).start()

    if os.path.exists(xml_path): os.remove(xml_path)
    final_png = f"{output_name}-1.png"
    if os.path.exists(final_png):
        subprocess.run(f"feh {final_png} >/dev/null 2>&1", shell=True)
 
def play_audio(xml_path):
    wav_output = "temp_audio.wav"
    musescore_path = '/usr/local/bin/musescore4portable'
    cmd = f"{musescore_path} {xml_path} -o {wav_output} -T 10 -r 115 >/dev/null 2>&1"
    subprocess.run(cmd, shell=True)
    subprocess.run(f"aplay {wav_output} >/dev/null 2>&1", shell=True)
    
# my_notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']
# display_treble(my_notes)

treble_notes = [('C4', 1.0), ('E4', 1.0), ('G4', 2.0), ('rest', 4.0)]
bass_notes = [('C3', 4.0), ('B3', 4.0)]
os.system('clear')
display_grandstaff(treble_notes, bass_notes, key_sig=-4, time_sig='3/4')
