import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime
from flask_cors import CORS
from os import environ

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# Initialize Firestore DB
cred = credentials.Certificate('../key.json')
default_app = initialize_app(cred)
db = firestore.client()
attractions_ref = db.collection('attractions')

#Add customer to queue
@app.route("/attractions/addCustomer", methods=['POST'])
def add_customer():
    try: 
        data = request.json
        attraction_name = data["attractionName"]
        docs = attractions_ref.where("attractionName", "==", attraction_name).get()
        max_queue_num = 0
        if len(docs) > 0:
            for doc in docs:
                doc_dict = doc.to_dict()
                if doc_dict["queueNumber"] > max_queue_num:
                    max_queue_num = doc_dict["queueNumber"]
        data["queueNumber"] = max_queue_num + 1
        data["notified"] = False
        data["timestamp"] = datetime.now()
        attractions_ref.add(data)
        return jsonify({
            "attractionName": attraction_name,
            "queueNumber": max_queue_num + 1,
            "code": 201,
            "success": True
        })
    except Exception as e:
        return jsonify({
            "code": 400,
            "message": f"An Error Occured: {e}",
            "success": False
        }) 

#Get how many customers in one attraction queue
@app.route("/attractions/<string:aName>", methods=['GET'])
def get_attraction(aName):
    try: 
        num_in_queue = attractions_ref.where("attractionName", "==", aName).get()
        return jsonify({
            "numberInQueue": len(num_in_queue) - 1, #minus 1 because of the root document (queue number 0)
            "code": 200
        })
    except Exception as e:
        return jsonify({
            "message": f"An Error Occured: {e}",
            "code": 500
        })

#Remove customer from queue
@app.route("/attractions/kick", methods=['DELETE'])
def kick():
    try: 
        data = request.json
        cid = data["customerID"]
        aName = data["attractionName"]
        doc = attractions_ref.where("attractionName", "==", aName).where("customerID", "==", cid).get()
        docId = doc[0].id
        attractions_ref.document(docId).delete()
        return jsonify({
            "success": True,
            "code": 200
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"An Error Occured: {e}",
            "code": 500
        })

#Get all number of records for ALL attraction queues 
@app.route("/attractions/all", methods=['GET'])
def all():
    try: 
        docs = list(attractions_ref.stream())
        # docDict = {}
        # for doc in docs:
        #     docDict[doc.id] = doc.to_dict()
        # return jsonify(
        #     docDict
        # ), 200
        return jsonify({
            #docDict
            "crowdSize": len(docs),
            "code": 200
        })
    except Exception as e:
        return jsonify({
            "message": f"An Error Occured: {e}",
            "code": 500
        })

#Returns the people queueing for a particular attraction in the correct order
@app.route("/attractions/attractionSorted/<string:aName>", methods=['GET'])
def attraction_sorted(aName):
    try: 
        docs = attractions_ref.where("attractionName", "==", aName).order_by("timestamp").stream()
        #docs = attractions_ref.where("attractionName", "==", aName).order_by("timestamp").get()
        docList = []
        for doc in docs:
            docList.append(doc.to_dict())
        return jsonify(
            docList
        ), 200
    except Exception as e:
        return jsonify({
            "message": f"An Error Occured: {e}",
            "code": 500
        })

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port, debug=True)
