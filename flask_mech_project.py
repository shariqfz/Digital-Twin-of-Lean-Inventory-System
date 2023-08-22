
from flask import Flask, jsonify
from flask_cors import CORS
import datetime
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app)

scheduler = BackgroundScheduler({'apscheduler.timezone': 'Asia/Calcutta'})
scheduler.start()

# data = {'Initial_Level': {0: 100, 1: 95, 2: 89, 3: 81, 4: 75, 5: 73, 6: 64, 7: 60, 8: 55, 9: 52, 10: 51, 11: 45, 12: 37, 13: 29, 14: 25, 15: 21, 16: 15}, 'Timestamp': {0: '0:0', 1: '1:13', 2: '2:47', 3: '4:25', 4: '6:17', 5: '7:24', 6: '9:22', 7: '10:49', 8: '11:58', 9: '13:56', 10: '14:52', 11: '15:31', 12: '17:21', 13: '19:10', 14: '21:1', 15: '22:21', 16: '23:10'}, 'Deduction': {0: 5, 1: 6, 2: 8, 3: 6, 4: 2, 5: 9, 6: 4, 7: 5, 8: 3, 9: 1, 10: 6, 11: 8, 12: 8, 13: 4, 14: 4, 15: 6, 16: 6}, 'Next_deduction_after_hours': {0: 1.23, 1: 1.57, 2: 1.62, 3: 1.88, 4: 1.1, 5: 1.97, 6: 1.47, 7: 1.15, 8: 1.97, 9: 0.92, 10: 0.65, 11: 1.83, 12: 1.82, 13: 1.87, 14: 1.32, 15: 0.82, 16: 1.15}}
import json
with open(r'data.json', 'r') as f:
    data = json.load(f, parse_int=int)

@app.route('/')
def index():
    return '<h1>Live Inventory</h1>'

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(data) 

@app.route('/livedata', methods=['GET', 'POST'])
def live_data():
    x, y = get_live_data_row()
    return jsonify({x:y})

iter = data.__iter__()
idx = 0
def live_data_generator():
    global idx
    idx = idx + 1
    yield idx-1, data[next(iter)]

def get_live_data_row():
    return next(live_data_generator())   
    

if __name__ == '__main__':
    app.run(debug=True)
    scheduler = APScheduler()
    scheduler.add_job(func=get_live_data_row, args=['job run'],
                      trigger='interval', id='job', seconds=5)
    scheduler.start()
