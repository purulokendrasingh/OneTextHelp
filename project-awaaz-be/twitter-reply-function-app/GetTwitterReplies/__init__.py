import datetime
import logging
import requests
import os
import json
import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    searchApiResponse = GetTwitterSearchResults()
    searchApiJson = searchApiResponse.json()

    logging.info(searchApiJson)

    if searchApiResponse.ok and searchApiJson['meta']['result_count'] > 0:
        SendRepliesToUser(searchApiJson)

    logging.info('Hello World %s', utc_timestamp)


def GetTwitterSearchResults():
    twitterSearchApiUrlTemplate = os.environ["TwitterSearchApiUrl"]
    bearerToken = os.environ["BearerToken"]

    headers = {"Content-Type": "application/json",
               "Authorization": bearerToken}

    start_time = datetime.datetime.utcnow() - datetime.timedelta(hours=0, minutes=1)

    url = twitterSearchApiUrlTemplate.replace('STARTTIME', start_time.strftime('%Y-%m-%dT%H:%M:%SZ'))

    response = requests.get(url=url, headers=headers)
    return response


def SendRepliesToUser(payload):
    repliesApiUrl = os.environ["RepliesApiUrl"]
    headers = {"Content-Type": "application/json"}

    y = json.dumps(payload)

    response = requests.post(url=repliesApiUrl, headers=headers, data=y)
    return response
