"""
функции обработки разных команд и сообщений для бота
"""

from telegram import Update
from telegram.ext import ContextTypes
from db import init_db, add_user
from utils import validate_date

# для обработки ошибок
import traceback
import logging


# Определяем функцию для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Инициализируем базу данных
    init_db()
    
    # Получаем данные пользователя
    user = update.effective_user
    
    # Добавляем пользователя в базу данных
    add_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
    )
    
    # Отправляем приветственное сообщение
    await update.message.reply_text(f'Привет, {user.first_name}! Я твой бот. Ты успешно зарегистрирован!')

# Определяем функцию для обработки текстовых сообщений
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)

# Определяем функцию для обработки неизвестных команд
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'такой команды нет')

# Определяем функцию для обработки команды /add_frend_birthday
async def add_frend_birthday(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Получаем данные пользователя
    user = update.effective_user
    
    # Получаем имя друга
    try:
        frend_name = update.message.text.split(' ')[1]
        frend_birthday = validate_date(update.message.text.split(' ')[2])

        await update.message.reply_text(f'получены данные о {frend_name} с датой {frend_birthday.day}.{frend_birthday.month}')


    except:
        await update.message.reply_text('информация отправлена не по рекомендуемому формату')



# Определяем функцию для обработки команды /help
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Отправляем сообщение с инструкцией по использованию бота
    await update.message.reply_text('Чтобы добавить друга с датой рождения, отправьте команду /add_frend_birthday и имя друга, а затем дату в формате ДД/ММ/ГГГГ, например: "/add_frend_birthday Иван 29/03/2019"')


# Функция-обработчик ошибок
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Функция для обработки исключений в Telegram-боте.
    """
    # Получаем ошибку
    error = context.error

    # Логируем ошибку с подробностями
    logging.error(
        msg="Exception while handling an update:",
        exc_info=(type(error), error, error.__traceback__)
    )

    # Для отладки: выводим traceback в консоль
    traceback.print_exception(type(error), error, error.__traceback__)

    # Опционально: уведомляем пользователя о внутренней ошибке
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "Извини, произошла внутренняя ошибка. Разработчик уже уведомлён."
        )