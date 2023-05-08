from typing import Final
import lichess.api
from lichess.format import SINGLE_PGN
from lichess_client import APIClient
import asyncio
# pip install python-telegram-bot
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

print('Starting up bot...')

TOKEN: Final = '6264740670:AAHjJxYHFP8napVe2BNY8fb6NxQagtVIqzY'
BOT_USERNAME: Final = '@LichessChallengeBot'


# Lets us use the /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello there! I can create Lichess Challenges for you in groups')


# Lets us use the /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Try typing anything and I will do my best to respond!')


# Lets us use the /custom command
async def create_challenge(username: str):
    client = APIClient(token="lip_COSzqPKqM3MzaaS8IYLL")
    response = await client.challenges.create(username=username, color="white" , rated=True, time_limit=180 , time_increment=0)
    print((response))
    response=str(response)
    challenge_url_index=response.rfind('/');
    return response[challenge_url_index+1:challenge_url_index+7]
async def createTGP(update: Update, context: ContextTypes.DEFAULT_TYPE):

    challenge_id = await create_challenge(username="Thegreatprotector")
    if challenge_id != "plain'":
        challenge_id = 'https://lichess.org/' + challenge_id
        print(f"Challenge created! Challenge ID: {challenge_id}")
        # await update.message.reply_text('Create your own game nub')
        await update.message.reply_text(f"Challenge created! Challenge ID: {challenge_id}")
    else:
        await update.message.reply_text(f"Too Many Reqs")
async def createGambit(update: Update, context: ContextTypes.DEFAULT_TYPE):

    challenge_id = await create_challenge(username="gambit_pnav")
    if challenge_id != "plain'":
        challenge_id = 'https://lichess.org/' + challenge_id
        print(f"Challenge created! Challenge ID: {challenge_id}")
        # await update.message.reply_text('Create your own game nub')
        await update.message.reply_text(f"Challenge created! Challenge ID: {challenge_id}")
    else:
        await update.message.reply_text(f"Too Many Reqs")
async def createKrisnam(update: Update, context: ContextTypes.DEFAULT_TYPE):

    challenge_id = await create_challenge(username="KrisnamS")
    print(challenge_id)

    if challenge_id != "plain'":
        challenge_id = 'https://lichess.org/' + challenge_id
        print(f"Challenge created! Challenge ID: {challenge_id}")
        #await update.message.reply_text('Create your own game nub')
        await update.message.reply_text(f"Challenge created! Challenge ID: {challenge_id}")
    else:
        await update.message.reply_text(f"Too Many Reqs")
# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# Run the program
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('createtgp', createTGP))
    app.add_handler(CommandHandler('creategambit', createGambit))
    app.add_handler(CommandHandler('createkrisnam', createKrisnam))

    # Messages
    #app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Log all errors
    app.add_error_handler(error)

    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=5)
