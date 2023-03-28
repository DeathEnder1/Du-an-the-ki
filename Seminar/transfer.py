from telegram.ext import *
from telegram import *
import sqlite3
conn = sqlite3.connect('Banking.db', check_same_thread=False)
c= conn.cursor()
import os
import sys
if not os.environ.get('PYTHONHASHSEED'):
    os.environ['PYTHONHASHSEED'] = '1234'
    os.execv(sys.executable, ['python3'] + sys.argv) 
    
reply_kb=[
    ['10','50'],
    ['100','500'],
    ['1000','5000'],
]
markup = ReplyKeyboardMarkup(reply_kb, one_time_keyboard=True)
TRANSFER,CASH=0,1
PW=0,1
async def transfer_command(update, context):
    uid = update.message.chat_id
    c.execute("SELECT uid FROM fbank1 WHERE uid={}".format(uid))
    find=c.fetchone()
    if find is None:
        await update.message.reply_text("Please register to continue")
    else:   
        await update.message.reply_text("Please input the uid that you want to transfer to")
        return TRANSFER

async def receive_user(update, context)->int:
    global receiver
    uid= update.message.text
    receiver_uid=str(update.message.chat_id)
    if uid==receiver_uid: 
        await update.message.reply_text("You can't transfer money to yourself") 
        return ConversationHandler.END
    else:
        c.execute("SELECT num from fbank1 WHERE uid={}".format(uid))
        find=c.fetchone()
        if find is None:
            await update.message.reply_text("No such user available")
            return ConversationHandler.END
        else:
            await update.message.reply_text("Please input the money you want to send", reply_markup=markup,)
            receiver=uid
            return CASH
    
async def get_pw(update,context):
    global money_to_send
    data= update.message.text
    sender=update.message.chat_id
    if data.isdecimal():
        d1=int(data)
        c.execute("SELECT num from fbank1 WHERE uid={}".format(sender))
        v=c.fetchall()
        v1=v[0]
        sender_num=v1[0]
        if sender_num<d1:
            await update.message.reply_text("Not enough money to be transfered", reply_markup=ReplyKeyboardRemove(),)
            return ConversationHandler.END 
        else:
            await update.message.reply_text("Please input your password to continue the transaction", reply_markup=ReplyKeyboardRemove(),)
            money_to_send=d1
            return PW
    else: 
        await update.message.reply_text("Please enter a number")
    
async def transferring(update,context):
    # count=0 
    pw=update.message.text  
    hpw=hash(pw)
    sender=update.message.chat_id
    c.execute("SELECT password FROM fbank1 WHERE uid={}".format(sender))
    # for count in range(5):
    p=c.fetchall()
    p1=p[0]
    hp1=p1[0]
    if hpw!=hp1:
        count+=1
        await update.message.reply_text("Incorrect password please try again later")
        # await update.message.reply_text("Nokori ha {} ".format(5-count))
        return ConversationHandler.END
    else: 
        c.execute("SELECT num from fbank1 WHERE uid={}".format(sender))
        v=c.fetchall()
        v1=v[0]
        sender_num=v1[0]
        c.execute("SELECT num from fbank1 WHERE uid={}".format(receiver))
        r=c.fetchall()
        r1=r[0]
        receiver_num=r1[0]
        c.execute("""UPDATE fbank1
                    set num = {}
                    where uid= {}
                    """.format(sender_num-money_to_send,sender))
        c.execute("""UPDATE fbank1
                    set num = {}
                    where uid= {}
                    """.format(receiver_num+money_to_send,receiver))
        conn.commit()
        await update.message.reply_text("Transfer completed")
        bot_message = " お金が届いたよ !!"
        # chatid = "6208967501"
        send_text = 'https://api.telegram.org/bot' + keys.API_KEY + '/sendMessage?chat_id=' + receiver + '&text=' + bot_message
        response = requests.get(send_text)
        response.json()
        return ConversationHandler.END
    
