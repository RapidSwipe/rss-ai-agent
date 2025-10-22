import feedparser
import schedule
import time
import requests
import os
from bs4 import BeautifulSoup

import config
import summarizer
import notifier

def load_processed_links() -> set:
    if not os.path.exists(config.PROCESSED_LINKS_FILE):
        return set()
    try:
        with open(config.PROCESSED_LINKS_FILE, 'r') as f:
            return set(line.strip() for line in f)
    except Exception as e:
        print(f"Błąd odczytu pliku processed_links.txt: {e}")
        return set()

def save_processed_link(link: str, processed_set: set):
    try:
        with open(config.PROCESSED_LINKS_FILE, 'a') as f:
            f.write(f"{link}\n")
        processed_set.add(link)
    except Exception as e:
        print(f"Błąd zapisu linku {link}: {e}")

def fetch_article_content(url: str) -> str | None:
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        main_content = soup.find('article') or soup.find('main')

        if main_content:
            paragraphs = main_content.find_all('p')
        else:
            paragraphs = soup.body.find_all('p')

        content = "\n".join([p.get_text() for p in paragraphs])

        if not content:
             print("Nie znaleziono treści <p>, używam opisu z RSS.")
             return None

        return content

    except requests.RequestException as e:
        print(f"Błąd podczas pobierania {url}: {e}")
        return None
    except Exception as e:
        print(f"Błąd parsowania {url}: {e}")
        return None

def run_agent():
    print(f"\n[{time.ctime()}] Uruchamiam agenta, sprawdzam nowe artykuły...")
    processed_links = load_processed_links()
    new_summaries = []

    for feed_url in config.RSS_FEEDS:
        print(f"--- Przetwarzam kanał: {feed_url}")
        try:
            feed = feedparser.parse(feed_url)

            for entry in feed.entries:
                link = entry.link
                title = entry.title

                if link in processed_links:
                    continue

                print(f"  Znaleziono nowy artykuł: {title}")

                content = fetch_article_content(link)

                if not content:
                    content = entry.get('summary') or entry.get('description', '')
                    if not content:
                         print(f"  Brak treści lub opisu dla {link}. Pomijam.")
                         save_processed_link(link, processed_links)
                         continue
                    else:
                        content = BeautifulSoup(content, 'html.parser').get_text()

                summary = summarizer.get_summary(title, content)

                if summary:
                    new_summaries.append((title, link, summary))
                    save_processed_link(link, processed_links)
                else:
                    print(f"  Nie udało się wygenerować podsumowania dla {title}.")

                time.sleep(1)

        except Exception as e:
            print(f"Błąd przetwarzania kanału {feed_url}: {e}")

    if new_summaries:
        print(f"Zakończono skanowanie. Znaleziono {len(new_summaries)} nowych podsumowań.")
        notifier.send_email_notification(new_summaries)
    else:
        print("Zakończono skanowanie. Brak nowych artykułów.")


if __name__ == "__main__":
    print("🤖 News Summarizer Agent został uruchomiony.")
    print(f"Zadanie będzie uruchamiane co {config.SCHEDULE_HOURS} godzin.")

    run_agent()
    schedule.every(config.SCHEDULE_HOURS).hours.do(run_agent)

    while True:
        schedule.run_pending()
        time.sleep(60)