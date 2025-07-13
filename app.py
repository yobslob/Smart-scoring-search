from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Load startup data
with open('data/startups.json', 'r') as f:
    startups = json.load(f)

@app.route('/startups', methods=['GET'])
def get_startups():
    regions = request.args.getlist('regions')
    if regions:
        filtered = [s for s in startups if s['region'] in regions]
    else:
        filtered = startups
    return jsonify(filtered)