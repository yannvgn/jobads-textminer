from flask import Flask, jsonify, request, abort
from datetime import datetime

import jobads.fetch.ads 

app = Flask(__name__)

# Routing

# Deprecated
@app.route('/api/ads/search/<q>', methods=['GET'])
def get_ads_legacy(q):
    limit, offset = _getLimitOffset(request)
    filters = _getFilters(request)
    ads=jobads.fetch.ads.getAdsBySimpleQuery(q=q, limit=limit, offset=offset, filters=filters)
    return jsonify(ads)

@app.route('/api/ads/search', methods=['POST', 'GET'])
def get_ads():
    limit, offset = _getLimitOffset(request)
    filters = _getFilters(request)
    q = _getRequiredParam(request, 'q')
    ads=jobads.fetch.ads.getAdsBySimpleQuery(q=q, limit=limit, offset=offset, filters=filters)
    return jsonify(ads)

@app.route('/api/ads/get/<ids>', methods=['GET'])
def get_ads_by_ids(ids):
    ads = jobads.fetch.ads.getAdsByIds(ids.split(','))
    return jsonify(ads)

# Deprecated
@app.route('/api/ads/coords/search/<q>', methods=['GET'])
def get_ads_coords_legacy(q):
    coords=jobads.fetch.ads.getAdsCoordsBySimpleQuery(q, filters=_getFilters(request))
    return jsonify(coords)

@app.route('/api/ads/coords/search', methods=['POST', 'GET'])
def get_ads_coords():
    q = _getRequiredParam(request, 'q')
    coords=jobads.fetch.ads.getAdsCoordsBySimpleQuery(q, filters=_getFilters(request))
    return jsonify(coords)

@app.route('/api/ads/get_basic_info', methods=['POST', 'GET'])
def get_ads_basic_info():
    ids = _getRequiredParam(request, 'ids')
    if type(ids) != list:
        ids = str(ids).split(',')
    
    basic_info=jobads.fetch.ads.getAdsBasicInfoByIds(ids)
    return jsonify(basic_info)


# Internal functions

def _getParam(req, key, default=None):
    return req.get_json().get(key, default) if req.is_json else req.args.get(key, default)

def _getRequiredParam(req, key, errorCode=400):
    p = _getParam(req, key)
    if p == None:
        abort(400)
    else:
        return p

def _getLimitOffset(req):
    limit = _getParam(req, 'limit')
    offset = _getParam(req, 'offset')
    if limit != None:
        try:
            limit = int(limit)
            if limit < 0:
                abort(400)
        except ValueError:
            abort(400)
    if offset != None:
        try:
            offset = int(offset)
            if offset < 0:
                abort(400)
        except ValueError:
            abort(400)
    return limit, offset
    
def _getFilters(req):
    filters = {}
    filters.update(_getJobtypeFilter(req))
    filters.update(_getGeoFilter(req))
    filters.update(_getSalaryFilter(req))
    filters.update(_getFromDateFilter(req))
    return filters

def _getJobtypeFilter(req):
    jobtype = _getParam(req, 'jobtype')
    if jobtype != None:
        return {'jobtype': jobtype}
    else:
        return {}

def _getGeoFilter(req):
    lat = _getParam(req, 'lat')
    lon = _getParam(req, 'lon')
    dist = _getParam(req, 'dist')
    if (lat != None and lon != None and dist != None):
        try:
            lat = float(lat)
            lon = float(lon)
            return {'geodistance': {'lat': lat, 'lon': lon, 'dist': dist}}
        except ValueError:
            abort(400)
    else:
        return {}

def _getSalaryFilter(req):
    salary_min = _getParam(req, 'salary_min')
    if salary_min != None:
        try:
            salary_min = float(salary_min)
            return {'salary': {'min': salary_min}}
        except ValueError:
            abort(400)
    else:
        return {}

def _getFromDateFilter(req):
    fromDate = _getParam(req, 'from_date')
    if fromDate != None:
        try:
            d = datetime.strptime(fromDate, '%Y-%m-%dT%H:%M:%S.%fZ')
            return {'from_date': d}
        except ValueError:
            abort(400)
    else:
        return {}

if __name__ == '__main__':
    app.run(debug=True)
