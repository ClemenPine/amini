import re

from discord import Message

from util import corpora, parser

RESTRICTED = False

def exec(message: Message):
	id = message.author.id
	ngram = parser.get_arg(message)

	lengram = len(ngram)

	if lengram < 1 or lengram > 3:
		return "Please specify an ngram between 1-3 chars"

	ngrams = corpora.ngrams(lengram, id=id)
	corpus = corpora.get_corpus(id)

	pattern = re.compile(ngram.replace('.', '\.').replace('_', '.'))
	number = sum(value for key, value in ngrams.items() if pattern.search(key))
	
	if number == 0:
		return f"`{ngram}` not found in corpus `{corpus}`"

	total = sum(ngrams.values())

	return f"`{ngram}` occurs in {number / total:.2%} of `{corpus}`"
	