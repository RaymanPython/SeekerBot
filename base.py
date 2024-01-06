import sqlite3

# Подключаемся к базе данных
conn = sqlite3.connect('base.db')
cursor = conn.cursor()

# Добавляем столбец "city" в таблицу "users"
# cursor.execute("ALTER TABLE users ADD COLUMN city VARCHAR(255)")

# Заполняем столбец "city" значениями "все"
# cursor.execute("UPDATE users SET city = 'все'")
# conn.commit()
# Создаем триггер для автоматического заполнения столбца "city" при вставке новых записей
# Удаляем столбец "city" из таблицы "users"
# cursor.execute("ALTER TABLE users DROP COLUMN city")
# Изменяем таблицу и задаем автоматическое значение "все" для столбца "city"
cursor.execute("ALTER TABLE users ADD COLUMN city VARCHAR(255) DEFAULT 'все'")

# Сохраняем изменения и закрываем соединение с базой данных
conn.commit()
conn.close()
