import re

from discord import Message

from util import corpora, parser

RESTRICTED = True

def exec(message: Message):
	id = message.author.id
	query = parser.get_args(message)

	ntype = len(query[0]) if len(query) > 0 else None

	if not query or ntype < 1 or ntype > 3:
		return "Please provide at least 1 ngram between 1-3 chars"

	if len(query) > 5:
		return "Please provide no more than 5 ngrams"

	ngrams = corpora.ngrams(ntype, id=id)
	corpus = corpora.get_corpus(id)

	count = 0
	for item in query:
		if len(item) != ntype:
			return "All ngrams must be same length"
		pattern = re.compile(item.replace('.', '\.').replace('_', '.'))
		count += sum(value for key, value in ngrams.items() if pattern.search(key))
	
	if count == 0:
		return f"`{' '.join(query)}` not found in corpus `{corpus}`"

	total = sum(ngrams.values())

	return f"`{' '.join(query)}` occur in {count / total:.2%} of `{corpus}`"
	
