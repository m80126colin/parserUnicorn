import jieba, os
from os import path
import itertools

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

def intersect(dataset, limit):
	print('[Intersect] Start processing intersect ...')
	# unique id list
	id_list    = [ [key, len(list(group))]
		for key, group in itertools.groupby(
			sorted([ x for data in dataset for x in data ]))
	]
	# dictionary for id
	size       = len(id_list)
	id_dict    = dict()
	for i in range(size):
		id_dict[ id_list[i][0] ] = i
	# translate dataset into id
	id_dataset = [ [ id_dict[x] for x in data ] for data in dataset ]
	# calulate intersection between data
	print('[Intersect] Start calculating intersection ...')
	size          = len(id_dataset)
	article_count = [ len(data) for data in dataset ]
	article       = [ [
		len(list(set(id_dataset[i]) & set(id_dataset[j])))
		for j in range(size) ]
		for i in range(size) ]
	#
	print('[Intersect] Start calculating intersect between people ...')
	## valid id list
	valid_id_list = [ x
		for x in sorted(id_list, key = lambda x : -x[1])
		if x[1] > 1
	]
	peo_list = [ id_dict[ x[0] ] for x in valid_id_list[:limit] ]
	size     = len(peo_list)
	people   = [ [
			[ k for k in range(len(id_dataset))
				if peo_list[i] in id_dataset[k]
					and peo_list[j] in id_dataset[k]
			] if i is not j else []
		for j in range(size) ]
		for i in range(size) ]
	print('[Intersect] Done!')
	# return
	return dict(
		list          = id_list,
		article       = article,
		article_count = article_count,
		people        = people,
		peo_list      = peo_list)

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