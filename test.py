import boto3
import json
import requests
from requests_aws4auth import AWS4Auth
import ast
import asyncio

region = 'ap-northeast-3' # For example, us-west-1
service = 'es'
# credentials = boto3.Session().get_credentials()
# awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

apigatewayendpoint = 'https://o0p2k383h8.execute-api.ap-northeast-3.amazonaws.com/opensearch-api-test/'

######## methods for sending request to lambda, don't directly call
## TODO: error handling

def GetMessageMethod(index, _embedding, _id, _date="2024-01-01 00:00:00", _user="Admin", _date_before="2025-12-31 11:59:59"):
    params = { "type": "GetMessage", "size": 25 , "q": index, "embedding": str(_embedding), "id": _id, "date": _date, "user": _user, "date_before": _date_before}
    r = requests.get(apigatewayendpoint, params)
    # print(r.text)
    response = r.json()
    # print(response["hits"]["hits"][0]['_source']['user'])
    if r.status_code == 200: 
        return response["hits"]["hits"][0]['_source']
    else:
        return {"embedding": f"Error, status code {r.status_code}\n Error message:\n {r.text}"}

def GetUserMethod(index, _id):
    params = { "type": "GetUser", "size": 25 , "q": index, "id": _id}
    r = requests.get(apigatewayendpoint, params)
    response = r.json()
    # print(r.text)
    if r.status_code == 200: 
        return response["hits"]["hits"][0]['_source']
    else:
        return {"embedding": f"Error, status code {r.status_code}\n Error message:\n {r.text}"}

def PostMessageMethod(index, _message, _embedding, _id, _date, _user="Admin", _url=""):
    params = { "type": "PostMessage", "size": 25 , "q": index, "message": _message, "embedding": str(_embedding), "id": _id, "date": _date, "user": _user, "url": _url}
    r = requests.get(apigatewayendpoint, params)
    # print(r.text)
    # print(type(params["embedding"]))
    if r.status_code == 200: 
        return True
    else:
        return {"embedding": f"Error, status code {r.status_code}\n Error message:\n {r.text}"}

def PostUserMethod(index, _embedding, _id=1, _date="2024-01-01 00:00:00", _date_before="2025-12-31 11:59:59"):
    params = { "type": "PostUser", "size": 25 , "q": index, "embedding": str(_embedding), "id": _id, "date": _date, "date_before": _date_before}
    r = requests.get(apigatewayendpoint, params)
    # print(r.text)
    # print(type(params["embedding"]))
    if r.status_code == 200: 
        return True
    else:
        return {"embedding": f"Error, status code {r.status_code}\n Error message:\n {r.text}"}

def Putmethod(index, newIndexType):
    params = { "type": "Put", "size": 25 , "q": index, "newIndexType": newIndexType}
    r = requests.get(apigatewayendpoint, params)
    # print(r.text)
    if r.status_code == 200: 
        return True
    else:
        return {"embedding": f"Error, status code {r.status_code}\n Error message:\n {r.text}"}

###############################################################################################
# functions for linebot, modify if you want
# will have extra 1 second delay for syncronize

async def addNewUserInformation(userID, _embedding=[0,0,0], _date="2024-01-01 00:00:00", _date_before="2025-12-31 11:59:59"):
    Putmethod(userID, "User")
    if PostUserMethod(userID, _embedding, 1, _date, _date_before):
        await asyncio.sleep(1)
        return True
    else:
        return False
    
async def updateUserInformation(userID, _embedding=[0,0,0], _date="2024-01-01 00:00:00", _date_before="2025-12-31 11:59:59"):
    userSetting = GetUserMethod(userID, 1)

    if _embedding == [0,0,0]:
        _embedding = userSetting["embedding"]
    if _date == "2024-01-01 00:00:00":
        _date = userSetting['date']
    if _date_before == "2025-12-31 11:59:59":
        _date_before = userSetting["date_before"]

    if PostUserMethod(userID, _embedding, 1, _date, _date_before):
        await asyncio.sleep(1)
        return True
    else:
        return False
    


async def addNewGroup(GroupID):
    Putmethod(GroupID, "Group")
    if PostMessageMethod(GroupID, "1", [0,0,0], 1, "2024-01-01 00:00:00"):
        await asyncio.sleep(1)
        return True
    else:
        return False

async def addMessage(GroupID, _message, _embedding, _date, _user="Admin", _url=""):
    GroupMcount = int(GetMessageMethod(GroupID, [0,0,0], 1)['message'])

    if not PostMessageMethod(GroupID, _message, _embedding, GroupMcount+1, _date, _user, _url):
        return False
    if not PostMessageMethod(GroupID, str(GroupMcount+1), [0,0,0], 1, "2024-01-01 00:00:00"):
        return False
    
    # uncomment if needed to avoid synchronize problem
    # await asyncio.sleep(1)
    return True

async def queryMessage(userID, GroupID, _embedding=[0,0,0], _date="2024-01-01 00:00:00", _user="Admin", _date_before="2025-12-31 11:59:59"):
    userSetting = GetUserMethod(userID, 1)
    print(userSetting['embedding'])
    return GetMessageMethod(GroupID, userSetting['embedding'], 0, userSetting['date'], _user, userSetting['date_before'])

async def GetUserSetting(userID):
    return GetUserMethod(userID, 1)

async def GetGruopInfo(GruopID):
    return GetMessageMethod(GruopID, [0,0,0], 1)


## example for async function

async def testasync():
    c = await addNewGroup("drinks")
    print(c)
    print("000")
    a = await addMessage("drinks", "testdrink", [5,4,3], "2024-07-03 15:26:11", _url="https://docs.python.org/3/library/asyncio-task.html#coroutines")
    print(a)
    print("111")
    b = await queryMessage("test-user3", "drinks")
    print(b)
    print("222")

if __name__ == '__main__':
    # Getmethod("test-index3", "aaa", [1,2,3], 1)
    # s = str([1.1,2.2,3.3])
    # lst = ast.literal_eval(s)
    # print(lst, type(lst))
    # Postmethod("test-index3", "ccc", [5.14,6.02,3.74], 2)
    # GetMessageMethod("message-test2", [2,4,3], 1, _date="2024-07-02 14:52:57")
    # Putmethod("message-test2", "aaa", [1,2,3], 1, "Group")
    # PostMessageMethod("message-test2", "我是誰", [19.392,-1.214,0.9124], 4, "2024-07-02 16:08:15", "User李")
    # Putmethod("user-test", "aaa", [1,2,3], 1, "User")
    # PostUserMethod("user-test", [2.2,4.4,3.22], 4, "2024-07-01 10:35:34", "2025-11-06 10:21:32")
    # GetUserMthod("test-user1", 1)
    # addNewUserInformation("test-user1", [1,2,3], "2024-07-02 12:22:14")
    # updateUserInformation("test-user1", _date_before="2024-12-11 00:00:00")
    # GetUserMethod("test-user1", 1)
    # print(addNewGroup("food"))
    # GetMessageMethod("stocks", [0,0,0], 1)
    # addMessage("sports", "btestb", [-0.42,1.124,-2.974], "2024-07-03 14:48:12", "Admin", "www.testing.com")
    # print(addMessage("stocks", "ctestcc", [3,-1.34,-4.12], "2024-07-03 11:56:41", "Admin"))
    # updateUserInformation("test-user1", [3,-1.34,-4.12])
    # print(queryMessage("test-user1", "sports"))
    # print(GetUserSetting("test-user1"))
    re = asyncio.run(GetGruopInfo("sports"))
    print(re)
    # asyncio.run(testasync())