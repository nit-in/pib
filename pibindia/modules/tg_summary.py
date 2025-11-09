import os
from llama_cpp import Llama
import re

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

llm = Llama(
    model_path="models/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
    n_ctx=2048,
    n_threads=2,
    n_batch=128,
    use_mlock=True,
    verbose=False,
)


def escape_md(text):
    return re.sub(r"([_*\[\]()~`>#+\-=|{}.!])", r"\\\1", text)


def summarize_text(text):
    prompt = f"""
Summarize ONLY the provided PIB press release text.

🎯 Guidelines:
- Write for UPSC and other competitive exams.
- Keep it very precise and very concise, factual, and to the point.
- Ignore all external links, references, or other PIB releases.
- DO NOT include unrelated or speculative information.
- Focus strictly on the provided text content.

🧾 Format for Telegram:
• Use bullet points (•)
• Include relevant emojis in every post for readability (📅🏛️📊👥💡📈)
• Highlight key facts, dates, numbers, names, schemes, and ministries.
• Avoid repetition or unnecessary words.
• Maintain neutral, official tone.

Output must be short very precise and very concise , clear, and ready to post.

Text:
{text}
"""
    result = llm(prompt, max_tokens=350, temperature=0.3, top_p=0.95)
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
