import telebot
from multiprocessing import Process

from neural.model import Model
from utils.db_connection import Db_Connection
from utils.parser import Parser

""" Графический интерфейс, бот """

class Main():
    def __int__(self):
        super(Main, self).__init__()

    bot = telebot.TeleBot('token')
    @bot.message_handler(commands=['start'])
    def send_welcome(self, message):
        self.bot.reply_to(message, "Hi")

    bot.polling()

# Запуск всей программы в нескольких потоках
if __name__ == "__main__":
    main = Main()
    model = Model()
    db_connection = Db_Connection()
    parser = Parser()

    #TODO: изменить функцию в main. Если нужно запускать отдельно - раскомментить main() класса
    p1 = Process(target=main.send_welcome())  #Инициализация потоков
    p2 = Process(target=model)
    p3 = Process(target=db_connection)  #TODO: возможно убрать, брать static method
    p4 = Process(target=parser.main())

    p1.start()
    p2.start()
    p3.start()
    p4.start()

    p1.join()   #Запуск потоков
    p2.join()
    p3.join()
    p4.join()