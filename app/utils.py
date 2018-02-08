import re
from datetime import datetime

import bleach

from app.core import *


def prepare_text(text: str, preview: bool=False):
    if preview:
        if len(text) > 200:
            text = text[:197].strip() + ".."
    text = text.replace("\n", "<br>")
    text = re.sub('(?:https?)?://[^\s<]+', lambda f: '<a href="{0}" target="_blank">{0}</a>'.format(f.group(0)), text)
    return text


def priority_as_str(value: int):
    if value == Priority.HIGH.value:
        return "High"
    elif value == Priority.NORMAL.value:
        return "Normal"
    elif value == Priority.LOW.value:
        return "Low"
    else:
        raise Exception("Unknown priority {}".format(value))


def status_as_str(value: int):
    if value == Status.TODO.value:
        return "To do"
    elif value == Status.DOING.value:
        return "Doing"
    elif value == Status.DONE.value:
        return "Done"
    else:
        raise Exception("Unknown status {}".format(value))


def extract_tags(tags_str: str):
    used = []
    for tag_name in tags_str.split(','):
        tag_name = re.sub("\s+", "-", strip_html_tags(tag_name))
        if tag_name:
            if tag_name in used:
                continue
            used.append(tag_name)
            tag = get_tag_by_name(tag_name)
            if not tag:
                tag = Tag.create(name=tag_name)
            yield tag


def utc_timestamp():
    return int(datetime.utcnow().timestamp())


def strip_html_tags(text: str):
    return bleach.clean(text, strip=True, strip_comments=True).strip()