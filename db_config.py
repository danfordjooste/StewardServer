from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
 
# MySQL configurations (port = 3306)
app.config['MYSQL_DATABASE_USER'] = 'sql3338132'
app.config['MYSQL_DATABASE_PASSWORD'] = 'HHE61CWk5S'
app.config['MYSQL_DATABASE_DB'] = '	sql3338132'
app.config['MYSQL_DATABASE_HOST'] = 'sql3.freemysqlhosting.net'
mysql.init_app(app)