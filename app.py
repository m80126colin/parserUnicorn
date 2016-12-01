import os, json, io, csv
import bottle, flask
from unicorn import *
from bottle import Bottle, route, view

app = Bottle()

@app.route('/hello/<name>')
def index(name):
	return bottle.template('<b>Hello {{name}}</b>!', name = name)

@app.route('/cloud')
@view('cloud')
def cloud_GET():
	return dict()

@app.route('/parser')
@view('parser')
def parser_GET():
	return dict()

@app.route('/cloud', method = 'POST')
def cloud_POST():
	data = bottle.request.json
	res  = clouds.makeCloud(data)
	return json.dumps(res)

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
	data = bottle.request.query
	print(data)
	if 'token' in data:
		parser.setToken(data.get('token'))

	res  = parser.getAllComments(nodeId)
	filename = '%s.csv' % nodeId
	print('Filename:', filename)

	path    = os.path.join('.', 'tmp')
	if not os.path.exists(path):
		os.makedirs(path)

	csvfile = open(os.path.join(path, filename), 'w', encoding = 'utf-8')

	data      = res.get('data')
	if len(data) > 0:
		writer = csv.DictWriter( csvfile, sorted(data[0].keys()) )
		writer.writeheader()
		for row in data:
			writer.writerow(row)
	csvfile.close()
	return bottle.static_file(filename, root = path, download = filename)

# static files

@app.route('/public/<filename:path>')
def staticFiles(filename):
	path = os.path.join('.', 'public')
	return bottle.static_file(filename, root = path)

bottle.run(app, host = 'localhost', port = 5566)