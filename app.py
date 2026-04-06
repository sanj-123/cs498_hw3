from flask import Flask, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import WriteConcern, ReadPreference
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client["ev_db"]
collection = db["vehicles"]
app = Flask(__name__)

@app.route("/insert-fast", methods=["POST"])
def insert_fast():
    data = request.get_json()
    coll = collection.with_options(write_concern=WriteConcern(w=1))
    result = coll.insert_one(data)
    return jsonify({"inserted_id": str(result.inserted_id)})

@app.route("/insert-safe", methods=["POST"])
def insert_safe():
    data = request.get_json()
    coll = collection.with_options(write_concern=WriteConcern(w="majority"))
    result = coll.insert_one(data)
    return jsonify({"inserted_id": str(result.inserted_id)})

@app.route("/count-tesla-primary", methods=["GET"])
def count_tesla_primary():
    coll = collection.with_options(read_preference=ReadPreference.PRIMARY)
    count = coll.count_documents({"Make": "TESLA"})
    return jsonify({"count": count})

@app.route("/count-bmw-secondary", methods=["GET"])
def count_bmw_secondary():
    coll = collection.with_options(read_preference=ReadPreference.SECONDARY_PREFERRED)
    count = coll.count_documents({"Make": "BMW"})
    return jsonify({"count": count})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)