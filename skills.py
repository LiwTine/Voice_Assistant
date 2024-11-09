import os
import random as rd
import sys
import threading
import time
import datetime

import requests
from num2words import num2words
from word2numberi18n import w2n

import PLAY
import voice
import words


# класс, который содержит в себе: выключить пк, спящий режим, отключить бота
class Shutdown:

    @staticmethod
    def Shutdown_PC():
        voice.play('С разочарованием отключу его через десять секунд. Надеюсь, ты вернёшься')
        time.sleep(10)
        os.system('shutdown -s -t ')

    @staticmethod
    def lock_down_PC():
        voice.play('Хмм..., введу его через десять секунд, удачи создатель')
        time.sleep(10)
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    @staticmethod
    def Shutdown_Bot():
        voice.play('Хорошо, отключаюсь')
        sys.exit()


# Класс, который содержит функции: таймер и текущее время
class Time:

    num_time = 0

    @staticmethod
    def time_now():
        time_time = datetime.datetime.now().time()
        minute = time_time.minute  # берёт hour из метода now()
        hour = time_time.hour  # берёт minute из метода now()
        second = time_time.second  # берёт second из метода now()           20:48:12

        def find_minute(minute):
            if minute == 1:
                return 'минута'
            for i in words.time_numbers:
                if i == minute:
                    return 'минуты'
            return 'минут'

        def find_hour(hour):
            if (hour >= 5) and (hour <= 10):
                return hour, 'утра...'
            elif (hour == 11) or (hour == 12):
                return hour, 'дня...'
            elif (hour > 12) and (hour < 16):
                return hour - 12, 'дня...'
            elif (hour > 15) and (hour < 24):
                return hour - 12, 'вечера...'
            elif (hour >= 0) and (hour < 5):
                return hour, 'ночи...'

        words_minute = find_minute(minute)
        words_hour, time_day = find_hour(hour)

        voice.play(f"Сейчас по Киевскому времени {num2words(minute, lang='ru')} {words_minute}"
                   f"{words.time_words[words_hour + 1]} {time_day}")

    @staticmethod
    def timer():  # с помощью этой функции ассистент ставит таймер, на время, которое пользователь задаёт через голос
        voice.play('на сколько поставить таймер')
        timer_sentence = PLAY.additional_main()  # пользователь задает на которое время поставить таймер
        word_list = timer_sentence.split()       # разбить строку на слова

        def num():  # ищет число в разбитой строке
            instance = w2n.W2N(lang_param="ru")
            for num in word_list:
                num = instance.word_to_num(num)
                if True:
                    return num

        def word():  # ищет ключевое слово в разбитой строке
            for word in words.time_set:
                for i in word_list:
                    if word == i:
                        del words.time_set
                        return word

        def timer_main():  # определяет на сколько поставить таймер; голосовой ассистент уведомляет об этом
            word_a = word()
            num_b = num()
            voice.play(f"Таймер на {num2words(int(num_b), lang='ru')} {word_a} поставила")

            if word_a == "минут" or word_a == "минуты" or word_a == 'минуту':
                Time.num_time += num_b * 60
            elif word_a == 'секунду' or word_a == 'секунды' or word_a == 'секунд':
                Time.num_time += num_b
            else:
                Time.num_time += 60 * (num_b * 60)

        def time_asd():
            thread_timer = threading.Thread(target=timer_main())
            thread_timer.start()
            time.sleep(Time.num_time)
            voice.play("Время таймера вышло, котик. Пора поднять свою жопу и пойти чем-то заняться")

        time_asd()


# ассистент предоставляет нам актуальную инфу о погоде(с помощью запроса на англоязычный сайт с погодой)
def weather():  # +
    voice.play('Сейчас гляну...')
    city_s = 'Kyiv, UA'
    API_key = '881cad74742d7ed14bf6a12984df5d36'
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city_s}&appid={API_key}&lang=ru"
                            f"&units=metric")
    data = response.json()

    city = data['name']
    cur_weather = data['main']['temp']
    humidity = data['main']['humidity']
    # pressure = data['main']['pressure']
    wind = data['wind']['speed']
    # main = data['weather'][0]['main']
    description = data['weather'][0]['description']

    voice.play(f"На данное время в городе {city} {description}, и {num2words(int(round(cur_weather)), lang='ru')}"
               f" градусов по цельсию. Влажность {num2words(int(round(humidity)), lang='ru')}"
               f"процентов, так же скорость ветра {num2words(int(round(wind)), lang='ru')} метров в секунду.")


# с помощью этой функции можно поменять имя, по которому ассистент будет обращаться к пользователю
def change_name_user():  # +
    voice.play('Назови новое имя')
    new_name = PLAY.additional_main()
    file_name_user = open("NAME.txt", "w", encoding='utf-8')
    file_name_user.write(f"{new_name}")
    file_name_user.close()


# подбрасывает монетку
def coin():
    coin = rd.randint(0, 1)
    if coin == 1:
        voice.play("решка")
    else:
        voice.play("орёл")


# открывает браузер
def website():
    pass
