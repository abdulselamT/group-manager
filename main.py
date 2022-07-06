from email import message
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup,InlineKeyboardButton
from telebot import custom_filters
from constants import API_KEY
import sqlite3
admin_state={}
def is_admin(user_id):
    c=bot.get_chat_member(-1001747735158,user_id).status in ['administrator','creator']
    if c:
        try:
            b=admin_state[user_id]
        except:
            admin_state[user_id]=0
    return c
conn=sqlite3.connect('keyword.db',check_same_thread=False)
c=conn.cursor()
def keywords():
    conn=sqlite3.connect('keyword.db',check_same_thread=False)
    c=conn.cursor()
    c.execute('SELECT keyword FROM keywords ')
    d=c.fetchall()
    myli=[]
    for j in d:
        myli.append(j[0])
    
    conn.commit()
    return myli
#keywords()
def addkeyword(kes):
    conn=sqlite3.connect('keyword.db',check_same_thread=False)
    c=conn.cursor()
    for j in kes:
        c.execute('SELECT keyword FROM keywords WHERE keyword = ?', (j, ))
        d=c.fetchone()
        if not d:
            c.execute('INSERT INTO keywords values (?) ', (j,))
            conn.commit()
            
def deletekeyword(ke):
    conn=sqlite3.connect('keyword.db',check_same_thread=False)
    c=conn.cursor()
    c.execute('DELETE  FROM keywords WHERE keyword = ?', (ke, ))
    d=c.fetchone
    conn.commit()
def menub():
    markup = InlineKeyboardMarkup()
    markup.width =1
    markup.add(
                InlineKeyboardButton('keywords',callback_data='keywords'),
                InlineKeyboardButton('add_keywords',callback_data='add_keywords'),
                InlineKeyboardButton('remove_keywords',callback_data='remove_keywords'),
                )
    return markup    
def inlinemarkup(a=0,b=12):
    markup = InlineKeyboardMarkup()
    l=keywords()
    if len(l)<b:
        b=len(l)
    if a<0:
        a=0
    for k in range(a,b,3):
        m=l[k:k+3]
        try:
            markup.add(
                    InlineKeyboardButton(l[k],callback_data=l[k]),
                    InlineKeyboardButton(l[k+1],callback_data=l[k+1]),
                    InlineKeyboardButton(l[k+2],callback_data=l[k+2])
                    )
        except:
            c=-1
            for j in range(b-k):
                markup.add(
                    InlineKeyboardButton(l[c],callback_data=l[c])

                )
                c-=1

    if a>0 and b<len(l):
        markup.add(
                InlineKeyboardButton('⬅️',callback_data='p-'+str(b)),
                InlineKeyboardButton('➡️',callback_data='n-'+str(b)),
            )
    elif b==len(l):
        markup.add(
                InlineKeyboardButton('⬅️',callback_data='p-'+str(b)),
            )
    elif a==0:
        markup.add(
                InlineKeyboardButton('➡️',callback_data='n-'+str(b)),
            )



    markup.add(
                InlineKeyboardButton('⬆️',callback_data='back'),
            )
    return markup

bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['remove_keyword'],func=lambda m: m.chat.id in admin_state)
def deletek(msg):
    bot.send_message(chat_id=msg.chat.id,text="please select akeyboar which you want to delete",reply_markup=inlinemarkup())
    #admin_state[msg.from_user.id]='removing_keyword'

#@bot.message_handler(commands=['keywords'],func=lambda m: m.chat.id in admin_state)
def mykewords(user_id):
    x=keywords()
    if not x:
        bot.send_message(chat_id=user_id,text="no keyboards")
        return 1
    te=''
    for j in range(0,len(x),3) :
        try:
            te += x[j]+"--" 
            te+=x[j+1]+ "--" 
            te+= x[j+2]+"\n"
        except:
            pass
    bot.send_message(chat_id=user_id ,text=te)

@bot.message_handler(func=lambda m:is_admin(m.from_user.id)  and admin_state[m.from_user.id]=='adding' and m.text[0] !='/')
def addKeyWord(msg):
    l=msg.text
    kes=[i.strip() for i in l.split('\n')]
    addkeyword(kes)
    admin_state[msg.from_user.id ]=False
    bot.send_message(chat_id=msg.chat.id,text="successfully added")
    admin_state[msg.from_user.id]=0



@bot.message_handler(chat_id=[-1001747735158],func=lambda m : True )
def any_msg(msg):
    check=keywords()
   
    te=[i.strip() for i in msg.text.split()]
   
    for j in te :
        if j in check:
            bot.delete_message(chat_id=-1001747735158,message_id=msg.message_id)
            break
    print(msg.text)



@bot.message_handler(commands=['start'])
def start(msg):
    
    if is_admin(msg.chat.id):
        bot.send_message(chat_id=msg.chat.id,text="wellcome",reply_markup=menub())
        admin_state[msg.chat.id]=0
    else:
         bot.send_message(chat_id=msg.chat.id,text="you should be admin of the group to access this bot")


@bot.callback_query_handler(func=lambda m : is_admin(m.from_user.id))
def deletekey(call):
    if 'p-' == call.data[:2]:
        b=int(call.data[2:])-12
        a=int(call.data[2:])-24
        bot.edit_message_reply_markup(chat_id=call.from_user.id,message_id=call.message.id,reply_markup=inlinemarkup(a,b))
    elif 'n-' == call.data[:2]:
         b=int(call.data[2:])+12
         a=int(call.data[2:])
         bot.edit_message_reply_markup(chat_id=call.from_user.id,message_id=call.message.id,reply_markup=inlinemarkup(a,b))
    elif call.data not in ['keywords','add_keywords','remove_keywords','back','next','prev']:
        if admin_state[call.from_user.id] == 'removing':
            deletekeyword(call.data)
            print(call.message.id)
            bot.answer_callback_query(call.id,call.data + " deleted",show_alert=True)
            bot.edit_message_reply_markup(chat_id=call.from_user.id,message_id=call.message.id,reply_markup=inlinemarkup())
            return 0
    elif call.data == 'keywords':
        bot.edit_message_reply_markup(chat_id=call.from_user.id,message_id=call.message.id,reply_markup=inlinemarkup())
        admin_state[call.from_user.id]=0
    elif call.data=='remove_keywords':
        bot.edit_message_reply_markup(chat_id=call.from_user.id,message_id=call.message.id,reply_markup=inlinemarkup())
        bot.send_message(chat_id=call.from_user.id,text='select to delete 👆')
        admin_state[call.from_user.id] = 'removing'
    elif call.data == 'add_keywords':
        bot.send_message(chat_id=call.from_user.id,text='OK Enter your keywords line by line')
        admin_state[call.from_user.id]='adding'
    elif call.data =='back':
        bot.edit_message_reply_markup(chat_id=call.from_user.id,message_id=call.message.id,reply_markup=menub())
        admin_state[call.from_user.id]=0
    elif call.data =='prev':
        bot.edit_message_reply_markup(chat_id=call.from_user.id,message_id=call.message.id,reply_markup=inlinemarkup(-1))

bot.add_custom_filter(custom_filters.ChatFilter())

bot.infinity_polling()

