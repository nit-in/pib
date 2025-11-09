import requests
from scrapy.selector import Selector


def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        sel = Selector(text=response.text)
        content = sel.xpath(
            "//div[contains(@class,'innner-page-main-about-us-content-right-part')]//text()[normalize-space()] | //div[@id='PRBody']//text()[normalize-space()]"
        ).getall()
        cleaned_text = " ".join([t.strip() for t in content if t.strip()])
        return cleaned_text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
