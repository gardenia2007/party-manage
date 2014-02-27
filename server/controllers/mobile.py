# -*- coding: utf-8 -*- 

import web
import urllib
import json

from auth import User
from auth import Report
from config import setting

render = web.config._render
db = web.config._db


require = [
	# {'field':'rdsqs_fz',		'name':'入党申请书',				 'type':'date'},
	{'field':'sxhb_fz', 		'name':'思想汇报',				 'type':'count'},
	{'field':'kcxs_fz', 		'name':'考察写实',				 'type':'count'},
	{'field':'zs_fz', 			'name':'政审',				 	 'type':'date'},
	{'field':'xxcjd_fz',		'name':'学习成绩单',				 'type':'date'},
	{'field':'bjyj_fz',		 	'name':'班级意见',				 'type':'date'},
	{'field':'bzryj_fz',		'name':'班主任意见',				 'type':'date'},
	{'field':'tzbyj_fz', 		'name':'团支部意见',				 'type':'date'},
	{'field':'dxjyzs_fz',		'name':'党校结业证',				 'type':'date'},
	{'field':'zz_fz',		 	'name':'自传',				 	 'type':'date'},
	{'field':'rdzys_fz',		'name':'入党志愿书',				 'type':'date'},
	{'field':'fzpj_fz',		 	'name':'发展票决',				 'type':'date'},
	{'field':'sxhb_yb',		 	'name':'思想汇报',				 'type':'count'},
	{'field':'kcxs_yb', 		'name':'考察写实',				 'type':'count'},
	{'field':'dxjyzs_yb',		'name':'党校结业证',				 'type':'date'},
	{'field':'bnzj_yb', 		'name':'半年总结',				 'type':'date'},
	{'field':'qnzj_yb',			'name':'全年总结',				 'type':'date'},
	{'field':'zzsq_yb',			'name':'转正申请',				 'type':'date'},
	{'field':'zzpj_yb', 		'name':'转正票决',				 'type':'date'},
]


class Index:
	def GET(self):
		return "hello!"
	def POST(self):
		pass

class Login:
	def GET(self):
		self.POST()
	def POST(self):
		raw_data = web.data()
		result = {'status':False}
		try:
			data = json.loads(raw_data)
			sql = 'SELECT zb.id as zb_id, zb.name as zb_name from admin, \
					zb where admin.name=$name and admin.pw=$pw and admin.zb=zb.id'
			info = db.query(sql, vars={'name':data['name'], 'pw':data['pw']})[0]
			result = {'status':True, 'zb_id':info.zb_id, 'zb_name':info.zb_name}
		except Exception, e:
			print e, 'not found'
		return json.dumps(result)

class InfoAll:
	def GET(self, uid):
		try:
			user = list(db.select('user', {'xh':uid}, where="xh = $xh and zb >= 0"))
			if len(user) == 0:
				return
			data, user = [], user[0]
			for item in require:
				v = user.get(item['field'])
				if v is not None: value = str(v)
				else: value = ''
				data.append(dict(item, **{'value':value}))
			return json.dumps(data)
		except Exception, e:
			raise e
	def POST(self, uid):
		pass

class InfoUpdate:
	def GET(self, uid):
		pass
	def POST(self, uid):
		raw_data = web.data()
		# raw_data = '[{"field":"rdsqs_fz","name":"入党申请书","value":"1234","type":"date"},{"field":"sxhb_fz","name":"思想汇报","value":"1234","type":"count"}]'
		try:
			data = json.loads(raw_data)
			sql = 'UPDATE user set '
			for item in data:
				sql = sql + " %s = '%s' ,"%(item['field'], item['value'])
			sql =  sql[:-1] + ' where xh = $xh and zb >= 0'
			r = db.query(sql, vars={'xh':uid})
			print r
			if r == 0:
				return json.dumps({'status':-1})
			else:
				return json.dumps({'status':0})
		except Exception, e:
			raise e

class InfoBasic:
	def GET(self, uid):
		try:
			# 以学号作为唯一id
			user = list(db.query("SELECT user.xm, zb.name, zb.id as zb_id from user,zb \
				where user.zb = zb.id and user.xh = $xh and user.zb >= 0", vars={'xh':uid}))[0]
			d = {'status':True, 'name':user['xm'], 'zb':user['name'], 'zb_id':user['zb_id']}
		except Exception, e:
			d = {'status':False}
		return json.dumps(d)
	def POST(self, uid):
		pass



