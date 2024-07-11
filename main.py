from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

import os
import google.generativeai as genai  
import test_db as db 
from datetime import datetime
import time

app = Flask(__name__)

configuration = Configuration(access_token=os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

Users = {}

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

def verify_user(uid, embedding):
    if uid not in Users:
        Users[uid] = genai.GenerativeModel('gemini-1.5-flash')
        db.addNewUserInformation(uid, embedding)
        time.sleep(2)

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):

    title = model.generate_content(event.message.text + "\n please directly output only the title in english\n")
    summary = model.generate_content(event.message.text + "\n output 5 keywords in english\n")
    embedding = genai.embed_content(model='models/embedding-001', content=summary.text, task_type="retrieval_document", title=title.text)['embedding']
    embedding = [round(i, 5) for i in embedding]
    # print("embedding cc : ", embedding) # length 768, type dict
    user_id = "abcdefg123"
    # verify_user(user_id, embedding)
    zz = [0]*768
    action = event.message.text.split(' ')[0][1:]
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("action cc : _", action, "_")
    # print("group info : ", db.GetGruopInfo("1"))
    # db.addNewGroup("9")
    reply = ""
    if action == 'add':
        # db.addNewGroup("4")
        # time.sleep(2)
        # success = db.addMessage("9", event.message.text[1:], embedding, now)
        success = db.addMessage("7", ' '.join(summary.text.split('\n')), embedding, now)
        print("add: ", success)
        reply = "add success"
    elif action == 'query':
        question = ' '.join(event.message.text.split(' ')[1:])
        print("qu cc: ", question)
        embedding = genai.embed_content(model='models/embedding-001', content=question, task_type="retrieval_document", title=question)['embedding']
        embedding = [round(i, 5) for i in embedding]
        print("embed cc: ", embedding)
        db.updateUserInformation(user_id, embedding)
        time.sleep(2)
        query = db.queryMessage(user_id, "7")
        reply = query['message']

    # print(event.message.text)
    # print(response.text)

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply)]
            )
        )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)


