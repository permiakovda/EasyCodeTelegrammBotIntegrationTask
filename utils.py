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


# валидация даты
def validate_date(date):
    # требуется дата в формате "29.03.2019"
    try:
        current_day = datetime.datetime.strptime(date, "%d.%m.%Y")
    except Exception as e:
        raise NotValidDate(date)

    
    return current_day




