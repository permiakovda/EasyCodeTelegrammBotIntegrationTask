"""
дополнительные функции для валидации и т.д.
"""

import datetime
current_day = '1992 14 10'
try:
    current_day = datetime.datetime.strptime("29/03/2019", "%d/%m/%Y")
except Exception:
    print('Дата не по шаблону')

print(current_day)


