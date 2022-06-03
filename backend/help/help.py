import os


def start_debug():
    os.environ["FLASK_DEBUG"] = "1"


def stop_debug():
    os.environ["FLASK_DEBUG"] = "0"


def empty_checker(*args):
    for x in args:
        if not x or not len(x):
            raise ValueError
