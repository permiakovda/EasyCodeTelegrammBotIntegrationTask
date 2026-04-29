"""
телеграмм бот для напоминая про ДР
"""

# importing os module for environment variables
import os
# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values 
import logging
# importing necessary functions from telegram library
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


# Импортируем функции работы с БД
from db import init_db, add_user

# импорт модуля для обработки команд и сообщений
# from handlers import unknown

# loading variables from .env file
load_dotenv() 

# accessing and printing value
TOKEN = os.getenv("BOT_TOKEN")

# Включаем логирование
logging.basicConfig(format='%(asctime)s — %(name)s — %(levelname)s — %(message)s', level=logging.INFO)

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
        last_name=user.last_name
    )
    
    # Отправляем приветственное сообщение
    await update.message.reply_text(f'Привет, {user.first_name}! Я твой бот. Ты успешно зарегистрирован!')

# Определяем функцию для обработки текстовых сообщений
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'такой команды нет')
    

# Основная функция
def main():
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()
    # Добавляем обработчики
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Добавляем обработчик для неизвестных команд
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()