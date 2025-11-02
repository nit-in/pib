import os
import requests
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

client = OpenAI(api_key=OPENAI_API_KEY)


def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def summarize_text(text):
    prompt = f"""Summarize and strip html the following PIB press releases/html for UPSC and other competitive exams.
Keep it concise, factual, and formatted for Telegram (bullet points, emojis if needed).
Focus on names, numbers, dates, ministries, initiatives, and key takeaways.

Text:
{text}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()


def post_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }
    res = requests.post(url, data=payload)
    if res.status_code != 200:
        print("Telegram Error:", res.text)
    else:
        print("Summary sent successfully!")
