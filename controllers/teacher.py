# -*- coding: utf-8 -*- 

import web
import random
from config import setting
from auth import User

render = setting.render
db = setting.db

class Index(User):
	def __init__(self):
		User.__init__(self)
	def GET(self):
		raise web.seeother('/teacher/student/my')
	def POST(self):
		pass

class StudentMy(User):
	def __init__(self):
		User.__init__(self)
	def GET(self):
		data = db.query("SELECT * from st, student where st.teacher=%d and ( st.status='wait' or st.status='pass' ) and student.id=st.student"\
			%(web.ctx.session.uid))
		return render.teacher.student_my(web.ctx.session, 'student_my', data)

class TeacherAll(User):
	def __init__(self):
		User.__init__(self)
	def GET(self):
		return render.student.teacher_all(web.ctx.session, 'teacher_all')

class StudentInfo(User):
	def __init__(self):
		User.__init__(self)
	def GET(self, sid):
		data = db.select('student', dict(id=sid), where='id=$id')[0]
		return render.teacher.student_info(data, web.input().status)

class Info(User):
	def __init__(self):
		User.__init__(self)
	def GET(self):
		data = db.select('teacher', where='id=%d'%(web.ctx.session.uid))[0]
		return render.teacher.info(web.ctx.session, 'teacher_info', data)
	def POST(self):
		i = web.input()
		# 设置默认头像
		if len(i.photo)==0:
			i.photo = setting.default_photo_url
		db.update('teacher', where='id=%d'%(web.ctx.session.uid), email=i.email,\
			phone=i.phone, office=i.office, intro=i.intro, lab=i.lab, photo=i.photo)
		return self.success('个人信息修改成功！')

class Pass(User):
	def __init__(self):
		User.__init__(self)
	def GET(self, st_id):
			db.update('st', web.db.sqlwhere({'id':st_id}), status='pass')
			web.seeother('/teacher/student/my')

class Fail(User):
	def __init__(self):
		User.__init__(self)
	def GET(self, st_id):
		try:
			st = db.select('st', dict(id=st_id), where='id=$id')[0]
			print st
			if st.status == 'pass':
				return self.error('该学生已为通过状态，无法放弃选择！')
			else:
				db.update('st', web.db.sqlwhere({'id':st_id}), status='fail')
		except Exception, e:
			print e
			return self.error('未知错误，请重试。')
		else:
			web.seeother('/teacher/student/my')
		
