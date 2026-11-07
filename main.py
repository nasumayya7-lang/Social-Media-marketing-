import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

PHONES = {
    "iphone13": {"name": "iPhone 13 - 128GB", "price": "₦450,000"},
    "samsung_a55": {"name": "Samsung A55 - 256GB", "price": "₦380,000"},
    "tecno_spark": {"name": "Tecno Spark 20", "price": "₦185,000"},
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📱 Duba Wayoyi", callback_data="phones")],
        [InlineKeyboardButton("🎁 Daily Bonus", callback_data="bonus")],
        [InlineKeyboardButton("👥 Referral", callback_data="referral")],
    ]
    await update.message.reply_text(
        "Sannu! Barka da zuwa Phone Store 🛒\n\nZabi abin da kake so:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "phones":
        keyboard = []
        for key, p in PHONES.items():
            keyboard.append([InlineKeyboardButton(f"{p['name']} - {p['price']}", callback_data=f"buy_{key}")])
        keyboard.append([InlineKeyboardButton("⬅️ Komawa", callback_data="back")])
        await query.edit_message_text("Zabi waya:", reply_markup=InlineKeyboardMarkup(keyboard))
    
    elif query.data.startswith("buy_"):
        key = query.data.replace("buy_", "")
        p = PHONES[key]
        user = query.from_user
        if ADMIN_ID != 0:
            await context.bot.send_message(ADMIN_ID, f"🔔 SABON ORDER!\n\nWayar: {p['name']}\nFarashi: {p['price']}\nKwastoma: @{user.username}\nID: {user.id}\nSuna: {user.first_name}")
        await query.edit_message_text(f"Na gode! Ka zabi:\n\n{p['name']}\n{p['price']}\n\nMun aika order dinka ga mai shago. Zai tuntube ka yanzu. ✅")
    
    elif query.data == "bonus":
        await query.edit_message_text("🎁 Ka samu Daily Bonus na ₦500! Ka dawo gobe ka sake samu.")
    elif query.data == "referral":
        link = f"https://t.me/{context.bot.username}?start={query.from_user.id}"
        await query.edit_message_text(f"👥 Link dinka na Referral:\n\n{link}\n\nIdan kowa ya shigo ta link dinka, za ka samu bonus.")
    elif query.data == "back":
        await start(update, context)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    print("Bot yana aiki...")
    app.run_polling()

if __name__ == "__main__":
    main()
