import boto3
import json
import requests
from requests_aws4auth import AWS4Auth

region = 'ap-northeast-3' # For example, us-west-1
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

host = 'https://search-linebot-search-3uafa4oepdfjx4tfk3emvsh5a4.aos.ap-northeast-3.on.aws' # The OpenSearch domain endpoint with https:// and without a trailing slash
datatype = '_doc'
# index = 'movies'
index = 'test-index'
# url = host + '/' + index + '/_search'
# url_index = host + '/' + index
# url_post = host + '/' + index + '/' + datatype + '/'
# Lambda execution starts here
def lambda_handler(event, context):

    # Put the user query into the query DSL for more accurate search results.
    # Note that certain fields are boosted (^).
    # query = {
    #     "size": 25,
    #     "query": {
    #         "multi_match": {
    #             "query": "thor",
    #             "fields": ["title^4", "plot^2", "actors", "directors"]
    #         }
    #     }
    # }
  #   query = {
  #   "size": 2,
  #   "query": {
  #     "knn": {
  #       "item_vector": {
  #         "vector": [
  #           2, 4, 3
  #         ],
  #         "k": 10,
  #         "filter": {
  #           "bool": {
  #             "must": [
  #               {
  #                 "range": {
  #                   "rating": {
  #                     "gte": 1,
  #                     "lte": 10
  #                   }
  #                 }
  #               }
  #             ]
  #           }
  #         }
  #       }
  #     }
  #   }
  # }
    query = {
      "size": 2,
      "query": {
        "knn": {
          "embedding": {
            "vector": [
              2, 4, 3
            ],
            "k": 10
          }
        }
      }
    }
    
    # test_index = '{"settings": {"index": {"knn": true}},"mappings": {"properties": {"item_vector": {"type": "knn_vector","dimension": 3,"method": {"name": "hnsw","space_type": "l2","engine": "faiss"}}}}}'
    test_index = """{
    "settings": {
       "index.knn": true
    },
    "mappings": {
       "properties": {
          "embedding": {
             "type": "knn_vector",
             "dimension": 3
          },
          "message": {
             "type": "text"
          }
       }
    }
}"""
    
    data = json.loads(test_index)
    # post_item = '{ "item_vector": [6.4, 3.4, 6.6], "size" : "small", "rating" : 9 }'
    # print(post_item)
    # # data_post = json.loads(post_item)
    # post_item = '{"embedding": ' + str(event['queryStringParameters']['embedding']) + ', "message": "' + event['queryStringParameters']['message'] + '"}'
    # print(post_item)
    # data_post = json.loads(post_item)


    index = 'test-index'
    index = event['queryStringParameters']['q']
    url = host + '/' + index + '/_search'
    url_index = host + '/' + index
    url_post = host + '/' + index + '/' + datatype + '/'
    
    # Elasticsearch 6.x requires an explicit Content-Type header
    headers = { "Content-Type": "application/json" }
    if(event['queryStringParameters']['type'] == "Get"):
        r = requests.get(url, auth=awsauth, headers=headers, data=json.dumps(query))
    elif(event['queryStringParameters']['type'] == "Post"):
        r = requests.post(url_post + event['queryStringParameters']['id'], auth=awsauth, headers=headers, data=json.dumps(data_post))
    elif(event['queryStringParameters']['type'] == "Put"):
        r = requests.put(url_index, auth=awsauth, headers=headers, data=json.dumps(data))
    else:
        print("No Re", type(event['queryStringParameters']['type']), event['queryStringParameters']['type'])
    
    # Make the signed HTTP request
    # r = requests.get(url, auth=awsauth, headers=headers, data=json.dumps(query))
    # r = requests.put(url_index, auth=awsauth, headers=headers, data=json.dumps(data))
    # r = requests.post(url_post + '1', auth=awsauth, headers=headers, data=json.dumps(data))

    # Create the response and add some extra content to support CORS
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": '*',
        },
        "isBase64Encoded": False
    }

    # Add the search results to the response
    response['body'] = r.text
    print(event['queryStringParameters'])
    return response