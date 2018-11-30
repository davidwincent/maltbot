import os
import asyncore
from pyinotify import *


# Instanciate a new WatchManager (will be used to store watches).
WM = WatchManager()


class Handler(ProcessEvent):
    def process_IN_CREATE(self, event):
        return

    def process_IN_DELETE(self, event):
        return

    def process_IN_CLOSE_WRITE(self, event):
        if not event.name.endswith(".py"):
            return
        runtests()


def watch():
    mask = IN_CLOSE_WRITE
    notifier = AsyncNotifier(WM, Handler())
    watch = WM.add_watch('./', mask, rec=True)
    # Loop forever and handle events.
    asyncore.loop()


def runtests():
    os.system("clear")
    os.system("pytest")


runtests()
watch()
