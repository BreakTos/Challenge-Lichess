from typing import Final
import lichess.api
from lichess.format import SINGLE_PGN
from lichess_client import APIClient
import asyncio
import json
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

print('Starting up bot...')
AllKeys={}
TOKEN: Final = '6264740670:AAHjJxYHFP8napVe2BNY8fb6NxQagtVIqzY' # Replace with your Token
BOT_USERNAME: Final = '@LichessChallengeBot'

async def open(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = 'https://lichess.org/'+"api"+'/challenge/open'
    msg = update.message.text
    # print(msg+"x")
    msgg:list = msg.split(' ')
    # print(msgg[1])
    response =  requests.post(url,json={
        "clock.limit":msgg[1],
        "clock.increment":msgg[2]
    })
    
    await update.message.reply_text(response.json()["url"])


# Lets us use the /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello there! I can create Lichess Challenges for you in groups. Use /challenge 'opponentName' 'seconds' 'increment' ")


# Lets us use the /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Try typing anything and I will do my best to respond!')

async  def update(update: Update, context: ContextTypes.DEFAULT_TYPE):

    msg: str = update.message.text
    dig = str(update)
    dig = dig[dig.find("first_name"):dig.find("is_bot") - 2]
    dig = dig[dig.rfind("=") + 1:]
    Fuser=(list)(msg[7:].split())
    print(Fuser)
    AllKeys[dig]=Fuser[0]
    print(AllKeys)
    await update.message.reply_text(f"Updated your Key, Now you can use /challenge command")
# Lets us use the /custom command
async def create_challenge(challenger: int , username: str , color:str , time_limit:int , time_increment:int):
    
    client = APIClient(token=AllKeys[(str)(challenger)]) # Replace with your Token
    color=str(color)
    response = await client.challenges.create(username=username, color=color , rated=True, time_limit=time_limit , time_increment=time_increment)
    print((response))
    print("lichess.org/"+username)
    response=str(response)
    challenge_url_index=response.rfind('/');
    end=challenge_url_index+1
    while(response[end]!="'"): end+=1
    return response[challenge_url_index+1:end]
async def challenge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dig=str(update)
    dig=dig[dig.find("first_name"):dig.find("is_bot")-2]
    dig=dig[dig.rfind("=")+1:]
    print(dig+"helllo")
    if dig not in AllKeys.keys():
        await update.message.reply_text(f"https://lichess.org/account/oauth/token/create?scopes[]=challenge:write&scopes[]=puzzle:read&description=Prefilled+token+example")
        await update.message.reply_text(f"Copy the key from here and send /update 'yourApiKey' to send challenges")
        return
    msg: str = update.message.text
    Fuser=(list)(msg[11:].split())
    print(Fuser)
    col=""
    if len(Fuser[1])==5:
        col=Fuser[1]
    challenge_id = await create_challenge(challenger=dig,username=Fuser[0],color=col,time_limit=Fuser[-2],time_increment=Fuser[-1])
    if challenge_id != "plain" and challenge_id !='json':
        challenge_id = 'https://lichess.org/' + challenge_id
        print(f"Challenge created! Challenge ID: {challenge_id}")
        # await update.message.reply_text('Create your own game nub')
        await update.message.reply_text(f"Challenge created! Challenge ID: {challenge_id}")
    else:
        if challenge_id=='plain':
            await update.message.reply_text(f"Too Many Reqs")
        else:
            await update.message.reply_text(f"Account does not exist or closed")

# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# Run the program
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('challenge', challenge))
    app.add_handler(CommandHandler('update', update))
    app.add_handler(CommandHandler('open', open))

    #app.add_handler(CommandHandler('createrandom', createRand))

    # Messages
    #app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Log all errors
    app.add_error_handler(error)

    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=5)
