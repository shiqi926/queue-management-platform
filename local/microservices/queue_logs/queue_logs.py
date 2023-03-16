import os, sys
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
from flask_cors import CORS
import json
from datetime import datetime, timedelta


app = Flask(__name__)
CORS(app)

# Initialize Firestore DB
cred = credentials.Certificate('../key.json')
default_app = initialize_app(cred)
db = firestore.client()
queue_ref = db.collection('queue_logs')

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

if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    app.run(host = "0.0.0.0", port = 5003, debug = True)
    
    




