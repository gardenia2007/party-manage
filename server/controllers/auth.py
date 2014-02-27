# -*- coding: utf-8 -*- 
import web
import datetime
from config import setting

# translate

class Admin:
	def __init__(self):
		self.session = web.config._session
		if not self.session.is_login:
			raise web.seeother('/admin/login')
		# except Exception, e:
			# return self.error('未知错误，请重试。')
	def error(self, msg):
		return web.config._render.error_page(self.session, '', msg)
	def success(self, msg):
		return web.config._render.success_page(self.session, '', msg)

class User:
	def __init__(self):
		self.session = web.config._session
	def error(self, msg):
		return web.config._render.error_page(self.session, '', msg)
	def success(self, msg):
		return web.config._render.success_page(self.session, '', msg)
	def get_all_info(self, user):
		report = Report()
		fz_expect_num = report.get_quater_num(user['qdjjfz_sj'], user['rdsj_sj'])
		yb_expect_num = report.get_quater_num(user['rdsj_sj'], user['zzsj_sj'])
		d = {'expect_sxhb_fz':fz_expect_num, 'expect_kcxs_fz':fz_expect_num,
			 'expect_sxhb_yb':yb_expect_num, 'expect_kcxs_yb':yb_expect_num}
		new_user = dict(user, **d)
		return new_user

class Report:
	def __init__(self):
		pass
	def get_quater_num(self, begin, end):
		if begin is None or begin == '':
			return 0
		if end is None or end == '':
			end = datetime.date.today()
		# 从begin到end总季度数
		total_quater = ( end.year - begin.year ) * 4 \
			+ ( self.quater(end) - self.quater(begin))
		return total_quater
	def quater(self, d): # 对应的季度
		return d.month / 4

