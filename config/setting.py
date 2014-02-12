# -*- coding: utf-8 -*- 
import web
import os

# render = web.template.render('/var/www/stu-select/templates/', cache=False)
# db = web.database(dbn='sqlite', db='/var/www/stu-select/db/testdb')

web.config.debug = True

config = web.storage(
	site_name = U"计算机学院党员发展推进系统",
	site_desc = '计算机学院党员发展推进系统',
	email='gardeniaxy@gmail.com',
	root = '',
	refer = '',
	static = '/static',
	app_name = 'csparty',
	# 年级
	grade = '1',
)

default_photo_url = '/mentor/static/img/avatar.png'

# web.template.Template.globals['cxt'] = web.ext


