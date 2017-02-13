#!flask/bin/python
from flask import Flask, jsonify, request, abort
import jobads.fetch.ads 

app = Flask(__name__)

@app.route('/api/ads/search/<q>', methods=['GET'])
def get_ads(q):
    limit=request.args.get("limit",10)
    offset=request.args.get("offset",0)
    
    jobtype = request.args.get('jobtype', None)

    geofilter = None    
    lat = request.args.get('lat', None)
    lon = request.args.get('lon', None)
    dist = request.args.get('dist', None)

    try:
        limit=int(limit)
        offset=int(offset)
    except ValueError:
        abort(400)
    if (limit < 0 or offset < 0):
        abort(400)

    if (lat != None and lon != None and dist != None):
        try:
            lat = float(lat)
            lon = float(lon)
            geofilter = {'lat': lat, 'lon': lon, 'dist': dist}
        except ValueError:
            abort(400)

    ads=jobads.fetch.ads.getAdsBySimpleQuery(q=q, limit=limit, offset=offset, jobtype=jobtype, geofilter=geofilter)
    return jsonify(ads)

@app.route('/api/ads/search', methods=['POST'])
def get_ads_post():
    data = request.get_json()
    limit=request.args.get("limit")
    offset=request.args.get("offset")
    if data and 'q' in data:
        ads=jobads.fetch.ads.getAdsBySimpleQuery(q=str(data['q']), limit=limit, offset=offset)
        return jsonify(ads)
    else:
        abort(400)

@app.route('/api/ads/coords/search/<q>', methods=['GET'])
def get_ads_coords(q):
    coords=jobads.fetch.ads.getAdsCoordsBySimpleQuery(q)
    return jsonify(coords)

if __name__ == '__main__':
    app.run(debug=True)
