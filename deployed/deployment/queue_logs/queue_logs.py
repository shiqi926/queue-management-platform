import os, sys
import base64
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
from flask_cors import CORS
import json
from datetime import datetime, timedelta
from google.cloud import pubsub_v1

app = Flask(__name__)
CORS(app)

# Initialize Firestore DB
cred = credentials.Certificate('../key.json')
default_app = initialize_app(cred)
db = firestore.client()
queue_ref = db.collection('queue_logs')

@app.route("/", methods=["POST"])
def index():
    envelope = request.get_json()
    if not envelope:
        msg = "no Pub/Sub message received"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    if not isinstance(envelope, dict) or "message" not in envelope:
        msg = "invalid Pub/Sub message format"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    pubsub_message = envelope["message"]
    #queue_ref.add({"data": json.dumps(envelope)})

    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        #action,attractionName,customerID,timestamp
        data = base64.b64decode(pubsub_message["data"]).decode("utf-8").strip()
        #queue_ref.add({"data": data})
        data = data.split(",")
        for i in range(0, len(data), 4):
            log = {
                "action": data[i],
                "attractionName": data[i+1],
                "customerID": data[i+2],
                "timestamp": data[i+3]
            }
            queue_ref.add(log)
        return("Logged", 204)


@app.route('/queueLogs/logs', methods=['GET'])
def logs():
    try: 
        today = datetime.today()
        ytd = today - timedelta(days=1)
        ytd = ytd.strftime('%Y-%m-%d')
        tmr = today + timedelta(days=1)
        tmr = tmr.strftime('%Y-%m-%d')
        attractions = ["Viking Ship", "Rollercoaster", "Carousell"]
        res = {}

        for attr in attractions:
            res[attr] = []
            docs = queue_ref.where("timestamp", ">", ytd).where("timestamp", "<", tmr).where("attractionName", "==", attr).stream()
            for doc in docs:
                res[attr].append(doc.to_dict())
            
        res["success"] = True
        res["code"] = 200
        return jsonify(res)

    except Exception as e:
        return jsonify({
            "code": 400,
            "message": f"An Error Occured: {e}",
            "success": False
        }) 

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port, debug=True)
    
    




