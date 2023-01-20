from flask import Flask, render_template, request, redirect
import json
from datetime import datetime
from collections import Counter
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

application = Flask(__name__)

application.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://ClimbingDB:PostgresPassword@awseb-e-uxswatm7qi-stack-awsebrdsdatabase-1nfndsualofh.ctt3bhz1abz7.ap-southeast-2.rds.amazonaws.com:5432/ebdb"
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(application)

class Climb(db.Model):
    __tablename__ = 'Climbs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location = db.Column(db.String(10), nullable=False)
    black = db.Column(db.Integer, nullable=False)
    white = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __init__(self, black, white, location, date):
        self.black = black
        self.white = white
        self.location = location
        self.date = date

@application.route('/')
def index():
    today = datetime.now().strftime("%Y-%m-%d")
    return render_template('index.html', today=today)

@application.route('/climbing', methods=['POST'])
def climbing():

    date = request.form['date']
    white = int(request.form['white'])
    black = int(request.form['black'])
    location = request.form['location']
    climbing = {'date': date, 'white': white, 'black': black, 'location': location}

    #trying to add to the database
    climb = Climb(white=white, black=black, location=location, date=date)
    db.session.add(climb)
    db.session.commit()

    today = datetime.now().strftime("%Y-%m-%d")
    return render_template('index.html', today=today, success=True)


@application.route('/data', methods=['GET', 'POST'])
def data():
    #delete the climb if needed
    if request.method == 'POST':
        if 'delete_climb' in request.form:
            deleteID = request.form['delete_climb']
            climb_to_delete = Climb.query.filter_by(id=deleteID).first()
            db.session.delete(climb_to_delete)
            db.session.commit()


    #query the database
    allClimbs = Climb.query.all()    
    location_list = db.session.query(Climb.location).all()
    location_list = [location[0] for location in location_list]

    #calculate statistics
    avg_white = round(db.session.query(func.avg(Climb.white)).scalar(), 1)
    avg_black = round(db.session.query(func.avg(Climb.black)).scalar(), 1)
    location_counts = Counter(location_list)
    most_common_location = location_counts.most_common(1)[0][0]

    return render_template('data.html', climbing=allClimbs, avg_white=avg_white, avg_black=avg_black, most_common_location=most_common_location)

if __name__ == '__main__':
    application.run()