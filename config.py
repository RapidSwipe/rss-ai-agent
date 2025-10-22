import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

RSS_FEEDS = [
    "https://techcrunch.com/feed/",
    "https://www.artificialintelligence-news.com/feed/",
    "https://openai.com/blog/rss/",
    "https://www.deeplearning.ai/feed/"
]

SUMMARY_PROMPT = """
Jesteś ekspertem w analizie i syntezie informacji. Twoim zadaniem jest podsumowanie poniższego artykułu.
Skup się wyłącznie na kluczowych informacjach, najważniejszych wnioskach i faktach.
Stwórz zwięzłe podsumowanie w 3-5 zdaniach.

Oto artykuł:
---
Tytuł: {title}
Treść: {content}
---
Podsumowanie (3-5 zdań):
"""

PROCESSED_LINKS_FILE = "processed_links.txt"
SCHEDULE_HOURS = 6