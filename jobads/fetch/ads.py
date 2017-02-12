from jobads import config
from flask import request
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

def getAdsBySimpleQuery(q):
    if type(q) != str:
        return {}
    
    return _formatQueryResponse(_queryElastic(body={
        'from' : request.arg.get('limit'), 'size' : request.args.get('offset'),
        'query': {
            'multi_match' : {
                'query':    q,
                'fields': [ 'title_fr', 'description_fr', 'company', 'location' ]
            }
        }
    }))
