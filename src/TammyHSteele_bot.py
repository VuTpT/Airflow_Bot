import os
from typing import Final
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from dotenv import load_dotenv

load_dotenv()

TOKEN: Final = os.getenv('TOKEN_BOT')
BOT_USERNAME: Final = os.getenv('NAME_BOT')


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Thinks for chatting with me! I am a apple!')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I am a banana! Please type something so I can respond!')


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command!')


async def service_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ['python', 'CEH'], ['javascript', 'python', 'C++'], ['java']
    ]

    await update.message.reply_text('Do you want to see!',
                                    reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True,
                                                                     one_time_keyboard=True))


async def favorite_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton('java',
                                 'https://translate.google.com/?hl=vi&tab=TT&sl=en&tl=vi&text=favorite&op=translate'),
            InlineKeyboardButton('python',
                                 'https://translate.google.com/?hl=vi&tab=TT&sl=en&tl=vi&text=favorite&op=translate'),
        ]
    ]

    await update.message.reply_text('Training', reply_markup=InlineKeyboardMarkup(keyboard))


# Responses

def handle_response(text: str) -> str:
    processed: str = text.lower()

    print(processed)

    if 'hello' in processed:
        return 'Hey there! 1'

    if 'how are you' in processed:
        return 'Hey there! 2'

    if 'i love python' in processed:
        return 'Hey there! 3'

    return 'I do not understand what you wrote...'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f' Message type: {message_type}')
    print(f' Text: {text}')

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(CommandHandler('service', service_command))
    app.add_handler(CommandHandler('favorite', favorite_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3)
