import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

from helper import localized_text, random_cat_photo, BOT_LANGUAGE, TELEGRAM_BOT_TOKEN


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

keyboard_cats_count = [
    [
        InlineKeyboardButton("5", callback_data="cat_photos_5"),
        InlineKeyboardButton("10", callback_data="cat_photos_10"),
        InlineKeyboardButton("15", callback_data="cat_photos_15"),
        InlineKeyboardButton("20", callback_data="cat_photos_20"),
    ]
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(localized_text("help_text", BOT_LANGUAGE))


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    
    await query.answer()
    
    if query.data == "some_cat_photos":
        await query.edit_message_text(text=localized_text("how_many_cats", BOT_LANGUAGE),
                                reply_markup=InlineKeyboardMarkup(keyboard_cats_count))
    elif query.data[0:11] == "cat_photos_":
        count = int(query.data[11:])
        return await send_cat_photos(update, count)

async def cats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton(localized_text("confirmation_button_text", BOT_LANGUAGE), 
                              callback_data="some_cat_photos")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(localized_text("cat_photos_request", BOT_LANGUAGE), 
                                    reply_markup=reply_markup)

async def send_cat_photos(update: Update, cats: int):
    for i in range(cats):
        img = random_cat_photo()
        await update.effective_message.reply_photo(photo=img)           

def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(callback_handler))
    application.add_handler(CommandHandler("cats", cats_command))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()