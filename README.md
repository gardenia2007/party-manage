> http://code.google.com/p/modwsgi/downloads/list 
> tar xvfz mod_wsgi-X.Y.tar.gz

#### install apxs2
> sudo apt-get install apache2-****** 
> ./configure 
> make 
> make install 

#### Edit '/etc/apache2/httpd.conf'

> LoadModule wsgi_module modules/mod_wsgi.so 
> WSGIScriptAlias /appname /var/www/webpy-app/code.py/ 
> 
> Alias /appname/static /var/www/webpy-app/static/ 
> AddType text/html .py 
> 
> <Directory /var/www/webpy-app/> 
> 	Order deny,allow 
> 	Allow from all 
> </Directory> 

#### Restart Apache Web Server

#### DON'T FORGET EDIT root_path in 'config/setting' 

