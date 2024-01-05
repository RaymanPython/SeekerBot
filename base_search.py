# функции для поиска по определённым алгоритмам 


import asyncio
from sqlalchemy import create_engine, select, and_
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import selectinload, sessionmaker
from sqlalchemy.orm.query import Query
from sqlalchemy.future import select as async_select
from models import User  # Здесь предполагается, что у вас есть модель User

async def find_similar_users(id_user, k):
    # Создаем асинхронный движок для работы с базой данных SQLite
    engine = create_async_engine("sqlite+aiosqlite:///database.db")

    # Создаем асинхронную сессию для работы с базой данных
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    # Создаем асинхронное соединение и получаем асинхронную сессию
    async with async_session() as session:
        # Выполняем асинхронный запрос для получения описания пользователя id_user
        user_about = await session.execute(async_select(User.about).where(User.id == id_user))
        about = user_about.scalar()

        # Выполняем асинхронный запрос для получения ID пользователей с наиболее схожими описаниями
        query = session.query(User.id).filter(and_(User.id != id_user, User.about.like(f"%{about}%")))
        query = query.limit(k)
        similar_users = await session.execute(query)

        # Извлекаем и возвращаем ID пользователей
        return [user_id for user_id, in similar_users.all()]

# Пример использования функции
async def main():
    id_user = 1  # ID пользователя, для которого нужно найти похожих пользователей
    k = 5  # Количество пользователей, которых нужно вернуть

    similar_users = await find_similar_users(id_user, k)
    print(f"ID похожих пользователей: {similar_users}")

asyncio.run(main())
