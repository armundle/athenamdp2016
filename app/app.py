from flask import Flask, jsonify, render_template, Response, request
import traceback
from athena import get_open_appts, book_appointment, get_booked_appointment, reset_appointment
from athena import extract_time, format_12
import json

app = Flask(__name__)


def bad_request(body=None):
    if body is None:
        response = Response("Bad request")
    else:
        response = Response(body)
    response.headers['status'] = 400
    return response


APPT = {
        "summary": "Your OBGYN appointment with Dr. Bonnie Buttercup is scheduled for May 1st 2016 at 8:30 am.",
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
                        'day': 24,
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

@app.route('/timeline', methods=['GET'])
def timeline():
    with open("timeline_sample_1.json") as json_file:
        json_data = json.load(json_file)
        return jsonify(json_data)


@app.route('/', methods=['GET'])
def home():
    return render_template('dist/index.html')


@app.route('/reset', methods=['GET'])
def reset():
    return jsonify(result=reset_appointment())


@app.route('/book', methods=['GET'])
def book():
    appt = book_appointment(create_appointment()[0])
    date = appt['date']
    time = appt['starttime']
    print date
    print time
    return jsonify(result = appt)


@app.route('/booked', methods=['GET'])
def booked():
    appt = get_booked_appointment()['appointments'][0]
    print appt
    date = appt['date']
    time = appt['starttime']
    print date
    print time
    return jsonify(result = get_booked_appointment())


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

@app.route('/info', methods=['POST'])
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


@app.route('/appointment', methods=['GET'])
def get_patient_info():
    try:
        response = {}
        response['test'] = ["February 30 2016", "March 29 2016"]
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": traceback.format_exc(e)})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
