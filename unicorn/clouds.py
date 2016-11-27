import jieba

def makeCloud(strList, maxFont = 48, minFont = 10):
	res       = []
	countDict = dict()
	tokens    = [ x for strs in strList for x in jieba.cut(strs) ]
	total     = len(tokens)

	for tok in tokens:
		if tok not in countDict:
			countDict[tok] = 0
		countDict[tok] = countDict[tok] + 1

	for tok in countDict:
		fontSize = countDict[tok] * (maxFont - minFont) / total + minFont
		res.append([tok, fontSize])

	return res