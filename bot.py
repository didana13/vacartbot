from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = "8748626214:AAFw-InOPZ0FKJrC1q4Y89C4fHtC94bO_54"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("Router", callback_data="router")],
        [InlineKeyboardButton("Modem Router", callback_data="modem_router")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "یکی از مفاهیم را انتخاب کنید:",
        reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "router":

        await query.message.reply_text(
            "روتر (Router) یک دستگاه شبکه است که وظیفه دارد اطلاعات را بین شبکه‌های مختلف جابه‌جا کند.\n\n"
            "به زبان ساده، روتر مسیر مناسب برای رسیدن داده‌ها به مقصد را پیدا می‌کند.\n\n"
            "مثال: وقتی با گوشی یا لپ‌تاپ به اینترنت وصل می‌شوید، روتر درخواست‌ها را به اینترنت ارسال کرده و پاسخ را برمی‌گرداند.\n\n"
            "یکی از وظایف مهم روتر، مسیریابی بسته‌های اطلاعاتی است.\n\n"
            "بسیاری از مودم‌های امروزی دارای روتر داخلی هستند."
        )

    elif query.data == "modem_router":

        await query.message.reply_text(
            "مودم-روتر دستگاهی است که هم وظیفه مودم و هم روتر را انجام می‌دهد.\n\n"
            "یعنی هم اینترنت را از ISP دریافت می‌کند و هم آن را بین دستگاه‌ها پخش می‌کند."
        )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()