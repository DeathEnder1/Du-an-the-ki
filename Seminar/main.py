import const as keys
from telegram.ext import *
import responses as res
from telegram import LabeledPrice
import sqlite3

print("Starting...")

async def  start_command(update, context: ContextTypes.DEFAULT_TYPE): #answer '/help' command
    await update.message.reply_text('Type something')

async def help_command(update, context):
    await update.message.reply_text('Fucking google it')
    
async def handle_messages(update,context):
    txt= str(update.message.text).lower()
    response= res.sample_responses(txt)
    
    await update.message.reply_text(response)

# async def uid(update, context: CallbackContext):
#     uid = update.message.chat.id
#     await update.message.reply_text(f"Your uid is {uid}")

# async def name(update, context: CallbackContext):
#     first = update.message.chat.first_name
#     # last = update.message.chat.last_name
#     await update.message.reply_text(f"Your first name is {first}")


async def error(update, context):
    print(f"Update {update} caused error {context.error}")

async def register(update, context):
    uid = update.message.chat_id
    last = update.message.chat.last_name
    username= update.message.chat.username
    c.execute("INSERT INTO Bank VALUES (?, ?, ?)",(uid,last,1000))
    await update.message.reply_text("Registered")
    conn.commit()

async def add_command(update, context):
    await update.message.reply_text("You value is ?")  
    return DATA 

async def add_input(update,context)->int:
    data=int(update.message.text)
    uid=update.message.chat_id
    c.execute("SELECT num from Bank WHERE uid={}".format(uid))
    v1=c.fetchall()
    v_1=v1[0]
    num=int(v_1[0])
    num+=data
    c.execute("""UPDATE Bank
                SET num={}
                WHERE uid={}""".format(num,uid))
   
    await update.message.reply_text("Added")
    conn.commit()
    return ConversationHandler.END
    
async def add_quit(update, context: CallbackContext):
    await update.message.reply_text("Done")
    return ConversationHandler.END

async def withdraw_command(update, context):
    await update.message.reply_text("You value is ?")  
    return DATA

async def withdraw_input(update,context)->int:
    data=int(update.message.text)
    uid=update.message.chat_id
    # await update.message.reply_text("Your value is {}".format(data))
    c.execute("SELECT num from Bank WHERE uid={}".format(uid))
    v1=c.fetchall()
    v_1=v1[0]
    num=v_1[0]
    if data>num:
        await update.message.reply_text("Not enough money to withdraw")
        return ConversationHandler.END
    else: 
        num-=data
        c.execute("""UPDATE Bank
                    SET num={}
                    WHERE uid={}""".format(num,uid))
        conn.commit()
        await update.message.reply_text("Withdrawed")
        return ConversationHandler.END

async def withdraw_quit(update, context: CallbackContext):
    await update.message.reply_text("Done") 
    return ConversationHandler.END

async def show_data(update,context):
    uid=update.message.chat_id
    c.execute("SELECT num from Bank WHERE uid={}".format(uid))
    v1=c.fetchall()
    v_1=v1[0]
    num=v_1[0]
    await update.message.reply_text("Your balance: {}".format(num))
if __name__ == '__main__':
    try:
        DATA=0,1
        conn = sqlite3.connect('bank.db', check_same_thread=False)
        c= conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS Bank (
                    uid text,
                    last text,
                    num interger
            )""")
        application= Application.builder().token(keys.API_KEY).build()
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("register", register))
        
        application.add_handler(ConversationHandler(
            [CommandHandler("add", add_command)],
            states={
                DATA: [MessageHandler(filters.TEXT,add_input)]
                },
            fallbacks=[CommandHandler("quit",add_quit)]
        )
        ) 
        
        application.add_handler(ConversationHandler(
            [CommandHandler("withdraw", withdraw_command)],
            states={
                DATA: [MessageHandler(filters.TEXT,withdraw_input)]
                },
            fallbacks=[CommandHandler("quit",withdraw_quit)]
        )
        )

        application.add_handler(CommandHandler("Show",show_data))
        
        application.add_handler(MessageHandler(filters.TEXT,handle_messages))
        
        application.add_error_handler(error)
        application.run_polling()
        conn.commit()
    except Exception as error:
        print('Cause: {}'.format(error))


        