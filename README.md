## functions are written in test.py

### Note
currently, use asycn approach to ensure data intergrity, use asyncio.run(your_func()) to run, your_func() also has to be async

if don't need to consider data intergrity, delete all async declare before functions and run normally

### index structure
GroupIndex:
    user (news source?)
    url
    message (news)
    embedding
    date

UserIndex:
    embedding (768, currently for testing only 3)
    date
    date_before
    (can search from date ~ date_before)

### functions
#### addNewUserInformation()
requires userID, add new object for user setting
returns bool indicate success

#### updateUserInformation
requires userID, update user setting
returns bool indicate success

it will first use GetMessageMethod() to get old setting

#### addNewGroup
requires GroupID, add new index for Group

initially, there's a object with id=1, which is used to keep track of total number of object
returns bool indicate success

#### addMessage
requires GroupID, _message, _embedding, _date
returns bool indicate success

it will first use GetMessageMethod() to get number count of objects, then assign new object with id = count+1

#### queryMessage
currently onlny requires userID, will perform search based on userSetting
returns a dict containing information of best match data

#### GetUserSetting, GetGruopInfo
straightforward, returns a dict containing information


### for modifying aws
#### current work flow
python file calls requests.get() -> aws api geteway -> aws lambda (function written in /my-opensearch-function/opensearch-lambda.py) -> aws opensearch

if need to add new field, adjust api gateway on aws console -> modify lambda func and upload to aws lambda

#### opensearch console
https://search-linebot-search-3uafa4oepdfjx4tfk3emvsh5a4.aos.ap-northeast-3.on.aws/_dashboards
name: Eric, passwd:LiuLiuLeeLai123!

can see and manually delete index

#### remain indecies
User: test-user3
Group: stocks, sports, 