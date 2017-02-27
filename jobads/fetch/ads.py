from jobads import config
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=config['elasticsearch']['hosts'], verify_certs=True)

def getAdsBySimpleQuery(q,limit=None,offset=None,filters={}):
    if limit == None:
        limit = 10
    if offset == None:
        offset = 0

    return _formatQueryResponse(_queryElastic(body={
        'from': offset, 'size': limit,
        'query': {
            'bool': {
                'must': {
                    'multi_match': {
                        'query': str(q),
                        'fields': ['title_fr', 'description_fr', 'company', 'location']
                    }
                },
                'filter': _makeFilterBody(filters)
            }
        }
    }))

def getAdsByIds(ids):
    return {
        'results': [_formatResult(doc) for doc in _mgetQuery(body={'ids' : ids})['docs']]
    }

def getAdsBasicInfoByIds(ids):
    return {
        'results': [_formatResult(doc) for doc in _mgetQuery(body={'ids' : ids}, _source=['company', 'title_fr', 'jobtype'])['docs']]
    }

def getAdsCoordsBySimpleQuery(q, filters={}):
    nb_max_results = 1000
    filterBody = _makeFilterBody(filters)
    filterBody.append({'exists': {'field': 'geolocation'}})

    esResult = _queryElastic(_source=['geolocation'], body={
        'query': { 
            'bool': {
                'must': {
                    'multi_match': {
                        'query': str(q),
                        'fields': [ 'title_fr', 'description_fr', 'company', 'location']
                    }
                },
                'filter': filterBody
            }
        },
        'size': nb_max_results
    })

    return _formatQueryResponse(esResult)



# Internal functions

def _formatResult(r):
    if r.get('found') == False:
        return None

    result = r['_source']
    result['_id'] = r['_id']
    if '_score' in r:
        result['_score'] = r['_score']
    return result

def _formatQueryResponse(esResult):
    return {
        'results': [_formatResult(hit) for hit in esResult['hits']['hits']],
        'total': esResult['hits']['total'],
        'max_score': esResult['hits']['max_score']
    }

def _queryElastic(**args):
    return es.search(index=config['elasticsearch']['job_ads_index'], doc_type=config['elasticsearch']['ad_doc_type'], **args)

def _mgetQuery(**args):
    return es.mget(index=config['elasticsearch']['job_ads_index'], doc_type=config['elasticsearch']['ad_doc_type'],  **args)

def _makeFilterBody(filters):
    filterBody = []
    if 'jobtype' in filters:
        filterBody.append({'term': {'jobtype': filters['jobtype']}})
    if 'geodistance' in filters:
        filterBody.append({
            'geo_distance' : {
                'distance' : str(filters['geodistance']['dist']),
                'geolocation' : {
                    'lat' : float(filters['geodistance']['lat']),
                    'lon' : float(filters['geodistance']['lon'])
                }
            }
        })
    if 'salary' in filters:
        filterBody.append({
            'range': {
                'salary.min' : {'gte': filters['salary']['min']}
            }
        })
    return filterBody
