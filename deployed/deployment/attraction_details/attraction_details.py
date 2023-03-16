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
attraction_details_ref = db.collection('attraction_details')

#Get all the attraction details
@app.route("/attractionDetails/list", methods=['GET'])
def all():
    try: 
        docs = attraction_details_ref.stream()
        docDict = []
        for doc in docs:
            docDict.append(doc.to_dict())
        return jsonify({
            "code": 200,
            "attList": docDict
        })
    except Exception as e:
        return jsonify({
            "message": f"An Error Occured while fetching list of attraction details: {e}",
            "code": 500
        })

#Get single attraction details
@app.route("/attractionDetails/<string:aName>", methods=['GET'])
def one(aName):
    try: 
        doc = attraction_details_ref.where("attractionName", "==", aName).get()[0].to_dict()
        return jsonify({
            "code": 200,
            "attDet": doc
        })
    except Exception as e:
        return jsonify({
            "message": f"An Error Occured while fetching the attraction details of {aName}: {e}",
            "code": 500
        })

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port, debug=True)
