import os
from flask import Flask, request, jsonify, make_response
from firebase_admin import credentials, firestore, initialize_app
from flask_cors import CORS
import json
from os import environ

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# Initialize Firestore DB
cred = credentials.Certificate('../key.json')
default_app = initialize_app(cred)
db = firestore.client()
customers_ref = db.collection('customers')

#adding a new customer
@app.route('/customers/add', methods=['POST'])
def create():
    try:
        data = request.json
        cid = data["cid"]
        customers_ref.document(cid).set(data)
        return jsonify({
            "success": True,
            "code": 201
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"An Error Occurred:{e}",
            "code": 400
        })

@app.route('/customers/getcust/<string:cid>', methods=['GET'])
def read(cid):
    try:
        data = customers_ref.document(cid).get()
        resp = data.to_dict()
        resp["code"] = 200
        return jsonify(resp)
    except Exception as e:
        resp = {
            "success": False,
            "message": f"An Error Occured:{e}",
            "code": 400
        }
        return jsonify(resp)

@app.route('/customers/updatecust/<string:cid>', methods=['PATCH'])
def clear(cid):
    try:
        customers_ref.document(cid).update({"currentAttraction": ""})
        return jsonify({
            "code": 200,
            "success": True
        })
    except Exception as e:
        resp = {
            "success": False,
            "message": f"An Error Occured:{e}",
            "code": 400
        }
        return jsonify(resp)

@app.route('/customers/updatecust/<string:cid>/<string:attraction_joining>', methods=['PATCH'])
def update(cid, attraction_joining):
    try:
        customers_ref.document(cid).update({"currentAttraction": attraction_joining})
        return jsonify({
            "code": 200,
            "success": True
        })
    except Exception as e:
        resp = {
            "success": False,
            "message": f"An Error Occured:{e}",
            "code": 400
        }
        return jsonify(resp)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug = True)


