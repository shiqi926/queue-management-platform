import os, sys
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
from flask_cors import CORS
import json
from os import environ
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import amqp_setup
from datetime import datetime, timedelta


app = Flask(__name__)
CORS(app)

# Initialize Firestore DB
cred = credentials.Certificate('../key.json')
default_app = initialize_app(cred)
db = firestore.client()
queue_ref = db.collection('queue_logs')

monitorBindingKey='*.queue'

def receiveQueueLog():
    amqp_setup.check_setup()
        
    queue_name = 'Queue_Log'
    
    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived a queue log by " + __file__)
    queue = json.loads(body)
    queue_ref.add(queue)

if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    receiveQueueLog()
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    
    




