import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()
# Подключение к базе данных
conn = sqlite3.connect(os.getenv('DATABASE_NAME'))

# Создание таблицы
cur = conn.cursor()
# Добавление нового столбца is_registered с типом данных BOOL и значением по умолчанию false
cur.execute("ALTER TABLE users ADD COLUMN index_user INTEGER DEFAULT 0")
conn.commit()

# Закрытие соединения
cur.close()
conn.close()
