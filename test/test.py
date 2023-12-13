from dateutil.rrule import rrule, rrulestr, weekday, WEEKLY, MO, TU, WE, TH, FR
from dateutil.relativedelta import relativedelta
from datetime import datetime, time

def test_rrule():
    today = datetime.today()
    in_a_week = today + relativedelta(weeks=1)
    woche = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]


    rule = rrule(freq=WEEKLY, byweekday=(MO, TU, WE, TH, FR), byhour=(8, 9, 10, 11, 12), byminute=0, bysecond=0)
    date_list: list[datetime] = rule.between(after=today, before=in_a_week)

    for date in date_list:
        print(f"am {woche[date.weekday()]:>10} um {date.time()} Uhr")


def day1_part1():
    with open("test/input.txt", mode="r") as file:
        data = file.read().splitlines()

    all_of_em = 0
    for line in data:
        chars = ""
        for variation in [line, reversed(line)]:
            for char in variation:
                if char.isdigit():
                    chars += char
                    break
        all_of_em += int(chars)

    return all_of_em

def day1_part2():
    with open("test/input.txt", mode="r") as file:
        data = file.read().splitlines()

    digits = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", *"0123456789"]

    all_of_em = 0
    for line in data:
        default = {digit: line.find(digit) for digit in digits if line.find(digit) != -1}
        right = {digit: line.rfind(digit) for digit in digits if line.rfind(digit) != -1}

        default_min = min(default, key=default.get)
        right_min = max(right, key=right.get)

        default_digit = default_min if default_min.isdigit() else str(digits.index(default_min))
        right_digit = right_min if right_min.isdigit() else str(digits.index(right_min))

        digit = int(default_digit + right_digit)
        all_of_em += digit

    return all_of_em

if __name__ == "__main__":
    print(f"day1: {day1_part1()}, {day1_part2()}")