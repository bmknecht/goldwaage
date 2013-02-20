import codecs

from jinja2 import Environment, PackageLoader

def __generate_fulltext_html(text, env):
	template = env.get_template('fulltext.html')

	with codecs.open('fulltext.html', mode='w', encoding='utf-8') as f:
		f.write(template.render(fulltext=text.replace('\n','<br>')))

def __annihilate_zero_weights(words_and_weights):
	return { word:weight for word,weight in words_and_weights.items() if weight > 0 }

def __generate_wordlist_html(words_and_weighted_frequencies, env):
	template = env.get_template('wordlist.html')
	
	with codecs.open('wordlist.html', mode='w', encoding='utf-8') as f:
		f.write(template.render(words_and_frequencies={
			word:max(weights) for word,weights in words_and_weighted_frequencies.items()} ))

def generatehtml(words_and_weighted_frequencies, text):
	env = Environment(loader=PackageLoader('goldwaage', 'templates'))
	env.filters['drop_boring_entries'] = __annihilate_zero_weights

	__generate_fulltext_html(text, env)
	__generate_wordlist_html(words_and_weighted_frequencies, env)
	
