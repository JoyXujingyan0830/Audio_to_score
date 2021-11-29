import json
from sklearn import metrics
import numpy as np

def read_lst(lst_path):
	with open(lst_path) as f:
		data = f.readlines()
	data = [d.rstrip(",") for d in data]
	return data

def frame_roll_from_path(path, max_frame=-1, frames_per_second=100, notes_num=88):
	segments = read_lst(path)
	segments = [seg.rstrip().split('\t') for seg in segments]
	if max_frame == -1:
		max_frame = int(float(segments[-1][1]) * frames_per_second + 1)
	frame_roll = np.zeros([max_frame, notes_num + 1])
	frame_roll[:, notes_num] = 1
	for seg in segments:
		st = int(float(seg[0]) * frames_per_second)
		ed = int(float(seg[1]) * frames_per_second + 1)
		if st >= max_frame:
			break
		if ed > max_frame:
			ed = max_frame
		frame_roll[st : ed, int(float(seg[2]))] = 1
		frame_roll[st : ed, notes_num] = 0
		if ed == max_frame:
			break
	return frame_roll, max_frame

def measure_for_transcription(est_path, ref_path):
	ref_frame_roll, max_frame = frame_roll_from_path(ref_path)
	est_frame_roll, _ = frame_roll_from_path(est_path, max_frame)
	pre = metrics.average_precision_score(ref_frame_roll, est_frame_roll, average='micro')
	return pre

def save_json(path, data):
	with open(path,'w') as f:
		json.dump(data,f)

if __name__ == '__main__':

	TEST_DATA_LST_PATH = "testlist/test3.lst"
	refpath = "/Users/joy/Downloads/spring/MSI-DIS/sample_"
	# refpath = "E:/model/vocaltrans/MSI-DIS/sample_"

	lst = read_lst(TEST_DATA_LST_PATH)
	score = {}
	res = []

	for index in range(len(lst)):
		d = lst[index].split(",")
		name1 = d[0]
		name2 = d[1]
		data1 = d[2].split(".")
		data2 = d[3].split(".")
		path1 = refpath +str(index)+"/"+name1+"_est.txt"
		path2 = refpath + str(index) +"/"+ name2 + "_est.txt"
		ref1 = data1[0]+"_ref.txt"
		ref2 = data2[0] + "_ref.txt"
		pre1 = measure_for_transcription(path1, ref1)
		pre2 = measure_for_transcription(path2, ref2)
		res.append([name1, pre1,name2, pre2])

	res_path = "score/upresvocal.json"
	save_json(res_path, res)


