#!/usr/bin/python
import codecs
import sys
import argparse
import re

def collectwords(text):
	return set(text.split())
	
def countwords(text):
	dc = {}
	for word in collectwords(text):
		if word in dc:
			dc[word] += 1
		else:
			dc[word] = 1
	
	return dc

def chooseword(text):
	chosenword = sorted(countwords(text.lower()).items(), key=lambda x: x[1])[0]
	print(type(chosenword[0]))
	print(type(u'chosen word: {w}, occurences: {o}'))
	print(chosenword[0], chosenword[1])
	print(u'chosen word: {w}, occurences: {o}'.format(w=chosenword[0], o=chosenword[1]))
	return chosenword[0]

def analyzetext(text, wlen, steplen):
	splittext = text.lower().split()
	wdict = { word:[] for word in collectwords(text) }

	for i in xrange(0, wlen+len(splittext), steplen):
		window = splittext[max(i-wlen,0):i]
		for w, d in wdict.items():
			d.append(window.count(w))
	return wdict

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
	        description='zaehlt vorkomnisse des wortes')
	parser.add_argument('textfile')
	parser.add_argument('command', choices=['list', 'analyze'])
	parser.add_argument('-w', '--word')
	parser.add_argument('-l', '--wlength', default=10, type=int)
	parser.add_argument('-s', '--steplen', default=1, type=int)
	args = parser.parse_args()

	if args.steplen >= args.wlength:
		raise ValueError('window length must be greater than step width')
	
	text = codecs.open(args.textfile, encoding='utf-8').read()
	cleantext = re.sub(u'[^a-zA-Z\xdc\xfc\xe4\xc4\xf6\xd6\n ]',u'',text)
	if args.command == 'analyze':

		wdict = analyzetext(
				cleantext,
				args.wlength,
				args.steplen)
		
		word_to_analyze = args.word.lower() if args.word else chooseword(cleantext)
			
		for i,v in enumerate(wdict[word_to_analyze]):
			print(str(i)+':'+'#'*v)
	elif args.command == 'list':
		words = collectwords(cleantext)
		
		for w in sorted(words, key=unicode.lower):
			print(w) 
		

