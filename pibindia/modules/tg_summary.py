import os
import requests

from llama_cpp import Llama
from scrapy.selector import Selector
import re

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

llm = Llama(
    model_path="models/mistral-7b-instruct-v0.2.Q4_K_M.gguf", n_ctx=4096, n_threads=4
)


def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        sel = Selector(text=response.text)
        content = sel.xpath(
            "//div[contains(@class,'innner-page-main-about-us-content-right-part')]//text()[normalize-space()] | //div[@id='PRBody']//text()[normalize-space()]"
        ).getall()
        cleaned_text = " ".join([t.strip() for t in content if t.strip()])
        print(cleaned_text)
        return cleaned_text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None


def escape_md(text):
    return re.sub(r"([_*\[\]()~`>#+\-=|{}.!])", r"\\\1", text)


def summarize_text(text):
    prompt = f"""Summarize the following PIB press releases for UPSC and other competitive exams.
Keep it concise, factual, and formatted for Telegram (bullet points, emojis if needed).
Focus on names, numbers, dates, ministries, initiatives, and key takeaways.
Use Telegram Markdown for better presentation — use bullets, headings, subheadings.

Text:
{text}
"""
    result = llm(prompt, max_tokens=512, temperature=0.4, top_p=0.9)
    return result["choices"][0]["text"].strip()


def post_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    safe_message = escape_md(message)
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": safe_message,
        "parse_mode": "MarkdownV2",
        "disable_web_page_preview": True,
    }
    for attempt in range(3):
        res = requests.post(url, data=payload)
        if res.status_code == 200:
            print("Summary sent successfully!")
            return True
        else:
            print(f"Telegram Error (Attempt {attempt+1}): {res.text}")
    return False
