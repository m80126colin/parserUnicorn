import sys, requests, json
from urllib import parse

def __log__(message, mode = 'debug'):
	if mode == 'log':
		print(message, file = sys.stderr)

def __commentForm__(comment, nodeid):
	comment['parent'] = nodeid
	comment['author'] = comment['from']['id']
	del comment['from']
	return comment

class Comments:

	# constructor

	def __init__(self, token = '', limit = 500):
		self.token = token
		self.limit = limit

	# private methods

	## requests and API calls

	def __sendRequests__(self, url):
		res = requests.get(url)
		if res.status_code == requests.codes.ok:
			__log__('[Requests] Success!')
			return json.loads(res.text)
		else:
			__log__('[Requests] Error. Status code: %d' % res.status_code)
		return None

	def __graphAPICall__(self, node, version = '2.8', **args):
		# set token
		args.setdefault('access_token', self.token)
		# graph API
		api = 'https://graph.facebook.com/v%s/%s?%s'
		url = api % (version, node, parse.urlencode(args))
		__log__('[GraphAPI] Url: %s' % url)
		# send request
		return self.__sendRequests__(url)

	## Paging

	def __hasNext__(self, obj):
		return ('paging' in obj) and ('next' in obj['paging'])

	def __getAfter__(self, obj):
		return obj.get('paging').get('cursors').get('after')

	def __getNext__(self, obj):
		return obj.get('paging').get('next')

	def __pagingByAfter__(self, node, **args):
		args.setdefault('limit', self.limit)
		res = self.__graphAPICall__(node, **args)
		yield res.get('data')
		while self.__hasNext__(res):
			args['after'] = self.__getAfter__(res)
			res   = self.__graphAPICall__(node, **args)
			yield res.get('data')

	def __pagingByNext__(self, node, **args):
		args.setdefault('limit', self.limit)
		res = self.__graphAPICall__(node, **args)
		yield res.get('data')
		while self.__hasNext__(res):
			url = self.__getNext__(res)
			res = self.__sendRequests__(url)
			yield res.get('data')

	## others

	def __getSummary__(self, nodeId):
		fld   = 'comment_count'
		node  = '%s/comments' % nodeId
		res   = self.__graphAPICall__(node, fields = fld, summary = 1)
		lists = [ x
			for ls in self.__pagingByAfter__(node, fields = fld)
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

	def __retrieveUrl__(self, url):
		sp = [ x for x in parse.urlsplit(url).path.split('/') if x != '' ]
		if len(sp) < 2:
			__log__('[Retrieve] Invalid Url: %s' % url)
			return None
		return sp[0], sp[-1]

	# public methods

	def retrieveUrl(self, url):
		spList = [ x for x in parse.urlsplit(url).path.split('/') if x != '' ]
		if len(spList) < 1:
			__log__('[Retrieve] Invalid Url: %s' % url)
			return None
		if '-' in spList[0]:
			spList[0] = spList[0].split('-')[-1]
		res = dict(page = spList[0])
		if len(spList) >= 2:
			res['post'] = spList[-1]
		return res

	def getPageIdByName(self, name):
		res = self.__graphAPICall__(name)
		__log__(res)
		return res.get('id')

	def getAllPosts(self, data):
		extUrl = self.retrieveUrl(data.get('url'))
		pageId = self.getPageIdByName(extUrl.get('page'))

		data.setdefault('since', '')
		data.setdefault('until', '')
		res = [ x
			for ls in
				self.__pagingByNext__('%s/posts' % pageId,
					fields = 'id,created_time,comments.limit(0).summary(1),likes.limit(0).summary(1),shares',
					since  = data.get('since'),
					until  = data.get('until'),
					limit  = 100)
			for x in ls ]
		return res

	def setToken(self, token):
		self.__init__(token)

	def getAllComments(self, nodeId):
		total, lists = self.__getSummary__(nodeId)
		__log__('[Comment] Total comments: %d' % total, 'log')
		# get all comments
		acc      = 0
		comments = []
		for c in lists:
			node = c.get('id')
			temp = [
				self.__dataForm__(x, node)
				for ls in self.__pagingByAfter__('%s/comments' % node)
				for x in ls ]
			acc      = acc + c.get('comment_count')
			comments = comments + temp
			__log__('[Comment] Progress: %d/%d' % (acc, total), 'log')
		# return
		__log__(comments)
		return dict(id = nodeId, data = comments)

	def getPostFullId(self, url):
		# retrieve url
		name, postid = self.__retrieveUrl__(url)
		__log__('[getPostFullId] Retrieve Url, Name: %s, Post ID: %s' % (name, postid), 'log')
		# get page ID
		pageid = self.getPageIdByName(name)
		__log__('[getPostFullId] Page ID: %s' % pageid, 'log')
		# return full ID
		return '%s_%s' % (pageid, postid)

	# Node

	def getNodeLikes(self, nodeid):
		node = '%s/likes' % nodeid
		xs   = [ x.get('id')
			for ls in self.__pagingByAfter__(node)
			for x in ls ]
		return dict(id = nodeid, likes = xs)

	def getNodeComments(self, nodeid):
		# node = '%s/comments' % nodeid
		# xs   = [ __commentForm__(x, nodeid)
		#	for ls in self.__pagingByAfter__(node)
		#	for x in ls ]
		# 
		total, lists = self.__getSummary__(nodeid)
		__log__('[getNodeComments] Total comments: %d' % total, 'log')
		# get all comments
		acc      = 0
		comments = []
		for c in lists:
			node = c.get('id')
			temp = [ __commentForm__(x, node)
				for ls in self.__pagingByAfter__('%s/comments' % node)
				for x in ls ]
			acc      = acc + c.get('comment_count')
			comments = comments + temp
			__log__('[getNodeComments] Progress: %d/%d' % (acc, total), 'log')
		# return
		__log__(comments)
		return dict(id = nodeid, comments = comments)

	def getNodeShares(self, nodeid):
		res = self.__graphAPICall__(nodeid, fields = 'shares')
		__log__(res, 'log')
		return dict(id = nodeid, shares = res.get('shares'))

	def getAll(self, url):
		# get summary
		nodeId = self.getPostFullId(url)
		total, lists = self.__getSummary__(nodeId)
		__log__('[Comment] Total comments: %d' % total, 'log')
		# get all comments
		acc      = 0
		comments = []
		for c in lists:
			node = c.get('id')
			temp = [
				self.__dataForm__(x, node)
				for ls in self.__pagingByAfter__('%s/comments' % node)
				for x in ls ]
			acc      = acc + c.get('comment_count')
			comments = comments + temp
			__log__('[Comment] Progress: %d/%d' % (acc, total), 'log')
		# return
		__log__(comments)
		return dict(id = nodeId, data = comments)