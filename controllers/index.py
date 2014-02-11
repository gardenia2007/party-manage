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
			report = Report()
			fz_expect_num = report.get_quater_num(user['qdjjfz_sj'])
			yb_expect_num = report.get_quater_num(user['rdsj_sj'])
			d = {'expect_sxhb_fz':fz_expect_num, 'expect_kcxs_fz':fz_expect_num,
				 'expect_sxhb_yb':yb_expect_num, 'expect_kcxs_yb':yb_expect_num}
			all_user.append(dict(user, **d))
		print all_user
		data = {"zb":all_zb, "user":all_user}
		return render.index(self.session, data)
	def POST(self):
		pass

class Logout:
    def GET(self):
    	web.ctx.session.kill()
	web.seeother('/')
    def POST(self):
        pass

class Login:
	def GET(self):
		i = web.input(post='0')
		if i.post == '1':
			return self.POST()
		else:
			return render.login(True)
	def login_as(self, role, i):
		if role == 'student': # 学生用学号登录
			sql = "SELECT * FROM %s WHERE no=$n AND pw=$p"%(role)
		else: # 教师用姓名
			sql = "SELECT * FROM %s WHERE name=$n AND pw=$p"%(role)
		results = list(db.query(sql, vars={'n':i.username, 'p':i.password}))
		if len(results) >= 1:
			web.ctx.session.is_login = True
			web.ctx.session.uid = results[0].id
			web.ctx.session.name = results[0].name
			web.ctx.session.role= role
			web.ctx.session.is_admin = False
			web.seeother('/'+role)
			return True
		else:
			return False
	def POST(self):
		i = web.input()
		if i.grade != setting.config.grade:
			return web.seeother(setting.config.refer+'%s/login?post=1&username=%s&password=%s&grade=%s'\
				%(i.grade, i.username, i.password, i.grade))
		if i.username == 'admin':
			r = list(db.select('admin', where=web.db.sqlwhere({'name':i.username, 'pw':i.password})))
			if len(r) >= 1:
				web.ctx.session.name = 'Admin'
				web.ctx.session.role= 'admin'
				web.ctx.session.is_login = True
				web.ctx.session.is_admin = True
			web.seeother('/admin')
			return
		elif(self.login_as('student', i)):
			return
		elif(self.login_as('teacher', i)):
			return
		else:
			return render.login(False)

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

