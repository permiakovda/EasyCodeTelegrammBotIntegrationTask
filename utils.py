"""
дополнительные функции для валидации и т.д.
"""

# импорт библиотеки для рабоыт со временем
import datetime

# валидация даты
def validate_date(date):
    # требуется дата в формате "29/03/2019"
    try:
        current_day = datetime.datetime.strptime(date, "%d/%m/%Y")
    except Exception:
        print('Дата не по шаблону')
    
    return current_day




