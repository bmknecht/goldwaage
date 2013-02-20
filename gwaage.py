#!/usr/bin/python
import codecs
import sys
import argparse
import re
from goldwaage import output

def uprint(text):
	if isinstance(text, unicode):
		print(text.encode('utf-8'))
	else:
		print(text)

def collectwords(text):
	return set(text.split())
	
def countwords(text):
	dc = {}
	for word in text.split():
		if word in dc:
			dc[word] += 1
		else:
			dc[word] = 1
	
	return dc

def get_weighted_frequencies(freqs_per_word, text, windowwidth):
	wweight = {}
	print('adding weights...')
	for word,freq_per_window in freqs_per_word.items():
		freqsum = sum(freq_per_window)
		wweight[word] = []
		for freq in freq_per_window:
			weight = float(windowwidth)/freqsum
			wweight[word].append((freq-1)*weight)
	
	return wweight

def get_frequencies_per_word(text, wlen, steplen):
	print('analyzing...')

	splittext = text.lower().split()
	wdict = { word:[] for word in collectwords(text.lower()) }
	
	for i in xrange(0, wlen+len(splittext), steplen):
		window = splittext[max(i-wlen,0):i]
		print "\r{p}%".format(p=int(float(i)/(wlen+len(splittext))*100)),
		sys.stdout.flush()
		for w, d in wdict.items():
			d.append(window.count(w))
	print()
	return wdict

def analyzetext(cleantext, wlength, steplen):
	wdict = get_frequencies_per_word(
			cleantext,
			wlength,
			steplen)
	
	return get_weighted_frequencies(wdict, cleantext, wlength)
	

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
	        description='zaehlt vorkomnisse des wortes')
	parser.add_argument('command', choices=['list', 'analyze', 'full'])
	parser.add_argument('textfile')
	parser.add_argument('-w', '--word')
	parser.add_argument('-l', '--wlength', default=10, type=int)
	parser.add_argument('-s', '--steplen', default=1, type=int)
	args = parser.parse_args()

	if args.steplen >= args.wlength:
		raise ValueError('window length must be greater than step width')
	
	text = codecs.open(args.textfile, encoding='utf-8').read()
	print('cleaning...')
	cleantext = re.sub(u'[^a-zA-Z\xdc\xfc\xe4\xc4\xf6\xd6\n ]',u'',text)

	if args.command == 'analyze':
		weighted_frequency_per_word = analyzetext(cleantext, args.wlength, args.steplen)

		if args.word:
			uprint(u'{f}'.format(f=weighted_frequency_per_word[args.word]))
		else:
			print('creating word-and-weight-list...')
			weight_word_list = []
			for word,freqs in weighted_frequency_per_word.items():
				for freq in freqs:
					if freq > 0:
						weight_word_list.append((word,freq))
	
			print('sorting list...')
			sorted_ww_list = sorted(weight_word_list, key=lambda x: x[1])		

			for word,freq in sorted_ww_list[-5:]:
				uprint(u'{w},{f}'.format(w=word, f=freq))
	elif args.command == 'full':
		weighted_frequency_per_word = analyzetext(cleantext, args.wlength, args.steplen)
		output.generatehtml(weighted_frequency_per_word, text)

	elif args.command == 'list':
		words = collectwords(cleantext)
		
		for w in sorted(words, key=unicode.lower):
			uprint(w) 

