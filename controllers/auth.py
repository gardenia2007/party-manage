# -*- coding: utf-8 -*- 
import web
import datetime
from config import setting

class Admin:
	def __init__(self):
		self.session = web.config._session
		try:
			if not (web.ctx.session.is_login and web.ctx.session.is_admin):
				raise web.seeother('/login')
		except Exception, e:
			#raise e
			return self.error('未知错误，请重试。')
		else:
			pass
	def error(self, msg):
		return setting.render.error_page(web.ctx.session, '', msg)
	def success(self, msg):
		return setting.render.success_page(web.ctx.session, '', msg)

class User:
	def __init__(self):
		self.session = web.config._session
	def error(self, msg):
		return setting.render.error_page(web.ctx.session, '', msg)
	def success(self, msg):
		return setting.render.success_page(web.ctx.session, '', msg)

class Report:
	def __init__(self):
		pass
	def get_quater_num(self, begin):
		if begin is None or begin == '':
			return 0
		today = datetime.date.today()
		# 从begin到today的总季度数
		total_quater = ( today.year - begin.year ) * 4 \
			+ ( self.quater(today) - self.quater(begin))
		return total_quater
	def quater(self, d): # 对应的季度
		return d.month / 4
