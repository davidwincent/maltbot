"""A slack bot"""
import os
import time
from slackclient import SlackClient
from ducksearch import beer

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
# API_APP_ID = os.environ["API_APP_ID"]
BOT_TAG = "<@" + os.environ["USER_ID"] + ">"
SLACK_CLIENT = SlackClient(SLACK_BOT_TOKEN)
ID = 1


def _id():
    return ID


def _parse_events(events):
    if not events:
        return
    for event in events:
        print(">>>", event)
        if ("type" in event
                and event["type"] == "message"
                and not "hidden" in event
                and not "subtype" in event
                and "text" in event
                and "channel" in event):
            _text_message(event)
        print("")


def _parse_text(text):
    if not text:
        return {"text": ""}
    if text.startswith(BOT_TAG):
        return {"self_mention": True, "text": text[len(BOT_TAG):].strip()}
    return {"text": text.strip()}


def _text_message(event):
    if event["channel"].startswith("D"):
        text = event["text"]
    else:
        parsed_text = _parse_text(event["text"])
        if not "self_mention" in parsed_text:
            return
        text = parsed_text["text"]
    beer_url = beer(text)
    if beer_url:
        response = beer_url
    else:
        response = ":nohomo:"
    rtm_send(event["channel"], response)


def rtm_listen():
    """Listen to direct messages and mentions using rtm"""

    if SLACK_CLIENT.rtm_connect():
        while SLACK_CLIENT.server.connected is True:
            _parse_events(SLACK_CLIENT.rtm_read())
            time.sleep(1)
    else:
        print("Connection Failed")


def rtm_send(channel, message, thread=None, reply_broadcast=None):
    """Send message using rtm"""
    SLACK_CLIENT.rtm_send_message(channel, message, thread, reply_broadcast)
