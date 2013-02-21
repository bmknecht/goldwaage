#!/usr/bin/python
'''analyzes a given unicode text from a file to find wrong usage
of multiple words by approximity'''

import argparse


from goldwaage import analyze, output, parser


def uprint(text):
    '''force unicode output, avoid errors when piping to "less"'''
    if isinstance(text, unicode):
        print(text.encode('utf-8'))
    else:
        print(text)


def parsearguments():
    '''parse, validate and return arguments'''
    argparser = argparse.ArgumentParser(
        description='zaehlt vorkomnisse des wortes')
    argparser.add_argument('command', choices=['list', 'full'])
    argparser.add_argument('textfile')
    argparser.add_argument('-w', '--word')
    argparser.add_argument('-l', '--wlength', default=30, type=int)
    argparser.add_argument('-s', '--steplen', default=1, type=int)
    args = argparser.parse_args()

    if args.steplen >= args.wlength:
        raise ValueError('window length must be greater than step width')

    return args


def processarguments(cleantext, args):
    '''choose algorithm by command line arguments'''
    if args.command == 'full':
        weighted_frequency_per_word = analyze.analyzetext(
            cleantext, args.wlength, args.steplen)
        output.generatehtml(weighted_frequency_per_word)

    elif args.command == 'list':
        words = parser.collectwords(cleantext)

        for word in sorted(words, key=unicode.lower):
            uprint(word)


def _main():
    '''main function for direct execution'''
    args = parsearguments()
    cleantext, _ = parser.readtext(args)

    processarguments(cleantext, args)


if __name__ == '__main__':
    _main()
