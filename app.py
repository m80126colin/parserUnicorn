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
class _api:
	root      = 'api'
	download  = 'download'

	post      = 'post'
	intersect = 'intersect'

	@staticmethod
	def url(*p):
		return '/%s/%s' % (_api.root, '/'.join(p))

	@staticmethod
	def dl_url(*p):
		return _api.url(_api.download, *p)

	@staticmethod
	def dl_path(*p):
		return ['.', _api.download] + list(p)

	@staticmethod
	def dl_file(*p):
		return path.join( _api.dl_path(*p) )

# folder for wordcount and association rule
_wc_folder = 'wordcount'
_as_folder = 'apriori'
_cm_folder = 'comment'

_path_download   = ['.', 'downloads']
_folder_download = path.join(*_path_download)

_wc_paths  = ['.', 'tmp', _wc_folder]
_as_paths  = ['.', 'tmp', _as_folder]
_cm_paths  = ['.', 'tmp', _cm_folder]
_dl_paths  = ['.', 'downloads']

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
		link = _api.url(_wc_folder, file)
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
		if x.get('support') >= 0.5 and x.get('confident') >= 0.5
		], _as_paths)
	# return
	return dict(
		list  = json.dumps(res.get('result')[0:500]),
		link  = _api.url(_as_folder, file),
		link2 = _api.url(_as_folder, file2)
	)

# parser routes

@api.route('/allposts', method = 'POST')
def allposts_POST():
	data = bottle.request.json
	res  = uni.fbgraph.getAllPosts(data, data.get('token'))
	# return
	return json.dumps(res)

######################################################################
#  intersect route
######################################################################

def lineData(data):
	raw = [ line.decode().strip() for line in data.file.readlines() ]
	return raw

@api.route('/intersect', method = 'POST')
def api_POST_intersect():
	files   = bottle.request.files
	limit   = int(bottle.request.params.limit)
	# dataset
	dataset = [ lineData(files.get(file)) for file in files ]
	# calculate intersection
	result  = uni.analysis.intersect(dataset, limit)
	# make csv
	people  = [ result.get('list')[idx][0] for idx in result.get('peo_list') ]
	## make data
	data    = []
	data.append(['#'] + people)
	size    = len(people)
	for i in range(size):
		tmp = [ people[i] ]
		for j in range(size):
			tmp.append( len(result.get('people')[i][j]) )
		data.append(tmp)
	# write csv
	file    = uni.utiltools.writeCsv(data, _api.dl_path(_api.intersect))
	# make data
	data    = []
	size    = len(people)
	for i in range(size):
		for j in range(size):
			tmp = result.get('people')[i][j]
			data.append([ people[i], people[j], len(tmp) ] + tmp)
	# write csv
	file2   = uni.utiltools.writeCsv(data, _api.dl_path(_api.intersect))
	# return
	return json.dumps(dict(
		link    = _api.dl_url(_api.intersect, file),
		link2   = _api.dl_url(_api.intersect, file2),
		article = result.get('article'),
		count   = result.get('article_count')
	))

######################################################################
#  post route
######################################################################

# post id

@api.route('/post/id', method = 'POST')
def api_POST_post_id():
	data   = bottle.request.json
	args   = [ data.get('url'), data.get('token') ]
	# get posts id
	postid = uni.fbgraph.getPostFullId(*args)
	# return
	return json.dumps( dict(postid = postid) )

## post shares

@api.route('/post/shares', method = 'POST')
def api_POST_post_shares():
	data  = bottle.request.json
	args  = [ data.get('postid'), data.get('token') ]
	# get shares
	res   = uni.fbgraph.node.shares(*args)
	count = res.get('shares').get('count')
	# return
	return json.dumps( dict(count = count) )

## post likes

@api.route('/post/likes', method = 'POST')
def api_POST_post_likes():
	data = bottle.request.json
	# get likes
	nodeid = data.get('postid')
	res    = uni.fbgraph.node.likes(nodeid, data.get('token'))
	# write csv
	rec    = [ [x] for x in res.get('likes') ]
	file   = '%s_likes.csv' % nodeid
	uni.utiltools.writeCsv(rec, _api.dl_path(_api.post), file)
	# return
	return json.dumps(dict(
		link  = _api.dl_url(_api.post, file),
		count = len(res.get('likes'))
	))

## post comments

@api.route('/post/comments', method = 'POST')
def api_POST_post_comments():
	data   = bottle.request.json
	# get comments
	nodeid = data.get('postid')
	res    = uni.fbgraph.node.comments(nodeid, data.get('token'))
	# write csv
	rec    = res.get('comments')
	file   = '%s_comments.csv' % nodeid
	uni.utiltools.writeCsvDict(rec, _api.dl_path(_api.post), file)
	# return
	return json.dumps(dict(
		link  = _api.dl_url(_api.post, file),
		count = len(res.get('comments'))
	))

######################################################################
#  all comments route
######################################################################

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
	file = uni.utiltools.writeCsvDict(
		res.get('data'),
		_cm_paths,
		'%s.csv' % nodeId)
	# return downloadable file
	return bottle.static_file(file, root = _cm_dirs, download = file)

######################################################################
#  word count file
######################################################################

@api.route('/%s/<file:path>' % _wc_folder, method = 'GET')
def wordcountFiles(file):
	return bottle.static_file(file, root = _wc_dirs, download = file)

@api.route('/%s/<file:path>' % _as_folder, method = 'GET')
def aprioriFiles(file):
	return bottle.static_file(file, root = _as_dirs, download = file)

@api.route('/%s/<paths:path>' % _api.download, method = 'GET')
def api_download_file(paths):
	dirs = _api.dl_path( *paths.split('/') )
	folder, file = path.join(*dirs[:-1]), dirs[-1]
	return bottle.static_file(file, root = folder, download = file)

######################################################################
#
#  app
#
######################################################################

app = Bottle()

@app.route('/')
def app_index():
	dirs = path.join('.', 'dist')
	file = 'index.html'
	return bottle.static_file(file, root = dirs)

@app.route('/static/<file:path>')
def app_static_file(file):
	dirs = path.join('.', 'dist', 'static')
	return bottle.static_file(file, root = dirs)

# setup api

app.mount(_api.root, api)

# run app server at localhost:5566
bottle.run(app, host = _host, port = _port)