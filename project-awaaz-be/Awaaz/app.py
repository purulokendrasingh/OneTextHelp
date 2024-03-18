import logging

import requests
from flask import Flask, request
from twilio.rest import Client
import json
import uuid
import nlp_module
from datetime import datetime
from azure.cosmos import CosmosClient

app = Flask(__name__)

ACCOUNT_SID = "5tvh859h98rgmh589v35mh895vyh589m"
AUTH_TOKEN = "985vh835vmjo849v89gh359834gmhv3598"
TWILIO_NUMBER = '+0000000000'
ACKNOWLEDGEMENT_MESSAGE = 'Hi {0}\nWe hope you are safe. OneTextHelp is here for you. Your message has been broadcasted. We ' \
                          'will let you know if someone reverts. Stay Strong. We are in this together. '
COSMOS_ACCOUNT_URI = "https://onetexthelp-db.documents.azure.com:443/"
COSMOS_ACCOUNT_KEY = "4389thm498t4j084j08rj48hg804j408mtj408j480tjv048gj4m80j7he297r3hr9m=="


@app.route("/health")
def hello():
    return "OneTextHelp services are online"


@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    user_phone_number = request.values.get('From', None)
    body = request.values.get('Body', None)

    names_array = nlp_module.get_human_names(body)
    names_in_post = ""

    if len(names_array) > 0:
        names_in_post = names_array[0]

    logic_app_endpoint = "https://onetexthelp.azurewebsites.net:443/api/test1/triggers/manual/" \
                         "invoke?api-version=2020-05-01-preview&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0" \
                         "&sig=YUL8ERyjlLQC93pyoCAG9VTImq3TnMOp9EdTGPoyDY8"

    headers = {"Content-Type": "application/json"}

    new_guid = uuid.uuid4().hex
    post_url = "https://forums.onetexthelp.com/queries/{0}".format(new_guid)

    data = {
        "phone": user_phone_number,
        "message": body,
        "postUrl": post_url,
        "postId": new_guid,
        "name": names_in_post,
        "datetime": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    y = json.dumps(data)

    requests.post(url=logic_app_endpoint, headers=headers, data=y)

    # Send the acknowledgement message back
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    message_body = ACKNOWLEDGEMENT_MESSAGE.format(names_in_post) + '\n\n' + '- OneTextHelp Team'

    message = client.messages.create(
        body=message_body,
        from_=TWILIO_NUMBER,
        to=user_phone_number
    )

    return str(message)


@app.route("/replies", methods=['POST'])
def twitter_replies():
    # Get the response, map it with a class, fetch phones numbers via the conversation_id and send the replies back
    if request.json['meta']['result_count'] <= 0:
        return 1

    data = request.json['data']

    if len(data) <= 0:
        return 2

    conversation_ids = []
    for item in data:
        if item['conversation_id'] not in conversation_ids:
            conversation_ids.append(item['conversation_id'])

    cosmos_url = COSMOS_ACCOUNT_URI
    cosmos_key = COSMOS_ACCOUNT_KEY
    cosmos_client = CosmosClient(cosmos_url, credential=cosmos_key)

    database_name = 'OneTextHelp'
    database = cosmos_client.get_database_client(database_name)
    message_details_container_name = 'MessageDetails'
    message_details_container = database.get_container_client(message_details_container_name)

    messageDetailsFilter = '"' + '","'.join(conversation_ids) + '"'

    query = 'SELECT r.phone,r.TweetId FROM r WHERE r.TweetId in ({0})'.format(messageDetailsFilter)

    items = list(message_details_container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))

    original_tweet_ids = list(map(lambda a: str(a['TweetId']), items))
    duplicateCheckQueryFilter = '"' + '","'.join(original_tweet_ids) + '"'

    duplicateCheckQuery = 'SELECT r.replyTweetId FROM r WHERE r.originalTweetId in ({0})'.format(
        duplicateCheckQueryFilter)
    print(duplicateCheckQuery)

    reply_details_container_name = 'ReplyDetails'
    reply_details_container = database.get_container_client(reply_details_container_name)

    allReplyIdRecords = list(reply_details_container.query_items(
        query=duplicateCheckQuery,
        enable_cross_partition_query=True
    ))

    allReplyIds = map(lambda a: a['replyTweetId'], allReplyIdRecords)

    responseDictionary = {}
    tweetIdPair = {}

    for item in items:
        dictKey = item['phone']
        compositeKey = str(item['TweetId'])
        message = ''

        replyTweetIds = []
        for elem in data:
            if elem['conversation_id'] == compositeKey and elem['id'] not in allReplyIds:
                replyTweetIds.append(elem['id'])

        for newId in replyTweetIds:
            tweetIdPair[compositeKey] = newId

        for elem in data:
            if elem['id'] in replyTweetIds:
                message += elem['text'] + "\n\n"

        if dictKey in responseDictionary.keys():
            responseDictionary[dictKey] += message
        else:
            responseDictionary[dictKey] = message

    for originalTweetId in tweetIdPair.keys():
        reply_details_container.upsert_item({
            'id': uuid.uuid4().hex,
            'originalTweetId': originalTweetId,
            'replyTweetId': tweetIdPair[originalTweetId]
        })

    for phoneNumber in responseDictionary.keys():
        try:
            if responseDictionary[phoneNumber] != '':
                # Send the acknowledgement message back
                client = Client(ACCOUNT_SID, AUTH_TOKEN)

                message = client.messages.create(
                    body=responseDictionary[phoneNumber] + '\n\n' + '- OneTextHelp Team',
                    from_=TWILIO_NUMBER,
                    to=phoneNumber
                )
        except:
            logging.info("Error while sending message for number: {0}".format(phoneNumber))

    return responseDictionary


if __name__ == "__main__":
    app.run(debug=True)
