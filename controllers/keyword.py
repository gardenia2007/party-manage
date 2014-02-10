#-*- encoding:utf-8 -*-

import web, time
import random
from config import setting
from auth import User

db = setting.db
render = setting.render

class Index(User):
	def __init__(self):
		User.__init__(self)
	def GET(self):
		plot_data = {'word':[], 'data':[]}
		time_cond = self.get_time_cond()
		keyword = self.get_keyword()
		for word in keyword.split(','):
			count = db.query("SELECT count(*) AS c FROM renren WHERE r_status LIKE '%%%s%%' AND %s"%(word, time_cond))
			#plot_data['word'].append(word.encode('utf-8'))
			plot_data['data'].append(count[0].c)
		plot_data['word'] = keyword.encode('utf-8').split(',')
		web.ctx.session.word = plot_data['word']
		web.ctx.session.time_cond = time_cond
		return render.keyword(web.ctx.session, plot_data, web.input(start='0', end='0'), keyword = keyword)
	def POST(self):
		pass
	def get_keyword(self):
		return db.select('user', what="u_keyword", where="u_id=%d"%(web.ctx.session.uid))[0].u_keyword


class List(User):
	def __init__(self):
		User.__init__(self)
	def GET(self):
		data = []
		stus = db.query('SELECT s_renren, s_name, COUNT(*) AS c FROM stu, renren WHERE r_status LIKE "%%%s%%" AND s_id = r_stu and s_grade in %s and %s group by s_id order by count(*) DESC'\
			%(web.ctx.session.word[int(web.input(y=-1).y)], str(web.ctx.session.grade_id), web.ctx.session.time_cond))
		for stu in stus:
			data.append([str(stu['s_name']).encode('utf-8'), stu['c'], stu['s_renren']])
		return render.status.list(data)
	def POST(self):
		pass

class Update(User):
	def __init__(self):
		User.__init__(self)
	def GET(self):
		db.update('user', where="u_id = %d"%(web.ctx.session.uid),\
		 u_keyword=web.input(keyword='').keyword)
		raise web.seeother('/keyword')
	def POST(self):
		pass

class Tmp():
	def GET(self):
		return
		for s in db.select('renren'):
			if type(s.r_createtime) == int: continue
			try:
				db.update('renren', where='r_id=%d'%(s.r_id), r_createtime=int(time.mktime(time.strptime(s.r_createtime,'%Y-%m-%d %H:%M:%S'))))
			except:
				continue
			
		
