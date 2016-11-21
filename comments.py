import sys
import requests
import json
from urllib import parse

def __log__(message, mode = 'debug'):
	if mode == 'log':
		print(message, file = sys.stderr)

class Comments:

	# constructor

	def __init__(self, token = '', limit = 500):
		self.token = token
		self.limit = limit

	# private methods

	def __graphAPICall__(self, node, version = '2.8', **args):
		# set token
		args.setdefault('access_token', self.token)
		# graph API
		api = 'https://graph.facebook.com/v%s/%s?%s'
		url = api % (version, node, parse.urlencode(args))
		__log__('[GraphAPI] Url: %s' % url)
		# send request
		res = requests.get(url)
		if res.status_code == requests.codes.ok:
			__log__('[GraphAPI] API call success!')
			return json.loads(res.text)
		else:
			__log__('[GraphAPI] Error. Status code: %d' % res.status_code)
		return None

	def __retrieveUrl__(self, url):
		sp = [ x for x in parse.urlsplit(url).path.split('/') if x != '' ]
		if len(sp) < 2:
			__log__('[Retrieve] Invalid Url: %s' % url)
			return None
		return sp[0], sp[-1]

	def __getPageIdByName__(self, name):
		res = self.__graphAPICall__(name)
		__log__(res)
		return res.get('id')

	def __hasNext__(self, obj):
		return ('paging' in obj) and ('next' in obj['paging'])

	def __getAfter__(self, obj):
		return obj.get('paging').get('cursors').get('after')

	def __getDataWithPaging__(self, node, **args):
		args.setdefault('limit', self.limit)
		res = self.__graphAPICall__(node, **args)
		yield res.get('data')
		while self.__hasNext__(res):
			args['after'] = self.__getAfter__(res)
			res   = self.__graphAPICall__(node, **args)
			yield res.get('data')

	def __getSummary__(self, nodeId):
		fld   = 'comment_count'
		node  = '%s/comments' % nodeId
		res   = self.__graphAPICall__(node, fields = fld, summary = 1)
		lists = [ x
			for ls in self.__getDataWithPaging__(node, fields = fld)
			for x in ls
			if x.get(fld) > 0 ]
		lists.append( dict(
			comment_count = res.get('summary').get('total_count'),
			id = nodeId) )
		return sum( map( lambda x : x.get(fld), lists ) ), lists

	def __dataForm__(self, obj, node):
		obj['parent'] = node
		obj['author'] = obj['from']['id']
		del obj['from']
		return obj

	# public methods

	def setToken(self, token):
		self.__init__(token)

	def getAll(self, url):
		# retrieve url
		name, postId = self.__retrieveUrl__(url)
		__log__('[Comment] Name: %s'    % name,   'log')
		__log__('[Comment] Post Id: %s' % postId, 'log')
		# get page id
		pageId = self.__getPageIdByName__(name)
		__log__('[Comment] Page Id: %s' % pageId, 'log')
		# get summary
		total, lists = self.__getSummary__('%s_%s' % (pageId, postId))
		__log__('[Comment] Total comments: %d' % total, 'log')
		# get all comments
		acc      = 0
		comments = []
		for c in lists:
			node = c.get('id')
			temp = [
				self.__dataForm__(x, node)
				for ls in self.__getDataWithPaging__('%s/comments' % node)
				for x in ls ]
			acc      = acc + c.get('comment_count')
			comments = comments + temp
			__log__('[Comment] Progress: %d/%d' % (acc, total), 'log')
		# return
		__log__(comments)
		return comments