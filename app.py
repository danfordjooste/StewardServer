import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, url_for, render_template, jsonify
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URI',
    'postgresql://postgres:root@localhost/stewDB')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.debug=True
    
#app.config['SECRET_KEY'] = 'super-secret'
#app.config['SECURITY_REGISTERABLE'] = True
#app.debug = True
db = SQLAlchemy(app)

migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class pourDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deviceNum = db.Column(db.String(20))
    deviceName = db.Column(db.String(40))
    pourVolume = db.Column(db.Integer)
    approxTime = db.Column(db.String(20))
    commitTime = db.Column(db.String(20))
    battVolt = db.Column(db.Integer)
    timerCounter = db.Column(db.Integer)
    pourTime = db.Column(db.Integer)
    pulseCount = db.Column(db.Integer)

    def __init__(self, deviceNum, deviceName, pourVolume, approxTime, commitTime, battVolt, timerCounter, pourTime, pulseCount):
            self.deviceNum = deviceNum
            self.deviceName = deviceName
            self.pourVolume = pourVolume
            self.approxTime = approxTime
            self.commitTime = commitTime
            self.battVolt = battVolt
            self.timerCounter = timerCounter
            self.pourTime = pourTime
            self.pulseCount = pulseCount
    
    def __repr__(self):
        return '<pourDB %r>' % self.deviceNum

class deviceDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deviceNum = db.Column(db.String(20))
    deviceName = db.Column(db.String(40))
    OnOff = db.Column(db.Integer)
    last_battVolt = db.Column(db.Integer)
    last_rcPeriod = db.Column(db.Integer)
    last_update = db.Column(db.Integer)

    def __init__(self, deviceNum, deviceName, OnOff, last_battVolt, last_rcPeriod, last_update):
            self.deviceNum = deviceNum
            self.deviceName = deviceName
            self.OnOff = OnOff
            self.last_battVolt = last_battVolt
            self.last_rcPeriod = last_rcPeriod
            self.last_update = last_update
    
    def __repr__(self):
        return '<deviceDB %r>' % self.deviceNum

class timeDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mon = db.Column(db.Integer)
    tue = db.Column(db.Integer)
    wed = db.Column(db.Integer)
    thu = db.Column(db.Integer)
    fri = db.Column(db.Integer)
    sat = db.Column(db.Integer)
    sun = db.Column(db.Integer)

    def __init__(self, mon, tue, wed, thu, fri, sat, sun):
            self.mon = mon
            self.tue = tue
            self.wed = wed
            self.thu = thu
            self.fri = fri
            self.sat = sat
            self.sun = sun
    
    def __repr__(self):
        return '<timeDB %r>' % self.mon

@app.route('/')
def index():
    dt = datetime.datetime.now()#gets local time
    currentDay = dt.weekday()
    currentTime = dt.strftime("%D %H:%M:%S")
    myPour = pourDB.query.all()
    myDevice = deviceDB.query.all()
    onTime = timeDB.query.filter_by(id='1')
    offTime = timeDB.query.filter_by(id='2')
    return render_template('home.html', myPour=myPour, currentTime=currentTime, currentDay=currentDay, myDevice=myDevice, onTime=onTime,offTime=offTime)

@app.route('/addOnTime')
def addOnTime():
    return render_template('newTime.html', title='Add ON Time:')

@app.route('/addOnTimeDatabase',methods=['POST'])
def addOnTimeDatabase():
        onTime = timeDB(request.form['mon'],request.form['tue'],request.form['wed'],request.form['thu'],request.form['fri'],request.form['sat'],request.form['sun'])
        db.session.add(onTime)
        db.session.commit()    
        return redirect(url_for('index'))

@app.route('/editOnTime')
def editOnTime():
    return render_template('editOnTime.html',title='Edit ON Time:')

@app.route('/editOnTimeDatabase',methods=['POST'])
def editOnTimeDatabase():
    editOn = timeDB.query.get({"id": 1})
    editOn.mon = request.form['mon']
    editOn.tue = request.form['tue']
    editOn.wed = request.form['wed']
    editOn.thu = request.form['thu']
    editOn.fri = request.form['fri']
    editOn.sat = request.form['sat']
    editOn.sun = request.form['sun']
    db.session.commit()  
    return redirect(url_for('index'))

@app.route('/editOffTime')
def editOffTime():
    return render_template('editOffTime.html',title='Edit OFF Time:')

@app.route('/editOffTimeDatabase',methods=['POST'])
def editOffTimeDatabase():
    editOn = timeDB.query.get({"id": 2})
    editOn.mon = request.form['mon']
    editOn.tue = request.form['tue']
    editOn.wed = request.form['wed']
    editOn.thu = request.form['thu']
    editOn.fri = request.form['fri']
    editOn.sat = request.form['sat']
    editOn.sun = request.form['sun']
    db.session.commit()  
    return redirect(url_for('index'))

@app.route('/getTime', methods=['GET'])
def getTime():
    dt = datetime.datetime.now()#gets local time
    currentTime = dt.strftime("%D %H:%M:%S")
    return '%s.%s##' % (currentTime)

@app.route('/getOperatingTime', methods=['GET'])
def getOperatingTime():
    on= timeDB.query.get({"id": 1})
    off = timeDB.query.get({"id": 2})

    dt = datetime.datetime.now()#gets local time
    currentDay = dt.weekday()
    if currentDay == 0:
        onTime = on.mon
        offTime = off.mon
    elif currentDay == 1:
        onTime = on.tue 
        offTime = off.tue
    elif currentDay == 2:
        onTime = on.wed 
        offTime = off.wed
    elif currentDay == 3:
        onTime = on.thu 
        offTime = off.thu
    elif currentDay == 4:
        onTime = on.fri 
        offTime = off.fri
    elif currentDay == 5:
        onTime = on.sat 
        offTime = off.sat
    else:
        onTime = on.sun
        offTime = off.sun
    return 'ON %s OFF %s##' % (onTime, offTime)

@app.route('/get_user', methods=['GET'])
def post_user():
    resp = jsonify('Successful GET')
    resp.status_code = 200
    return resp

@app.route('/jsonpost_status', methods=['POST'])
def jsonpost_status():
    dt = datetime.datetime.now()#gets local time
    currentTime = dt.strftime("%D %H:%M:%S")

    device = pourDB(request.json['deviceNum'], deviceName, request.json['OnOff'], request.json['last_battVolt'], request.json['last_rcPeriod'], currentTime)
    
    db.session.commit()
    resp = jsonify('{}',deviceName)#sends device name back
    resp.status_code = 200
    return resp


@app.route('/jsonpost_data', methods=['POST'])
def jsonpost_user():
    dt = datetime.datetime.now()#gets local time
    currentTime = dt.strftime("%D %H:%M:%S")

    pourInfo = pourDB(request.json['deviceNum'], request.json['deviceName'], request.json['pourVolume'], request.json['approxTime'],currentTime, request.json['battVolt'], request.json['timerCounter'], request.json['pourTime'], request.json['pulseCount'])
    
    db.session.add(pourInfo)# this add to the database the user
    db.session.commit()
    resp = jsonify('Successful Transfer!')
    resp.status_code = 200
    return resp
    #return redirect('/')


if __name__ == "__main__":
    #manager.run()
    app.run()