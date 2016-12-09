import jieba, os

path  = os.path.dirname(os.path.realpath(__file__))
file  = os.path.join(path, 'stopwords.txt')

sw    = [ line.rstrip() for line in open(file, 'r', encoding = 'utf-8') ]
sw[0] = sw[0][1:]

stopwords = {}.fromkeys(sw)

def __wordCounts__(xs):
	res = dict()
	for x in xs:
		if x not in res:
			res[x] = 0
		res[x] = res[x] + 1
	return res

def wordCount(strList, maxFont = 48, minFont = 10):
	tokens    = [ x
		for strs in strList
		for x in jieba.cut(strs)
		if x not in stopwords ]
	total     = len(tokens)

	# count words
	countDict = __wordCounts__(tokens)

	res       = []
	for tok in countDict:
		# fontSize = countDict[tok] * (maxFont - minFont) / total + minFont
		fontSize = countDict[tok]
		res.append([tok, fontSize])

	return res