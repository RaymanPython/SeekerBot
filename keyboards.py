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


inlinekeyboardsearch = InlineKeyboardMarkup(row_width=2)
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

none_keyboard = InlineKeyboardMarkup()
