# -*- coding: utf-8 -*- 

import web
import random
import csv
import codecs
from auth import Admin
from config import setting

render = web.config._render
db = web.config._db


class Index(Admin):
	def __init__(self):
		Admin.__init__(self)
	def GET(self):
		web.seeother('/admin/user/list')
		# return render.admin.index(self.session, '', {})

class Login:
	def GET(self):
		return render.admin.login(True)
	def POST(self):
		i, self.session = web.input(), web.config._session
		# r = list(db.select('admin', where=web.db.sqlwhere({'name':i.username, 'pw':i.password})))
		print i.username
		print i.username.encode('utf-8')
		r = list(db.query("SELECT admin.*, zb.name as zb_name from admin, zb where zb.id=admin.zb and admin.name=$name and pw=$pw",\
			{'name':i.username, 'pw':i.password}))
		if len(r) >= 1:
			self.session.uid   = str(r[0]['id'])
			self.session.name  = r[0]['name']
			self.session.power = str(r[0]['power'])
			self.session.zb    = str(r[0]['zb'])
			self.session.zb_name = r[0]['zb_name']
			self.session.is_login = True
			web.seeother('/admin')
		else:
			return render.admin.login(False)

class Logout:
    def GET(self):
		web.config._session.kill()
		web.seeother('/')

# 添加党员
class AddUser(Admin):
	def __init__(self):
		Admin.__init__(self)
	def GET(self):
		all_zb = list(db.select('zb'))
		return render.admin.user_add(self.session, 'user_add', {'all_zb':all_zb})
	def POST(self):
		i = web.input()
		if self.session == '1':
			zb = i.zb
		else:
			zb = self.session.zb
		r = db.insert('user', xm=i.name, xh=i.no, rdsqs_sj=i.rdsqs_sj, qdjjfz_sj=i.qdjjfz_sj,\
			rdsj_sj=i.rdsj_sj, zzsj_sj=i.zzsj_sj, zb=zb, rdsqs_fz=i.rdsqs_sj)
		if r :
			return self.success('添加成功！')
		else:
			return self.error('添加失败，请重试！')

class UpdateUser(Admin):
	def __init__(self):
		Admin.__init__(self)
	def GET(self, id):
		info = list(db.select('user', where="id=$id", vars={'id':id}))
		if len(info) == 0:
			return self.error('没有此用户信息！')
		else:
			all_zb = list(db.select('zb'))
			return render.admin.user_update(self.session, 'user_update',\
				{'info':info[0], 'all_zb':all_zb})
	def POST(self, id):
		i = web.input()
		sql = 'UPDATE user set '
		for k in i:
			sql = sql + " %s = '%s' ,"%(k, i[k])
		sql =  sql[:-1] + ' where id = $id'
		r = db.query(sql, vars={'id':id})
		print r
		if r :
			return self.success('更新成功！')
		else:
			return self.error('更新失败，请重试！')

class DelUser(Admin):
	def __init__(self):
		Admin.__init__(self)
	def GET(self, id):
		if self.session.power == '1':
			zb = -1 # 如果管理员删除，则不会再显示
		else:
			zb = 0 # 支书删除，仅修改该党员的党支部为无
		db.update('user', zb=zb, where="id=$id", vars={'id':id})
		web.seeother('/admin/user/list')

class ListUser(Admin):
	def __init__(self):
		Admin.__init__(self)
	def GET(self):
		if self.session.power == '1':
			# 超级管理员获得全部党员
			all_user = list(db.query('SELECT user.*, zb.name as zb_name from user, zb where user.zb = zb.id'))
		else:
			# 选择全部属于本支部的用户
			all_user = list(db.select('user', where=web.db.sqlwhere({'zb':self.session.zb})))
		return render.admin.user_list(self.session, 'user_list', {'all_user':all_user})

class AddZb(Admin):
	def __init__(self):
		Admin.__init__(self)
		print self.session.power == '1'
		if self.session.power != '1': # 是否是超级管理员
			web.seeother('/')
	def GET(self):
		return render.admin.zb_add(self.session, 'zb_add')
	def POST(self):
		i = web.input()
		r = db.insert('zb', name=i.name)
		if r :
			return self.success('添加成功！')
		else:
			return self.error('添加失败，请重试！')

class ListZb(Admin):
	def __init__(self):
		Admin.__init__(self)
		if self.session.power != '1': # 是否是超级管理员
			web.seeother('/')
	def GET(self):
		all_zb = list(db.select('zb'))
		return render.admin.zb_list(self.session, 'zb_list', {'all_zb':all_zb})

# 删除一个支部，需要修改原属于本支部的党员的状态为游离状态
class DelZb(Admin):
	def __init__(self):
		Admin.__init__(self)
		if self.session.power != '1': # 是否是超级管理员
			web.seeother('/')
	def GET(self, id):
		db.delete('zb', where="id=$id", vars={'id':id})
		# 修改原属于本支部的党员的状态为游离状态
		db.update('user', zb=0, where="zb=$zb", vars={'zb':id})
		web.seeother('/admin/zb/list')

class AddZs(Admin):
	def __init__(self):
		Admin.__init__(self)
		if self.session.power != '1': # 是否是超级管理员
			web.seeother('/')
	def GET(self):
		all_zb = list(db.select('zb'))
		return render.admin.zs_add(self.session, 'zs_add', {'all_zb':all_zb})
	def POST(self):
		i = web.input()
		r = db.insert('admin', name=i.name, pw=i.pw, power='0', zb=i.zb)
		if r :
			return self.success('添加成功！')
		else:
			return self.error('添加失败，请重试！')

class ListZs(Admin):
	def __init__(self):
		Admin.__init__(self)
		if self.session.power != '1': # 是否是超级管理员
			web.seeother('/')
	def GET(self):
		all_zs = list(db.query("SELECT admin.* , zb.name as zb from admin, zb where admin.power = '0' and admin.zb = zb.id"))
		return render.admin.zs_list(self.session, 'zs_list', {'all_zs':all_zs})

# 删除一个党支书
class DelZs(Admin):
	def __init__(self):
		Admin.__init__(self)
		if self.session.power != '1': # 是否是超级管理员
			web.seeother('/')
	def GET(self, id):
		db.delete('admin', where="id=$id", vars={'id':id})
		web.seeother('/admin/zs/list')
