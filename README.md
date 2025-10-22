# 🤖 RSS AI Agent - News Summarizer Agent

Agent AI napisany w Pythonie, który automatyzuje proces czytania newsów. Agent monitoruje wybrane kanały RSS, pobiera treść nowych artykułów, wysyła je do modelu LLM (np. GPT-3.5-turbo) w celu wygenerowania zwięzłego podsumowania, a następnie wysyła gotowy "digest" (zbiór podsumowań) na Twój adres e-mail.

## 💡 Kluczowe Funkcjonalności

* **Automatyczne monitorowanie RSS:** Śledzi wiele kanałów RSS jednocześnie (lista w `config.py`).
* **Inteligentne podsumowania:** Wykorzystuje API OpenAI do generowania 3-5 zdaniowych podsumowań dla każdego artykułu.
* **Pobieranie pełnej treści:** Próbuje pobrać pełną treść artykułu (scraping), a nie tylko krótki opis z RSS, dla lepszego kontekstu podsumowania.
* **Unikanie duplikatów:** Zapisuje przetworzone linki w `processed_links.txt`, aby nie wysyłać tych samych newsów ponownie.
* **Automatyzacja (Scheduling):** Uruchamia się automatycznie co X godzin (wartość domyślna w `config.py`).
* **Powiadomienia:** Wysyła zbiorczy e-mail (przez SMTP) ze wszystkimi nowymi podsumowaniami.

## 🛠️ Stack Technologiczny

* **Python 3.x**
* **OpenAI API** (do podsumowań)
* **feedparser** (do czytania RSS)
* **schedule** (do automatyzacji zadań)
* **smtplib** (do wysyłania e-maili przez SMTP)
* **requests** + **BeautifulSoup4** (do pobierania pełnej treści artykułów)
* **python-dotenv** (do zarządzania sekretami)

## ⚙️ Instalacja i Konfiguracja

### Krok 1: Pobierz pliki i przejdź do folderu

Umieść wszystkie pliki projektu (np. `agent.py`, `config.py` itd.) w jednym folderze `rss-ai-agent/`.

### Krok 2: Stwórz i aktywuj środowisko wirtualne

Zalecane jest użycie wirtualnego środowiska, aby odizolować zależności.

```bash
# Stwórz środowisko
python -m venv venv

# Aktywuj środowisko (Windows)
.\venv\Scripts\Activate.ps1

# Aktywuj środowisko (macOS/Linux)
source venv/bin/activate
```

### Krok 3: Zainstaluj zależności

Z aktywnym środowiskiem wirtualnym `(venv)`, zainstaluj wszystkie wymagane biblioteki.

```bash
pip install -r requirements.txt
```

### Krok 4: Skonfiguruj plik .env

Utwórz plik o nazwie `.env` w głównym katalogu projektu. Służy on do bezpiecznego przechowywania Twoich kluczy API i danych logowania.

Skopiuj poniższą strukturę do swojego pliku `.env` i uzupełnij ją:

```ini
# Klucz API OpenAI
OPENAI_API_KEY="sk-..."

# Konfiguracja SMTP (na przykładzie Gmaila)
EMAIL_HOST="smtp.gmail.com"
EMAIL_PORT=587
EMAIL_USER="twoj.email@gmail.com"
EMAIL_PASS="twoje_haslo_do_aplikacji_google_16_znakow"

# Email, na który mają przychodzić podsumowania
EMAIL_RECEIVER="email_odbiorcy@example.com"
```

**Ważne:** W przypadku Gmaila, `EMAIL_PASS` to **Hasło do aplikacji** (App Password), które musisz wygenerować w ustawieniach swojego konta Google. Wymaga to włączonej Weryfikacji Dwuetapowej.

## ▶️ Uruchomienie Agenta

Po zakończeniu konfiguracji, możesz uruchomić agenta.

1. Upewnij się, że Twoje środowisko wirtualne `(venv)` jest aktywne.

2. Uruchom główny skrypt:

```bash
python agent.py
```

Agent uruchomi się raz przy starcie, przetworzy wszystkie nowe artykuły i wyśle e-mail. Następnie będzie działał w tle, powtarzając proces co 6 godzin (lub zgodnie z ustawieniem `SCHEDULE_HOURS` w `config.py`).

Aby zatrzymać agenta, naciśnij `Ctrl + C` w terminalu.

## 📂 Struktura Projektu

```
rss-ai-agent/
├── .env                 #  Przechowuje klucze API
├── .gitignore           # Ignoruje pliki wrażliwe (venv, .env, etc.)
├── README.md            # Dokumentacja
├── requirements.txt     # Zależności Pythona
├── config.py            # Konfiguracja (lista RSS, prompt, wczytywanie .env)
├── agent.py             # Główna logika, pętla i harmonogram (scheduler)
├── summarizer.py        # Moduł integracji z API OpenAI
├── notifier.py          # Moduł do wysyłania powiadomień e-mail
└── processed_links.txt  # (Generowany) Baza danych przetworzonych linków
```

## 🎯 Możliwe Usprawnienia

* **Dodatkowe źródła RSS:** Rozszerz listę `RSS_FEEDS` w `config.py` o więcej kanałów.
* **Lepsza ekstrakcja treści:** Zaimplementuj dedykowane parsery dla popularnych stron (np. używając `newspaper3k`).
* **Baza danych:** Zamień `processed_links.txt` na SQLite lub PostgreSQL dla lepszej skalowalności.
* **Dashboard:** Stwórz prosty web interface (Flask/FastAPI) do zarządzania feedami i przeglądania podsumowań.
* **Inne modele LLM:** Eksperymentuj z innymi modelami (GPT-4, Claude, lokalne modele przez Ollama).
* **Kategoryzacja:** Dodaj automatyczną kategoryzację artykułów (tech, biznes, AI, etc.).

## 📝 Licencja

Ten projekt jest otwarty i dostępny na zasadach MIT License.

## 👨‍💻 Autor

**Szymon Cieślik**
AI Engineer | Automation Developer
[LinkedIn](https://linkedin.com/in/szymon-cieslik-873003203) | [GitHub](https://github.com/RapidSwipe)

---
