#!/usr/bin/python

import web
import sys, os

abspath = os.path.dirname(__file__) 
sys.path.append(abspath) 
os.chdir(abspath) 

from config.url import urls
from config.setting import db

default_encoding = 'utf-8' 
if sys.getdefaultencoding() != default_encoding: 
    reload(sys) 
    sys.setdefaultencoding(default_encoding) 

app = web.application(urls, globals())

if web.config.get('_session') is None:
    store = web.session.DBStore(db, 'sessions')
    session = web.session.Session(app, store, initializer={'is_login':False, 'is_admin':False})
    #session = web.session.Session(app, web.session.DiskStore(os.path.join(curdir,'sessions')), initializer={'is_login':False, 'is_admin':False})
    web.config._session = session
else:
    session = web.config._session

def session_hook():
	web.ctx.session = session

web.input._unicode = False

app.add_processor(web.loadhook(session_hook))
#application = app.wsgifunc()

if __name__ == "__main__":
	#application.run()
	app.run()

