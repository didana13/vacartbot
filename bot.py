import os
from threading import Thread
from flask import Flask

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("TOKEN")

CHANNEL_USERNAME = "vacart_com"  # بدون @

web = Flask(__name__)

@web.route("/")
def home():
    return "Bot is running"

def run_web():
    web.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))


# ---------------- CHECK SUBSCRIPTION ----------------
async def is_joined(update, context):
    try:
        user_id = update.effective_user.id
        member = await context.bot.get_chat_member(chat_id=f"@{CHANNEL_USERNAME}", user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


# ---------------- MAIN MENU ----------------
def main_menu(lang="fa"):
    if lang == "fa":
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("📡 Router", callback_data="router")],
            [InlineKeyboardButton("📶 Modem Router", callback_data="modem")],
            [InlineKeyboardButton("🌐 English", callback_data="lang_en")]
        ])
    else:
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("📡 Router", callback_data="router")],
            [InlineKeyboardButton("📶 Modem Router", callback_data="modem")],
            [InlineKeyboardButton("🇮🇷 فارسی", callback_data="lang_fa")]
        ])


user_lang = {}


# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await is_joined(update, context):
        keyboard = [
            [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL_USERNAME}")],
            [InlineKeyboardButton("🔄 Check Again", callback_data="check_join")]
        ]
        await update.message.reply_text(
            "❌ You must join our channel first:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    lang = user_lang.get(update.effective_user.id, "fa")
    await update.message.reply_text(
        "یکی از گزینه‌ها را انتخاب کنید:" if lang == "fa" else "Choose an option:",
        reply_markup=main_menu(lang)
    )


# ---------------- BUTTONS ----------------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # LANGUAGE
    if query.data == "lang_en":
        user_lang[user_id] = "en"
        await query.message.edit_text("Language changed to English 🇬🇧", reply_markup=main_menu("en"))
        return

    if query.data == "lang_fa":
        user_lang[user_id] = "fa"
        await query.message.edit_text("زبان تغییر کرد 🇮🇷", reply_markup=main_menu("fa"))
        return

    # CHECK JOIN
    if query.data == "check_join":
        if await is_joined(update, context):
            await query.message.edit_text("✅ Access granted", reply_markup=main_menu())
        else:
            await query.answer("❌ هنوز عضو نشدی", show_alert=True)
        return

    # BACK BUTTON
    back = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data="back")]
    ])

    if query.data == "router":
        text = "Router is a network device that connects networks."
        await query.message.edit_text(text, reply_markup=back)

    elif query.data == "modem":
        text = "Modem Router combines modem + router functions."
        await query.message.edit_text(text, reply_markup=back)

    elif query.data == "back":
        lang = user_lang.get(user_id, "fa")
        await query.message.edit_text(
            "Main Menu" if lang == "en" else "منو اصلی",
            reply_markup=main_menu(lang)
        )


# ---------------- RUN BOT ----------------
def run_bot():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()


# ---------------- RUN BOTH ----------------
if __name__ == "__main__":
    Thread(target=run_web).start()
    run_bot()