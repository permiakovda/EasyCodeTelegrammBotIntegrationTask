"""
телеграмм бот для напоминая про ДР
"""

# importing os module for environment variables
import os
# importing necessary functions from dotenv library
from dotenv import load_dotenv
# импорт библиотеки для логирования ошибок и сообщений
import logging
# importing necessary functions from telegram library
from telegram.ext import Application, CommandHandler, MessageHandler, filters
# импорт модуля для обработки команд и сообщений
from handlers import unknown, start, echo, add_frend_birthday, help, error, frends_list, delete_frend

# loading variables from .env file
load_dotenv() 
# accessing and printing value
TOKEN = os.getenv("BOT_TOKEN")

# Включаем логирование
logging.basicConfig(format='%(asctime)s — %(name)s — %(levelname)s — %(message)s', level=logging.INFO)

# Основная функция
def main():
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()
    # Добавляем обработчики
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help))
    application.add_handler(CommandHandler('add_frend_birthday', add_frend_birthday))
    application.add_handler(CommandHandler('frends_list', frends_list))
    application.add_handler(CommandHandler('delete_frend', delete_frend))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Добавляем обработчик для неизвестных команд
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    # Добавляем обработчик ошибок
    application.add_error_handler(error)

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()