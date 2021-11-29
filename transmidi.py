import pretty_midi

def read_lst(lst_path):
	with open(lst_path) as f:
		data = f.readlines()
	data = [d.rstrip(",") for d in data]
	return data

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

	TEST_DATA_LST_PATH = "E:/model/data/urmp/testset/test1.lst"
	refpath = "E:/model/vocaltrans/MSI-DIS/sample_"
	path = "G:/align/AuSep_1_vn_12_Spring_ref.txt"

	lst = read_lst(TEST_DATA_LST_PATH)

	for index in range(len(lst)):
		d = lst[index].split(",")
		name1 = d[0]
		name2 = d[1]
		data1 = d[2].split(".")
		data2 = d[3].split(".")
		path1 = refpath +str(index)+"/"+name1+"_est.txt"
		path2 = refpath + str(index) +"/"+ name2 + "_est.txt"

		mid = pretty_midi.PrettyMIDI()
		cello_program = pretty_midi.instrument_name_to_program('Cello')
		cello = pretty_midi.Instrument(program=cello_program)
		with open(path1, "r") as f:
			for line in f.readlines():
				data = line.split("\t")
				note = pretty_midi.Note(velocity=100, pitch=int(data[2][:2]) + 21, start=float(data[0]),
										end=float(data[1]))
				cello.notes.append(note)
		mid.instruments.append(cello)
		mid.write("G:/align/" + name1 + "&" + name2+"_"+name1 + ".mid")

		mid = pretty_midi.PrettyMIDI()
		cello_program = pretty_midi.instrument_name_to_program('Cello')
		cello = pretty_midi.Instrument(program=cello_program)
		with open(path2, "r") as f:
			for line in f.readlines():
				data = line.split("\t")
				note = pretty_midi.Note(velocity=100, pitch=int(data[2][:2]) + 21, start=float(data[0]), end=float(data[1]))
				cello.notes.append(note)
		mid.instruments.append(cello)
		mid.write("G:/align/" + name1 + "&" + name2+"_"+name2 + ".mid")




