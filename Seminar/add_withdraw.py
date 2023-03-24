from telegram.ext import *
from telegram import *
import sqlite3
conn = sqlite3.connect('Banking.db', check_same_thread=False)
c= conn.cursor()
DATA=0,1
reply_kb=[
    ['10','50'],
    ['100','500'],
    ['1000','5000'],
]
markup = ReplyKeyboardMarkup(reply_kb, one_time_keyboard=True)
async def add_command(update, context):
    uid = update.message.chat_id
    c.execute("SELECT uid FROM fbank1 WHERE uid={}".format(uid))
    find=c.fetchone()
    
    if find is None:
        await update.message.reply_text("Please register to continue")
    else:   
        await update.message.reply_text("You value is ?", reply_markup=markup,)  
        return DATA 
async def add_input(update,context)->int:
    data=update.message.text
    if data.isdecimal():
        d1=int(data)
        if d1>=0:
            uid=update.message.chat_id
            c.execute("SELECT num from fbank1 WHERE uid={}".format(uid))
            v1=c.fetchall()
            v_1=v1[0]
            num=int(v_1[0])
            num+=d1
            c.execute("""UPDATE fbank1
                        SET num={}
                        WHERE uid={}""".format(num,uid))
        
            await update.message.reply_text("Added",  reply_markup=ReplyKeyboardRemove(),)
            conn.commit()
            return ConversationHandler.END
        else:
            await update.message.reply_text("Please enter a positive number",  reply_markup=ReplyKeyboardRemove(),)
    else:
        await update.message.reply_text("Please enter a number")
        
async def withdraw_command(update, context):
    uid = update.message.chat_id
    c.execute("SELECT uid FROM fbank1 WHERE uid={}".format(uid))
    find=c.fetchone()
    if find is None:
        await update.message.reply_text("Please register to continue")
    else:   
        await update.message.reply_text("You value is ?", reply_markup=markup,)  
        return DATA 

async def withdraw_input(update,context)->int:
    data=update.message.text
    if data.isdecimal():
        d1=int(data)
        if d1>0:
            uid=update.message.chat_id
            c.execute("SELECT num from fbank1 WHERE uid={}".format(uid))
            v1=c.fetchall()
            v_1=v1[0]
            num=v_1[0]
            if d1>num:
                await update.message.reply_text("Not enough money to withdraw",  reply_markup=ReplyKeyboardRemove(),)
                return ConversationHandler.END
            else: 
                num-=d1
                c.execute("""UPDATE fbank1
                            SET num={}
                            WHERE uid={}""".format(num,uid))
                conn.commit()
                await update.message.reply_text("Withdrawed",  reply_markup=ReplyKeyboardRemove(),)
                return ConversationHandler.END
        else:
            await update.message.reply_text("Please enter a positive number",  reply_markup=ReplyKeyboardRemove(),)
    else:
        await update.message.reply_text("Please enter a number")