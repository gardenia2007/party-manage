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
		return render.admin.index(self.session, '', {})

class Login:
	def GET(self):
		return render.admin.login(True)
	def POST(self):
		i, self.session = web.input(), web.config._session
		r = list(db.select('admin', where=web.db.sqlwhere({'name':i.username, 'pw':i.password})))
		if len(r) >= 1:
			self.session.uid   = str(r[0]['id'])
			self.session.name  = str(r[0]['name'])
			self.session.power = str(r[0]['power'])
			self.session.zb    = str(r[0]['zb'])
			self.session.is_login = True
			web.seeother('/admin')
		else:
			return render.admin.login(False)

class Logout:
    def GET(self):
		web.config._session.kill()
		web.seeother('/')

class InfoStudent(Admin):
	def __init__(self):
		Admin.__init__(self)
	def GET(self):
		student = db.query('SELECT *, student.name as stu_name, teacher.name as tea_name from student, st, teacher where st.id = student.st and teacher.id=st.teacher')
		return render.admin.info_student(self.session, 'info-student', student)

class InfoTeacher(Admin):
	def __init__(self):
		Admin.__init__(self)
	def GET(self):
		teacher = list(db.select('teacher'))
		st = {}
		for t in teacher:
			st[t.id] = list(db.query("SELECT student.name from student, st where st.teacher=%d and st.status='pass' and st.student=student.id"%(t.id)))
		data = {'teacher':teacher, 'st':st}
		return render.admin.info_teacher(self.session, 'info-teacher', data)

class ManageTeacher(Admin):
	def __init__(self):
		Admin.__init__(self)
	def GET(self):
		teacher = list(db.select('teacher', where=web.db.sqlwhere({'zb':self.session.zb})))
		return render.admin.manage_teacher(self.session, 'manage-teacher', teacher)

# 添加党员
class AddUser(Admin):
	def __init__(self):
		Admin.__init__(self)
	def GET(self):
		return render.admin.user_add(self.session, 'user_add')
	def POST(self):
		i = web.input()
		r = db.insert('user', xm=i.name, xh=i.no, rdsqs_sj=i.rdsqs_sj, qdjjfz_sj=i.qdjjfz_sj,\
			rdsj_sj=i.rdsj_sj, zzsj_sj=i.zzsj_sj)
		if r :
			return self.success('添加成功！')
		else:
			return self.error('添加失败，请重试！')

class DelUser(Admin):
	def __init__(self):
		Admin.__init__(self)
	def GET(self, id):
		# 修改该党员的状态为游离状态
		db.update('user', zb=0, where="id=$id", vars={'id':id})
		web.seeother('/admin/user/list')

class ListUser(Admin):
	def __init__(self):
		Admin.__init__(self)
	def GET(self):
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

class StatusTeacher(Admin):
	def __init__(self):
		Admin.__init__(self)
	def GET(self, u_id):
		web.seeother('/admin')
	def POST(self):
		pass

class StatusStudent(Admin):
	def __init__(self):
		Admin.__init__(self)
	def GET(self, u_id):
		web.seeother('/admin')
	def POST(self):
		pass

class UpdateTeacherInfo(Admin):
	def __init__(self):
		Admin.__init__(self)
	def GET(self, tid):
		data = db.select('teacher', where='id=%s'%(int(tid)))[0]
		return render.teacher.info(self.session, 'teacher_info', data)
	def POST(self, tid):
		i = web.input()
		# 设置默认头像
		if len(i.photo)==0:
			i.photo = setting.default_photo_url
		db.update('teacher', where='id=%s'%(int(tid)), email=i.email,\
			phone=i.phone, office=i.office, intro=i.intro, lab=i.lab, photo=i.photo)
		return self.success('教师信息修改成功！')
