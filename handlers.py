"""
функции обработки разных команд и сообщений для бота
"""

from telegram import Update
from telegram.ext import ContextTypes
from db import init_db, add_user

# для обработки ошибок
from telegram.constants import ParseMode
from telegram.helpers import mention_html
import sys
import traceback
import html
import json
import logging
import traceback


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
    await update.message.reply_text('Чтобы добавить друга с датой рождения, отправьте команду /add_frend_birthday и имя друга, а затем дату в формате ДД/ММ/ГГГГ, например: "/add_frend_birthday Иван 29/03/2019"')



# это общая функция обработчика ошибок. 
# Если нужна дополнительная информация о конкретном типе сообщения, 
# добавьте ее в полезную нагрузку в соответствующем предложении `if ...`
# def error(update, context):
#     # добавьте все идентификаторы разработчиков в этот список. 
#     # Можно добавить идентификаторы каналов или групп.
#     devs = [208589966]
#    # Уведомление пользователя об этой проблеме. 
#    # Уведомления будут работать, только если сообщение НЕ является 
#    # обратным вызовом, встроенным запросом или обновлением опроса. 
#    # В случае, если это необходимо, то имейте в виду, что отправка 
#    # сообщения может потерпеть неудачу
#     if update.effective_message:
#         text = "К сожалению произошла ошибка в момент обработки сообщения. " \
#                "Мы уже работаем над этой проблемой."
#         update.effective_message.reply_text(text)
#     # Трассировка создается из `sys.exc_info`, которая возвращается в  
#     # как третье значение возвращаемого кортежа. Затем используется  
#     # `traceback.format_tb`, для получения `traceback` в виде строки.
#     trace = "".join(traceback.format_tb(sys.exc_info()[2]))
#     # попробуем получить как можно больше информации из обновления telegram
#     payload = []
#     # обычно всегда есть пользователь. Если нет, то это 
#     # либо канал, либо обновление опроса.
#     if update.effective_user:
#         bad_user = mention_html(update.effective_user.id, update.effective_user.first_name)
#         payload.append(f' с пользователем {bad_user}')
#     # есть ситуаций, когда что то с чатом
#     if update.effective_chat:
#         payload.append(f' внутри чата <i>{update.effective_chat.title}</i>')
#         if update.effective_chat.username:
#             payload.append(f' (@{update.effective_chat.username})')
#     # полезная нагрузка - опрос
#     if update.poll:
#         payload.append(f' с id опроса {update.poll.id}.')
#     # Поместим это в 'хорошо' отформатированный текст
#     text = f"Ошибка <code>{context.error}</code> случилась{''.join(payload)}. " \
#            f"Полная трассировка:\n\n<code>{trace}</code>"
#     # и отправляем все разработчикам
#     for dev_id in devs:
#         context.bot.send_message(dev_id, text, parse_mode=ParseMode.HTML)
#     # Необходимо снова вызывать ошибку, для того, чтобы модуль `logger` ее записал.
#     # Если вы не используете этот модуль, то самое время задуматься.
#     raise




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