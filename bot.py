import feedparser
import asyncio
from telegram import Bot

# --- Configuración ---
TELEGRAM_TOKEN = "8364853526:AAHEgoy8KDvkY49uP6XbGZdVLTq3KF6jBCk"
CHAT_ID = 1849086200  # tu chat ID

FEEDS = [
    "https://www.eurohoops.net/feed/",
    "https://basketnews.com/rss/"
]

KEYWORDS = [
    "polémica", "arbitral", "árbitro", "árbitros", "colegiado", "jueces",
    "revisión", "instant replay", "error", "errores", "fallo", "fallos",
    "decisión", "decisiones", "dudosa", "falta", "técnica", "antideportiva",
    "descalificante", "pasos", "violación", "posesión", "tiempo muerto",
    "fuera", "tapón", "goaltending",
    "referee", "referees", "ref", "officiating", "official review", "tough call",
    "controversy", "controversial", "mistake", "mistakes", "wrong call",
    "missed call", "referee complaint", "protest", "objection", "disputed play",
    "challenge", "video review"
]

bot = Bot(token=TELEGRAM_TOKEN)
sent_items = set()
 
# Artículo de prueba
test_entry = {
    "title": "Prueba de polémica arbitral",
    "summary": "Esto es solo un test para comprobar el bot",
    "link": "https://test.com/fake-article"
}

if test_entry["link"] not in sent_links:
    bot.send_message(chat_id=CHAT_ID, text=f"🔥 Jugada polémica encontrada:\n{test_entry['title']}\n{test_entry['link']}")
    sent_links.add(test_entry["link"])

async def check_feeds():
    for feed_url in FEEDS:
        feed = feedparser.parse(feed_url)
        print(f"Revisando feed: {feed_url}, artículos encontrados: {len(feed.entries)}")
        for entry in feed.entries:
            url = entry.link
            title = entry.title
            summary = entry.get("summary", "")
            combined_text = (title + " " + summary).lower()

            if any(keyword.lower() in combined_text for keyword in KEYWORDS):
                if url not in sent_items:
                    message = f"⚠ Nueva jugada polémica:\n{title}\n{url}"
                    await bot.send_message(chat_id=CHAT_ID, text=message)
                    sent_items.add(url)

async def main():
    await bot.send_message(chat_id=CHAT_ID, text="✅ Bot iniciado y funcionando")
    while True:
        try:
            await check_feeds()
            await asyncio.sleep(300)  # revisa cada 5 minutos
        except Exception as e:
            print("Error:", e)
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())

