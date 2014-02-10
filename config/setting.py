# -*- coding: utf-8 -*- 
import web
import os

# render = web.template.render('/var/www/stu-select/templates/', cache=False)
# db = web.database(dbn='sqlite', db='/var/www/stu-select/db/testdb')

web.config.debug = False

config = web.storage(
	site_name = U"本科生导师互选系统",
	site_desc = '本科生导师互选系统',
	email='gardeniaxy@gmail.com',
	root = 'http://202.118.228.42/mentor',
	refer = 'http://202.118.228.42/mentor/',
	static = '/mentor/static',
	app_name = 'mentor',
	# 年级
	grade = '1',
)

default_photo_url = '/mentor/static/img/avatar.png'

# web.template.Template.globals['cxt'] = web.ext


