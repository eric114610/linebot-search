import boto3
import json
import requests
from requests_aws4auth import AWS4Auth
import ast

region = 'ap-northeast-3' # For example, us-west-1
service = 'es'
# credentials = boto3.Session().get_credentials()
# awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

apigatewayendpoint = 'https://10p2k383h8.execute-api.ap-northeast-3.amazonaws.com/opensearch-api-test/'

def GetMessageMethod(index, _embedding, _id, _date="2024-01-01 00:00:00", _user="Admin", _date_before="2025-12-31 11:59:59"):
    params = { "type": "GetMessage", "size": 25 , "q": index, "embedding": str(_embedding), "id": _id, "date": _date, "user": _user, "date_before": _date_before}
    r = requests.get(apigatewayendpoint, params)
    # print(r.text)
    response = r.json()
    print(response["hits"]["hits"][0]['_source']['user'])
    return

def GetUserMthod(index, _id):
    params = { "type": "GetUser", "size": 25 , "q": index, "id": _id}
    r = requests.get(apigatewayendpoint, params)
    print(r.text)
    return

def PostMessageMethod(index, _message, _embedding, _id, _date, _user="Admin"):
    params = { "type": "PostMessage", "size": 25 , "q": index, "message": _message, "embedding": str(_embedding), "id": _id, "date": _date, "user": _user}
    r = requests.get(apigatewayendpoint, params)
    print(r.text)
    # print(type(params["embedding"]))
    return

def PostUserMethod(index, _embedding, _id, _date="2024-01-01 00:00:00", _date_before="2025-12-31 11:59:59"):
    params = { "type": "PostUser", "size": 25 , "q": index, "embedding": str(_embedding), "id": _id, "date": _date, "date_before": _date_before}
    r = requests.get(apigatewayendpoint, params)
    print(r.text)
    # print(type(params["embedding"]))
    return

def Putmethod(index, newIndexType):
    params = { "type": "Put", "size": 25 , "q": index, "newIndexType": newIndexType}
    r = requests.get(apigatewayendpoint, params)
    print(r.text)
    return

if __name__ == '__main__':
    # Getmethod("test-index3", "aaa", [1,2,3], 1)
    # s = str([1.1,2.2,3.3])
    # lst = ast.literal_eval(s)
    # print(lst, type(lst))
    # Postmethod("test-index3", "ccc", [5.14,6.02,3.74], 2)
    GetMessageMethod("message-test2", [2,4,3], 1, _date="2024-07-02 14:52:57")
    # Putmethod("message-test2", "aaa", [1,2,3], 1, "Group")
    # PostMessageMethod("message-test2", "我是誰", [19.392,-1.214,0.9124], 4, "2024-07-02 16:08:15", "User李")
    # Putmethod("user-test", "aaa", [1,2,3], 1, "User")
    # PostUserMethod("user-test", [2.2,4.4,3.22], 4, "2024-07-01 10:35:34", "2025-11-06 10:21:32")
    # GetUserMthod("user-test", 4)