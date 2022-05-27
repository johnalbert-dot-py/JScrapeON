import os.path

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__)) + "/../"
DEBUG = False


def GET_KEY_VALUE(key, dict):
    if key in dict:
        return dict[key]
    else:
        return ""
