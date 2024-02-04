# return tuple ('May', '31.05.2022', 31) for month and year

import calendar
from datetime import datetime
from calendar import monthrange


def custom_month_date(month_number: int, current_year: int):
    end_month = monthrange(current_year, month_number)[1]
    months_name = calendar.month_name[month_number]
    check_date = datetime(current_year, month_number, end_month).strftime("%d.%m.%Y")

    return months_name, check_date, end_month


if __name__ == '__main__':
    print(custom_month_date(5, 2022))
    assert custom_month_date(5, 2022) == ('May', '31.05.2022', 31)
