from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


def inlinekeyboardlikes(user_id):
    inlinekeyboardlikes = InlineKeyboardMarkup(row_width=2)
    inlinekeyboardlikes.add(
        InlineKeyboardButton(text="🤝", callback_data=f"like_{user_id}"), 
        InlineKeyboardButton(text="👎 ", callback_data=f"dislike_{user_id}")
    )
    return inlinekeyboardlikes


def inlinekeyboardlikes1(user_id):
    inlinekeyboardlikes = InlineKeyboardMarkup(row_width=2)
    inlinekeyboardlikes.add(
        InlineKeyboardButton(text="🤝", callback_data=f"like1_{user_id}"), 
        InlineKeyboardButton(text="👎 ", callback_data=f"dislike1_{user_id}")
    )
    return inlinekeyboardlikes


def inlinekeyboardlink(link):
    keyboard = InlineKeyboardMarkup()
    url_button = InlineKeyboardButton(text="Click me", url=link)
    keyboard.add(url_button)
    return keyboard


def inlinekeyboardgo():
    inlinekeyboardgo = InlineKeyboardMarkup(row_width=1)
    inlinekeyboardgo .add(
                InlineKeyboardButton(text="дальше", callback_data="go"), 
                )
    return inlinekeyboardgo


inlinekeyboardsearch = InlineKeyboardMarkup(row_width=1)
inlinekeyboardsearch .add(
                InlineKeyboardButton(text="дальше", callback_data="go"), 
                )

keboardgender = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) # default - False
button1 = KeyboardButton('Я парень')
button2 = KeyboardButton('Я девушка')
keboardgender.add(button1).insert(button2)

comands = InlineKeyboardMarkup()
buttonc1 = InlineKeyboardButton(text="Моя анкета", callback_data="my")    
buttonc2 = InlineKeyboardButton(text="Хочу найти человека", callback_data="search")  
buttonc3 = InlineKeyboardButton(text="Инструкция", callback_data="help")        
comands.add(buttonc1).add(buttonc2).add(buttonc3)

keboardcity = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) # default - False
buttoncity = KeyboardButton('Ищу в любом городе')
keboardcity.add(buttoncity)

keboardbool = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) # default - False
buttonbool1 = KeyboardButton('Да')
buttonbool2 = KeyboardButton('Нет')
keboardbool.add(buttonbool1).insert(buttonbool2)


keboardmain = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False) # default - False
buttonmain1 = KeyboardButton('🔎', request_contact=False, request_location=False,
                                  request_poll=None, request=True, url=None, switch_inline_query=None,
                                  switch_inline_query_current_chat=None, callback_data=None)
buttonmain1.request = "/search"
buttonmain2 = KeyboardButton('📝', request_contact=False, request_location=False,
                                  request_poll=None, request=True, url=None, switch_inline_query=None,
                                  switch_inline_query_current_chat=None, callback_data=None)
buttonmain2.request = "/my"
buttonmain3 = KeyboardButton('🆘', request_contact=False, request_location=False,
                                  request_poll=None, request=True, url=None, switch_inline_query=None,
                                  switch_inline_query_current_chat=None, callback_data=None)
buttonmain3.request = "/help"

keboardmain.add(buttonmain1).insert(buttonmain2).insert(buttonmain3)

none_keyboard = InlineKeyboardMarkup()
