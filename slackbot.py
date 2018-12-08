"""A slack bot"""
# pylint: disable=broad-except
import os
import time
from traceback import format_exc
from slackclient import SlackClient
from ducksearch import beer
from pick import Pick
from browser import HttpError

RECONNECT_TRIES = 10
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
            try:
                print(">>>", event)
                if "hidden" in event:
                    continue
                if "subtype" in event:
                    continue
                if "channel" in event:
                    channel = event["channel"]
                if ("type" in event
                        and event["type"] == "message"
                        and "text" in event):
                    self.__text_message(event)
                print("")
            except Exception as error:
                self.__handle_error(error, channel)

    def __text_message(self, event):
        if event["channel"].startswith("D"):
            text = event["text"]
        else:
            parsed_text = _parse_text(event["text"])
            if not "self_mention" in parsed_text:
                return
            text = parsed_text["text"]
        try:
            beer_url = beer(text)
            if beer_url:
                message = beer_url
        except HttpError as http_error:
            self.__handle_error(http_error, channel="CEG4LEXJN")
            message = "För mycket :beersdeluxe:"
        if not message:
            message = ":%(reaction)s:" % {
                "reaction": self.pick_reaction.one()}
        self.rtm_send(event["channel"], message)

    def __rtm_listen(self):
        """Listen to direct messages and mentions using rtm"""

        reconnect_count = 0
        while reconnect_count < RECONNECT_TRIES:
            if self.bot_client.rtm_connect():
                while self.bot_client.server.connected is True:
                    try:
                        events = self.bot_client.rtm_read()
                    except TimeoutError as timeout_error:
                        self.__handle_error(timeout_error)
                        reconnect_count = 0
                    self.__parse_events(events)
                    time.sleep(1)
            else:
                raise Exception("Connection Failed")
            time.sleep(10)
            reconnect_count += 1

    def __handle_error(self, error, channel=None):
        exc = format_exc()
        print(" [[EXCEPTION]]", error)
        print(exc)
        print("")
        if not channel:
            return
        try:
            stack_trace = {
                "text": "```%(error)s: %(exc)s```" % {
                    "error": error,
                    "exc": exc}}
            self.bot_client.api_call("chat.postMessage",
                                     channel=channel,
                                     text=":scream:",
                                     attachments=[stack_trace])
        except Exception as io_error:
            print(" [[IO_EXCEPTION]]", error)
            print(io_error)
            print("")

    def start(self):
        """start chatbot"""
        try:
            # beer("debug")
            self.pick_reaction = Pick(self.list_custom_emojis(), max_repeat=7)
            self.__rtm_listen()
        except Exception as error:
            self.__handle_error(error, channel="CEG4LEXJN")

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
        return list(result["emoji"].keys())
