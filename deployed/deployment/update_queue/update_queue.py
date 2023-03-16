import os, sys
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import json
from os import environ
from google.cloud import pubsub
from datetime import datetime

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# Initialize customers and attractions microservices
customers_URL = environ.get('customers_URL') or "https://customers-wy3g4hhdja-uc.a.run.app/customers"
attractions_URL = environ.get('attractions_URL') or "https://attractions-wy3g4hhdja-uc.a.run.app/attractions"


@app.route('/updateQueue/leave', methods=['POST'])
def leave():
    publish_client = pubsub.PublisherClient()
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
                    topic = 'projects/esd-g9t7/topics/queueLogs'
                    #action,attractionName,customerID,timestamp
                    log = "LEFT," + aName + "," + cid + "," + str(datetime.now())
                    future = publish_client.publish(topic, bytes(log, encoding='utf8'))
                    future.result()
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

    message = ""

    first_cid = rList[0]
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
                        #action,attractionName,customerID,timestamp
                        log = data["action"]+ "," + aName + "," + cid + "," + str(datetime.now())
                        if cid != first_cid:
                            message += ","
                        message += log
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
    publisher = pubsub.PublisherClient()
    topic = 'projects/esd-g9t7/topics/queueLogs'
    future = publisher.publish(topic, bytes(message, encoding='utf8'))
    return jsonify({
        "success": True,
        "code": 200
    })

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port, debug=True)
