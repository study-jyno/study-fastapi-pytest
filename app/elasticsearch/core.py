from opensearchpy import OpenSearch
from opensearchpy.exceptions import NotFoundError

from app.config import ES_HOST, ES_PORT, ES_USER, ES_PASSWORD

host = ES_HOST
port = ES_PORT
auth = (ES_USER, ES_PASSWORD)  # 로그인 하려는 유저

# Create the client with SSL/TLS enabled, but hostname verification disabled.
es_client = OpenSearch(
    hosts=[{'host': host, 'port': port}],
    http_compress=True,  # enables gzip compression for request bodies
    http_auth=auth,
    use_ssl=True,
    verify_certs=True,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
)

# Create an index with non-default settings.
index_name = 'auditlog-log-index'
index_body = {
    'settings': {
        'index': {
            'number_of_shards': 4
        }
    }
}

try:
    _response = es_client.search(
        body={
            'query': {
                'match': {
                    "_index": index_name
                }
            }
        },
        index=index_name
    )
except NotFoundError as e:
    es_client.indices.create(index_name, body=index_body)


def get_open_search_client():
    return es_client
