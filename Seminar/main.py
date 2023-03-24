import const as keys
from telegram.ext import *
import responses as res
import sqlite3
from register import *
from add_withdraw import *
from transfer import *
from others import *

receiver=''
money_to_send=0
print("Starting...")
  
if __name__ == '__main__':
    try:
        DATA=0,1
        TRANSFER,CASH=0,1
        PW=0,1
        conn = sqlite3.connect('Banking.db', check_same_thread=False)
        c= conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS fbank1 (
                    uid text NOT NULL,
                    last text,
                    num interger, 
                    password interger
            )""")
        application= Application.builder().token(keys.API_KEY).build()
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CallbackQueryHandler(button))
        application.add_handler(CommandHandler("help", help_command))
        # application.add_handler(CommandHandler("register", register))
        application.add_handler(ConversationHandler(
            [CommandHandler("register", register)],
            states={
                PW: [MessageHandler(filters.TEXT,create_pw)]
                },
            fallbacks=[CommandHandler("quit",quit)]
        )
        ) 
        
        application.add_handler(ConversationHandler(
            [CommandHandler("add", add_command)],
            states={
                DATA: [MessageHandler(filters.TEXT,add_input)]
                },
            fallbacks=[CommandHandler("quit",quit)]
        )
        ) 
        
        application.add_handler(ConversationHandler(
            [CommandHandler("withdraw", withdraw_command)],
            states={
                DATA: [MessageHandler(filters.TEXT,withdraw_input)]
                },
            fallbacks=[CommandHandler("quit",quit)]
        )
        )

        application.add_handler(ConversationHandler(
            [CommandHandler("transfer", transfer_command)],
            states={
                TRANSFER: [MessageHandler(filters.TEXT, receive_user)],
                CASH: [MessageHandler(filters.TEXT,get_pw)],
                PW: [MessageHandler(filters.TEXT, transferring)]
            },
            fallbacks=[CommandHandler("quit",quit)]
        ))
        
        application.add_handler(CommandHandler("Show",show_data))
        application.add_handler(CommandHandler("Show_uid",show_uid))
        
        application.add_handler(MessageHandler(filters.TEXT,handle_messages))
        
        application.add_error_handler(error)
        application.run_polling()
        conn.commit()
    except Exception as error:
        print('Cause: {}'.format(error))


        