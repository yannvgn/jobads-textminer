#!flask/bin/python
from flask import Flask, jsonify, request, abort
import jobads.fetch.ads 

app = Flask(__name__)

@app.route('/api/ads/search/<q>', methods=['GET'])
def get_ads(q):
    ads=jobads.fetch.ads.getAdsBySimpleQuery(q)
    return jsonify(ads)

@app.route('/api/ads/search', methods=['POST'])
def get_ads_post():
    data = request.get_json()
    if data and 'q' in data:
        ads=jobads.fetch.ads.getAdsBySimpleQuery(str(data['q']))
        return jsonify(ads)
    else:
        abort(400)

if __name__ == '__main__':
    app.run(debug=True)
