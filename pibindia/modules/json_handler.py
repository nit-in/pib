import json
from pathlib import Path


def article_jdata(
    prid, article_date, article_title, article_ministry, article_url, article_data
):
    article_json = {
        "id": prid,
        "date": article_date,
        "title": article_title,
        "ministry": article_ministry,
        "url": article_url,
        "article": article_data,
    }
    return article_json


def is_valid_json(text):
    try:
        json.loads(text)
        return True
    except json.JSONDecodeError as e:
        return False, str(e)


def save_json(jpath, article_data):
    with open(jpath, "a", encoding="utf-8") as j:
        json.dump(article_data, j, ensure_ascii=False, indent=4)
