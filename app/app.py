from flask import Flask, jsonify, render_template, Response, request
import traceback
from athena import get_open_appts

app = Flask(__name__)


def bad_request(body=None):
    if body is None:
        response = Response("Bad request")
    else:
        response = Response(body)
    response.headers['status'] = 400
    return response


# get this from timeline
# input will be a preferences for each appointment required
# select only one match for each appointment and this will
# be a list of all the appointment for the patient
def create_appointment():
    dates = [{'start_time' : {'year': 2016,
                        'month': 04,
                        'day': 24,
                        'hour': 8,
                        'minute': 0}
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


@app.route('/athena/get-appointment', methods=['GET'])
def get_appointment():
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
