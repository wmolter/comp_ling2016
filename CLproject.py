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
			if post[0] == '.':
				if post[1] == 'ACTION':
					word_counter['.action'] += 1
					post = post[2:]
				else:
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

def freq_diff(word_freq1, word_freq2, top_num = 10):
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

	return freq_diff.most_common(top_num)

def most_common_precedents(target_word, category, num_precedents = 3):
	precedents = Counter()

	file_list = young_and_old[category]
	user_pattern = re.compile(r'u\d')

	for file_name in file_list:
		chat_log = nps_chat.posts(file_name)
		for post in chat_log:
			if post == ['JOIN'] or post == ['PART'] or post[0] == ':':
				continue
			if post[0] == '.':
				if post[1] == 'ACTION':
					previous_word = '.action'
					post = post[2:]
				else:
					continue
			else:
				previous_word = '<s>'
			for word in post:
				word = word.lower()
				if word == target_word:
					if re.match(user_pattern, previous_word):
						precedents['user_name'] += 1
					else:
						precedents[previous_word] += 1
				previous_word = word
	return precedents.most_common(num_precedents)

def show_most_common_context(freq_diff_counter, first_category, second_category):
	print 
	print "The following words are used more by " + first_category + " than by " + second_category
	for item in freq_diff_counter:
		word = item[0]
		count = item[1]
		first_precedents = most_common_precedents(word, first_category)
		second_precedents = most_common_precedents(word, second_category)
		print 
		print first_category + " uses the word '" + word + "' " + str(count) + " more than " + second_category
		print first_category + " uses the word with the following words most " + str(first_precedents)
		print second_category + " uses the word with the following words most " + str(second_precedents)

fileids_list = nps_chat.fileids()
fid = {"20s":[], "30s":[], "40s":[],"adu":[],"tee":[]}

for f_id in fileids_list:
	tag = f_id[6:9]
	fid[tag].append(f_id)

young_and_old = {"young": fid["tee"]+fid["20s"] , "old": fid["30s"]+fid["40s"]+fid["adu"]}


(young_word_freq, young_words) = word_freq("young", True)
(old_word_freq, old_words) = word_freq("old", True)

old_more_than_young = freq_diff(old_word_freq, young_word_freq)

show_most_common_context(old_more_than_young, 'old', 'young')

young_more_than_old = freq_diff(young_word_freq, old_word_freq)

show_most_common_context(young_more_than_old, 'young', 'old')





