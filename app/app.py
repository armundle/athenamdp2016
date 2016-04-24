from flask import Flask, jsonify, render_template, Response, request
import traceback
from athena import get_open_appts, book_appointment, get_booked_appointment, reset_appointment
from athena import extract_time, format_12, get_datetime, format_date
import json
import calendar
from datetime import datetime
from shutil import copyfile
from flask.ext.cors import CORS

app = Flask(__name__)
CORS(app)


def bad_request(body=None):
    if body is None:
        response = Response("Bad request")
    else:
        response = Response(body)
    response.headers['status'] = 400
    return response


TIMELINE = {
        "summary": "Your O-B-G-Y-N appointment with Dr. Bonnie Buttercup is scheduled for April 26th 2016 at 11:15 am.",
        #"appointment_date": {
            #"day": "monday",
            #"date": "2016-05-01 8:30 AM"
        #},
        "week": 0,
        "timeline": "pregnancy",
        "appointment_name": "OBGYN Appointment",
        #"appointment_id": "988639184",
        "category": "Single",
        "booking Date": {
            "booking_id": "2821481491",
            "booking_date": {
                "day": "sunday",
                "date": "04/23/2016"
            }
        },
        "Address": [
            {
                "name": "Seton Northwest Hospital",
                "department": "OBGYN",
                "address_line1": "11113 Research Blvd",
                "address_line2": "STE 400",
                "city": "Austin",
                "zip": "78759",
                "phoneno": "512-442-4522"
            }
        ]
    }


def create_appointment():
    dates = [{'start_time' : {'year': 2016,
                        'month': 04,
                        'day': 26,
                        'hour': 11,
                        'minute': 15}
             },
            {'start_time' : {'year': 2016,
                        'month': 04,
                        'day': 30,
                        'hour': 9,
                        'minute': 0}
             }
            ]

    return get_open_appts(dates)



def refactor(data):
   json_data = dict(data)
   appt_data = json_data['appointments']
   all_dates = []
   date_hash = {}
   for ind in appt_data:
       appt_date = datetime.strptime(ind['appointment_date']['date'], '%Y-%m-%d %I:%M %p')
       date_hash[appt_date] = ind
   rebuilt_timeline = []
   for ind_date in sorted(date_hash.keys()):
       rebuilt_timeline.append(date_hash[ind_date])
   json_data['appointments'] = rebuilt_timeline
   return json_data


@app.route('/timeline', methods=['GET'])
def timeline():
    with open("timeline_booked.json") as json_file:
        json_data = json.load(json_file)
        return jsonify(json_data)


@app.route('/', methods=['GET'])
def home():
    return render_template('dist/index.html')


@app.route('/reset', methods=['GET'])
def reset():
    copyfile('timeline_original.json', 'timeline_booked.json')
    return jsonify(result=reset_appointment())


@app.route('/book', methods=['GET'])
def book():
    open_appt = create_appointment()
    if len(open_appt) < 1:
        return jsonify({'error': "No matching slots"})

    dateformat = '%Y-%m-%d'

    appts = book_appointment(open_appt[0])
    appt = appts[0]
    time = appt['starttime']
    date = appt['date']
    date_str =  str(format_date(dateformat, get_datetime(date)))
    time_str = str(format_12(time))

    day = calendar.day_name[get_datetime(date).weekday()]


    appointment_date = {"day": day,
                        "date": date_str + " " + time_str}

    appointment_id = appt['appointmentid']

    TIMELINE['appointment_date'] = appointment_date
    TIMELINE['appointment_id'] = appointment_id

    #print TIMELINE


    with open("timeline_original.json") as fr:
        data = json.load(fr)
        data['appointments'].append(TIMELINE)
        ref_data = refactor(data)

    with open("timeline_booked.json", 'w') as fw:
        print type(ref_data)
        json.dump(ref_data, fw)

    r = {'appointment_date' : appointment_date,
         'appointment_id' : appointment_id}

    print r

    return jsonify(result = r)


@app.route('/booked', methods=['GET'])
def booked():
    dateformat = '%Y-%m-%d'

    appts = get_booked_appointment()['appointments']
    if len(appts) < 1 :
        return jsonify({})
    appt  = appts[0]

    time = appt['starttime']
    date = appt['date']
    date_str =  str(format_date(dateformat, get_datetime(date)))
    time_str = str(format_12(time))

    day = calendar.day_name[get_datetime(date).weekday()]


    appointment_date = {"day": day,
                        "date": date_str + " " + time_str}
    print appointment_date

    r = {'appointment_date' : appointment_date,
         'appointment_id' : appt['appointmentid']}
    print r
    return jsonify(result = r)


@app.route('/appointment', methods=['GET'])
def athena():
    appt = create_appointment()
    return jsonify(result=appt)


@app.route('/help', methods=['GET'])
def help():
    methods = [{"path": "/", "verb": "/GET"},
                    {"path": "/info", "verb": "POST"},
                     {"path": "/appointment", "verb": "GET"}]

    return jsonify(results=methods)

@app.route('/info', methods=['GET'])
def info():
    try:
        requestBody = request.get_json()
        if "preferences" in requestBody.keys():
            print requestBody
            return jsonify({"request": requestBody})
        else:
            return bad_request()
    except Exception as e:
        return jsonify({"error": traceback.format_exc(e)})



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
