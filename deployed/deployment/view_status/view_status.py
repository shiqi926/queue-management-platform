import os, sys
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import json

from os import environ

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# Initialize attractions microservices
attractions_URL = environ.get('attractions_URL') or "https://attractions-wy3g4hhdja-uc.a.run.app/attractions"
customers_URL = environ.get('customers_URL') or "https://customers-wy3g4hhdja-uc.a.run.app/customers"
attraction_details_URL = environ.get("attraction_details_URL") or "https://attraction-details-wy3g4hhdja-uc.a.run.app/attractionDetails"


@app.route('/viewStatus/status/<string:cid>/<string:aName>', methods=['GET'])
def status(cid, aName):
    try:
        attraction_details = requests.get(f"{attraction_details_URL}/{aName}").json()
        capacity = attraction_details["attDet"]["capacity"]
        duration = attraction_details["attDet"]["duration"]
        try:
            cust_data = requests.get(f"{customers_URL}/getcust/{cid}").json()
            current_attraction = cust_data["currentAttraction"]
            if current_attraction == "" or current_attraction != aName:
                try:
                    ride_data = requests.get(f"{attractions_URL}/{aName}").json()
                    queue_len = ride_data["numberInQueue"]
                    wait_time = (queue_len // capacity) * duration
                    return jsonify({
                        "code": 200,
                        "numberInQueue": queue_len,
                        "success": True,
                        "currentAttraction": current_attraction,
                        "waitTime": wait_time
                    })
                except Exception as e:
                    return jsonify({
                        "success": False,
                        "code": 500,
                        "message": f"View Status: An Error Occurred while trying to fetch attraction queue: {e}"
                    })
            else:
                try:
                    queue_data = requests.get(f"{attractions_URL}/attractionSorted/{aName}").json()
                    people_in_front = 0
                    for person in queue_data:
                        if person["customerID"] == cid:
                            wait_time = (people_in_front // capacity) * duration
                            return jsonify({
                                "success": True,
                                "code": 200,
                                "numberInQueue": people_in_front,
                                "notJoined": False,
                                "waitTime": wait_time,
                                "currentAttraction": current_attraction,
                            })
                        else:
                            people_in_front += 1
                    return jsonify({
                        "success": False,
                        "code": 404,
                        "message": f"View Status: CID not found in {aName} queue"
                    })
                except Exception as e:
                    return jsonify({
                        "success": False,
                        "code": 500,
                        "message": f"View Status: An Error Occurred while trying to fetch customer queue status: {e}"
                    })
        except Exception as e:
                return jsonify({
                    "success": False,
                    "code": 500,
                    "message": f"View Status: An Error Occurred while trying to fetch customer current attraction: {e}"
                })
    except Exception as e:
        return jsonify({
            "success": False,
            "code": 500,
            "message": f"View Status: An Error Occurred while trying to fetch attraction details: {e}"
        })


@app.route('/viewStatus/<string:aName>', methods=["GET"])
def admin_status(aName):
    try:
        attraction_details = requests.get(f"{attraction_details_URL}/{aName}").json()
        capacity = attraction_details["attDet"]["capacity"]
        duration = attraction_details["attDet"]["duration"]
        try:
            ride_data = requests.get(f"{attractions_URL}/{aName}").json()
            queue_len = ride_data["numberInQueue"]
            wait_time = (queue_len // capacity) * duration
            return jsonify({
                "code": 200,
                "numberInQueue": queue_len,
                "success": True,
                "waitTime": wait_time
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "code": 500,
                "message": f"View Status: An Error Occurred while trying to fetch attraction queue: {e}"
            })
    except Exception as e:
        return jsonify({
            "success": False,
            "code": 500,
            "message": f"View Status: An Error Occurred while trying to fetch attraction details: {e}"
        })

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port, debug=True)