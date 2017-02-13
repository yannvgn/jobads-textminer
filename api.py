#!flask/bin/python
from flask import Flask, jsonify, request, abort
import jobads.fetch.ads 

app = Flask(__name__)

@app.route('/api/ads/search/<q>', methods=['GET'])
def get_ads(q):
    limit=request.args.get("limit",10)
    offset=request.args.get("offset",0)
    #print(offset)
    
    try:
        limit=int(limit)
        offset=int(offset)
    except ValueError:
        print("error in casting")

    if (int(limit)<0 or int(offset)<0):
        abort(400)
    else:
        ads=jobads.fetch.ads.getAdsBySimpleQuery(q, limit, offset)
        return jsonify(ads)

@app.route('/api/ads/search', methods=['POST'])
def get_ads_post():
    data = request.get_json()
    limit=request.args.get("limit")
    offset=request.args.get("offset")
    if data and 'q' in data:
        ads=jobads.fetch.ads.getAdsBySimpleQuery(str(data['q']), limit, offset)
        return jsonify(ads)
    else:
        abort(400)

if __name__ == '__main__':
    app.run(debug=True)
