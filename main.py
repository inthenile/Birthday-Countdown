import sys
from datetime import datetime, timedelta
from contextlib import suppress
import time

name = input("Enter your name (optional), press \"ENTER\" to leave this blank.\n")

def greetings(name):
    print("Hello " + name + "! Let's get a countdown for your birthday! :)")
    print("If you would like to change your name, type \"50\"!\n")
    get_day()

# Grabbing the day of birth
def get_day():
    try:
        user_day = int(input("Which DAY of the month (1-31) were you born on?\n"))
        if (31 >= user_day > 0):
            print("Your DAY input is " + str(user_day) + ", if you entered a wrong DAY,you can enter \"50\" to change the input!\n")
            get_month(user_day)
            # Gives the user to change their name if they've typed it wrong and calls the first greetings function
        elif user_day == 50:
            greetings(name=input("Enter your name (optional), press \"ENTER\" to leave this blank.\n"))
            # If the number is greater or less than the given conditions, the function is called again;
            # the same principle follows for month and year as well
        else:
            print("The day should be between 1 and 31!\n")
            get_day()
    except ValueError as e:
        print(f"You might want to change what you typed. => {e}")
        get_day()

# Grabbing the month of birth
def get_month(user_day):
    try:
        user_month = int(input("Choose the MONTH (1-12) you were born in. "
                               "Or enter \"50\" to change the value of (\"DAY\").\n"))
        print("Your input is " + str(user_month))

        if (12 >= user_month > 0):
            print("Your MONTH input is " + str(
                user_month) + ", if you entered the wrong MONTH,you can enter \"50\" to change the input!\n")
            get_year(user_day, user_month)
        elif (user_month == 50):
            get_day()
        else:
            print("The month should be between 1 and 12!\n")
            get_month(user_day)
    except ValueError as e:
        print(f"Please check your input. => {e}")
        get_month(user_day)


def get_year(user_day, user_month):
    # Grabbing year of birth
    try:
        user_year = int(input("Lastly, enter the YEAR you were born in and let the countdown begin! :) "
                              "Or enter \"50\" to change the value of (\"MONTH\")\n"))
        if (user_year == 50):
            print("Hopefully you were not born in 50! That number is reserved as a placeholder to reset values :)")
            get_month(user_day)
        else:
            confirmation(user_day, user_month, user_year)
    except ValueError as e:
        print(f"Check your input please. => {e}")
        get_year(user_day, user_month)

def confirmation(user_day, user_month, user_year):
    prompt = input(f"Your input is \"{user_day}.{user_month}.{user_year}\" .If these values are all correct, press \"Y\" to proceed. "
                       "If you want to change the \"YEAR\", enter \"50\"!\n")

    if (prompt == "50"):
        get_year(user_day, user_month)
    if (prompt == "y".upper() or "y".lower()):
        # Suppressing the value error if the leap year actually exists. The non-leap years will still raise the error.
        if (bool(datetime(year=user_year, month=user_month, day=user_day))):
            with suppress(ValueError):
                start_countdown(user_day, user_month, user_year)
    else:
        print(f"You entered {prompt}. Please use \"Y\" key to proceed, or enter \"50\" to change the \"YEAR\"\n")
        confirmation(user_day, user_month, user_year)


def start_countdown(user_day, user_month, user_year):

    # setting some useful variables
    now = datetime.now()
    birthday = datetime(user_year, user_month, user_day)
    # You can get the amount of days the person has been alive for! :)
    lived_days = now - birthday
    print("You have been alive for " + str(lived_days.days) + " days! That's amazing. You are doing awesome!")

    # Checking if the input was for a leap year.
    # Checking if, after the birthday countdown ends, the user chooses to restart their countdown.

    if (user_day==29 and user_month==2):
        #Checking if the current year is a leap year
        #Unless the current year is a leap year, the next birthday will fall on the 28 February
        if (datetime.now().year % 4 == 0 or datetime.now().year % 400 == 0):
            print("This is a lap year. You will be able to celebrate your birthday, actually on the date you were born in!")
            if (user_month < now.month):
                next_birthday = datetime(now.year + 1, user_month, user_day)
                # getting the current age accordingly to be able to use it in the countdown
                current_age = now.year - user_year
            elif (user_month >= now.month):
                next_birthday = datetime(now.year, user_month, user_day)
                # If the birthday month is yet to come, we are reducing the current age by one
                # because the birthday hasn't happened yet
                current_age = (now.year-1) - user_year

        else:
            if (user_month < now.month):
                next_birthday = datetime(now.year + 1, user_month, user_day-1)
                current_age = now.year - user_year
            elif (user_month >= now.month):
                next_birthday = datetime(now.year, user_month, user_day-1)
                current_age = (now.year - 1) - user_year
            print("This year is not a lap year, so the countdown will be for the February 28!")

    # checking whether the month or day is passed for the current year or not
    else:
        if (user_month < now.month):
            next_birthday = datetime(now.year + 1, user_month, user_day)
            current_age = now.year - user_year

        elif (user_month >= now.month):
            next_birthday = datetime(now.year, user_month, user_day)
            current_age = (now.year - 1) - user_year

    till_birthday = next_birthday - now

    # The remaining seconds until the birthday to help us calculate the days, hours and minutes remaining
    seconds_left = int(till_birthday.total_seconds())

    if (user_month < now.month) or (user_month >= now.month):
        countdown(current_age, seconds_left)
    # checking if the birthday is today!
    if (next_birthday.day == now.day and user_month == now.month):
        celebrate(current_age)

def countdown(current_age, seconds_left):
    # If there are no seconds left, there is no reason to tell them their age, because the celebrate function will occur
    # Not only is it superfluous, but it is also wrong, since the age shown here will be one fewer than their new age.
    # if there are seconds remaining until the user's birthday, we display their current age,
    # else, the program moves on.
    if (seconds_left > 0):
        print(f"You are {current_age} years old right now.")
    else:
        pass

    # turning the seconds into days, hours, minutes and starting the countdown
    days_left = int(seconds_left / 86400)
    hours_left = int(seconds_left / 3600)
    minutes_left =int(seconds_left / 60)
    # creating variables to reduce minutes, hours, and days every time they pass.
    minute_reduce = int(timedelta(seconds=60).total_seconds())
    hour_reduce = int(timedelta(seconds=3600).total_seconds())
    day_reduce = int(timedelta(seconds=86400).total_seconds())
    # is true as long as there are seconds remaining, nested inside are minutes, hours and days
    # which are true as long as there is at least 1 remaining
    # they check whether the reducers reached 0
    # if that's the case, they are decremented by one, else, the seconds keep counting down
    while seconds_left > 0:
        while minutes_left > 0:
            while hours_left > 0:
                while days_left > 0:
                    if day_reduce == 0:
                        days_left -= 1
                        # restarting the value to keep decrementing the days
                        day_reduce = int(timedelta(seconds=86400).total_seconds())
                    else:
                        break
                if hour_reduce == 0:
                    hours_left -= 1
                    # restarting the value to keep decrementing the hours
                    hour_reduce = int(timedelta(seconds=3600).total_seconds())
                else:
                    break
            if minute_reduce == 0:
                minutes_left-=1
                #restarting the value to keep decrementing the minutes
                minute_reduce = int(timedelta(seconds=60).total_seconds())
            else:
                break

        # Formatting the seconds into looking like a digital clock
        formatted_time = str(timedelta(seconds=seconds_left))
        # The timer shows the remaining time until the next birthday
        timer = f"You are turning {current_age+1} in => {formatted_time}"
        print(timer)
        # Decrementing the values here
        seconds_left -= 1
        minute_reduce -= 1
        hour_reduce -= 1
        day_reduce -=1
        # Making the countdown happen every second.
        time.sleep(1)
    # Congratulation message when the timer runs out
    if seconds_left == 0:
        celebrate(current_age)

# function to celebrate when the timer hits 0!
def celebrate(current_age):
    # increasing the current age by one!
    current_age = current_age + 1
    print(f"YAY! IT'S YOUR BIRTHDAY TODAY {name.upper()}! YOU ARE \"{current_age}\" YEARS OLD! :) I HOPE YOU HAVE A WONDERFUL YOUR BIRTHDAY!\n")

    input("Enter any key to exit the program!\n")
    sys.exit(0)

if __name__ == '__main__':
    greetings(name)