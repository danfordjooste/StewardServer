import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, url_for, render_template, jsonify, json
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import datetime
from pytz import timezone

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URI',
    'postgresql://postgres:root@localhost/stewDB')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug=True
    
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
    OnOff = db.Column(db.String(20))
    last_battVolt = db.Column(db.Integer)
    last_rcPeriod = db.Column(db.Integer)
    last_update = db.Column(db.String(20))

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

@app.route('/readMe')
def readMe():
    return render_template('readMe.html', title="READ ME")

@app.route('/addTime',methods=['GET','POST'])
def addTime():
    editTime = 0
    if request.method == 'POST':
        addTime = timeDB(request.form['mon'],request.form['tue'],request.form['wed'],request.form['thu'],request.form['fri'],request.form['sat'],request.form['sun'])
        db.session.add(addTime)
        db.session.commit()  
        return redirect(url_for('index'))
    else:
        return render_template('editTime.html',title='Start Time Database:', editTime=editTime)


@app.route('/editOnTime',methods=['GET','POST'])
def editOnTime():
    editTime = timeDB.query.get({"id": 1})
    if request.method == 'POST':
        editTime.mon = request.form['mon']
        editTime.tue = request.form['tue']
        editTime.wed = request.form['wed']
        editTime.thu = request.form['thu']
        editTime.fri = request.form['fri']
        editTime.sat = request.form['sat']
        editTime.sun = request.form['sun']
        db.session.commit()  
        return redirect(url_for('index'))
    else:
        return render_template('editTime.html',title='Edit ON Time:', editTime=editTime)


@app.route('/editOffTime',methods=['GET','POST'])
def editOffTime():
    editTime = timeDB.query.get({"id": 2})
    if request.method == 'POST':
        editTime.mon = request.form['mon']
        editTime.tue = request.form['tue']
        editTime.wed = request.form['wed']
        editTime.thu = request.form['thu']
        editTime.fri = request.form['fri']
        editTime.sat = request.form['sat']
        editTime.sun = request.form['sun']
        db.session.commit()  
        return redirect(url_for('index'))
    else:
        return render_template('editTime.html',title='Edit OFF Time:', editTime=editTime)

@app.route('/getTime', methods=['GET'])
def getTime():
    dt = datetime.datetime.now()#gets local time
    currentTime = dt.strftime("%H:%M:%S")
    return '%s##' % (currentTime)

@app.route('/getPSTOpen', methods=['GET'])
def getPSTOpen():
    on= timeDB.query.get({"id": 1})

    dt = datetime.datetime.now()#gets local time
    currentDay = dt.weekday()
    if currentDay == 0:     onTime = on.mon
    elif currentDay == 1:   onTime = on.tue 
    elif currentDay == 2:   onTime = on.wed 
    elif currentDay == 3:   onTime = on.thu 
    elif currentDay == 4:   onTime = on.fri 
    elif currentDay == 5:   onTime = on.sat 
    else:   onTime = on.sun
    return '%s##' % (onTime)

@app.route('/getPSTClose', methods=['GET'])
def getPSTClose():
    off = timeDB.query.get({"id": 2})
    dt = datetime.datetime.now()#gets local time
    currentDay = dt.weekday()
    if currentDay == 0:     offTime = off.mon
    elif currentDay == 1:   offTime = off.tue
    elif currentDay == 2:   offTime = off.wed
    elif currentDay == 3:   offTime = off.thu
    elif currentDay == 4:   offTime = off.fri
    elif currentDay == 5:   offTime = off.sat
    else:   offTime = off.sun
    return '%s##' % (offTime)

@app.route('/editDeviceName',methods=['GET','POST'])
def editDeviceName():
    if request.method == 'POST':
        deviceID = request.form['deviceID']
        editDevice = deviceDB.query.get({"id": deviceID})
        editDevice.deviceName=request.form['newDeviceDetail']
        db.session.commit()
        return redirect(url_for('index'))
    else:
        myDevice = deviceDB.query.all()
        return render_template('editDeviceDetail.html', title='Edit Device Name:', myDevice=myDevice,Description='Enter New Device Name')
    
@app.route('/editDeviceNum',methods=['GET','POST'])
def editDeviceNum():
    if request.method == 'POST':
        deviceID = request.form['deviceID']
        editDevice = deviceDB.query.get({"id": deviceID})
        editDevice.deviceNum=request.form['newDeviceDetail']
        db.session.commit()
        return redirect(url_for('index'))
    else:
        myDevice = deviceDB.query.all()
        return render_template('editDeviceDetail.html', title='Edit Device Name:', myDevice=myDevice, Description='Enter New Device Num:')

@app.route('/addNewDevice', methods=['POST'])
def addNewDevice():
    dt = datetime.datetime.now()#gets local time
    currentDay = dt.weekday()
    currentTime = dt.strftime("%D %H:%M:%S")
    device = deviceDB('deviceNum', 'newName', 0, 0, 0, 'new')
    db.session.add(device)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/deleteDevice',methods=['GET','POST'])
def deleteDevice():
    if request.method == 'POST':
        deviceID = request.form['delID']
        delDevice = deviceDB.query.get({"id": deviceID})
        db.session.delete(delDevice)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        myDevice = deviceDB.query.all()
        return render_template('deleteDevice.html', title='Delete Device:', myDevice=myDevice)

@app.route('/deleteEntry',methods=['GET','POST'])
def deleteEntry():
    if request.method == 'POST':
        pourID = request.form['delID']
        delEntry = pourDB.query.get({"id": pourID})
        db.session.delete(delEntry)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        myPour = pourDB.query.all()
        return render_template('deleteEntry.html', title='Delete Entry:', myPour=myPour)


@app.route('/jsonpost_status', methods=['POST'])
def jsonpost_status():
    dt = datetime.datetime.now()#gets local time
    currentDay = dt.weekday()
    currentTime = dt.strftime("%D %H:%M:%S")

    content = request.get_json()
    thisDeviceNum = content["deviceNum"]
    thisDeviceInfo = deviceDB.query.filter_by(deviceNum=thisDeviceNum).first()
    thisDeviceInfo.OnOff = request.json['OnOff']
    thisDeviceInfo.last_battVolt = request.json['last_battVolt']
    thisDeviceInfo.last_rcPeriod = request.json['last_rcPeriod']
    thisDeviceInfo.last_update = currentTime
    db.session.commit()
    return '1##'


@app.route('/jsonpost_data', methods=['POST'])
def jsonpost_data():
    dt = datetime.datetime.now()#gets local time
    currentTime = dt.strftime("%D %H:%M:%S")

    content = request.get_json()
    thisDeviceNum = content["deviceNum"]
    thisDeviceInfo = deviceDB.query.filter_by(deviceNum=thisDeviceNum).first()

    pourInfo = pourDB(thisDeviceNum, thisDeviceInfo.deviceName, request.json['pourVolume'], request.json['approxTime'],currentTime, request.json['battVolt'], request.json['timerCounter'], request.json['pourTime'], request.json['pulseCount'])
    
    db.session.add(pourInfo)# this add to the database the user
    db.session.commit()
    resp = jsonify('1!##')
    resp.status_code = 200
    return resp


if __name__ == "__main__":
    #manager.run()
    app.run()