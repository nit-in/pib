import time
import requests
from scrapy.selector import Selector


def get_text(url, retries=5, backoff_factor=1, timeout=10):
    attempt = 0
    while attempt < retries:
        try:
            print(f"Fetching URL: {url} (Attempt {attempt + 1}/{retries})")
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            sel = Selector(text=response.text)
            content = sel.xpath(
                "//div[contains(@class,'innner-page-main-about-us-content-right-part')]//text()[normalize-space()] | //div[@id='PRBody']//text()[normalize-space()]"
            ).getall()
            cleaned_text = " ".join([t.strip() for t in content if t.strip()])
            return cleaned_text

        except requests.exceptions.RequestException as e:
            attempt += 1
            print(f"Request failed for {url}: {e}")
            if attempt < retries:
                sleep_time = backoff_factor * (2 ** (attempt - 1))
                print(f"Retrying in {sleep_time:.1f}s...")
                time.sleep(sleep_time)
            else:
                print(f"Failed after {retries} attempts: {url}")
                return None
