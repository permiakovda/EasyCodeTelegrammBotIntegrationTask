"""
функции обработки разных команд и сообщений для бота
"""

from telegram import Update
from telegram.ext import ContextTypes
from db import init_db, add_user




# Определяем функцию для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

# Определяем функцию для обработки неизвестных команд
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'такой команды нет')

# Определяем функцию для обработки команды /add_frend_birthday
async def add_frend_birthday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Получаем данные пользователя
    user = update.effective_user
    
    # Получаем имя друга
    frend_name = update.message.text.split(' ')[1]
    frend_birthday = update.message.text.split(' ')[2]

    print(f'новый дргу ${frend_name} с датой рождения {frend_birthday} у пользователя {user.username} ' )

# Определяем функцию для обработки команды /help
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Отправляем сообщение с инструкцией по использованию бота
    await update.message.reply_text('Чтобы добавить друга с датой рождения, отправьте команду /add_frend_birthday и имя друга, а затем дату в формате ДД.ММ.ГГГГ')