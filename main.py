"""Maltbot (@python) is a bot"""
from slackbot import Bot

VERSION = "alpha"
BOT = Bot()

print("Starting ("+VERSION+")")
BOT.start()
