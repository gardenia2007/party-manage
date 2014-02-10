# -*- coding: utf-8 -*- 

import web
import random
import csv
import codecs
from auth import Admin
from config import setting


render = setting.render
db = setting.db


class Index(Admin):
	def __init__(self):
		Admin.__init__(self)
	def GET(self):
		return render.admin.admin(web.ctx.session, 'admin', {})

class InfoStudent(Admin):
	def __init__(self):
		Admin.__init__(self)
	def GET(self):
		student = db.query('SELECT *, student.name as stu_name, teacher.name as tea_name from student, st, teacher where st.id = student.st and teacher.id=st.teacher')
		return render.admin.info_student(web.ctx.session, 'info-student', student)

class InfoTeacher(Admin):
	def __init__(self):
		Admin.__init__(self)
	def GET(self):
		teacher = list(db.select('teacher'))
		st = {}
		for t in teacher:
			st[t.id] = list(db.query("SELECT student.name from student, st where st.teacher=%d and st.status='pass' and st.student=student.id"%(t.id)))
		data = {'teacher':teacher, 'st':st}
		return render.admin.info_teacher(web.ctx.session, 'info-teacher', data)

class ManageTeacher(Admin):
	def __init__(self):
		Admin.__init__(self)
	def GET(self):
		teacher = list(db.select('teacher'))
		return render.admin.manage_teacher(web.ctx.session, 'manage-teacher', teacher)

class Upload(Admin):
	def __init__(self):
		Admin.__init__(self)
	def POST(self):
		t = db.transaction()
		try:
			db.query('DELETE from student where 1')
			db.query('DELETE from st where 1')
			db.query('UPDATE teacher set has=0 where 1')
			f = csv.reader(web.input(file={}).file.file)
			for s_class, s_no, s_name, s_email, s_phone in f:
				db.query('INSERT into student values (NULL, $n, $no, $no, $c, $e, $p, "", 0)', \
					vars={'no':s_no, 'n':s_name, 'c':s_class, 'e':s_email, 'p':s_phone})
		except Exception, e:
			t.rollback()
			# print e
			return self.error('未知错误，请重试。')
		else:
			t.commit()
			return self.success('上传成功')

class AddStudent(Admin):
	def __init__(self):
		Admin.__init__(self)
	def GET(self):
		pass
	def POST(self):
		i = web.input()
		db.insert('student', name=i.name, pw=i.pw, no=i.no, email=i.email,\
			classno=i.classno, phone=i.phone, intro=i.intro)
		web.seeother('/admin')

class AddTeacher(Admin):
	def __init__(self):
		Admin.__init__(self)
	def GET(self):
		pass
	def POST(self):
		i = web.input()
		db.insert('teacher', name=i.name, pw=i.pw, pos=i.pos, email=i.email,\
			office=i.office, phone=i.phone, intro=i.intro)
		web.seeother('/admin')

class DelTeacher(Admin):
	def __init__(self):
		Admin.__init__(self)
	def GET(self, u_id):
		db.delete('teacher', where="id=$id", vars={'id':u_id})
		web.seeother('/admin')
	def POST(self):
		pass

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
		return render.teacher.info(web.ctx.session, 'teacher_info', data)
	def POST(self, tid):
		i = web.input()
		# 设置默认头像
		if len(i.photo)==0:
			i.photo = setting.default_photo_url
		db.update('teacher', where='id=%s'%(int(tid)), email=i.email,\
			phone=i.phone, office=i.office, intro=i.intro, lab=i.lab, photo=i.photo)
		return self.success('教师信息修改成功！')
