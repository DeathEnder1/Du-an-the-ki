from telegram.ext import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
import responses as res
import sqlite3
conn = sqlite3.connect('Banking.db', check_same_thread=False)
c= conn.cursor()

async def  start_command(update, context: ContextTypes.DEFAULT_TYPE): #answer '/help' command
    
    # keyboard=[
    #     [
    #         InlineKeyboardButton("Option 1", callback_data='1'),
    #         InlineKeyboardButton("Option 2", callback_data='2'),
    #     ],
    #     [InlineKeyboardButton("Option 3",callback_data='3')]
    # ]
    # reply_markup= InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('To register please use the command /register \nIf you have already registered type /help to find more command')
    # await update.message.reply_text("choose ",reply_markup=reply_markup)
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f"Selected option: {query.data}")

async def help_command(update, context):
    await update.message.reply_text("Here is the list of commands that are available: \n/transfer: to transfer money to others \n/add: to add money into your account \n/withdraw to withdraw money from your account \n/show: to show your balance \n/show_uid: to show your uid")
    
async def handle_messages(update,context):
    txt= str(update.message.text).lower()
    response= res.sample_responses(txt)
    
    await update.message.reply_text(response)

async def error(update, context):
    print(f"Update {update} caused error {context.error}")
   
async def quit(update, context: CallbackContext):
    await update.message.reply_text("Done")
    return ConversationHandler.END

async def show_data(update,context):
    uid=update.message.chat_id
    c.execute("SELECT num from fbank1 WHERE uid={}".format(uid))
    v1=c.fetchall()
    v_1=v1[0]
    num=v_1[0]
    await update.message.reply_text("Your balance: {}".format(num))
    
async def show_uid(update,context):
    uid= update.message.chat_id
    await update.message.reply_text("Your uid: {}".format(uid))