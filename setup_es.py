from elasticsearch import Elasticsearch

def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        print('Connected Elasticsearch')
    else:
        print('Elasticsearch could not connect!')
    return _es

def create_index(es_object, index_name):
    created_index_indicator = False
    settings = {
        "settings": {
            "number_of_shards": 2,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "name_people": {
                    "type": "text"
                },
                "college": {
                    "type": "text"
                },
                "position": {
                    "type": "text"
                },
                "company": {
                    "type": "text"
                },
                "time_work_at_company": {
                    "type": "text",
                },
                "location": {
                    "type": "text",
                },
                "link": {
                    "type": "text",
                }
            }
        }
    }

    try:
        if not es_object.indices.exists(index_name):
            print("Not exists")
            res = es_object.indices.create(index=index_name, ignore=400, body=settings)
            print(res)
        created_index = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created_index

def store_record(elastic_object, index_name, index_id, record):
    is_stored = True
    try:
        output = elastic_object.index(index=index_name, id=index_id, body=record)
        print(output)
    except Exception as ex:
        print("Error in indexing data")
        print(str(ex))
        is_stored = False
    finally:
        return is_stored