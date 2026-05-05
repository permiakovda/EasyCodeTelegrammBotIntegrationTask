import sqlite3
import json

from utils import NameAlreadyExists

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


def add_user(user_id, username, first_name, last_name):
    """
    Добавляет нового пользователя в базу данных.
    Если пользователь с таким user_id уже существует, обновляет его данные.
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    # Создаем пустой JSON объект для будущего хранения дней рождений друзей
    empty_json_obj = json.dumps({})  # "{}"
    
    # Используем INSERT OR REPLACE для обновления данных, если пользователь уже существует
    cursor.execute('''
    INSERT OR REPLACE INTO users (user_id, username, first_name, last_name, frends_birthdays)
    VALUES (?, ?, ?, ?, ?)
    ''', (user_id, username, first_name, last_name, empty_json_obj))
    
    conn.commit()
    conn.close()


def is_user_exists(user_id):
    """
    проверка на существование пользователя в БД
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT 1 FROM users WHERE user_id = ? LIMIT 1", (user_id,))
        return cursor.fetchone() is not None
    except Exception as e:
        print(f"Ошибка при проверке пользователя: {e}")
        return False
    finally:
        conn.close()



def add_new_frend(user_id, frend_name, frend_birthday):
    """
    добавляем в бд информацию по новому другу и его ДР, если такого друга ещё нету в БД
    """
    try:
        # Определяем путь к базе данных
        db_path = "users.db"
        
        # Создаем подключение к базе данных
        conn = sqlite3.connect(db_path, check_same_thread=False)
        cursor = conn.cursor()

        # получить инфу о существующих друзьях и их д.р.
        cursor.execute("SELECT frends_birthdays FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        
        if result and result[0]:
            # Предполагаем, что frends_birthdays хранится как JSON-строка
            frends_birthdays = json.loads(result[0])
            if frends_birthdays.get(frend_name) is not None:
                raise NameAlreadyExists(frend_name)
        else:
            print('пусто')   # Пустой список, если нет записей
        

        # Внедрить информацию о новом друге
        profile = {f"{frend_name}": f"{frend_birthday}"} 
        cursor.execute("UPDATE users SET frends_birthdays = json_patch(frends_birthdays, ?) WHERE user_id = ?", (json.dumps(profile, ensure_ascii=False), user_id))
        conn.commit()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Соединение с SQLite закрыто")


def get_frends_list(user_id):
     # Определяем путь к базе данных
        db_path = "users.db"
        
        # Создаем подключение к базе данных
        conn = sqlite3.connect(db_path, check_same_thread=False)
        cursor = conn.cursor()

        # получить инфу о существующих друзьях и их д.р.
        cursor.execute("SELECT frends_birthdays FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        
        if result and result[0]:
            # Предполагаем, что frends_birthdays хранится как JSON-строка
            frends_birthdays = json.loads(result[0])
            return frends_birthdays
        else:
            return None