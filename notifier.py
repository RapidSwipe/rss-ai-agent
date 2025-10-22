import smtplib
import config
from email.message import EmailMessage

def send_email_notification(summaries_list: list[tuple]):
    if not all([config.EMAIL_HOST, config.EMAIL_PORT, config.EMAIL_USER, config.EMAIL_PASS, config.EMAIL_RECEIVER]):
        print("Brak pełnej konfiguracji e-mail w .env. Pomijam wysyłanie.")
        return

    subject = f"🤖 Twój AI News Digest - {len(summaries_list)} nowych artykułów"
    body = "Oto Twoje automatyczne podsumowanie najnowszych artykułów:\n\n"
    body += "=" * 30 + "\n\n"

    for title, link, summary in summaries_list:
        body += f"## {title}\n"
        body += f"Link: {link}\n\n"
        body += f"Podsumowanie:\n{summary}\n\n"
        body += "-" * 30 + "\n\n"

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = config.EMAIL_USER
    msg['To'] = config.EMAIL_RECEIVER

    try:
        print(f"Wysyłanie e-maila do {config.EMAIL_RECEIVER}...")
        with smtplib.SMTP(config.EMAIL_HOST, config.EMAIL_PORT) as server:
            server.starttls()
            server.login(config.EMAIL_USER, config.EMAIL_PASS)
            server.send_message(msg)
        print("E-mail został pomyślnie wysłany!")
    except Exception as e:
        print(f"Nie udało się wysłać e-maila: {e}")