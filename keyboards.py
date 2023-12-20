from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, KeyboardButtonPollType


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


inlinekeyboardgo = InlineKeyboardMarkup(row_width=2)
inlinekeyboardgo .add(
                InlineKeyboardButton(text="дальше", callback_data="go"), 
                )


inlinekeyboardsearch = InlineKeyboardMarkup(row_width=2)
inlinekeyboardsearch .add(
                InlineKeyboardButton(text="дальше", callback_data="go"), 
                )
keboardgender = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) # default - False
button1 = KeyboardButton('Я парень')
button2 = KeyboardButton('Я девушка')
keboardgender.add(button1).insert(button2)

none_keyboard = InlineKeyboardMarkup()
