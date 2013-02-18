#!/usr/bin/python
import codecs
import sys
import argparse

def analyzeword(text, word, wlen):
	words = text.split()
	l = []
	for i in xrange(wlen+len(words)):
		l.append(words[max(i-wlen,0):i].count(word))

	return l

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
	        description='zaehlt vorkomnisse des wortes')
	parser.add_argument('textfile')
	parser.add_argument('word')
	parser.add_argument('-w', '--wlength', default=1, type=int)
	args = parser.parse_args()
	
	l = analyzeword(
		codecs.open(args.textfile, encoding='utf-8').read(),
		args.word,
		args.wlength)

	for v in l:
		print('#'*v)

