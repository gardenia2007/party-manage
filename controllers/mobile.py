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
	{'filed':'rdsqs_fz',		'name':'入党申请书',				 'type':'date'},
	{'filed':'sxhb_fz', 		'name':'思想汇报',				 'type':'count'},
	{'filed':'kcxs_fz', 		'name':'考察写实',				 'type':'count'},
	{'filed':'zs_fz', 			'name':'政审',				 	 'type':'date'},
	{'filed':'xxcjd_fz',		'name':'学习成绩单',				 'type':'date'},
	{'filed':'bjyj_fz',		 	'name':'班级意见',				 'type':'date'},
	{'filed':'bzryj_fz',		'name':'班主任意见',				 'type':'date'},
	{'filed':'tzbyj_fz', 		'name':'团支部意见',				 'type':'date'},
	{'filed':'dxjyzs_fz',		'name':'党校结业证',				 'type':'date'},
	{'filed':'zz_fz',		 	'name':'自传',				 	 'type':'date'},
	{'filed':'rdzys_fz',		'name':'入党志愿书',				 'type':'date'},
	{'filed':'fzpj_fz',		 	'name':'发展票决',				 'type':'date'},
	{'filed':'sxhb_yb',		 	'name':'思想汇报',				 'type':'count'},
	{'filed':'kcxs_yb', 		'name':'考察写实',				 'type':'count'},
	{'filed':'dxjyzs_yb',		'name':'党校结业证',				 'type':'date'},
	{'filed':'bnzj_yb', 		'name':'半年总结',				 'type':'date'},
	{'filed':'qnzj_yb',			'name':'全年总结',				 'type':'date'},
	{'filed':'zzsq_yb',			'name':'转正申请',				 'type':'date'},
	{'filed':'zzpj_yb', 		'name':'转正票决',				 'type':'date'},
]


class Index:
	def GET(self):
		return "hello!"
	def POST(self):
		pass
 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	
class InfoAll:
	def GET(self, uid):
		try:
			user = db.select('user', {'xh':uid}, where="xh = $xh")[0]
			data = []
			for item in require:
				v = user.get(item['filed'])
				if v is not None: value = str(v)
				else: value = None
				data.append(dict(item, **{'value':value}))
			return json.dumps(data)
		except Exception, e:
			raise e
	def POST(self):
		pass

class InfoUpdate:
	def GET(self):
		pass
	def POST(self, uid):
		pass

class InfoBasic:
	def GET(self, uid):
		# 以学号作为唯一id
		user = list(db.query("SELECT user.xm, zb.name from user,zb where user.zb = zb.id and user.xh = $xh",\
			vars={'xh':uid}))
		if len(user) == 0:
			d = {'status':False}
		else:
			d = {'status':True, 'name':user[0]['xm'], 'zb':user[0]['name']}
		return json.dumps(d)
	def POST(self):
		pass



