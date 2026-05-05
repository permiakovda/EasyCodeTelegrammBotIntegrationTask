"""
функции обработки разных команд и сообщений для бота
"""

from telegram import Update
from telegram.ext import ContextTypes
from db import add_user, add_new_frend, is_user_exists, get_frends_list, delete_frend_from_db
from utils import validate_date, validate_only_letters, NotValidDate, NotValidName

# для обработки ошибок
import traceback
import logging


# Определяем функцию для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Получаем данные пользователя
    user = update.effective_user

    if is_user_exists(user_id=user.id):
        await update.message.reply_text(f'Ты уже зарегестрирован в системе!')
    else:
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
    # проверка наличия такого пользователя в БД
    if not(is_user_exists(user_id=update.effective_user.id)):
        await update.message.reply_text(f'Вас нет в системе, нажмите /start для начала')
        return None

    # Получаем данные пользователя
    user = update.effective_user
    
    # Получаем имя друга
    try:
        frend_name = validate_only_letters(update.message.text.split(' ')[1])
        frend_birthday = validate_date(update.message.text.split(' ')[2])

        await update.message.reply_text(f'получены данные о {frend_name} с датой {frend_birthday.day}.{frend_birthday.month}')
        add_new_frend(user_id=user.id, frend_name=frend_name, frend_birthday=frend_birthday)

    except NotValidDate as e:
        await update.message.reply_text('информация отправлена не по рекомендуемому формату')
    except NotValidName as e:
        await update.message.reply_text('такое имя не подойдет (спец символы, пробелы, числа не должны присутствовать)')



# Определяем функцию для обработки команды /frends_list
async def frends_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # проверка наличия такого пользователя в БД
    if not(is_user_exists(user_id=update.effective_user.id)):
        await update.message.reply_text(f'Вас нет в системе, нажмите /start для начала')
        return None

    # Получаем данные пользователя
    user = update.effective_user
    
    # Получаем информацию о друзьях
    frends_list = get_frends_list(user_id=user.id)
    frends_list_massage = ''

    for key, value in zip(frends_list.keys(), frends_list.values()):
        frends_list_massage += f"{key}: {value} \n"

    await update.message.reply_text(frends_list_massage)

# Определяем функцию для обработки команды /delete_frend
async def delete_frend(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # проверка наличия такого пользователя в БД
    if not(is_user_exists(user_id=update.effective_user.id)):
        await update.message.reply_text(f'Вас нет в системе, нажмите /start для начала')
        return None

    # Получаем данные пользователя
    user = update.effective_user
    #выполнить удаление пользователя по имени
    await update.message.reply_text(delete_frend_from_db(user_id=user.id, frend_name=validate_only_letters(update.message.text.split(' ')[1])))


# Определяем функцию для обработки команды /help
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Отправляем сообщение с инструкцией по использованию бота
    await update.message.reply_text('Чтобы добавить друга с датой рождения, отправьте команду /add_frend_birthday и имя друга, а затем дату в ' \
                                    'формате ДД/ММ/ГГГГ, например: "/add_frend_birthday Иван 29/03/2019". Что бы удалить друга напишите команду ' \
                                    '/delete_frend и через пробел укажите его имя, например "/delete_frend Иван". Что бы посмотреть список друзей ' \
                                    'используй команду /frends_list')


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

    print(error)

    # Опционально: уведомляем пользователя о внутренней ошибке
    if update and update.effective_message:
        await update.effective_message.reply_text(
            f"Извини, произошла внутренняя ошибка. {error}"
        )