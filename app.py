import os, json, io, csv, hashlib
import bottle
from unicorn import *
from os import path
from bottle import Bottle, route, view

# utils

def mkpath(*paths):
	dirs = ''
	for p in paths:
		dirs = path.join(dirs, p)
		if not path.exists(dirs):
			os.makedirs(dirs)
	return dirs

# app

app = Bottle()

# GET route

@app.route('/')
@view('index')
def index_GET():
	return dict()

@app.route('/cloud')
@view('cloud')
def cloud_GET():
	res  = []
	link = ''
	return dict(list = res, link = link)

@app.route('/parser')
@view('parser')
def parser_GET():
	return dict()

# cloud route

@app.route('/cloud', method = 'POST')
@view('cloud')
def cloud_POST():
	data = bottle.request.files.get('data')
	raw  = [ line.decode() for line in data.file.readlines() ]
	# word count
	res  = clouds.wordCount(raw)
	# md5
	m = hashlib.md5()
	m.update( repr(res).encode() )
	# make csv
	dirs = mkpath('.', 'tmp', 'wordcount')
	file = '%s.csv' % m.hexdigest()
	# write csv
	csvfile = open(path.join(dirs, file), 'w', encoding = 'utf-8')
	writer  = csv.writer(csvfile)
	for row in res:
		writer.writerow(row)
	csvfile.close()
	# return
	link = '/wordcount/' + file
	return dict(list = json.dumps(res), link = link)

# parser routes

parser = comments.Comments()

@app.route('/allposts', method = 'POST')
def allposts_POST():
	data = bottle.request.json
	if 'token' in data:
		parser.setToken(data.get('token'))

	res = parser.getAllPosts(data)
	return json.dumps(res)

@app.route('/allcomments/<nodeId>', method = 'GET')
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

# static files

@app.route('/public/<file:path>')
def staticFiles(file):
	dirs = path.join('.', 'public')
	return bottle.static_file(file, root = dirs)

@app.route('/wordcount/<file:path>')
def wordCountFiles(file):
	dirs = mkpath('.', 'tmp', 'wordcount')
	return bottle.static_file(file, root = dirs, download = file)

# run server at localhost:5566

bottle.run(app, host = 'localhost', port = 5566)