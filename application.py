from flask import Flask, render_template, request, redirect
import json
from datetime import datetime
from collections import Counter
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)

application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ClimbingDB:PostgresPassword@awseb-e-uxswatm7qi-stack-awsebrdsdatabase-1nfndsualofh.ctt3bhz1abz7.ap-southeast-2.rds.amazonaws.com:5432/db'

application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)

class Climb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    white = db.Column(db.Integer, nullable=False)
    black = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return '<Climb %r>' % self.id

db.create_all()

@application.route('/')
def index():
    today = datetime.now().strftime("%Y-%m-%d")
    return render_template('index.html', today=today)

@application.route('/climbing', methods=['POST'])
def climbing():

    currentDate = datetime.now()
    climb = Climb(white='1', black='1', location='kent', date=currentDate)
    db.session.add(climb)
    db.session.commit()



    date = request.form['date']
    white = int(request.form['white'])
    black = int(request.form['black'])
    location = request.form['location']
    climbing = {'date': date, 'white': white, 'black': black, 'location': location}

    try:
        with open('climbing.txt', 'r') as f:
            data = json.load(f)
    except:
        data = []

    data.append(climbing)
    with open('climbing.txt', 'w') as f:
        json.dump(data, f)

    today = datetime.now().strftime("%Y-%m-%d")
    return render_template('index.html', today=today, success=True)


@application.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        if 'delete_climb' in request.form:
            date = request.form['delete_climb']
            with open('climbing.txt', 'r') as f:
                climbing = json.load(f)
            climbing = [climb for climb in climbing if climb['date'] != date]
            with open('climbing.txt', 'w') as f:
                json.dump(climbing, f)
            
    with open('climbing.txt', 'r') as f:
        climbing = json.load(f)

    white = [climb['white'] for climb in climbing]
    black = [climb['black'] for climb in climbing]
    locations = [climb['location'] for climb in climbing]
    
    avg_white = round(sum(white) / len(white), 1)
    avg_black = round(sum(black) / len(black), 1)
    most_common_location = Counter(locations).most_common(1)[0][0]

    return render_template('data.html', climbing=climbing, avg_white=avg_white, avg_black=avg_black, most_common_location=most_common_location)

if __name__ == '__main__':
    application.run()
