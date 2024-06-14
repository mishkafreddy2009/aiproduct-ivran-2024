import telebot
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

""" Графический интерфейс, бот """

class Main():
    def __int__(self):
        super(Main, self).__init__()
        self.token = '7046388530:AAFfosL3ANMOOWkwPVBp95YLU8yrMwGenZ0'


    bot = telebot.TeleBot('token')
    @bot.message_handler(commands=['start'])
    def send_welcome(self, message):
        self.bot.reply_to(message, "Hi")

    bot.polling()

# if __name__ == "__main__":
    # send_welcome()