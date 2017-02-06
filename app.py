import bottle, json, csv
from bottle import Bottle, route
from os import path
import unicorn as uni

######################################################################
#
#  configs
#
######################################################################

# server hostname and port
_host = 'localhost'
_port = 5566

# root url of api server
_api_root  = '/api'

# folder for wordcount and association rule
_wc_folder = 'wordcount'
_as_folder = 'apriori'
_cm_folder = 'comment'

_wc_paths  = ['.', 'tmp', _wc_folder]
_as_paths  = ['.', 'tmp', _as_folder]
_cm_paths  = ['.', 'tmp', _cm_folder]

# initialization

## directory for wordcount and association rule
_wc_dirs   = uni.utiltools.mkpath(*_wc_paths)
_as_dirs   = uni.utiltools.mkpath(*_as_paths)
_cm_dirs   = uni.utiltools.mkpath(*_cm_paths)

## parser
parser = uni.comments.Comments()

######################################################################
#
#  api
#
######################################################################

api = Bottle()

# apiPath
def apiPath(*p):
	return '%s/%s' % ( _api_root, '/'.join(p) )

# word count by data
def wordCountData(data):
	raw = [ line.decode().strip() for line in data.file.readlines() ]
	# word count
	return uni.analysis.wordCount(raw)

# cloud route

@api.route('/cloud', method = 'POST')
def cloud_POST():
	data   = bottle.request.files.get('data')
	res    = wordCountData(data)
	# write into csv
	file   = uni.utiltools.writeCsv(res, _wc_paths)
	# return
	return dict(
		list = json.dumps(res),
		link = apiPath(_wc_folder, file)
	)


@api.route('/associ', method = 'POST')
def associ_POST():
	files   = bottle.request.files
	dataset = [ wordCountData(files.get(file)) for file in files ]
	# apriori
	res     = uni.analysis.apriori(dataset)
	# make csv
	file    = uni.utiltools.writeCsvDict(res.get('table'), _as_paths)
	file2   = uni.utiltools.writeCsvDict([ x
		for x in res.get('result')
		if x.get('support') >= 0.5 and x.get('confident') >= 0.5 ]
		, _as_paths)
	# return
	return dict(
		list  = json.dumps(res.get('result')[0:500]),
		link  = apiPath(_as_folder, file),
		link2 = apiPath(_as_folder, file2)
	)

# parser routes


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
	file = writeCsvDict(res.get('data'), filename = '%s.csv' % nodeId)
	# return downloadable file
	return bottle.static_file(file, root = _cm_dirs, download = file)

# word count file

@api.route('/%s/<file:path>' % _wc_folder, method = 'GET')
def wordcountFiles(file):
	return bottle.static_file(file, root = _wc_dirs, download = file)

@api.route('/%s/<file:path>' % _as_folder, method = 'GET')
def aprioriFiles(file):
	return bottle.static_file(file, root = _as_dirs, download = file)

######################################################################
#
#  app
#
######################################################################

app = Bottle()

# index html
@app.route('/')
def appRoot():
	dirs = path.join('.', 'dist')
	file = 'index.html'
	return bottle.static_file(file, root = dirs)

# 
@app.route('/static/<file:path>')
def appStaticFile(file):
	dirs = path.join('.', 'dist', 'static')
	return bottle.static_file(file, root = dirs)

# mount api server at _api_root
app.mount(_api_root, api)

# run app server at localhost:5566
bottle.run(app, host = _host, port = _port)