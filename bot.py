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
            [InlineKeyboardButton("MikroTik", callback_data="mikrotik")],
            [InlineKeyboardButton("English", callback_data="lang_en")]
        ])
    else:
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("Router", callback_data="router")],
            [InlineKeyboardButton("Modem Router", callback_data="modem")],
            [InlineKeyboardButton("MikroTik", callback_data="mikrotik")],
            [InlineKeyboardButton("Persian", callback_data="lang_fa")]
        ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await is_joined(update, context):
        keyboard = [
            [InlineKeyboardButton("Join Channel", url=f"https://t.me/{CHANNEL_USERNAME}")],
            [InlineKeyboardButton("Check Again", callback_data="check_join")]
        ]

        await update.effective_chat.send_message(
            "You must join our channel first.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    user_id = update.effective_user.id
    lang = user_lang.get(user_id, "fa")

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
    lang = user_lang.get(user_id, "fa")

    if query.data == "lang_en":
        user_lang[user_id] = "en"
        await query.message.edit_text(
            "Language changed",
            reply_markup=main_menu("en")
        )
        return

    if query.data == "lang_fa":
        user_lang[user_id] = "fa"
        await query.message.edit_text(
            "زبان تغییر کرد",
            reply_markup=main_menu("fa")
        )
        return

    if query.data == "check_join":
        if await is_joined(update, context):
            await query.message.edit_text(
                "Access granted",
                reply_markup=main_menu(lang)
            )
        else:
            await query.answer(
                "Not joined yet",
                show_alert=True
            )
        return

    back = InlineKeyboardMarkup([
        [InlineKeyboardButton("Back", callback_data="back")]
    ])

    if query.data == "router":

        if lang == "fa":
            text = (
                "روتر (Router) یک دستگاه شبکه است که وظیفه دارد اطلاعات را بین شبکه‌های مختلف جابه‌جا کند. "
                "به زبان ساده، روتر مسیر مناسب برای رسیدن داده‌ها به مقصد را پیدا می‌کند."
            )
        else:
            text = (
                "A Router is a network device that transfers data between different networks. "
                "Simply put, a router finds the best path for data to reach its destination."
            )

        await query.message.edit_text(text, reply_markup=back)

    elif query.data == "modem":

        if lang == "fa":
            text = (
                "بسیاری از دستگاه‌هایی که در خانه به نام مودم می‌شناسیم، در واقع مودم-روتر هستند؛ "
                "یعنی هم وظیفه اتصال به اینترنت را انجام می‌دهند (مودم) و هم اینترنت را بین دستگاه‌های مختلف "
                "توزیع می‌کنند (روتر)."
            )
        else:
            text = (
                "Many devices that we call modems at home are actually modem-routers. "
                "They both connect to the Internet (modem function) and distribute the Internet "
                "among different devices (router function)."
            )

        await query.message.edit_text(text, reply_markup=back)

    elif query.data == "mikrotik":

        if lang == "fa":
            text = (
                "روتر میکروتیک (MikroTik) دستگاهی قدرتمند و مقرون‌به‌صرفه برای مدیریت و مسیریابی "
                "ترافیک شبکه است. این دستگاه توسط شرکت لتونیایی میکروتیک تولید شده و از سیستم‌عامل "
                "انحصاری RouterOS بهره می‌برد. این سیستم‌عامل مسیریابی‌های پیشرفته، فایروال قدرتمند "
                "و قابلیت‌های متنوع شبکه را فراهم می‌کند."
            )
        else:
            text = (
                "A MikroTik router is a powerful and cost-effective device for managing and routing "
                "network traffic. It is produced by the Latvian company MikroTik and runs its proprietary "
                "RouterOS operating system. This operating system provides advanced routing, a powerful "
                "firewall, and a wide range of networking features."
            )

        await query.message.edit_text(text, reply_markup=back)

    elif query.data == "back":

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