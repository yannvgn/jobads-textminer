#!flask/bin/python
from flask import Flask, jsonify, request
import jobads.fetch.ads 

app = Flask(__name__)

@app.route('/api/ads/search/<q>', methods=['GET'])
def get_ads(q):
    ads=jobads.fetch.ads.getAdsBySimpleQuery(q)
    return jsonify(ads)

if __name__ == '__main__':
    app.run(debug=True)
