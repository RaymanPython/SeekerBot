# обрааботчики команд бота
import logging

from aiogram import Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor

import debug
import defs
import keyboards
from basedata import start_base, register_name, register_tg_link, register_about, register_tg_bio, register_photos_ids, \
    get_user_data, user_start, search_in_basedata, sleep_update, register_gender, register_city
from config import bot
from keyboards import inlinekeyboardgo, inlinekeyboardlikes, keboardgender
import texts

storage = MemoryStorage()
dp = Dispatcher(
    bot=bot,
    storage=storage
                )
# dp.middleware.setup(LoggingMiddleware())
logging.basicConfig(level=logging.ERROR)


async def on_error(event, exception):
    # Выводите ошибку в логи или куда-либо еще
    logging.error(f'Error: {event} {exception}')
    print("_____________________________________________________________")


dp.register_errors_handler(on_error)


@dp.errors_handler()
async def errors_handler(update, exception):
    # Выводим информацию об ошибке в консоль
    print(f"Произошла ошибка: {exception}")
    return True


# Класс хранения состояний
class ClientStorage(StatesGroup):
    start = State()
    name = State()
    gender = State()
    get_city = State()
    get_city_prov = State()
    about = State()
    photos = State()
    photos_add = State()
    register_name = State()
    register_about = State()
    register_photos = State()


def media_photo_id(photo_ids):
    media = [types.InputMediaPhoto(media=photo_ids[i], caption=f"Photo {i}") for i in range(len(photo_ids))]
    return media


async def send_media(chat_id, user_data):
    if len(user_data.photo_ids) <= 1:
        await bot.send_photo(chat_id, user_data.photo_ids[0], caption="Единственная фотография")
    else:
        await bot.send_media_group(chat_id, media=media_photo_id(user_data.photo_ids))


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message) -> None:
    debug.debug()
    await ClientStorage.start.set()
    await ClientStorage.next()
    await message.answer("Заполните вашу анкету. Как вас зовут?")
    await user_start(message.from_user.id)


# Обработчик ответа на имя
@dp.message_handler(state=ClientStorage.name)
async def text_name_answer(message: types.Message, state: ClientStorage) -> None:
    debug.debug()
    if await state.get_state() == "ClientStorage:name":
        user_id = message.from_user.id
        name = message.text
        # Записываем имя пользователя в базу данных
        # cursor = conn.cursor()
        await register_name(user_id, name)
        await register_tg_link(user_id, message.from_user.username)
        await ClientStorage.next()
        gender = await defs.check_gender(name) 
        if gender == 2:
            await message.answer(f"Спасибо {name} Вы заполнили! Теперь расскажите пожалуйста какой Ваш пол", reply_markup=keboardgender)
        else:
            await ClientStorage.next()
            await register_gender(user_id, gender)
            await message.answer(f"Спасибо {name} Вы заполнили! Теперь расскажите пожалуйста о том в каком городе Вы ищете людей?")


# Обработчик ответа на пол
@dp.message_handler(state=ClientStorage.gender)
async def gender_answer(message: types.Message, state: ClientStorage) -> None:
    debug.debug()
    user_id = message.from_user.id
    text = message.text.lower()
    if text == "я парень":
        gender = 1
    elif text == "я девушка":
        gender = 0
    else:
        await message.answer("Введите пожалуйста корректное имя пола", reply_markup=keboardgender)
        return
    await register_gender(user_id, gender)
    await ClientStorage.next()
    await message.answer("Спасибо Вы заполнили свой пол! Теперь расскажите пожалуйста о том в каком городе Вы ищете людей?", 
                         reply_markup=keyboards.keboardcity)


# Обработчик ответа на город
@dp.message_handler(state=ClientStorage.get_city)
async def get_city(message: types.Message, state: ClientStorage) -> None:
    debug.debug()
    user_id = message.from_user.id
    text = message.text.lower()
    if text == "ищу в любом городе":
        city = text
    else:
        city = defs.get_name_city(text)
        if city is None:
            await message.answer("Введите корректный город", 
                         reply_markup=keyboards.keboardcity)
            return 
        await register_city(user_id, city)
    await ClientStorage.next()
    await message.answer(f"Ваш город {city}?", 
                         reply_markup=keyboards.keboardbool)


# Обработчик ответа на город проверка
@dp.message_handler(state=ClientStorage.get_city_prov)
async def get_city_prov(message: types.Message, state: ClientStorage) -> None:
    debug.debug()
    user_id = message.from_user.id
    text = message.text.lower()
    if text == "да":
        await ClientStorage.next()
        await message.answer("Спасибо Вы заполнили! Теперь расскажите пожалуйста о том кого Вы хотите найти и о себе", 
                         reply_markup=keyboards.none_keyboard)
    else:
        await ClientStorage.get_city.set()
        await message.answer("Введите правилный город", 
                         reply_markup=keyboards.keboardcity)


# Обработчик ответа на описание
@dp.message_handler(state=ClientStorage.about)
async def text_about_answer(message: types.Message, state: ClientStorage) -> None:
    debug.debug()
    if await state.get_state() == "ClientStorage:about":
        user_id = message.from_user.id
        about_text = message.text
        # Записываем имя пользователя в базу данных
        # cursor = conn.cursor()
        await register_about(user_id, about_text)
        await register_tg_link(user_id, message.from_user.username)
        await register_tg_bio(user_id, "")
        await ClientStorage.next()
        await message.answer("Спасибо Вы заполнили! Теперь скиньте от 1 до 5 фотографий, которые помогут понять людям больше о Вас, можете скинуть одну фотографию или альбом")


@dp.message_handler(content_types=['photo'], state=ClientStorage.photos)
async def photos_answer(message: types.Message, state: ClientStorage) -> None:
    debug.debug()
    user_id = message.from_user.id
    # Получение идентификаторов фотографий из сообщения
    photo_ids_ = [list(set([photo.file_id for photo in message.photo]))[0]]
    if len(photo_ids_) == 0:
        await message.answer("Отправьте хотя бы одну фотографию")
    else:
        # Записываем имя пользователя в базу данных
        # cursor = conn.cursor()
        # count_photo - сколько мы сохраняли фотографий
        # limit_photo сколько осталось досутпных фотографий
        # lenphoto - количество фотографий которые пользователь хотел сохранить
        count_photo, limit_photo, lenphoto = await register_photos_ids(user_id, photo_ids_, True)
        # await register_tg_link(user_id, message.from_user.username)
        if limit_photo == 0:
            await state.finish()
            if count_photo == lenphoto:
                await message.answer("Спасибо Вы заполнили Вашу анкету! Лимит фотографий закончился для анкеты.\n Теперь Вы закончили заполнение анкеты и готовы познать полный функционал бота!")
            else:
                await message.answer(f"Спасибо Вы заполнили Вашу анкету! Лимит фотографий закончился, поэтому мы смогли сохранить только первые {count_photo} из {lenphoto} которые Вы отправили.\n Теперь Вы закончили заполнение анкеты и готовы познать полный функционал бота!")
        else:
            await ClientStorage.next()
            await message.answer(f"Спасибо мы сохранили Выши фотографии в базу данных, Вы можете добавить ещё не более чем {limit_photo} фотографий в анкеты или завершить заполнение", reply_markup=inlinekeyboardgo())            
        # await message.answer(message)
       

@dp.message_handler(content_types=['photo'], state=ClientStorage.photos_add)
async def photos_add_answer(message: types.Message, state: ClientStorage) -> None:
    debug.debug()
    user_id = message.from_user.id
    # Получение идентификаторов фотографий из сообщения
    photo_ids_ = [list(set([photo.file_id for photo in message.photo]))[0]]
    if len(photo_ids_) == 0:
        await message.answer("Отправьте хотя бы одну фотографию")
    else:
        # Записываем имя пользователя в базу данных
        # cursor = conn.cursor()
        # count_photo - сколько мы сохраняли фотографий
        # limit_photo сколько осталось досутпных фотографий
        # lenphoto - количество фотографий которые пользователь хотел сохранить
        count_photo, limit_photo, lenphoto = await register_photos_ids(user_id, photo_ids_, False)
        if limit_photo == 0:
            await state.finish()
            if count_photo == lenphoto:
                await message.answer("Спасибо Вы заполнили Вашу анкету! Лимит фотографий закончился для анкеты.\n Теперь Вы закончили заполнение анкеты и готовы познать полный функционал бота!")
            else:
                await message.answer(f"Спасибо Вы заполнили Вашу анкету! Лимит фотографий закончился, поэтому мы смогли сохранить только первые {count_photo} из {lenphoto} которые Вы отправили.\nТеперь Вы закончили заполнение анкеты и готовы познать полный функционал бота!")
        else:
            # await ClientStorage.next()
            await message.answer(f"Спасибо мы сохранили Выши фотографии в базу данных, Вы можете добавить ещё не более чем {limit_photo} фотографий в анкеты или заавершить заполнение", reply_markup=inlinekeyboardgo())

            
# обработка /search поиска анкеты ------
@dp.message_handler(commands=['search'])
async def search(message: types.Message) -> None:
    debug.debug()
    user_id = message.chat.id
    user_find = await search_in_basedata(user_id)
    if user_find is None:
        await message.answer("Никого больше нет, можете подождать хотя бы 24 минуты")
        await sleep_update(user_id)
        return 
    data = await get_user_data(user_find)
    await send_media(message.chat.id, data)
    await message.answer("Нашёл анкету:\n" + defs.string_about_user(data), reply_markup=inlinekeyboardlikes(user_find))


async def ankets_show1(chat_id_first, chat_id_second):
    user_data = await get_user_data(chat_id_first)
    await send_media(chat_id_second, user_data)
    await bot.send_message(chat_id_second, "Вас  лайкнул\n" + defs.string_about_user(user_data),
                           reply_markup=keyboards.inlinekeyboardlikes1(chat_id_first))


async def ankets_show2(chat_id_first, chat_id_second):
    user_data = await get_user_data(chat_id_first)
    await send_media(chat_id_second, user_data)
    await bot.send_message(chat_id_second, "Взаимный лайк\n" + defs.string_about_user(user_data),
                           reply_markup=keyboards.inlinekeyboardlink(user_data.tglink))


@dp.callback_query_handler(lambda c: c.data == 'go', state=ClientStorage.photos_add)
async def callbake_go(callback_data: types.CallbackQuery, state ):
    await state.finish()
    await callback_data.message.answer(text="Вы зраегистрировали анкету!", reply_markup=keyboards.comands)
    await bot.edit_message_reply_markup(callback_data.message.chat.id, callback_data.message.message_id,
                                         reply_markup=keyboards.none_keyboard)


@dp.callback_query_handler()
async def vote_callbake(callback: types.CallbackQuery) -> None: 
    debug.debug()
    if callback.data not in ["my", "search", "help"]:
        await bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id, reply_markup=keyboards.none_keyboard)
    if callback.data.startswith("like"):
        await callback.answer(text="Ура! Бот отправил лайк")
        await ankets_show1(callback.message.chat.id, int(callback.data.split("_")[1]))
        await search(callback.message)
    if callback.data.startswith("like1"):
        await callback.answer(text="Ура! Бот отправил лайк")
        await ankets_show2(callback.message.chat.id, int(callback.data.split("_")[1]))
        await ankets_show2(int(callback.data.split("_")[1]), callback.message.chat.id)
    elif callback.data.startswith("dislike"):
        await callback.answer(text="Жаль! Ищем дальше)")
        await search(callback.message)
    elif callback.data.startswith("dislike1"):
        await callback.answer(text="Жаль! Извините за беспокойство)")
    elif callback.data == "my":
        await my(callback.message)
    elif callback.data == "search":
        await search(callback.message)
    elif callback.data == "help":
        await help_command(callback.message)
    

# обработка /search поиска анкеты 
@dp.message_handler(commands=['my'])
async def my(message: types.Message) -> None:
    debug.debug()
    data = await get_user_data(message.chat.id)
    await send_media(message.chat.id, data)
    await message.answer(defs.string_about_user(data))


# Обработка команды /help
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply(texts.HELP_START, parse_mode=types.ParseMode.HTML)


# обработка /search поиска анкеты ------
@dp.message_handler(commands=['updates'])
async def updates(message: types.Message) -> None:
    debug.debug()
    # Получение списка обновлений
    updates = await bot.get_updates() 
    for i in updates:
        print(i)


async def on_startup(_) -> None:
    from config import BOT_TOKEN, DATABASE_NAME, DEBUG
    debug.debug()
    start_base()
    print(f"    токен бота: {BOT_TOKEN}")
    print(f"    путь к базе данных: {DATABASE_NAME}")
    print(f"    тип запуска дебаг/не дебаг: {DEBUG}")
    print("-----------------------------------------------------------------------------------------------")


if __name__ == '__main__':
    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
        on_startup=on_startup
        )
    dp.register_callback_query_handler(callbake_go, text="go")
