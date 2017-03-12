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
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import(
    InvalidSignatureError
)
from linebot.models import(
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print 'Silahkan set LINE_CHANNEL_SECRET pada environment variable.'
    sys.exit(1)
if channel_access_token is None:
    print 'Silahkan set LINE_CHANNEL_ACCESS_TOKEN pada environment variable.'
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request Body: " + body)

    #parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if event.message.text == 'gus':
            teks = 'engken gus?'
        else:
            teks = event.message.text
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=teks)
        )

    return 'OK'

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

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
