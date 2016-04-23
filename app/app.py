from flask import Flask, jsonify, render_template, Response, request
import traceback

app = Flask(__name__)


def bad_request(body=None):
    if body is None:
        response = Response("Bad request")
    else:
        response = Response(body)
    response.headers['status'] = 400
    return response


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/info', methods=['POST'])
def get_patient_info():
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
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": traceback.format_exc(e)})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
