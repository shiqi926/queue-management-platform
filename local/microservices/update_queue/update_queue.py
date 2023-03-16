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


@app.route('/updateQueue/leave', methods=['POST'])
def leave():
    data = request.json        
    cid = data['customerID']
    aName = data['attractionName']
    try:
        remove_cust = requests.delete(f"{attractions_URL}/kick", json=data).json()
        if remove_cust['code'] == 200:
            print(f"Successfully removed {cid} from {aName} queue!")
            try:
                update_cust = requests.patch(f"{customers_URL}/updatecust/{cid}").json()
                if update_cust["code"] == 200:
                    print(f"Successfully updated. {cid} is currently not queueing for any attraction")
                    ###AMQP to add to queue logs
                    log_message = json.dumps({
                        "timestamp": str(datetime.now()),
                        "customerID": cid,
                        "attractionName": aName,
                        "action": "LEFT"
                    })
                    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="leave.queue", body=log_message, properties=pika.BasicProperties(delivery_mode = 2)) 
                    return jsonify({
                        "success": True,
                        "code": 200
                    })
                else:
                    print("Failed to remove customer from queue.")
            except Exception as e:
                return jsonify({
                    "success": False,
                    "code": 400,
                    "message": f"An Error Occurred while trying to update customer queue status: {e}"
                })
        else:
            print("Failed to remove customer from queue")
    except Exception as e:
        return jsonify({
            "success": False,
            "code": 400,
            "message": f"An Error Occurred while trying to remove customer from queue: {e}"
        })


@app.route('/updateQueue/remove', methods=['POST'])
def remove():
    data = request.json        
    rList = data['removeList']
    aName = data['attractionName']
    for cid in rList:
        req_data = {
            "attractionName": aName,
            "customerID": cid
        }
        try:
            remove_cust = requests.delete(f"{attractions_URL}/kick", json=req_data).json()
            if remove_cust['code'] == 200:
                print(f"Successfully removed {cid} from {aName} queue!")
                try:
                    update_cust = requests.patch(f"{customers_URL}/updatecust/{cid}").json()
                    if update_cust["code"] == 200:
                        print(f"Successfully updated. {cid} is currently not queueing for any attraction")
                        ###AMQP to add to queue logs
                        log_message = json.dumps({
                            "timestamp": str(datetime.now()),
                            "customerID": cid,
                            "attractionName": aName,
                            "action": data["action"]
                        })
                        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="remove.queue", body=log_message, properties=pika.BasicProperties(delivery_mode = 2)) 
                    else:
                        print(f"Failed to update customer {cid} from queue status.")
                except Exception as e:
                    return jsonify({
                        "success": False,
                        "code": 400,
                        "message": f"An Error Occurred while trying to update customer queue status: {e}"
                    })
            else:
                msg = remove_cust["message"]
                print(f"Failed to remove customer {cid} from {aName} queue. {msg}")
        except Exception as e:
            return jsonify({
                "success": False,
                "code": 400,
                "message": f"An Error Occurred while trying to remove customer from queue: {e}"
            })
    return jsonify({
        "success": True,
        "code": 200
    })


if __name__ == '__main__':
    app.run(host="0.0.0.0", port = 8000, debug = True)
