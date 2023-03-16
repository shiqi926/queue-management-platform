import os, sys
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import json
from os import environ
from datetime import datetime

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# Initialize queue_logs microservices
queueLogs_URL = environ.get('queueLogs_URL') or "http://localhost:5003/queueLogs"

@app.route("/dashboard/<string:aName>", methods=["GET"])
def dashboard(aName):
    try:
        queue_logs = requests.get(f"{queueLogs_URL}/logs").json()
        chart_data = {
            "labels": ["0000", "0100", "0200", "0300", "0400", "0500", "0600", "0700", "0800", "0900", "1000", "1100", "1200", "1300", "1400", "1500", "1600", "1700", "1800", "1900", "2000", "2100", "2200", "2300"],
            "datasets": [
                {
                    "label": "JOINED",
                    "borderColor": "#28a745",
                    "data": [],
                    "fill": False,
                    "tension": 0.2
                },
                {
                    "label": "LEFT",
                    "borderColor": "#dc3545",
                    "data": [],
                    "fill": False,
                    "tension": 0.2
                },
                {
                    "label": "BOARDED",
                    "borderColor": "#007bff",
                    "data": [],
                    "fill": False,
                    "tension": 0.2
                },
                {
                    "label": "REMOVED",
                    "borderColor": "#ffc107",
                    "data": [],
                    "fill": False,
                    "tension": 0.2
                }
            ]
        }
        logs = {
            "joined": {"0000": 0, "0100": 0, "0200": 0, "0300": 0, "0400": 0, "0500": 0, "0600": 0, "0700": 0, "0800": 0, "0900": 0, "1000": 0, "1100": 0, "1200": 0, "1300": 0, "1400": 0, "1500": 0, "1600": 0, "1700": 0, "1800": 0, "1900": 0, "2000": 0, "2100": 0, "2200": 0, "2300": 0}, 
            "left": {"0000": 0, "0100": 0, "0200": 0, "0300": 0, "0400": 0, "0500": 0, "0600": 0, "0700": 0, "0800": 0, "0900": 0, "1000": 0, "1100": 0, "1200": 0, "1300": 0, "1400": 0, "1500": 0, "1600": 0, "1700": 0, "1800": 0, "1900": 0, "2000": 0, "2100": 0, "2200": 0, "2300": 0},
            "boarded": {"0000": 0, "0100": 0, "0200": 0, "0300": 0, "0400": 0, "0500": 0, "0600": 0, "0700": 0, "0800": 0, "0900": 0, "1000": 0, "1100": 0, "1200": 0, "1300": 0, "1400": 0, "1500": 0, "1600": 0, "1700": 0, "1800": 0, "1900": 0, "2000": 0, "2100": 0, "2200": 0, "2300": 0},
            "removed": {"0000": 0, "0100": 0, "0200": 0, "0300": 0, "0400": 0, "0500": 0, "0600": 0, "0700": 0, "0800": 0, "0900": 0, "1000": 0, "1100": 0, "1200": 0, "1300": 0, "1400": 0, "1500": 0, "1600": 0, "1700": 0, "1800": 0, "1900": 0, "2000": 0, "2100": 0, "2200": 0, "2300": 0}
        }
        attraction_logs = queue_logs[aName]
        for al in attraction_logs:
            time = al["timestamp"][11:13] + "00"
            status = al["action"]
            if status == "JOINED":
                logs['joined'][time] += 1
            elif status == "LEFT":
                logs['left'][time] += 1
            elif status == "BOARDED":
                logs['boarded'][time] += 1
            elif status == "REMOVED":
                logs['removed'][time] += 1
        
        chart_data['datasets'][0]["data"] = list(logs["joined"].values())
        chart_data['datasets'][1]["data"] = list(logs["left"].values())
        chart_data['datasets'][2]["data"] = list(logs["boarded"].values())
        chart_data['datasets'][3]["data"] = list(logs["removed"].values())
        
        return jsonify({
            "code": 200,
            "success": True,
            "chartData": chart_data 
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"An Error Occured: {e}",
            "code": 400
        })
        
@app.route("/dashboard/pie", methods=["GET"])
def pie():
    try:
        queue_logs = requests.get(f"{queueLogs_URL}/logs").json()
        chart_data = {
            "labels": ["Viking Ship", "Rollercoaster", "Carousell"],
            "datasets": [
                {
                    "label": "JOINED",
                    "backgroundColor": [
                        'rgb(255, 99, 132)',
                        'rgb(54, 162, 235)',
                        'rgb(255, 205, 86)'
                        ],
                    "data": [],
                    "hoverOffset": 4
                }
            ]
        }
        pie_data = {"Viking Ship": 0, "Rollercoaster": 0, "Carousell": 0}
        for attraction in pie_data:
            for log in queue_logs[attraction]:
                if log["action"] == "JOINED":
                    pie_data[log["attractionName"]] += 1

        chart_data['datasets'][0]["data"] = list(pie_data.values())
        return jsonify({
            "code": 200,
            "success": True,
            "chartData": chart_data 
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"An Error Occured: {e}",
            "code": 400
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 7003, debug = True)

