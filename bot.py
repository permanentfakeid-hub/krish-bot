import requests
import nest_asyncio
nest_asyncio.apply()

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import asyncio
import json
import re

API_KEY_TELEGRAM = "8457532570:AAHwDARusJC1TMQMMp_p3-KP7Xzo5wpMCn4"
API_URL = "https://numberimfo.vishalboss.sbs/api.php"

# Extract digits from any format and return last 10
def extract_numbers(text):
    nums = re.findall(r'\d+', text)
    clean = [n[-10:] for n in nums if len(n) >= 10]
    return list(set(clean))

# ---- ONLY THIS WILL SHOW ON /start ----
async def start(update, context):
    await update.message.reply_text("Send mobile number to search")

async def search_number(number):
    params = {"number": number, "key": "vishalboss_key_8b1dfd03d0693585963e9ad958d4de17e8f62400"}
    data = requests.get(API_URL, params=params).json()
    
    # Remove unwanted keys
    for k in ["developer", "owner", "powered_by", "status"]:
        data.pop(k, None)
    return data

async def get_details(update, context):
    numbers = extract_numbers(update.message.text)

    if not numbers:
        return await update.message.reply_text("Invalid number")

    for num in numbers:
        data = await search_number(num)
        pretty = json.dumps(data, indent=2, ensure_ascii=False)
        await update.message.reply_text(f"```json\n{pretty}\n```", parse_mode="Markdown")

async def main():
    app = ApplicationBuilder().token(API_KEY_TELEGRAM).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_details))

    print("Bot Running...")
    await app.run_polling()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())