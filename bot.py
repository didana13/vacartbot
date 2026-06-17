import os
from threading import Thread
from flask import Flask

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("TOKEN")
CHANNEL_USERNAME = "vacart_com"

web = Flask(__name__)

@web.route("/")
def home():
    return "Bot is running"

def run_web():
    web.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))


user_lang = {}


async def is_joined(update, context):
    try:
        user_id = update.effective_user.id
        member = await context.bot.get_chat_member(
            chat_id=f"@{CHANNEL_USERNAME}",
            user_id=user_id
        )
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


def main_menu(lang="fa"):
    if lang == "fa":
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("Router", callback_data="router")],
            [InlineKeyboardButton("Modem Router", callback_data="modem")],
            [InlineKeyboardButton("English", callback_data="lang_en")]
        ])
    else:
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("Router", callback_data="router")],
            [InlineKeyboardButton("Modem Router", callback_data="modem")],
            [InlineKeyboardButton("Persian", callback_data="lang_fa")]
        ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await is_joined(update, context):
        keyboard = [
            [InlineKeyboardButton("Join Channel", url=f"https://t.me/{CHANNEL_USERNAME}")],
            [InlineKeyboardButton("Check Again", callback_data="check_join")]
        ]
        await update.effective_chat.send_message(
            "You must join our channel first:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    user_id = update.effective_user.id
    lang = user_lang.get(user_id, "fa")

    # جلوگیری از شلوغ شدن گروه
    if update.effective_chat.type != "private":
        await context.bot.send_message(
            chat_id=user_id,
            text="Menu opened",
            reply_markup=main_menu(lang)
        )
        return

    await update.effective_chat.send_message(
        "Choose an option:" if lang == "en" else "یکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=main_menu(lang)
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if query.data == "lang_en":
        user_lang[user_id] = "en"
        await query.message.edit_text("Language changed", reply_markup=main_menu("en"))
        return

    if query.data == "lang_fa":
        user_lang[user_id] = "fa"
        await query.message.edit_text("زبان تغییر کرد", reply_markup=main_menu("fa"))
        return

    if query.data == "check_join":
        if await is_joined(update, context):
            await query.message.edit_text("Access granted", reply_markup=main_menu())
        else:
            await query.answer("Not joined yet", show_alert=True)
        return

    back = InlineKeyboardMarkup([
        [InlineKeyboardButton("Back", callback_data="back")]
    ])

    if query.data == "router":
        await query.message.edit_text(
            "روتر (Router) یک دستگاه شبکه است که وظیفه دارد اطلاعات را بین شبکه‌های مختلف جابه‌جا کند.\n\n"
            "به زبان ساده، روتر مسیر مناسب برای رسیدن داده‌ها به مقصد را پیدا می‌کند.\n\n"
            "مثال: وقتی با گوشی یا لپ‌تاپ به اینترنت وصل می‌شوید، روتر درخواست‌ها را به اینترنت ارسال کرده و پاسخ را برمی‌گرداند.\n\n"
            "یکی از وظایف مهم روتر، مسیریابی بسته‌های اطلاعاتی است.\n\n"
            "بسیاری از مودم‌های امروزی دارای روتر داخلی هستند.",
            reply_markup=back
        )

    elif query.data == "modem":
        await query.message.edit_text(
            "مودم-روتر دستگاهی است که هم وظیفه مودم و هم روتر را انجام می‌دهد.\n\n"
            "یعنی هم اینترنت را از ISP دریافت می‌کند و هم آن را بین دستگاه‌ها پخش می‌کند.",
            reply_markup=back
        )

    elif query.data == "back":
        lang = user_lang.get(user_id, "fa")
        await query.message.edit_text(
            "Main Menu" if lang == "en" else "منو اصلی",
            reply_markup=main_menu(lang)
        )


def run_bot():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()


if __name__ == "__main__":
    Thread(target=run_web).start()
    run_bot()