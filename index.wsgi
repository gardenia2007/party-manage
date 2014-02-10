import os
import sae
import web

from config.url import urls
from config.setting import config

web.config._db =  web.database(dbn='mysql', user=sae.const.MYSQL_USER,\
	pw=sae.const.MYSQL_PASS, host=sae.const.MYSQL_HOST, port=3307, db=sae.const.MYSQL_DB)

# template
app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
web.config._render = web.template.render(templates_root)

web.template.Template.globals['config'] = config
web.template.Template.globals['render'] = web.config._render


app = web.application(urls, globals())

# session
store = web.session.DBStore(web.config._db, 'sessions')
session = web.session.Session(app, store, initializer={'is_login':False})
web.config._session = session



application = sae.create_wsgi_app(app.wsgifunc())

