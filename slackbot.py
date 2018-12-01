"""A slack bot"""
import os
import time
from slackclient import SlackClient
from ducksearch import beer
from pick import Pick

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
BOT_OAUTH_TOKEN = os.environ["BOT_OAUTH_TOKEN"]
BOT_TAG = "<@" + os.environ["BOT_USER_ID"] + ">"


def _parse_text(text):
    if not text:
        return {"text": ""}
    if text.startswith(BOT_TAG):
        return {"self_mention": True, "text": text[len(BOT_TAG):].strip()}
    return {"text": text.strip()}


def _validate_result(result):
    if "ok" in result and result["ok"] is True:
        return
    raise ValueError(result)


class Bot:
    """class Bot handles chat interaction (@python)"""

    def __init__(self):
        self.bot_client = SlackClient(SLACK_BOT_TOKEN)
        self.oauth_client = SlackClient(BOT_OAUTH_TOKEN)
        self.id_seed = 1
        self.pick_reaction = None

    def __id(self):
        return self.id_seed

    def __parse_events(self, events):
        if not events:
            return
        for event in events:
            print(">>>", event)
            if "hidden" in event:
                continue
            if "subtype" in event:
                continue
            if ("type" in event
                    and event["type"] == "message"
                    and "text" in event
                    and "channel" in event):
                self.__text_message(event)
            print("")

    def __text_message(self, event):
        if event["channel"].startswith("D"):
            text = event["text"]
        else:
            parsed_text = _parse_text(event["text"])
            if not "self_mention" in parsed_text:
                return
            text = parsed_text["text"]
        beer_url = beer(text)
        if beer_url:
            message = beer_url
        else:
            message = self.pick_reaction.one()
        self.rtm_send(event["channel"], message)

    def __rtm_listen(self):
        """Listen to direct messages and mentions using rtm"""

        if self.bot_client.rtm_connect():
            while self.bot_client.server.connected is True:
                self.__parse_events(self.bot_client.rtm_read())
                time.sleep(1)
        else:
            print("Connection Failed")

    def start(self):
        """start chatbot"""
        self.pick_reaction = Pick(self.list_custom_emojis(), max_repeat=7)
        self.__rtm_listen()

    def rtm_send(self, channel, message, thread=None, reply_broadcast=None):
        """Send message using rtm"""
        print(" ->", "channel=", channel, "message=", message, "thread=",
              thread, "reply_broadcast=", reply_broadcast)
        self.bot_client.rtm_send_message(
            channel, message, thread, reply_broadcast)

    def introduce(self, channel):
        """Introduce self and set icon_emoji"""
        self.bot_client.api_call("chat.postMessage",
                                 channel=channel,
                                 username="python",
                                 text="I python, therefor I am")

    def list_custom_emojis(self):
        """Return a list of custom emojis in the workspace"""
        result = self.oauth_client.api_call("emoji.list")
        _validate_result(result)
        return list(
            map(lambda k: ":" + k + ":",
                result["emoji"].keys()))
