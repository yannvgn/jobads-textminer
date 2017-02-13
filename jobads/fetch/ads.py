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

def getAdsBySimpleQuery(q):
    q = str(q)
    
    return _formatQueryResponse(_queryElastic(body={
        'from' : 0, 'size' : 30,
        'query': {
            'multi_match' : {
                'query':    q,
                'fields': [ 'title_fr', 'description_fr', 'company', 'location' , 'id' ]
            }
        }
    }))
