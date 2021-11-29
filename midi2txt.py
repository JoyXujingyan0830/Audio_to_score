import pretty_midi

def mid2txt(midi_path,txt_path):
    midi_data = pretty_midi.PrettyMIDI(midi_path)
    res = []
    for instrument in midi_data.instruments:
        print("instrument:", instrument.program)
        for note in instrument.notes:
            res.append([str(round(note.start, 2)), '\t', str(round(note.end, 2)), '\t', str(note.pitch), '\n', ])
    with open(txt_path, "w") as fo:
        for inf in res:
            fo.writelines(inf)
    return

def txt2midi(pathmidi,pathtxt):
	mid = pretty_midi.PrettyMIDI()
	cello_program = pretty_midi.instrument_name_to_program('Cello')
	cello = pretty_midi.Instrument(program=cello_program)
	with open(pathtxt , "r") as f:
		for line in f.readlines():
			data = line.split("\t")
			note = pretty_midi.Note(velocity=100, pitch=int(data[2][:2]) + 21, start=float(data[0]), end=float(data[1]))
			cello.notes.append(note)
	mid.instruments.append(cello)
	mid.write(pathmidi)
	return

if __name__ == '__main__':

    midi_path = "/Users/joy/Downloads/CSD_LI_alto_midi.mid"
    txt_path = "/Users/joy/Downloads/align/txt/Vocal_ans"

    pathtxt = "/Users/joy/Downloads/spring/MSI-DIS/sample_1/Violin_est.txt"
    pathmidi = "/Users/joy/Downloads/align/midi/Violin_est.mid"
    # mid2txt(midi_path, txt_path)
    txt2midi(pathmidi,pathtxt)


