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
		raise web.seeother('/student/teacher/my')
	def POST(self):
		pass

class TeacherMy(User):
	def __init__(self):
		User.__init__(self)
	def GET(self):
		r = list(db.query('SELECT st.status, teacher.* from student, st, teacher where st.id=student.st and teacher.id=st.teacher and student.id=%d'%(web.ctx.session.uid)))
		if(len(r) <= 0):
			data = None
		else:
			data = r[0]
		return render.student.teacher_my(web.ctx.session, 'teacher_my', data)

class TeacherAll(User):
	def __init__(self):
		User.__init__(self)
	def GET(self):
		r = list(db.query('SELECT st.status, teacher.id from student, st, teacher where st.id=student.st and teacher.id=st.teacher and student.id=%d'%(web.ctx.session.uid)))
		if(len(r) <= 0):
			my = None
		else:
			my = r[0]
		data = {'teacher':db.select('teacher'), 'my':my}
		return render.student.teacher_all(web.ctx.session, 'teacher_all', data)

class TeacherInfo(User):
	def __init__(self):
		User.__init__(self)
	def GET(self, tid):
		data = db.select('teacher', dict(id=tid), where='id=$id')[0]
		return render.student.teacher_info(data)

class Info(User):
	def __init__(self):
		User.__init__(self)
	def GET(self):
		data = db.select('student', where='id=%d'%(web.ctx.session.uid))[0]
		return render.student.info(web.ctx.session, 'student_info', data)
	def POST(self):
		i = web.input()
		db.update('student', where='id=%d'%(web.ctx.session.uid), email=i.email,\
			phone=i.phone, classno=i.classno, intro=i.intro)
		return self.success('个人信息修改成功！')

class Choose(User):
	def __init__(self):
		User.__init__(self)
	def GET(self, tid):
		r = db.select('teacher', dict(id=tid), where='id=$id', what='total, has', limit=1)[0]
		if(r.has >= r.total):
			return self.error('此导师名额已满，请返回选择其他导师')
		t = db.transaction()
		try:
			if web.ctx.session.role != 'student':
				raise
			pre_st = db.select('student', where='id=%d'%(web.ctx.session.uid), what='st')[0].st
			if pre_st > 0:
				# delete previous teacher
				pre = db.select('st', where='id=%d'%(pre_st))[0]
				if pre.status == 'pass':
					# 原来的已经通过了就不能再选择了
					raise Exception
				db.query("UPDATE st SET status='delete' where id = %d"%(pre_st))
				db.query("UPDATE teacher SET has = has - 1 WHERE id = $id", vars={'id':pre.teacher})
			# choose new teacher
			db.query("UPDATE teacher SET has = has + 1 WHERE id = $id", vars={'id':tid})
			st_id = db.insert('st', student=web.ctx.session.uid, teacher=tid, status='wait')
			db.update('student', where='id=%d'%(web.ctx.session.uid), st=st_id)
		except Exception, e:
			print e
			t.rollback()
			return self.error('未知错误，请重试。')
		else:
			t.commit()
		web.seeother('/student/teacher/my')
	def del_previous():
		pass

class Delete(User):
	def __init__(self):
		User.__init__(self)
	def GET(self, tid):
		t = db.transaction()
		try:
			st = db.select('st', dict(tid=tid), where='teacher=$tid',\
				order='time DESC', limit=1)[0]
			if st.status=='pass':
				raise
			db.query("UPDATE teacher SET has = has - 1 WHERE id = $id", vars={'id':tid})
			db.query("UPDATE st SET status='delete' where id = %d"%(st.id))
			db.update('student', where='id=%d'%(web.ctx.session.uid), st=0)
		except Exception, e:
			t.rollback()
			return self.error('未知错误，请重试。')
		else:
			t.commit()
		web.seeother('/student/teacher/all')

		
