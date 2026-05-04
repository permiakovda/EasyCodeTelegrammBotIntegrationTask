"""
дополнительные функции для валидации и т.д.
"""

# импорт библиотеки для рабоыт со временем
import datetime

# Создаём собственный класс ошибки неправльной даты
class NotValidDate(Exception):
    """Ошибка: неправльный формат даты"""
    def __init__(self, value):
        self.value = value
        super().__init__(f"неправльная дата: {value}")
    
# Создаём собственный класс ошибки неправильного имени
class NotValidName(Exception):
    """Ошибка: такое имя неподходит"""
    def __init__(self, value):
        self.value = value
        super().__init__(f"недопустимое имя: {value}")

# Создаём собственный класс ошибки уже существующего имени в БД
class NameAlreadyExists(Exception):
    """Ошибка: такое имя уже есть """
    def __init__(self, value):
        self.value = value
        super().__init__(f"такое имя уже есть в бд: {value}")


# валидация имени
def validate_only_letters(text: str) -> str:
    """
    Проверяет, что строка состоит только из букв.
    Поддерживает буквы любых алфавитов (Unicode).
    """

    if not isinstance(text, str):
        raise TypeError("Ожидается строка (str).")
        
    # Убираем пробелы по краям
    text = text.strip()
        
    # Проверка: строка не пустая и состоит только из букв
    if not(bool(text) and text.isalpha()):
        raise NotValidName(text)
    
    return (text)



# валидация даты
def validate_date(date):
    # требуется дата в формате "29.03.2019"
    try:
        current_day = datetime.datetime.strptime(date, "%d.%m.%Y")
    except Exception as e:
        raise NotValidDate(date)

    return current_day




