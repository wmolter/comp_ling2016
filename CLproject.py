from nltk.corpus import nps_chat
from collections import defaultdict
from collections import Counter
import re

def word_freq(category, lowercase = False):
	word_counter = defaultdict(int)
	total_word_count = 0

	user_pattern = re.compile(r'U\d')

	file_list = young_and_old[category]

	for file_name in file_list:
		chat_log = nps_chat.posts(file_name)
		for post in chat_log:
			if post == ['JOIN'] or post == ['PART'] or post[0] == ':':
				continue
			for word in post:
				if re.match(user_pattern, word):
					continue
				if lowercase:
					word = word.lower()
				# if word == '#14-19teens':
				# 	print post
				word_counter[word] += 1
				total_word_count += 1

	word_freq = {}

	for key,value in word_counter.iteritems():
		word_freq[key] = 1.0*value / total_word_count
	return (word_freq, total_word_count)

def freq_diff(word_freq1, word_freq2):
	all_words_list = list( set(word_freq1.keys()) | set(word_freq2.keys()) )
	
	freq_diff = Counter()

	for gram in all_words_list:
		try:
			gf_1 = word_freq1[gram]
		except KeyError:
			gf_1 = 0
		try:
			gf_2 = word_freq2[gram]
		except KeyError:
			gf_2 = 0
		freq_diff[gram] = gf_1 - gf_2

	return freq_diff.most_common(25)


fileids_list = nps_chat.fileids()
fid = {"20s":[], "30s":[], "40s":[],"adu":[],"tee":[]}

for f_id in fileids_list:
	tag = f_id[6:9]
	fid[tag].append(f_id)

young_and_old = {"young": fid["tee"]+fid["20s"] , "old": fid["30s"]+fid["40s"]+fid["adu"]}


(young_word_freq, young_words) = word_freq("young", True)
(old_word_freq, old_words) = word_freq("old", True)

print "Words old people use more than young people"
print freq_diff(old_word_freq, young_word_freq)
print
print "Words young people use more than old people"
print freq_diff(young_word_freq, old_word_freq)


