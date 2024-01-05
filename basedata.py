import asyncio
import sqlite3
import aiosqlite
from config import DATABASE_NAME, PHOTO_LIMIT, DEBUG


class User_data:

    def __init__(self, name, about, photo_ids, tglink):
        self.name = name
        self.about = about
        self.photo_ids = photo_ids.split()
        self.tglink = tglink


async def user_start(user_id):
    async with aiosqlite.connect(DATABASE_NAME) as db:
        flag = await db.execute(f"SELECT 1 FROM users WHERE user_id = {str(user_id)}")
        await db.commit()
    if flag == 1:
        return True
    else:
        async with aiosqlite.connect(DATABASE_NAME) as db:
            await db.execute(f"INSERT INTO users (user_id) VALUES ({str(user_id)})")
            await db.commit()
            return True


async def register_value(name_value, user_id, field_value):
    async with aiosqlite.connect(DATABASE_NAME) as db:
        user_id = str(user_id)
        await db.execute(f"UPDATE users SET {name_value}=? WHERE user_id=?", (field_value, user_id))
        await db.commit()
        return True


async def register_name(user_id, name):
    await register_value("name", user_id, name)
    return True


async def register_tg_link(user_id, tglink):
    await register_value("tglink", user_id, "https://t.me/" + str(tglink))
    return True


async def register_tg_bio(user_id, about):
    await register_value("tg_bio", user_id, about)
    return True


async def register_about(user_id, tgbio):
    await register_value("about", user_id, tgbio)
    return True


async def register_gender(user_id, gender):
    await register_value("gender", user_id, gender)
    await register_value("search_gender", user_id, 1 - gender)
    return True


async def register_photos_ids(user_id, photo_ids, new_flag=True):
    try:
        photo_ids = list(set(photo_ids))
        for i in photo_ids:
            print(i, type(i))
        async with aiosqlite.connect(DATABASE_NAME) as db:
            count_photo = len([photo_ids])
        if new_flag:
            async with aiosqlite.connect(DATABASE_NAME) as db:
                # если поьзователь заново решается, то нам нужно очистиь поле 
                await db.execute("UPDATE users SET photo_ids = ? WHERE user_id = ?", ('', user_id))
                await db.commit()
                naw_len = 0
        else:
            async with aiosqlite.connect(DATABASE_NAME) as db:
                cursor = await db.execute('SELECT photo_ids FROM users WHERE user_id = ?', (user_id,))
                cf = await cursor.fetchone()
                naw_len = len(cf[0].split())
        count_photo = 0
        for i in range(len(photo_ids)):
            async with aiosqlite.connect(DATABASE_NAME) as db:
                if naw_len + count_photo >= PHOTO_LIMIT:
                    break
                await db.execute("UPDATE users SET photo_ids = photo_ids || ? WHERE user_id = ?", (' ' + photo_ids[i], user_id))
                await db.commit()
                count_photo += 1
        return (count_photo, max(PHOTO_LIMIT - naw_len - count_photo, 0), count_photo)
    except Exception as e:
        print(e)


def start_base():
    global conn, sursor
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    # Создаем таблицу, если она еще не существует
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        name TEXT,
        about TEXT,
        tg_bio TEXT,
        tglink TEXT,
        gender INTEGER,
        search_gender INTEGER,
        is_registered BOOL DEFAULT false,
        photo_ids TEXT DEFAULT '',
        index_ankket INTEGER DEFAULT 0                   
        )
    ''')
    conn.commit()
    return True


async def get_user_data(user_id):
    async with aiosqlite.connect(DATABASE_NAME) as db:
        cursor = await db.execute(f'SELECT name, about, photo_ids, tglink FROM users WHERE user_id = {str(user_id)}')
        user_data = await cursor.fetchone()
        return User_data(user_data[0], user_data[1], user_data[2], user_data[3])
    

async def sleep_update(user_id):
    if DEBUG:
        await asyncio.sleep(50)
    else:
        await asyncio.sleep(24 * 60)
    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute("UPDATE users SET index_ankket = ? WHERE user_id = ?", ("0", str(user_id)))
        await db.commit()

    
async def search_in_basedata(user_id):
    user_id = str(user_id)
    async with aiosqlite.connect(DATABASE_NAME) as db:
        cursor = await db.execute(f'SELECT index_ankket FROM users WHERE user_id={user_id}')
        k = await cursor.fetchone()
    k = k[0] + 1
    async with aiosqlite.connect(DATABASE_NAME) as db:
        cursor = await db.execute('SELECT user_id FROM users WHERE user_id != ? AND photo_ids != "" LIMIT ?', (user_id, str(k)))
        user_data = await cursor.fetchall()
    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute("UPDATE users SET index_ankket = ? WHERE user_id = ?", (str(k), user_id))
        await db.commit()
    if len(user_data) >= k:
        return user_data[-1][0]
    # await sleep_update(user_id)
    return None
        
    
async def main():
    return


if __name__ == "__main__":
    pass