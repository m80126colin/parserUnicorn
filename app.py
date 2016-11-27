import os, json, bottle
from unicorn import *
from bottle import route, view

@route('/hello/<name>')
def index(name):
	return bottle.template('<b>Hello {{name}}</b>!', name = name)

@route('/cloud')
@view('cloud')
def cloud():
	return dict()

@route('/cloud', method = 'POST')
def wordCloud():
	data = bottle.request.json
	print(type(data[0]))
	print(data)
	res  = clouds.makeCloud(data)
	return json.dumps(res)

# static files

@route('/public/<filename:path>')
def send_static(filename):
	path = os.path.join('.', 'public')
	print(path)
	return bottle.static_file(filename, root = path)

bottle.run(host = 'localhost', port = 5566)