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
		return render.flow.index(self.session, 'flow')
	def POST(self):
		pass
