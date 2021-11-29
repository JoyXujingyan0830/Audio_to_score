from gainscore import (measure_for_transcription,save_json,read_lst)
from transmidi import txt2midi

def tune_glitches(beatpoint,data,onetatum):
	tuned = []
	for i in range(len(beatpoint)-1):
		tatums = []
		for interval in range(beatpoint[i+1][0]-beatpoint[i][0]):
			percent = (float(data[beatpoint[i][0]+interval][1])-float(data[beatpoint[i][0]+interval][0]))/beatpoint[i][1]
			tatums.append([data[beatpoint[i][0] + interval][2],
						  data[beatpoint[i][0] + interval][0],
						  percent])
		tatums.sort(key=lambda x:x[2], reverse=False)
		tuned.append([tatums[0][1]+"\t"+str(float(tatums[0][1])+float(onetatum))+"\t"+tatums[0][0]])

	return tuned


if __name__ == '__main__':
	# path_orig = "G:/align/midi/"
	refpath = "E:/model/spring/MSI-DIS/sample_"
	TEST_DATA_LST_PATH = "testlist/test.lst"
	lst = read_lst(TEST_DATA_LST_PATH)
	path_beat = "txt/tunedtimes.txt"

	for i in range(len(lst)):
		name = lst[i].split(",")
		path1 = refpath +str(i)+"/"+name[0]+"_est.txt"
		path1 = "/Users/joy/Downloads/spring/MSI-DIS/sample_1/Violin_est.txt"
		data = []
		beat = []
		error = 0.1
		with open(path1, "r") as f:
			for line in f.readlines():
				data.append(line.split("\t"))

		with open(path_beat, "r") as f:
			for line in f.readlines():
				beat.append(line.split("\t"))

		res = []

		for time in range(len(beat)-1):
			delta = float(beat[time+1][0]) - float(beat[time][0]) + error
			onetatum = delta/4
			beatpoint = []
			for beatindex in range(len(beat)-1):
				for index in range(len(data)-1):

					if float(data[index][0]) <= float(beat[beatindex][0]) <= float(data[index+1][0]):
						currentbeatlength = float(beat[beatindex+1][0])-float(beat[beatindex+1][0]) + error
						beatpoint.append([beatindex, currentbeatlength])
						print(i,time,beatindex,index)

		#write down answers
			res = tune_glitches(beatpoint,data,onetatum)
			tuned_path = "txt/tuned_"+str(i)+".txt"
			txt2midi(tuned_path, "txt/tuned_"+str(i)+".mid")
			with open(tuned_path , "w") as fo:
				for inf in res:
					fo.writelines(inf)
		# get the newest scores

		score = {}
		res = []

		d = lst[i].split(",")
		data1 = d[2].split(".")
		ref1 = data1[0] + "_ref.txt"
		print(tuned_path)
		print(ref1)
		pre1 = measure_for_transcription(tuned_path, ref1)
		print (pre1)
		res.append(["tuned" + d[0] + "+" + d[1] + "_" + d[0], pre1])

		res_path = "score/newresults.json"
		save_json(res_path, res)
		break

	#get the original scores
	lst = read_lst(TEST_DATA_LST_PATH)
	score = {}
	res = []

	for index in range(len(lst)):
		index = 1
		d = lst[index].split(",")
		name1 = d[0]
		name2 = d[1]
		data1 = d[2].split(".")
		data2 = d[3].split(".")
		path1 = refpath +str(index)+"/"+name1+"_est.txt"
		nameestmidi = path_orig +name1+"+"+name2+"_"+name1+"_est.mid"
		ref1 = data1[0]+"_ref.txt"
		print(path1)
		print(ref1)
		pre1 = measure_for_transcription(path1, ref1)
		print (pre1)
		txt2midi(path1, nameestmidi)
		txt2midi(ref1 , data1[0]+"_ref.mid")
		res.append([name1+"+"+name2+"_"+name1, pre1])
		break

	res_path = "G:/align/score/4violinorig.json"
	save_json(res_path, res)


	




