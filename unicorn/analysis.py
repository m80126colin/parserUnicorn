import jieba, os
from os import path

_dict_path = path.join(path.dirname(path.realpath(__file__)), 'dictionary')

# setting jieba
jieba.set_dictionary( path.join(_dict_path, 'dict.txt.big') )
jieba.load_userdict( path.join(_dict_path, 'mydict.txt') )

# load stop words
def __loadStopwords__(filename):
	file  = path.join(_dict_path, filename)
	sw    = [ line.rstrip() for line in open(file, 'r', encoding = 'utf-8') ]
	sw[0] = sw[0][1:]
	return {}.fromkeys(sw)

stopwords = __loadStopwords__('stopwords.txt')

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

	return sorted(res, key = lambda x : -x[1])

def make_dict(lst, wc):
	res = dict()
	for w in lst:
		res[w] = 0

	for it in wc:
		res[ it[0] ] = it[1]

	return res

def ano_make_dict(lst, tbl):
	res = []
	tmp = dict()
	for idx in range(len(lst)):
		tmp[idx] = lst[idx]
	res.append(tmp)

	for x in tbl:
		tmp = dict()
		for idx in range(len(lst)):
			tmp[idx] = x.get(lst[idx])
		res.append(tmp)

	return res

def countField(tbl, f):
	return sum([
		1 if row.get(f) > 0 else 0
		for row in tbl ])

def sumField(tbl, f):
	return sum([ row.get(f) for row in tbl ])

def sumFieldIf(tbl, f1, f2):
	return sum([
		min([row.get(f1), row.get(f2)])
		for row in tbl
		if row.get(f2) > 0 ])

def apriori(dataset):
	selects = [
		sorted(x, key = lambda it : -it[1])[0:50]
		for x in dataset ]

	word_list = list()
	for x in selects:
		word_list = list(set(word_list) | set([ y[0] for y in x ]))

	def_dict = dict()
	for word in word_list:
		def_dict[word] = 0

	table = [ make_dict(word_list, x) for x in dataset ]

	another_table = ano_make_dict(word_list, table)

	gen = [ dict(
		itema     = wa,
		itemb     = wb,
		support   = round(countField(table, wa) / len(table), 2),
		confident = round(sumFieldIf(table, wa, wb) / sumField(table, wa), 2)
		) for (wa, wb) in itertools.combinations(word_list, 2) if sumField(table, wa) > 0 ]

	res = sorted(gen, key = lambda x : - (x.get('support') + x.get('confident')) )

	return dict(table = another_table, result = res)