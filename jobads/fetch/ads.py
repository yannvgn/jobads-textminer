from jobads import config
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=config['elasticsearch']['hosts'], verify_certs=True)

def getAdsBySimpleQuery(q):
    if type(q) != str:
        return []
    
    esResult = es.search(index=config['elasticsearch']['job_ads_index'], doc_type=config['elasticsearch']['ad_doc_type'], body={
        'query': {
            'multi_match' : {
                'query':    q,
                'fields': [ 'title_fr', 'description_fr', 'company', 'location' ]
            }
        }
    })
    results = []
    for result in esResult['hits']['hits']:
        results.append(result['_source'])
    return results
