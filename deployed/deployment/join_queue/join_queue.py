import os, sys
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS, cross_origin
import json
from os import environ
from google.cloud import pubsub
publish_client = pubsub.PublisherClient()
from datetime import datetime

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# Initialize customers and attractions microservices
customers_URL = environ.get('customers_URL') or "https://customers-wy3g4hhdja-uc.a.run.app/customers"
attractions_URL = environ.get('attractions_URL') or "https://attractions-wy3g4hhdja-uc.a.run.app/attractions"


@app.route('/joinQueue/join', methods=['POST', 'OPTIONS'])
def create():
    try:
        data = request.json
        cid = data["customerID"]
        attraction_joining = data["attractionName"]
        cust_data = requests.get(f"{customers_URL}/getcust/{cid}").json()
        current_attraction = cust_data["currentAttraction"]
        if current_attraction == "":
            print("Currently not in any queue, sending addCustomer request...")
            try:
                add_data = requests.post(f"{attractions_URL}/addCustomer", json=data).json()
                if add_data["success"]:
                    print("Successfully joined queue!")
                    try:
                        update_cust = requests.patch(f"{customers_URL}/updatecust/{cid}/{attraction_joining}").json()
                        print(update_cust)
                        if update_cust["code"] == 200:
                            print("Customer queue status updated")
                            topic = 'projects/esd-g9t7/topics/queueLogs'
                            #action,attractionName,customerID,timestamp
                            log = "JOINED" + "," + attraction_joining + "," + cid + "," + str(datetime.now())
                            future = publish_client.publish(topic, bytes(log, encoding='utf8'))
                            return jsonify({
                                "success": True,
                                "code": 201,
                                "queueNumber": add_data["queueNumber"],
                            })
                        else:
                            print("Customer status update failed")
                    except Exception as e:
                        return jsonify({
                            "success": False,
                            "code": 400,
                            "message": f"An Error Occurred while trying to update customer queue status: {e}"
                        })
                else:
                    print("Failed to join queue")
            except Exception as e:
                return jsonify({
                    "success": False,
                    "code": 400,
                    "message": f"An Error Occurred while trying to add customer to queue: {e}"
                })
        else:
            message = f"Customer is already in queue for {current_attraction}"
            return jsonify({"message": message, "currentAttraction": current_attraction, "code": 401})
    except Exception as e:
        return jsonify({
            "success": False,
            "code": 500,
            "message": f"An Error Occurred while trying to fetch customer queue status: {e}"
        })

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port, debug=True)


