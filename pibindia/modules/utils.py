import html
from unicodedata import normalize
import re


def remove_html_entities(txt):
    str_html = html.unescape(str(txt))
    str_normalized = normalize("NFKD", str_html)
    return str(str_normalized)


def sanitize_name(name):
    etxt = name.replace(" ", "_").replace("\n", "_").replace("’", "")
    stxt = re.sub("[`~!@#$%^&*();:',.+=\"<>|\\/?\n\t\r ]", "", etxt)
    return stxt
