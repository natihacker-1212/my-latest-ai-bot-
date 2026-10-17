import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("👋 ሰላም! እኔ የ AI ረዳትህ ነኝ። የ OpenAI's latest ቴክኖሎጂን በመጠቀም 24/7 በፕሪሚየም መንገድ ለመመለስ ዝግጁ ነኝ። ምን ልርዳህ?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text
    await update.message.reply_chat_action(action="typing")
    try:
        api_url = f"https://onrender.com{user_text}" 
        response = requests.get(api_url, timeout=30)
        if response.status_code == 200:
            ai_response = response.json().get("reply", "ይቅርታ፣ አሁን ላይ ምላሽ መስጠት አልቻልኩም።")
        else:
            ai_response = "❌ አገልጋዩ ላይ ትንሽ ቢዚ ነው፣ እባክህ ድጋሚ ሞክር።"
    except Exception as e:
        ai_response = "⚠️ ይቅርታ፣ ጥያቄህን ሳስተናግድ ስህተት አጋጥሞኛል።"
    await update.message.reply_text(ai_response)

def main() -> None:
    if not TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN missing!")
        return
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 ቦቱ ስራ ጀምሯል...")
    application.run_polling()

if __name__ == '__main__':
    main()
