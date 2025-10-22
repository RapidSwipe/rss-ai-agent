import config
from openai import OpenAI

try:
    client = OpenAI(api_key=config.OPENAI_API_KEY)
except Exception as e:
    print(f"Błąd inicjalizacji klienta OpenAI: {e}")
    client = None

def get_summary(title: str, content: str) -> str | None:
    if not client:
        print("Klient OpenAI nie jest skonfigurowany.")
        return None

    max_length = 8000
    if len(content) > max_length:
        content = content[:max_length] + "... (treść skrócona)"

    try:
        prompt = config.SUMMARY_PROMPT.format(title=title, content=content)

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=250
        )

        summary = completion.choices[0].message.content
        return summary.strip()

    except Exception as e:
        print(f"Błąd podczas generowania podsumowania dla '{title}': {e}")
        return None