# -*- coding: utf-8 -*- 

import web
import random
from config import setting
from auth import User

render = web.config._render
db = web.config._db

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
		return render.user.update_pw(self.session, 'update_pw')
	def POST(self):
		i = web.input()
		if i.new_password != i.new_password2:
			return self.error('两次输入的新密码不匹配，请重新输入!')
		if len(i.new_password) <= 3:
			return self.error('新密码长度太短！<br>为了帐号安全，请设置比较复杂的密码。')
		vars = {'id':self.session.uid, 'pw':i.old_password}
		old = db.select('admin', where=web.db.sqlwhere(vars))
		if len(old.list()) <= 0: # 检查原密码是否正确
			return self.error('原密码不正确，请重新输入!')
		vars = {'id':self.session.uid}
		db.update('admin', where=web.db.sqlwhere(vars), pw=i.new_password)
		return self.success('密码修改成功！')

