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
		pass
	def POST(self):
		pass

class UpdatePw(User):
	def __init__(self):
		User.__init__(self)
	def GET(self):
		return render.user.update_pw(web.ctx.session, 'update_pw')
	def POST(self):
		i,role = web.input(), web.ctx.session.role
		if i.new_password != i.new_password2:
			return self.error('两次输入的新密码不匹配，请重新输入!')
		if len(i.new_password) <= 3:
			return self.error('新密码长度太短！<br>为了帐号安全，请设置比较复杂的密码。')
		if web.ctx.session.is_admin == True:
			vars = {'name':'admin', 'pw':i.old_password}
		else:
			vars = {'id':web.ctx.session.uid, 'pw':i.old_password}
		old = db.select(role, where=web.db.sqlwhere(vars))
		if len(old.list()) <= 0:
			return self.error('原密码不正确，请重新输入!')
		if web.ctx.session.is_admin == True:
			vars = {'name':'admin'}
		else:
			vars = {'id':web.ctx.session.uid}
		db.update(role, where=web.db.sqlwhere(vars), pw=i.new_password)
		return self.success('密码修改成功！')
		
