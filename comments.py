import sys
import requests
import json
from urllib import parse

def log(message):
	print(message, file = sys.stderr)

class Comments:
	def __init__(self, token):
		self.token = token

	def graphAPICall(self, node, version = '2.8', **args):
		# graph API
		api = 'https://graph.facebook.com/v%s/%s?%s'
		args.setdefault('access_token', self.token)
		url = api % (version, node, parse.urlencode(args))
		log('[GraphAPI] Url: %s' % url)
		res = requests.get(url)
		if res.status_code == requests.codes.ok:
			log('[GraphAPI] API call success!')
			return json.loads(res.text)
		else:
			log('[GraphAPI] Error. Status code: %d' % res.status_code)
		return None

	def retrieveUrl(self, url):
		spUrl = parse.urlsplit(url)
		sp    = spUrl.path.split('/')
		if len(sp) < 2:
			log(url)
			return None
		return sp[1], sp[-1]

	def getPageIdByName(self, name):
		res = self.graphAPICall(name)
		log(res)
		return res.get('id')

	def getMainComments(self, node):
		data      = []
		fieldData = 'id,from,message,comment_count'
		res       = self.graphAPICall('%s/comments' % node, fields = fieldData)
		data      = data + res.get('data')
		while ('paging' in res) and ('next' in res['paging']):
			after = res['paging'].get('cursors').get('after')
			res   = self.graphAPICall('%s/comments' % node, fields = fieldData, after = after)
			data  = data + res.get('data')
		return data

	def getAll(self, url):
		# retrieve url
		name, postId = self.retrieveUrl(url)
		# get page id
		pageId = self.getPageIdByName(name)
		log(pageId)
		# get comments
		comments    = self.getMainComments('%s_%s' % (pageId, postId))
		# subComments = [ x for x in getSubComments(c.get('id')) for c in comments ]
		data        = comments # + subComments
		log(data)