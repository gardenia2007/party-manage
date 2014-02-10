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
		raise web.seeother('/status/value')
	def POST(self):
		pass


class Value(User):
	def __init__(self):
		User.__init__(self)
	def GET(self):
		# plot_data = [5, 16, 27, 20, 14, 11, 4]
		plot_data = {'emotion':[], 'data':[]}
		time_cond = self.get_time_cond()
		all_emo = ['none', 'happy', 'surprise', 'sad', 'fear', 'angry']
		for emo in all_emo:
			data = []
			data = db.query('select count(*) as count from renren where r_grade in %s AND %s AND r_emotion = "%s" '\
				%(str(web.ctx.session.grade_id), time_cond, emo))
			#print data[0]
			plot_data['data'].append(data[0]['count'])
			plot_data['emotion'].append(emo.encode('utf-8'))
		#print plot_data
		web.ctx.session.emotion = plot_data['emotion']
		web.ctx.session.time_cond = time_cond
		return render.status.value(web.ctx.session, plot_data, web.input(start='0', end='0'))
	def POST(self):
		pass


class Class(User):
	def __init__(self):
		User.__init__(self)
	def GET(self):
		time_cond = self.get_time_cond()
		web.ctx.session.time_cond = time_cond
		all_emo = ['NONE', 'none', 'happy', 'surprise', 'sad', 'fear', 'angry']
		all_class = list(db.query('SELECT DISTINCT r_class FROM renren WHERE r_grade IN %s AND r_class <> "NONE"'%(str(web.ctx.session.grade_id))))
		data = [[] for x in range(len(all_emo))]

		# for each class
		for c in all_class:
			if c.r_class == None: continue
			r = list(db.query("SELECT r_emotion, count(*) AS c FROM renren WHERE r_class = '%s'  AND %s GROUP BY r_emotion ORDER BY r_emotion ASC"\
				%(c.r_class, web.ctx.session.time_cond)))
			# for each emotion
			for idx, emo in enumerate(all_emo):
				tmp = 0
				for item in r:
					if item['r_emotion'] == emo:
						tmp = item['c']
						break
				data[idx].append(tmp)
		plot_data = {'emotion':all_emo, 'data':data,\
			'class':[c.r_class.encode('utf-8') for c in all_class]}
		web.ctx.session.emotion = all_emo
		return render.status.class_(web.ctx.session, plot_data, web.input(start='0', end='0'))
	def POST(self):
		pass


class List(User):
	def __init__(self):
		User.__init__(self)
	def GET(self, type):
		data = []
		stus = db.query('SELECT s_renren, s_name, count(*) from stu, renren where r_emotion = "%s" and s_id = r_stu and s_grade in %s and %s group by s_id order by count(*) DESC'\
			%(web.ctx.session.emotion[int(web.input(y=-1).y)], str(web.ctx.session.grade_id), web.ctx.session.time_cond))
		for stu in stus:
			data.append([str(stu['s_name']).encode('utf-8'), stu['count(*)'], stu['s_renren']])
		return render.status.list(data)
	def POST(self):
		pass


