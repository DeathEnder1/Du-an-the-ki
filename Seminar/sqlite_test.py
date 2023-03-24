# import const as keys
# from telegram import *
# from telegram.ext import *
# import responses as res
# import sqlite3
# from register import *
# from add_withdraw import *
# from transfer import *
# from others import *

# receiver=''
# money_to_send=0
# print("Starting...")

# import os
# import sys
# if not os.environ.get('PYTHONHASHSEED'):
#     os.environ['PYTHONHASHSEED'] = '1234'
#     os.execv(sys.executable, ['python3'] + sys.argv) 

# reply_kb=[
#     ['10','50'],
#     ['100','500'],
#     ['1000','5000'],
# ]
# markup = ReplyKeyboardMarkup(reply_kb, one_time_keyboard=True)

# async def register(update, context):
#     uid = update.message.chat_id
#     last = update.message.chat.last_name
#     c.execute("SELECT uid FROM fbank1 WHERE uid={}".format(uid))
#     find=c.fetchone()
    
#     if find is None:
#         c.execute("INSERT INTO fbank1 (uid,last,num) VALUES (?, ?, ?)",(uid,last,1000))
#         await update.message.reply_text("Please input the password you want to create")
#         conn.commit()
#         return PW
#     else:
#         await update.message.reply_text("Already registered")
#         ConversationHandler.END

# async def create_pw(update, context):
#     uid=update.message.chat_id
#     passw=update.message.text
#     hpw=hash(passw)
#     c.execute("""UPDATE fbank1
#                  SET password={}
#                  WHERE uid= {}""".format(hpw,uid))
#     conn.commit()
#     await update.message.reply_text("Register completed")
#     return ConversationHandler.END

# async def  start_command(update, context: ContextTypes.DEFAULT_TYPE): #answer '/help' command
    
#     # keyboard=[
#     #     [
#     #         InlineKeyboardButton("Option 1", callback_data='1'),
#     #         InlineKeyboardButton("Option 2", callback_data='2'),
#     #     ],
#     #     [InlineKeyboardButton("Option 3",callback_data='3')]
#     # ]
#     # reply_markup= InlineKeyboardMarkup(keyboard)
#     await update.message.reply_text('To register please use the command /register \nIf you have already registered type /help to find more command')
#     # await update.message.reply_text("choose ",reply_markup=reply_markup)
# async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     query = update.callback_query
#     await query.answer()
#     await query.edit_message_text(text=f"Selected option: {query.data}")

# async def help_command(update, context):
#     await update.message.reply_text("Here is the list of commands that are available: \n/transfer: to transfer money to others \n/add: to add money into your account \n/withdraw to withdraw money from your account \n/show: to show your balance \n/show_uid: to show your uid")
    
# async def handle_messages(update,context):
#     txt= str(update.message.text).lower()
#     response= res.sample_responses(txt)
    
#     await update.message.reply_text(response)

# async def error(update, context):
#     print(f"Update {update} caused error {context.error}")
   
# async def quit(update, context: CallbackContext):
#     await update.message.reply_text("Done")
#     return ConversationHandler.END

# async def show_data(update,context):
#     uid=update.message.chat_id
#     c.execute("SELECT num from fbank1 WHERE uid={}".format(uid))
#     v1=c.fetchall()
#     v_1=v1[0]
#     num=v_1[0]
#     await update.message.reply_text("Your balance: {}".format(num))
    
# async def show_uid(update,context):
#     uid= update.message.chat_id
#     await update.message.reply_text("Your uid: {}".format(uid))
    
# async def transfer_command(update, context):
#     uid = update.message.chat_id
#     c.execute("SELECT uid FROM fbank1 WHERE uid={}".format(uid))
#     find=c.fetchone()
#     if find is None:
#         await update.message.reply_text("Please register to continue")
#     else:   
#         await update.message.reply_text("Please input the uid that you want to transfer to")
#         return TRANSFER

# async def receive_user(update, context)->int:
#     global receiver
#     uid= update.message.text
#     receiver_uid=str(update.message.chat_id)
#     if uid==receiver_uid: 
#         await update.message.reply_text("You can't transfer money to yourself") 
#         return ConversationHandler.END
#     else:
#         c.execute("SELECT num from fbank1 WHERE uid={}".format(uid))
#         find=c.fetchone()
#         if find is None:
#             await update.message.reply_text("No such user available")
#             return ConversationHandler.END
#         else:
#             await update.message.reply_text("Please input the money you want to send", reply_markup=markup,)
#             receiver=uid
#             return CASH
    
# async def get_pw(update,context):
#     global money_to_send
#     data= update.message.text
#     sender=update.message.chat_id
#     if data.isdecimal():
#         d1=int(data)
#         c.execute("SELECT num from fbank1 WHERE uid={}".format(sender))
#         v=c.fetchall()
#         v1=v[0]
#         sender_num=v1[0]
#         if sender_num<d1:
#             await update.message.reply_text("Not enough money to be transfered", reply_markup=ReplyKeyboardRemove(),)
#             return ConversationHandler.END 
#         else:
#             await update.message.reply_text("Please input your password to continue the transaction", reply_markup=ReplyKeyboardRemove(),)
#             money_to_send=d1
#             return PW
#     else: 
#         await update.message.reply_text("Please enter a number")
    
# async def transferring(update,context):
#     # count=0 
#     pw=update.message.text  
#     hpw=hash(pw)
#     sender=update.message.chat_id
#     c.execute("SELECT password FROM fbank1 WHERE uid={}".format(sender))
#     # for count in range(5):
#     p=c.fetchall()
#     p1=p[0]
#     hp1=p1[0]
#     if hpw!=hp1:
#         count+=1
#         await update.message.reply_text("Incorrect password please try again later")
#         # await update.message.reply_text("Nokori ha {} ".format(5-count))
#         return ConversationHandler.END
#     else: 
#         c.execute("SELECT num from fbank1 WHERE uid={}".format(sender))
#         v=c.fetchall()
#         v1=v[0]
#         sender_num=v1[0]
#         c.execute("SELECT num from fbank1 WHERE uid={}".format(receiver))
#         r=c.fetchall()
#         r1=r[0]
#         receiver_num=r1[0]
#         c.execute("""UPDATE fbank1
#                     set num = {}
#                     where uid= {}
#                     """.format(sender_num-money_to_send,sender))
#         c.execute("""UPDATE fbank1
#                     set num = {}
#                     where uid= {}
#                     """.format(receiver_num+money_to_send,receiver))
#         conn.commit()
#         await update.message.reply_text("Transfer completed")
#         return ConversationHandler.END
    
# async def add_command(update, context):
#     uid = update.message.chat_id
#     c.execute("SELECT uid FROM fbank1 WHERE uid={}".format(uid))
#     find=c.fetchone()
    
#     if find is None:
#         await update.message.reply_text("Please register to continue")
#     else:   
#         await update.message.reply_text("You value is ?", reply_markup=markup,)  
#         return DATA 
# async def add_input(update,context)->int:
#     data=update.message.text
#     if data.isdecimal():
#         d1=int(data)
#         if d1>=0:
#             uid=update.message.chat_id
#             c.execute("SELECT num from fbank1 WHERE uid={}".format(uid))
#             v1=c.fetchall()
#             v_1=v1[0]
#             num=int(v_1[0])
#             num+=d1
#             c.execute("""UPDATE fbank1
#                         SET num={}
#                         WHERE uid={}""".format(num,uid))
        
#             await update.message.reply_text("Added",  reply_markup=ReplyKeyboardRemove(),)
#             conn.commit()
#             return ConversationHandler.END
#         else:
#             await update.message.reply_text("Please enter a positive number",  reply_markup=ReplyKeyboardRemove(),)
#     else:
#         await update.message.reply_text("Please enter a number")
        
# async def withdraw_command(update, context):
#     uid = update.message.chat_id
#     c.execute("SELECT uid FROM fbank1 WHERE uid={}".format(uid))
#     find=c.fetchone()
#     if find is None:
#         await update.message.reply_text("Please register to continue")
#     else:   
#         await update.message.reply_text("You value is ?", reply_markup=markup,)  
#         return DATA 

# async def withdraw_input(update,context)->int:
#     data=update.message.text
#     if data.isdecimal():
#         d1=int(data)
#         if d1>0:
#             uid=update.message.chat_id
#             c.execute("SELECT num from fbank1 WHERE uid={}".format(uid))
#             v1=c.fetchall()
#             v_1=v1[0]
#             num=v_1[0]
#             if d1>num:
#                 await update.message.reply_text("Not enough money to withdraw",  reply_markup=ReplyKeyboardRemove(),)
#                 return ConversationHandler.END
#             else: 
#                 num-=d1
#                 c.execute("""UPDATE fbank1
#                             SET num={}
#                             WHERE uid={}""".format(num,uid))
#                 conn.commit()
#                 await update.message.reply_text("Withdrawed",  reply_markup=ReplyKeyboardRemove(),)
#                 return ConversationHandler.END
#         else:
#             await update.message.reply_text("Please enter a positive number",  reply_markup=ReplyKeyboardRemove(),)
#     else:
#         await update.message.reply_text("Please enter a number")
        
# if __name__ == '__main__':
#     try:
#         DATA=0,1
#         TRANSFER,CASH=0,1
#         PW=0,1
#         conn = sqlite3.connect('Banking.db', check_same_thread=False)
#         c= conn.cursor()
#         c.execute("""CREATE TABLE IF NOT EXISTS fbank1 (
#                     uid text NOT NULL,
#                     last text,
#                     num interger, 
#                     password interger
#             )""")
#         application= Application.builder().token(keys.API_KEY).build()
#         application.add_handler(CommandHandler("start", start_command))
#         application.add_handler(CallbackQueryHandler(button))
#         application.add_handler(CommandHandler("help", help_command))
#         # application.add_handler(CommandHandler("register", register))
#         application.add_handler(ConversationHandler(
#             [CommandHandler("register", register)],
#             states={
#                 PW: [MessageHandler(filters.TEXT,create_pw)]
#                 },
#             fallbacks=[CommandHandler("quit",quit)]
#         )
#         ) 
        
#         application.add_handler(ConversationHandler(
#             [CommandHandler("add", add_command)],
#             states={
#                 DATA: [MessageHandler(filters.TEXT,add_input)]
#                 },
#             fallbacks=[CommandHandler("quit",quit)]
#         )
#         ) 
        
#         application.add_handler(ConversationHandler(
#             [CommandHandler("withdraw", withdraw_command)],
#             states={
#                 DATA: [MessageHandler(filters.TEXT,withdraw_input)]
#                 },
#             fallbacks=[CommandHandler("quit",quit)]
#         )
#         )

#         application.add_handler(ConversationHandler(
#             [CommandHandler("transfer", transfer_command)],
#             states={
#                 TRANSFER: [MessageHandler(filters.TEXT, receive_user)],
#                 CASH: [MessageHandler(filters.TEXT,get_pw)],
#                 PW: [MessageHandler(filters.TEXT, transferring)]
#             },
#             fallbacks=[CommandHandler("quit",quit)]
#         ))
        
#         application.add_handler(CommandHandler("Show",show_data))
#         application.add_handler(CommandHandler("Show_uid",show_uid))
        
#         application.add_handler(MessageHandler(filters.TEXT,handle_messages))
        
#         application.add_error_handler(error)
#         application.run_polling()
#         conn.commit()
#     except Exception as error:
#         print('Cause: {}'.format(error))