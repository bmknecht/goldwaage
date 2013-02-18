#!/usr/bin/python
import codecs
import sys
import argparse

def collectwords(text):
	return set(text.split())
	
def countwords(text):
	dc = {}
	for word in text:
		if word in dc:
			dc[word] += 1
		else:
			dc[word] = 1
	
	return dc

def analyzetext(text, wlen):
	splittext = text.split()
	wdict = { word:[] for word in collectwords(text) }

	for i in xrange(wlen+len(splittext)):
		window = splittext[max(i-wlen,0):i]
		for w, d in wdict.items():
			d.append(window.count(w))
	return wdict

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
	        description='zaehlt vorkomnisse des wortes')
	parser.add_argument('textfile')
	parser.add_argument('-w', '--word')
	parser.add_argument('-l', '--wlength', default=1, type=int)
	args = parser.parse_args()
	
	text = codecs.open(args.textfile, encoding='utf-8').read()
	if args.word:
		wdict = analyzetext(
				text,
				args.wlength)

		for v in wdict[args.word]:
			print('#'*v)
	else:
		words = collectwords(text)
		
		for w in sorted(words):
			print(w) 
		

