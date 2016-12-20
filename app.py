import os, json, io, csv, hashlib
import bottle
from unicorn import *
from os import path
from bottle import Bottle, route
import itertools

# configs

__api_root__ = '/api'

# utils

def mkpath(*paths):
	dirs = ''
	for p in paths:
		dirs = path.join(dirs, p)
		if not path.exists(dirs):
			os.makedirs(dirs)
	return dirs

def make_dict(lst, wc):
	res = dict()
	for w in lst:
		res[w] = 0

	for it in wc:
		res[ it[0] ] = it[1]

	return res

def countField(tbl, f):
	return sum([ 1 if row.get(f) > 0 else 0 for row in tbl ])

def sumField(tbl, f):
	return sum([ row.get(f) for row in tbl ])

def sumFieldIf(tbl, f1, f2):
	return sum([ min([row.get(f1), row.get(f2)]) for row in tbl if row.get(f2) > 0 ])

def apriori(dataset):
	selects = [ sorted(x, key = lambda it : -it[1])[0:1000] for x in dataset ]

	word_list = list()
	for x in selects:
		word_list = list(set(word_list) | set([ y[0] for y in x ]))

	def_dict = dict()
	for word in word_list:
		def_dict[word] = 0

	table = [ make_dict(word_list, x) for x in dataset ]

	gen = [ dict(
		itema     = wa,
		itemb     = wb,
		support   = countField(table, wa) / len(table),
		confident = sumFieldIf(table, wa, wb) / sumField(table, wa)
		) for (wa, wb) in itertools.combinations(word_list, 2) if sumField(table, wa) > 0 ]

	res = sorted(gen, key = lambda x : - (x.get('support') + x.get('confident')) )

	return dict(table = table, result = res)

# api

api = Bottle()

# write a csv file with md5 filename

def writeWordCountCsv(data):
	# md5
	m = hashlib.md5()
	m.update( repr(data).encode() )
	# make csv
	dirs = mkpath('.', 'tmp', 'wordcount')
	file = '%s.csv' % m.hexdigest()
	# write csv
	csvfile = open(path.join(dirs, file), 'w', encoding = 'utf-8')
	writer  = csv.writer(csvfile)
	for row in data:
		writer.writerow(row)
	csvfile.close()
	# return filename
	return file

# word count by data
def wordCountData(data):
	raw = [ line.decode() for line in data.file.readlines() ]
	# word count
	res  = clouds.wordCount(raw)
	return res

# cloud route

@api.route('/cloud', method = 'POST')
def cloud_POST():
	data = bottle.request.files.get('data')
	res  = wordCountData(data)
	# write into csv
	file = writeWordCountCsv(res)
	# return
	link = __api_root__ + '/wordcount/' + file
	return dict(list = json.dumps(res), link = link)


def writeCsvDict(res):
	# md5
	m = hashlib.md5()
	m.update( repr(res).encode() )
	# make csv
	dirs = mkpath('.', 'tmp', 'apriori')
	file = '%s.csv' % m.hexdigest()
	# write csv
	csvfile = open(path.join(dirs, file), 'w', encoding = 'utf-8')
	# write data into csv
	data = res
	if len(data) > 0:
		writer = csv.DictWriter( csvfile, sorted(data[0].keys()) )
		writer.writeheader()
		for row in data:
			writer.writerow(row)
	csvfile.close()
	# return filename
	return file

@api.route('/associ', method = 'POST')
def associ_POST():
	files = bottle.request.files
	dataset = [ wordCountData(files.get(file)) for file in files ]
	# apriori
	res = apriori(dataset)
	# make csv
	file  = writeCsvDict(res.get('table'))
	file2 = writeCsvDict(res.get('result'))
	# return
	link  = __api_root__ + '/apriori/' + file
	link2 = __api_root__ + '/apriori/' + file2
	return dict(list = json.dumps(res.get('result')[0:500]), link = link, link2 = link2)

# parser routes

parser = comments.Comments()

@api.route('/allposts', method = 'POST')
def allposts_POST():
	data = bottle.request.json
	if 'token' in data:
		parser.setToken(data.get('token'))

	res = parser.getAllPosts(data)
	return json.dumps(res)

# all comments file

@api.route('/allcomments/<nodeId>', method = 'GET')
def allcomments_GET(nodeId):
	# get data
	data = bottle.request.query
	print(data)

	# retrieve token
	if 'token' in data:
		parser.setToken(data.get('token'))

	# get comments
	res  = parser.getAllComments(nodeId)

	# make path and filename of csv
	dirs = mkpath('.', 'tmp', 'comment')
	file = '%s.csv' % nodeId
	print('Filename:', file)

	csvfile = open(path.join(dirs, file), 'w', encoding = 'utf-8')
	# write data into csv
	data = res.get('data')
	if len(data) > 0:
		writer = csv.DictWriter( csvfile, sorted(data[0].keys()) )
		writer.writeheader()
		for row in data:
			writer.writerow(row)
	csvfile.close()

	# return downloadable file
	return bottle.static_file(file, root = dirs, download = file)

# word count file

@api.route('/wordcount/<file:path>', method = 'GET')
def wordCountFiles(file):
	dirs = mkpath('.', 'tmp', 'wordcount')
	return bottle.static_file(file, root = dirs, download = file)

@api.route('/apriori/<file:path>', method = 'GET')
def aprioriFiles(file):
	dirs = mkpath('.', 'tmp', 'apriori')
	return bottle.static_file(file, root = dirs, download = file)

# app

app = Bottle()

@app.route('/static/<file:path>')
def appStaticFile(file):
	dirs = path.join('.', 'dist', 'static')
	return bottle.static_file(file, root = dirs)

@app.route('/')
def appRoot():
	dirs = path.join('.', 'dist')
	file = 'index.html'
	return bottle.static_file(file, root = dirs)

app.mount(__api_root__, api)

# run app server at localhost:5566
bottle.run(app, host = 'localhost', port = 5566)