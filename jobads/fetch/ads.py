from jobads import config
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=config['elasticsearch']['hosts'], verify_certs=True)

def _formatResult(hit):
    result = hit['_source']
    result['_id'] = hit['_id']
    result['_score'] = hit['_score']
    return result

def _formatQueryResponse(esResult):
    return {
        'results': [_formatResult(hit) for hit in esResult['hits']['hits']],
        'total': esResult['hits']['total'],
        'max_score': esResult['hits']['max_score']
    }

def _queryElastic(**args):
    return es.search(index=config['elasticsearch']['job_ads_index'], doc_type=config['elasticsearch']['ad_doc_type'], **args)

def getAdsBySimpleQuery(q,limit,offset,jobtype):
    q = str(q)
    
    filters = []

    if jobtype:
         filters.append({'term': {'jobtype': jobtype}})

    return _formatQueryResponse(_queryElastic(body={
        'from' : offset, 'size' : limit,
        'query': {
            'bool': {
                'must': {
                    'multi_match' : {
                        'query':    q,
                        'fields': [ 'title_fr', 'description_fr', 'company', 'location' , 'id' ]
                    }
                },
                'filter': filters
            }
        }
    }))

def getAdsCoordsBySimpleQuery(q):
    nb_max_results = 1000

    q = str(q)

    esResult = _queryElastic(_source=['geolocation'], body={
        'query': { 
            'bool': {
                'must': {
                    'multi_match' : {
                        'query':    q,
                        'fields': [ 'title_fr', 'description_fr', 'company', 'location']
                    }
                },
                'filter': {
                    'exists': {'field': 'geolocation'}
                }
            }
        },
        'size': nb_max_results
    })

    return _formatQueryResponse(esResult)
