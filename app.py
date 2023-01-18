from flask import Flask, render_template, request
import json
from datetime import datetime
from collections import Counter

app = Flask(__name__)

@app.route('/')
def index():
    today = datetime.now().strftime("%Y-%m-%d")
    return render_template('index.html', today=today)

@app.route('/climbing', methods=['POST'])
def climbing():
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


@app.route('/data')
def data():
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
    app.run()
