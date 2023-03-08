from colorama import Fore
from kommersant_dates import KommersantDates


def month_number():
    answer = input(Fore.GREEN+"Please enter months number\n"
                   "if you want to check last month press 'ENTER'\n"+Fore.RESET)
    if answer.isdigit():
        return int(answer)
    if answer == '':
        return KommersantDates().previous_month_number_int  #  previous month
    else:
        print(Fore.RED+"not correct answer"+Fore.RESET)
    return month_number()


if __name__ == '__main__':
    print(month_number())
