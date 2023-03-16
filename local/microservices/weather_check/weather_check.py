import os, sys
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import json
from os import environ

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# Initialize attractions microservices
forecast_URL = "https://api.data.gov.sg/v1/environment/2-hour-weather-forecast"
attraction_details_URL = environ.get("attraction_details_URL") or "http://localhost:5002/attractionDetails"


@app.route('/weatherCheck/forecast', methods=['GET'])
def forecast():
    try:
        forecast_data = requests.get(forecast_URL).json()
        forecasts = forecast_data["items"][0]["forecasts"]
        forecast = next((record["forecast"] for record in forecasts if record["area"] == "Sentosa"), "Unavaiabile")
        return jsonify({
            "success": True,
            "code": 200,
            "forecast": forecast
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "code": 500,
            "message": f"An Error Occurred while trying to fetch weather forecast: {e}"
        })

@app.route('/weatherCheck/availability/<string:aName>')
def availability(aName):
    try:
        forecast_data = requests.get(forecast_URL).json()
        forecasts = forecast_data["items"][0]["forecasts"]
        forecast = next((record["forecast"] for record in forecasts if record["area"] == "Sentosa"), "Unavaiabile")
        if "Thunder" not in forecast:
            return jsonify({
                "success": True,
                "code": 200,
                "available": True,
                "message": "No lightning risk for the next 2 hours"
            })
        else:
            try:
                attraction_details = requests.get(f"{attraction_details_URL}/{aName}").json()
                indoors = attraction_details["attDet"]["indoors"]
                if indoors:
                    return jsonify({
                        "success": True,
                        "code": 200,
                        "available": True,
                        "message": f"Lightning risk present but {aName} is situated indoors"
                    })
                else:
                    return jsonify({
                        "success": True,
                        "code": 200,
                        "available": False,
                        "message": f"{aName} is unavailabile due to lightning risk"
                    })       
            except Exception as e:
                return jsonify({
                    "success": False,
                    "code": 500,
                    "message": f"An Error Occurred while trying to get attraction details: {e}"
                })
    except Exception as e:
        return jsonify({
            "success": False,
            "code": 500,
            "message": f"An Error Occurred while trying to get weather forecast: {e}"
        })

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 7002, debug = True)