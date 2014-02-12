# -*- coding: utf-8 -*- 

import web
import urllib

from auth import User
from auth import Report
from config import setting

render = web.config._render
db = web.config._db

class Index(User):
	def GET(self):
		all_zb = list(db.select('zb'))
		all_user_db = list(db.query("SELECT * from user,zb where user.zb = zb.id"))
		all_user = []
		for user in all_user_db:
			all_user.append(self.get_all_info(user))
		print all_user
		data = {"zb":all_zb, "user":all_user}
		return render.index(self.session, data)
	def POST(self):
		pass

class DBtest:
    def GET(self):
        data = db.select('test')
        for x in data:
        	pass
    def POST(self):
        pass

class Test:
	def GET(self):
		pass

	def POST():
		pass

