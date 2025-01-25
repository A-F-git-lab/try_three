import asyncio
import logging
from pyowm import OWM
from pyowm.utils.config import get_default_config
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройки логирования
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s", level=logging.INFO)

# Ваши токены
TELEGRAM_TOKEN = "MY_TELEGRAM_TOKEN"
OWM_API_KEY = "MY_OWM_TOKEN_KEY"

config_dict = get_default_config()
config_dict["language"] = "ru"
owm = OWM(OWM_API_KEY, config_dict)
mgr = owm.weather_manager()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Добро пожаловать! Чтобы узнать погоду в вашем городе, просто напишите его название:"
    )

# Обработка текста
async def get_weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    city = update.message.text
    try:
        observation = mgr.weather_at_place(city)
        weather = observation.weather

        # Получение данных с проверкой на наличие
        temp = weather.temperature("celsius").get("temp", "N/A")
        status = weather.detailed_status.capitalize()
        wind_speed = weather.wind().get("speed", "N/A")
        humidity = weather.humidity if weather.humidity is not None else "N/A"

        # Формирование ответа
        response = (
            f"В городе {city} сейчас {status}.\n"
            f"Температура: {temp:.1f}°C.\n"
            f"Скорость ветра: {wind_speed} м/с.\n"
            f"Влажность: {humidity}%."
        )
    except Exception:
        response = "Не удалось найти погоду для указанного города. Проверьте название и попробуйте снова."
    await update.message.reply_text(response)

# Основная функция
async def main() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_weather))
    await application.run_polling()

# Запуск
if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
