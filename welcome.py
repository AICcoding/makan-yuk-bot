# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
from argparse import ArgumentParser
from flask import Flask, request, abort, jsonify
from models import db, Pedagang
from linebot import (
    LineBotApi, WebhookParser, WebhookHandler
)
from linebot.exceptions import(
    InvalidSignatureError
)
from linebot.models import(
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, URITemplateAction, PostbackTemplateAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent
)

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', None)
CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if CHANNEL_SECRET is None:
    print 'Silahkan set LINE_CHANNEL_SECRET pada environment variable.'
    sys.exit(1)
if CHANNEL_ACCESS_TOKEN is None:
    print 'Silahkan set LINE_CHANNEL_ACCESS_TOKEN pada environment variable.'
    sys.exit(1)

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

db.init_app(app)

@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

@app.route('/callback', methods=['POST'])
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
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    if event.message.text == 'gus':
        teks = 'engken gus?'
    else:
        teks = event.message.text
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=teks)
    )

@app.route('/myapp')
def WelcomeToMyapp():
    return 'Welcome again to my app running on Bluemix! 12 Mar'

@app.route('/api/people')
def GetPeople():
    list = [
        {'name': 'Sentanu', 'age': 28},
        {'name': 'Bill', 'val': 26}
    ]
    return jsonify(results=list)

@app.route('/api/people/<name>')
def SayHello(name):
    message = {
        'message': 'Hello ' + name
    }
    return jsonify(results=message)

@app.route('/pedagang', methods=['GET'])
def getProduct():  
    data = Pedagang.query.all() #fetch all products on the table

    data_all = []

    for pedagang in data:
        data_all.append([pedagang.id, pedagang.nama, pedagang.alamat]) #prepare visual data

    return jsonify(products=data_all)

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
