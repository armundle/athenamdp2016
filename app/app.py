from flask import Flask, jsonify, render_template, Response, request
import traceback
from athena import get_open_appts, book_appointment, get_booked_appointment, reset_appointment
import json

app = Flask(__name__)

#timeline = json.loads('timeline_sample_1.json')


def bad_request(body=None):
    if body is None:
        response = Response("Bad request")
    else:
        response = Response(body)
    response.headers['status'] = 400
    return response


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


@app.route('/', methods=['GET'])
def home():
    return render_template('dist/index.html')


@app.route('/reset', methods=['GET'])
def reset():
    return jsonify(result=reset_appointment())


@app.route('/book', methods=['GET'])
def book():
    return jsonify(result = book_appointment(create_appointment()[0]))


@app.route('/booked', methods=['GET'])
def booked():
    return jsonify(result = get_booked_appointment())


@app.route('/appointment', methods=['GET'])
def athena():
    appt = create_appointment()
    print appt
    return jsonify(result=appt)


@app.route('/help', methods=['GET'])
def help():
    methods = [{"path": "/", "verb": "/GET"},
                    {"path": "/info", "verb": "POST"},
                     {"path": "/appointment", "verb": "GET"}]

    return jsonify(results=methods)

@app.route('/info', methods=['POST'])
def get_appointment():
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
