import logging
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from flask import Flask, request

# Задайте ваш токен от BotFather
TOKEN = 'МОЙ_БОТ_ТОКЕН'

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем Flask приложение
app = Flask(__name__)

# Создаем бота
bot = Bot(token=TOKEN)

# Создаем диспетчер для обработки обновлений
dispatcher = Dispatcher(bot, None, workers=0)

# Функция для обработки команд
def start(update, context):
    update.message.reply_text('Привет! Я твой Telegram-бот.')

def help(update, context):
    update.message.reply_text('Отправь команду /start, чтобы я начал работать.')

# Обработчик ошибок
def error(update, context):
    logger.warning('Ошибка "%s" при обработке обновления "%s"', context.error, update)

# Добавляем обработчики команд
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help))
dispatcher.add_error_handler(error)

# Flask маршрут для webhook
@app.route('/bot', methods=['POST'])
def webhook():
    # Получаем обновление от Telegram
    update = Update.de_json(request.get_json(force=True), bot)
    # Передаем обновление в диспетчер
    dispatcher.process_update(update)
    return "ok", 200

# Устанавливаем webhook
def set_webhook():
    url = 'https://МОЙ_АКАУНТ.pythonanywhere.com/bot'  # Укажите ваш домен
    bot.set_webhook(url)

if __name__ == '__main__':
    set_webhook()  # Устанавливаем webhook
    app.run(host='0.0.0.0', port=5000)  # Запускаем Flask
