from nltk.corpus import nps_chat

fileids_list = nps_chat.fileids()
fid = {"20s":[], "30s":[], "40s":[],"adu":[],"tee":[]}

for f_id in fileids_list:
	tag = f_id[6:9]
	fid[tag].append(f_id)

young_and_old = {"young": fid["tee"]+fid["20s"] , "old": fid["30s"]+fid["40s"]+fid["adu"]}

print young_and_old


