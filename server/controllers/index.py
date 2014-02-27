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
		zb = int(web.input(id=90000).id)
		all_zb = list(db.select('zb', where="id<>0")) # 不显示id为0的那条记录（保留使用）
		if zb == 90000: # 显示全部的党员
			all_user_db = list(db.query("SELECT * from user,zb where user.zb = zb.id and user.zb <> 0"))
		else:
			all_user_db = list(db.query("SELECT user.*, zb.name as zb_name from user,zb where user.zb = zb.id and user.zb=$zb", vars={'zb':zb}))
		all_user = []
		for user in all_user_db:
			#  append应交材料份数等信息
			all_user.append(self.get_all_info(user))
		print all_user
		data = {"zb":all_zb, "user":all_user, "cur_id":zb}
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

