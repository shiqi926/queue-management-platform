import os, sys
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import json
from os import environ
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import amqp_setup
import pika
from datetime import datetime

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# Initialize customers and attractions microservices
customers_URL = environ.get('customers_URL') or "http://localhost:5000/customers"
attractions_URL = environ.get('attractions_URL') or "http://localhost:5001/attractions"


@app.route('/joinQueue/join', methods=['POST'])
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
                            ###AMQP to add to queue logs
                            print(amqp_setup.check_setup())
                            log_message = json.dumps({
                                "customerID": cid,
                                "timestamp": str(datetime.now()),
                                "action": "JOINED",
                                "attractionName": attraction_joining,
                            })
                            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="join.queue", body=log_message, properties=pika.BasicProperties(delivery_mode = 2)) 
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

if __name__ == '__main__':
    app.run(host="0.0.0.0", port = 7000, debug = True)


