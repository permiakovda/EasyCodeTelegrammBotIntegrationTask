import sqlite3
import os

def init_db():
    """
    Инициализирует базу данных, создает таблицу users, если она не существует.
    """
    # Определяем путь к базе данных
    db_path = "users.db"
    
    # Создаем подключение к базе данных (файл создастся автоматически, если его нет)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Создаем таблицу users, если она еще не существует
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE NOT NULL,
        username TEXT,
        first_name TEXT,
        last_name TEXT,
        frends_birthdays TEXT DEFAULT NULL
    )
    ''')
    
    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()
    
    print(f"База данных инициализирована: {db_path}")


def add_user(user_id, username, first_name, last_name):
    """
    Добавляет нового пользователя в базу данных.
    Если пользователь с таким user_id уже существует, обновляет его данные.
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    # Используем INSERT OR REPLACE для обновления данных, если пользователь уже существует
    cursor.execute('''
    INSERT OR REPLACE INTO users (user_id, username, first_name, last_name)
    VALUES (?, ?, ?, ?)
    ''', (user_id, username, first_name, last_name))
    
    conn.commit()
    conn.close()
    
    print(f"Пользователь {first_name} добавлен/обновлен в базе данных.")


def get_user(user_id):
    """
    Получает данные пользователя по его user_id.
    Возвращает словарь с данными или None, если пользователь не найден.
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    
    conn.close()
    
    if row:
        return {
            'id': row[0],
            'user_id': row[1],
            'username': row[2],
            'first_name': row[3],
            'last_name': row[4],
            'frends_birthdays': row[5]
        }
    return None

def add_new_frend(user_id, frend_name, frend_birthday):
    """
    добавляем в бд информацию по новому другу и его ДР, если такого друга ещё нету в БД
    """
    try:
        # Определяем путь к базе данных
        db_path = "users.db"
        
        # Создаем подключение к базе данных
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # получить инфу о существующих друзьях и их д.р.


        # обновить данные нужного ползователя
        sql = f"UPDATE users SET frends_birthdays = ? WHERE user_id = ?"
        cursor.execute(sql, (frend_birthday, user_id))

        try:
            cursor.execute("SELECT frends_birthdays FROM users WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()
        
            if result and result[0]:
                # Предполагаем, что frends_birthdays хранится как JSON-строка
                print(result[0])
            else:
                print('пусто')   # Пустой список, если нет записей
        except Exception as e:
            print(f"Ошибка при чтении данных: {e}")
        finally:
            conn.close()

        # conn.commit()
        # cursor.close()
        # conn.close()


    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if conn:
            conn.close()
            print("Соединение с SQLite закрыто")

