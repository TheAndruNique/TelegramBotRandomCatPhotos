import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

from helper import localized_text, random_cat_photo, BOT_LANGUAGE, TELEGRAM_BOT_TOKEN


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

keyboard_cat_image_request = [
    [InlineKeyboardButton("Next", callback_data="cat_image")]
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(localized_text("help_text", BOT_LANGUAGE))

processing_query = {}

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    await query.answer()

    if query.data == "cat_image":
        await cats_command(update, context)
    
async def cats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    processing_message = await update.effective_message.reply_text(localized_text("processing_text", BOT_LANGUAGE))
    
    img = random_cat_photo()
    if img is not None:
        await update.effective_message.reply_photo(photo=img, 
                                                reply_markup=InlineKeyboardMarkup(keyboard_cat_image_request))           
        await processing_message.delete()
    else:
        await processing_message.edit_text(localized_text("image_request_error_text", BOT_LANGUAGE))

def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(callback_handler))
    application.add_handler(CommandHandler("cats", cats_command))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()