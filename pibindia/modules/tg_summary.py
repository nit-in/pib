import os
import time
import requests
from scrapy.selector import Selector
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
    return re.sub(r"([_*\[\]()~`>#+\\-=|{}.!])", r"\\\1", text)

def count_tokens(text):
    return len(llm.tokenize(text.encode("utf-8")))

def clean_text(text):
    return re.sub(r"(Click here.*|For more information.*)", "", text, flags=re.I)

def split_text_by_tokens(text, max_tokens=1500):
    tokens = llm.tokenize(text.encode("utf-8"))
    chunks = []
    start = 0
    while start < len(tokens):
        end = start + max_tokens
        chunk = llm.detokenize(tokens[start:end]).decode("utf-8", errors="ignore")
        chunks.append(chunk)
        start = end
    return chunks

def safe_llm_call(prompt, max_tokens, retries=3):
    for attempt in range(retries):
        try:
            return llm(prompt, max_tokens=max_tokens, temperature=0.3, top_p=0.95)
        except Exception as e:
            print(f"LLM error (attempt {attempt+1}): {e}")
            time.sleep(2)
    return {"choices": [{"text": ""}]}

def summarize_text(text, max_chunk_tokens=None):
    text = clean_text(text)
    token_count = count_tokens(text)
    print(f"Total token count: {token_count}")

    # Auto-adjust chunk size based on model context
    if max_chunk_tokens is None:
        max_chunk_tokens = int(llm.n_ctx * 0.75)

    if token_count > max_chunk_tokens:
        chunks = split_text_by_tokens(text, max_chunk_tokens)
    else:
        chunks = [text]

    summaries = []
    for i, chunk in enumerate(chunks, 1):
        chunk_tokens = count_tokens(chunk)
        max_summary_tokens = min(int(chunk_tokens * 0.25), 512)
        print(f"Processing chunk {i}/{len(chunks)} ({chunk_tokens} tokens) → summary cap: {max_summary_tokens}")

        prompt = f"""
Summarize ONLY the provided PIB press release text.

🎯 Guidelines:
- Write for UPSC and other competitive exams.
- Keep it very precise and concise, factual, and to the point.
- Ignore all external links, references, or other PIB releases.
- DO NOT include unrelated or speculative information.
- Focus strictly on the provided text content.

🧾 Format for Telegram:
• Use bullet points (•)
• Include relevant emojis in every post for readability (📅🏛️📊👥💡📈)
• Highlight key facts, dates, numbers, names, schemes, and ministries.
• Avoid repetition or unnecessary words.
• Maintain neutral, official tone.

Output must be short, very precise, and ready to post.

Text:
{chunk}
"""
        result = safe_llm_call(prompt, max_summary_tokens)
        summaries.append(result["choices"][0]["text"].strip())

        time.sleep(1)

    final_summary = " ".join(summaries)
    print(f"Final summary length: {count_tokens(final_summary)} tokens")
    return final_summary

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
