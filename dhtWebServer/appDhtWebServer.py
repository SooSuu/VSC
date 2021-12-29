from flask import Flask, render_template, request, redirect, url_for, flash, session, Response
from datetime import datetime
import sqlite3 as sql

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_manager, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

# from camera_pi import Camera
from vaccine_graph import *
from graph import *


app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///iddatabase.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),nullable=False, unique=True)
    password = db.Column(db.String(80),nullable=False)
    
class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "E-mail"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")
    
    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError("That username already exists. Please choose a different one.")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "E-mail"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                if bcrypt.check_password_hash(user.password, form.password.data):
                    login_user(user)
                    return redirect(url_for('index'))

    return render_template("login.html", form = form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template("register.html", form = form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_login'))


# Retrieve data from database
def getData():
    con=sql.connect('../sensorsData.db')
    curs=con.cursor()

    for row in curs.execute("SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT 1"):
        time = str(row[0])
        temp = row[1]
        hum = row[2]
    con.close()
    return time, temp, hum

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')	

def get_temperature_setting_value():
    con=sql.connect('../sensorsData.db')
    curs=con.cursor()

    for row in curs.execute('SELECT * FROM TEMP_R ORDER BY CREATED_AT DESC LIMIT 1'):
        now_max = row[2]
        now_min = row[3]
    con.close()
    return now_max, now_min

# main route
@app.route("/")
def main_login():
	time, temp, hum = getData()
	templateData = {
		'time': time,
		'temp': temp,
		'hum': hum
	}
	return render_template('main_login.html', title = 'DHT Sensor Data', **templateData)

@app.route('/index')
def index() :
    time, temp, hum = getData()
    templateData = {
		'time': time,
		'temp': temp,
		'hum': hum
	}
    return render_template('index.html',**templateData)

# vaccine page

@app.route("/db_addvaccine")
def new_vaccine() :
    return render_template('db_addvaccine.html', title = 'Add Vaccine')

#vaccine gragh
@app.route('/graph')
def graph():
    return Response(graph(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/graph_tem')
def graph_tem():
    return Response(graph_tem(), mimetype='multipart/x-mixed-replace; boundary=frame')
    

@app.route('/addrec', methods = ['POST','GET'])
def addrec() :
    if request.method == 'POST' :
        try :
            name = request.form['nm']
            exp_date = request.form['exp_d']

            with sql.connect('../sensorsData.db') as con :
                cur = con.cursor()
                cur.execute('INSERT INTO VACCINE (NAME, EXPIRATION_DATE) VALUES (?,?)', (name, exp_date))
                con.commit()
                msg = 'Vaccine added successfully'
        except :
            con.rollback()
            msg = 'Error in insert operation'
        finally :
            return render_template('db_result.html', title = 'Add Result Massage', msg = msg)
            con.close()
    return ''


@app.route('/db_list')
def list() :
    con = sql.connect('../sensorsData.db')

    cur = con.cursor()
    cur.execute('SELECT * FROM VACCINE')
    rows = cur.fetchall()
    con.close()
    return render_template('db_list.html', title = 'List', rows = rows)

# alarm page
@app.route("/db_addalarm")
def set_alarm():
    return render_template("db_addalarm.html", title = 'Setting Temperature Alarm')

@app.route('/addtempr', methods = ['POST','GET'])
def addtempr() :
    if request.method == 'POST' :
        try :
            max = request.form['Max']
            min = request.form['Min']
            with sql.connect('../sensorsData.db') as con :
                cur = con.cursor()
                cur.execute('INSERT INTO TEMP_R (MAX, MIN) VALUES (?,?)', (max, min))
                con.commit()
                msg = 'Record successfully added'
        except :
            con.rollback()
            msg = 'Error in insert operation'
        finally :
            return render_template('db_alarm_result.html', title = 'Add Result Massage', msg = msg)
           
    return ''

@app.route("/db_list_tempr")
def re_alrm():
    global now_max, now_min
    now_max, now_min = get_temperature_setting_value()
    templateData = {
		'현재 최대 온도': now_max,
		'현재 최소 온도': now_min,
	}
    return render_template('db_list_tempr.html', rowo=templateData)

# CCTV
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

# app run
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=False)
