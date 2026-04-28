"""
телеграмм бот для напоминая про ДР
"""

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Включаем логирование
logging.basicConfig(format='%(asctime)s — %(name)s — %(levelname)s — %(message)s', level=logging.INFO)

# Определяем функцию для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text( f'Привет, {update.effective_user.first_name}! Я твой первый бот. Напиши мне что-нибудь!'  )

# Определяем функцию для обработки текстовых сообщений
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

# Основная функция
def main():
    # Создаем приложение
    application = Application.builder().token('6272186177:AAHGVe3k5UNwVEyrkeqJhODOP-u6QsBWMqc').build()
    # Добавляем обработчики
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()