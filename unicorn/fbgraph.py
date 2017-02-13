import sys, requests, json
from urllib import parse

api   = 'https://graph.facebook.com/v%s/%s?%s'
limit = 500

def _log(message, mode = 'debug'):
	if mode == 'log':
		print(message, file = sys.stderr)

## requests & graph API calls

def _sendRequests(url):
	res = requests.get(url)
	if res.status_code == requests.codes.ok:
		_log('[Requests] Success!')
		return json.loads(res.text)
	else:
		_log('[Requests] Error. Status code: %d' % res.status_code, 'log')
	return None

def _graphAPICall(node, token, version = '2.8', **args):
	# set token
	args.setdefault('access_token', token)
	# graph API
	url = api % (version, node, parse.urlencode(args))
	_log('[_graphAPICall] Url: %s' % url)
	# send request
	return _sendRequests(url)

## Paging

class _paging:
	@staticmethod
	def _hasNext(obj):
		return ('paging' in obj) and ('next' in obj['paging'])

	@staticmethod
	def _getAfter(obj):
		return obj.get('paging').get('cursors').get('after')

	@staticmethod
	def _getNext(obj):
		return obj.get('paging').get('next')

	@staticmethod
	def after(node, token, **args):
		args.setdefault('limit', limit)
		res = _graphAPICall(node, token, **args)
		yield res.get('data')
		while _paging._hasNext(res):
			args['after'] = _paging._getAfter(res)
			res = _graphAPICall(node, token, **args)
			yield res.get('data')

	@staticmethod
	def next(node, token, **args):
		args.setdefault('limit', limit)
		res = _graphAPICall(node, token, **args)
		yield res.get('data')
		while _paging._hasNext(res):
			url = _paging._getNext(res)
			res = _sendRequests(url)
			yield res.get('data')

## others

def _retrieveUrl(url):
	ls = [ x for x in parse.urlsplit(url).path.split('/') if x != '' ]
	if len(ls) < 1:
		_log('[Retrieve] Invalid Url: %s' % url)
		return None
	if '-' in ls[0]:
		ls[0] = ls[0].split('-')[-1]
	return ls[0], ls[-1]

def _commentForm(comment, nodeid):
	comment['parent'] = nodeid
	comment['author'] = comment['from']['id']
	del comment['from']
	return comment

def _getPageIdByName(name, token):
	res = _graphAPICall(name, token)
	_log(res)
	return res.get('id')

def _getCommentSummary(nodeid, token):
	fld = 'comment_count'
	node = '%s/comments' % nodeid
	res  = _graphAPICall(node, token, fields = fld, summary = 1)
	ls   = [ x
		for xs in _paging.after(node, token, fields = fld)
		for x in xs
		if x.get(fld) > 0 ]
	ls.append( dict(
		id            = nodeid,
		comment_count = res.get('summary').get('total_count')) )
	return sum( map( lambda x : x.get(fld), ls ) ), ls

def _getPostFullId(url, token):
	# retrieve url
	name, postid = _retrieveUrl(url)
	_log('[getPostFullId] Retrieve Url, Name: %s, Post ID: %s' % (name, postid), 'log')
	# get page ID
	pageid = _getPageIdByName(name, token)
	_log('[getPostFullId] Page ID: %s' % pageid, 'log')
	# return full ID
	return '%s_%s' % (pageid, postid)


# exports

retrieveUrl     = _retrieveUrl
getPageIdByName = _getPageIdByName
getPostFullId   = _getPostFullId

# Node

class node:
	url_likes    = '%s/likes'
	url_comments = '%s/comments'

	@staticmethod
	def likes(nodeid, token):
		xs = [ x.get('id')
			for page in _paging.after(node.url_likes % nodeid, token)
			for x in page ]
		return dict(id = nodeid, likes = xs)

	@staticmethod
	def shares(nodeid, token):
		res = _graphAPICall(nodeid, token, fields = 'shares')
		_log(res, 'log')
		return dict(id = nodeid, shares = res.get('shares'))

	@staticmethod
	def comments(nodeid, token):
		total, ls = _getCommentSummary(nodeid, token)
		_log('[getNodeComments] Total comments: %d' % total, 'log')
		# get all comments
		count    = 0
		comments = []
		for c in ls:
			subid    = c.get('id')
			temp     = [ _commentForm(x, node)
				for page in _paging.after(node.url_comments % subid, token)
				for x in page ]
			count    = count + c.get('comment_count')
			comments = comments + temp
			_log('[getNodeComments] Progress: %d/%d' % (count, total), 'log')
		# return
		_log(comments)
		return dict(id = nodeid, comments = comments)

def _getNodeShares(nodeid, token):
	res = _graphAPICall(nodeid, token, fields = 'shares')
	_log(res, 'log')
	return dict(id = nodeid, shares = res.get('shares'))