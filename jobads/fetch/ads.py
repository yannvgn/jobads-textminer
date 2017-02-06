from jobads import config
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=config['elasticsearch']['hosts'], verify_certs=True)

def getAdsBySimpleQuery(q):
    esResult = es.search(index=config['elasticsearch']['job_ads_index'], doc_type=config['elasticsearch']['ad_doc_type'], q=q)
    results = []
    for result in esResult['hits']['hits']:
        results.append(result['source'])
    return results
