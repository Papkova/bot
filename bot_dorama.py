import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from detectiv import detectives
from melod import melodrama
from comedies import comedy
from crimin import criminal
from horror import horrors
from dotenv import load_dotenv
from mini import mini_dorama
from schools import school
from drama import main_page, new_series, doram_catalog, novelties
from action import action_dorama
from fantas import fantasy
from historica import historical


load_dotenv()
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
ADMINS = [os.getenv("ADMIN")]


async def default_commands(dp):
    await dp.bot.set_my_commands([
           types.BotCommand(command="start", description="Запустити телеграм бот"),
           types.BotCommand(command="stop", description="Зупинити бота"),
           types.BotCommand(command="saini", description="Перейти на сайт"),
        ]
    )


async def on_startup(dp):
    await default_commands(dp)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    button1 = types.InlineKeyboardButton("Детективи", callback_data='detectives')
    button2 = types.InlineKeyboardButton('Мелодрама', callback_data='melodrama')
    button3 = types.InlineKeyboardButton('Комедія', callback_data='comedy')
    button4 = types.InlineKeyboardButton('Кримінал', callback_data='criminal')
    button5 = types.InlineKeyboardButton("Ужаси", callback_data='horrors')
    button6 = types.InlineKeyboardButton('Мини-дорами', callback_data='mini_dorama')
    button7 = types.InlineKeyboardButton('Школа', callback_data='school')
    button8 = types.InlineKeyboardButton('Бойовик', callback_data='action_dorama')
    button9 = types.InlineKeyboardButton('Фентазі', callback_data='fantasy')
    button10 = types.InlineKeyboardButton('Історичний', callback_data='historical')
# Створюємо клавіатуру з цими кнопками
    keyboard = types.InlineKeyboardMarkup().add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10)

    await message.reply("Виберіть жанр дорами:", reply_markup=keyboard)

# Обробник вибору жанру дорами (коли користувач натискає на кнопку)


@dp.callback_query_handler(lambda c: c.data in detectives or c.data in melodrama or c.data in comedy or c.data in criminal or c.data in horrors or c.data in mini_dorama or c.data in school or c.data in action_dorama or c.data in fantasy or c.data in historical)
async def get_drama_info(callback_query: types.CallbackQuery):
    selected_drama = callback_query.data  # Отримуємо обраний жанр дорами
    drama_data = None
    # Обробка події залежно від обраного жанру
    if selected_drama in detectives:
        drama_data = detectives[selected_drama]
    elif selected_drama in melodrama:
        drama_data = melodrama[selected_drama]
    elif selected_drama in comedy:
        drama_data = comedy[selected_drama]
    elif selected_drama in criminal:
        drama_data = criminal[selected_drama]
    elif selected_drama in horrors:
        drama_data = horrors[selected_drama]
    elif selected_drama in mini_dorama:
        drama_data = mini_dorama[selected_drama]
    elif selected_drama in school:
        drama_data = school[selected_drama]
    elif selected_drama in action_dorama:
        drama_data = action_dorama[selected_drama]
    elif selected_drama in fantasy:
        drama_data = fantasy[selected_drama]
    elif selected_drama in historical:
        drama_data = historical[selected_drama]
# Перевірка, чи інформація про дораму була знайдена
    if drama_data:
        # Відправляємо фотографію та інформацію про дораму користувачу
        await bot.send_photo(callback_query.message.chat.id, drama_data["photo"])
        url = drama_data["site_url"]
        rating = drama_data["rating"]
        description = drama_data["description"]

        message = f"<b>Опис:</b> {description}\n\n<b>Рейтинг:</b> {rating}"
        button = types.InlineKeyboardButton("Перейти на сайт", url=url)
        keyboard = types.InlineKeyboardMarkup().add(button)
        await bot.send_message(callback_query.message.chat.id, message, parse_mode="html", reply_markup=keyboard)
    else:
        await bot.send_message(callback_query.message.chat.id, "Дораму не знайдено")


@dp.message_handler(commands=['saini'])
async def start(message: types.Message):
    button1 = types.InlineKeyboardButton("Головна сторінка", callback_data='main_page')
    button2 = types.InlineKeyboardButton('Каталог дорам', callback_data='doram_catalog')
    button3 = types.InlineKeyboardButton('Нові серії', callback_data='new_series')
    button4 = types.InlineKeyboardButton('Новинки', callback_data='novelties')

    keyboard = types.InlineKeyboardMarkup().add(button1, button2, button3, button4)

    await message.reply("Перейдіть на сайт:", reply_markup=keyboard)

# Обробник вибору категорії
@dp.callback_query_handler(lambda c: c.data in ["main_page", "doram_catalog", "new_series", "novelties"])
async def get_drama_info(callback_query: types.CallbackQuery):
    selected_category = callback_query.data
    drama_data = None
# Визначає обрану категорію і відповідні її дані
    if selected_category == "main_page":
        drama_data = main_page
    elif selected_category == "doram_catalog":
        drama_data = doram_catalog
    elif selected_category == "new_series":
        drama_data = new_series
    elif selected_category == "novelties":
        drama_data = novelties
# Перевіряємо, чи є URL-адреса сайту у вибраної категорії і надсилаємо її
    if drama_data and "site_url" in drama_data:
        url = drama_data["site_url"]
        button = types.InlineKeyboardButton("Перейти на сайт", url=url)
        keyboard = types.InlineKeyboardMarkup().add(button)
        await bot.send_message(callback_query.message.chat.id, "Переходьте за посиланням:", reply_markup=keyboard)
    else:
        await bot.send_message(callback_query.message.chat.id, "Категорію не знайдено")

# Обробник вибору жанру "Детективи"
@dp.callback_query_handler(lambda c: c.data == 'detectives')
async def detectives_selection(callback_query: types.CallbackQuery):
    detectives_choice = InlineKeyboardMarkup()
    for detectives_drama in detectives:
        button = InlineKeyboardButton(text=detectives_drama, callback_data=detectives_drama)
        detectives_choice.add(button)

    await bot.send_message(callback_query.message.chat.id, 'Оберіть жанр  дорами  детектив🎞:',
                           reply_markup=detectives_choice)

# Обробник вибору певної дорами в жанрі "Детективи"
@dp.callback_query_handler(lambda c: c.data in detectives)
async def get_detectives_info(callback_query: types.CallbackQuery):
    selected_detectives = callback_query.data
    if selected_detectives in detectives:
        await bot.send_photo(callback_query.message.chat.id, detectives[selected_detectives]["photo"])
        url = detectives[selected_detectives]["site_url"]
        detectives_rating = detectives[selected_detectives]["rating"]
        detectives_description = detectives[selected_detectives]["description"]
        message = f"<b>Ссилка дорами:<b> {url}\n\n<b>Інформація:</b> {detectives_description}\n\n<b>Рейтинг:</b> {detectives_rating}"
        await bot.send_message(callback_query.message.chat.id, message, parse_mode="html")
    else:
        await bot.send_message(callback_query.message.chat.id, "Дораму не знайдено😞")


@dp.callback_query_handler(lambda c: c.data == 'melodrama')
async def melodrama_selection(callback_query: types.CallbackQuery):
    melodrama_choice = InlineKeyboardMarkup()
    for fantastic_drama in melodrama:
        button = InlineKeyboardButton(text=fantastic_drama, callback_data=fantastic_drama)
        melodrama_choice.add(button)

    await bot.send_message(callback_query.message.chat.id, 'Оберіть жанр дорами мелодрама🎞:', reply_markup=melodrama_choice)


@dp.callback_query_handler(lambda c: c.data in melodrama)
async def get_melodrama_info(callback_query: types.CallbackQuery):
    selected_melodrama = callback_query.data
    if selected_melodrama in melodrama:
        await bot.send_photo(callback_query.message.chat.id, melodrama[selected_melodrama]["photo"])
        url = melodrama[selected_melodrama]["site_url"]
        melodrama_rating = melodrama[selected_melodrama]["rating"]
        melodrama_description = melodrama[selected_melodrama]["description"]
        message = f"<b>Ссилка дорами:<b> {url}\n\n<b>Інформація:</b> {melodrama_description}\n\n<b>Рейтинг:</b> {melodrama_rating}"
        await bot.send_message(callback_query.message.chat.id, message, parse_mode="html")
    else:
        await bot.send_message(callback_query.message.chat.id, "Дораму не знайдено😞")


@dp.callback_query_handler(lambda c: c.data == 'comedy')
async def comedy_selection(callback_query: types.CallbackQuery):
    comedy_choice = InlineKeyboardMarkup()
    for comedy_drama in comedy:
        button = InlineKeyboardButton(text=comedy_drama, callback_data=comedy_drama)
        comedy_choice.add(button)

    await bot.send_message(callback_query.message.chat.id, 'Оберіть жанр дорами  комедія🎥:', reply_markup=comedy_choice)


@dp.callback_query_handler(lambda c: c.data in comedy)
async def get_comedy_info(callback_query: types.CallbackQuery):
    selected_comedy = callback_query.data
    if selected_comedy in comedy:
        await bot.send_photo(callback_query.message.chat.id, comedy[selected_comedy]["photo"])
        url = comedy[selected_comedy]["site_url"]
        comedy_rating = comedy[selected_comedy]["rating"]
        comedy_description = comedy[selected_comedy]["description"]
        message = f"<b>Ссилка дорами:<b> {url}\n\n<b>Інформація:<b> {comedy_description}\n\n<b>Рейтинг:<b> {comedy_rating}"
        await bot.send_message(callback_query.message.chat.id, message, parse_mode="html")
    else:
        await bot.send_message(callback_query.message.chat.id, "Дораму не знайдено😞")


@dp.callback_query_handler(lambda c: c.data == 'criminal')
async def criminal_selection(callback_query: types.CallbackQuery):
    criminal_choice = InlineKeyboardMarkup()
    for criminal_drama in criminal:
        data_size = len(criminal_drama.encode('utf-8'))
        if data_size > 64:
            continue
        button = InlineKeyboardButton(text=criminal_drama, callback_data=criminal_drama)
        criminal_choice.add(button)

    await bot.send_message(callback_query.message.chat.id, 'Оберіть жанр дорами кримінал:', reply_markup=criminal_choice)


@dp.callback_query_handler(lambda c: c.data in criminal)
async def get_criminal_info(callback_query: types.CallbackQuery):
    selected_criminal = callback_query.data
    if selected_criminal in criminal:
        await bot.send_photo(callback_query.message.chat.id, criminal[selected_criminal]["photo"])
        url = criminal[selected_criminal]["site_url"]
        criminal_rating = criminal[selected_criminal]["rating"]
        criminal_description = criminal[selected_criminal]["description"]
        message = f"<b>Ссилка дорами:<b> {url}\n\n<b>Інформація:</b> {criminal_description}\n\n<b>Рейтинг:</b> {criminal_rating}"
        await bot.send_message(callback_query.message.chat.id, message, parse_mode="html")
    else:
        await bot.send_message(callback_query.message.chat.id, "Дораму не знайдено😞")


@dp.callback_query_handler(lambda c: c.data == 'horrors')
async def horrors_selection(callback_query: types.CallbackQuery):
    horrors_choice = InlineKeyboardMarkup()
    for horrors_drama in horrors:
        button = InlineKeyboardButton(text=horrors_drama, callback_data=horrors_drama)
        horrors_choice.add(button)

    await bot.send_message(callback_query.message.chat.id, 'Оберіть жанр  дорами  ужастик🎞:',
                           reply_markup=horrors_choice)


@dp.callback_query_handler(lambda c: c.data in horrors)
async def get_horrors_info(callback_query: types.CallbackQuery):
    selected_horrors = callback_query.data
    if selected_horrors in horrors:
        await bot.send_photo(callback_query.message.chat.id, horrors[selected_horrors]["photo"])
        url = horrors[selected_horrors]["site_url"]
        horrors_rating = horrors[selected_horrors]["rating"]
        horrors_description = horrors[selected_horrors]["description"]
        message = f"<b>Ссилка дорами:<b> {url}\n\n<b>Інформація:</b> {horrors_description}\n\n<b>Рейтинг:</b> {horrors_rating}"
        await bot.send_message(callback_query.message.chat.id, message, parse_mode="html")
    else:
        await bot.send_message(callback_query.message.chat.id, "Дораму не знайдено😞")


@dp.callback_query_handler(lambda c: c.data == 'mini_dorama')
async def mini_dorama_selection(callback_query: types.CallbackQuery):
    mini_dorama_choice = InlineKeyboardMarkup()
    for mini_dorama_drama in mini_dorama:
        data_size = len(mini_dorama_drama.encode('utf-8'))
        if data_size > 64:
            continue
        button = InlineKeyboardButton(text=mini_dorama_drama, callback_data=mini_dorama_drama)
        mini_dorama_choice.add(button)

    await bot.send_message(callback_query.message.chat.id, 'Оберіть жанр дорами міні дорами:', reply_markup=mini_dorama_choice)


@dp.callback_query_handler(lambda c: c.data in mini_dorama)
async def get_mini_dorama_info(callback_query: types.CallbackQuery):
    selected_mini_dorama = callback_query.data
    if selected_mini_dorama in mini_dorama:
        await bot.send_photo(callback_query.message.chat.id, mini_dorama[selected_mini_dorama]["photo"])
        url = mini_dorama[selected_mini_dorama]["site_url"]
        mini_dorama_rating = mini_dorama[selected_mini_dorama]["rating"]
        mini_dorama_description = mini_dorama[selected_mini_dorama]["description"]
        message = f"<b>Ссилка дорами:<b> {url}\n\n<b>Інформація:</b> {mini_dorama_description}\n\n<b>Рейтинг:</b> {mini_dorama_rating}"
        await bot.send_message(callback_query.message.chat.id, message, parse_mode="html")
    else:
        await bot.send_message(callback_query.message.chat.id, "Дораму не знайдено😞")


@dp.callback_query_handler(lambda c: c.data == 'school')
async def school_selection(callback_query: types.CallbackQuery):
    school_choice = InlineKeyboardMarkup()
    for school_drama in school:
        data_size = len(school_drama.encode('utf-8'))
        if data_size > 64:
            continue
        button = InlineKeyboardButton(text=school_drama, callback_data=school_drama)
        school_choice.add(button)

    await bot.send_message(callback_query.message.chat.id, 'Оберіть жанр дорами школа:', reply_markup=school_choice)


@dp.callback_query_handler(lambda c: c.data in school)
async def get_school_info(callback_query: types.CallbackQuery):
    selected_school = callback_query.data
    if selected_school in school:
        await bot.send_photo(callback_query.message.chat.id, school[selected_school]["photo"])
        url = school[selected_school]["site_url"]
        school_rating = school[selected_school]["rating"]
        school_description = school[selected_school]["description"]
        message = f"<b>Ссилка дорами:<b> {url}\n\n<b>Інформація:</b> {school_description}\n\n<b>Рейтинг:</b> {school_rating}"
        await bot.send_message(callback_query.message.chat.id, message, parse_mode="html")
    else:
        await bot.send_message(callback_query.message.chat.id, "Дораму не знайдено😞")


@dp.callback_query_handler(lambda c: c.data == 'action_dorama')
async def action_dorama_selection(callback_query: types.CallbackQuery):
    action_dorama_choice = InlineKeyboardMarkup()
    for action_dorama_drama in action_dorama:
        data_size = len(action_dorama_drama.encode('utf-8'))
        if data_size > 64:
            continue
        button = InlineKeyboardButton(text=action_dorama_drama, callback_data=action_dorama_drama)
        action_dorama_choice.add(button)

    await bot.send_message(callback_query.message.chat.id, 'Оберіть жанр дорами бойовик:', reply_markup=action_dorama_choice)


@dp.callback_query_handler(lambda c: c.data in action_dorama)
async def get_action_dorama_info(callback_query: types.CallbackQuery):
    selected_action_dorama = callback_query.data
    if selected_action_dorama in action_dorama:
        await bot.send_photo(callback_query.message.chat.id, action_dorama[selected_action_dorama]["photo"])
        url = action_dorama[selected_action_dorama]["site_url"]
        action_dorama_rating = action_dorama[selected_action_dorama]["rating"]
        action_dorama_description = action_dorama[selected_action_dorama]["description"]
        message = f"<b>Ссилка дорами:<b> {url}\n\n<b>Інформація:</b> {action_dorama_description}\n\n<b>Рейтинг:</b> {action_dorama_rating}"
        await bot.send_message(callback_query.message.chat.id, message, parse_mode="html")
    else:
        await bot.send_message(callback_query.message.chat.id, "Дораму не знайдено😞")


@dp.callback_query_handler(lambda c: c.data == 'fantasy')
async def fantasy_selection(callback_query: types.CallbackQuery):
    fantasy_choice = InlineKeyboardMarkup()
    for fantasy_drama in fantasy:
        data_size = len(fantasy_drama.encode('utf-8'))
        if data_size > 64:
            continue
        button = InlineKeyboardButton(text=fantasy_drama, callback_data=fantasy_drama)
        fantasy_choice.add(button)

    await bot.send_message(callback_query.message.chat.id, 'Оберіть жанр дорами фентаці:', reply_markup=fantasy_choice)


@dp.callback_query_handler(lambda c: c.data in fantasy)
async def get_fantasy_info(callback_query: types.CallbackQuery):
    selected_fantasy = callback_query.data
    if selected_fantasy in fantasy:
        await bot.send_photo(callback_query.message.chat.id, fantasy[selected_fantasy]["photo"])
        url = fantasy[selected_fantasy]["site_url"]
        fantasy_rating = fantasy[selected_fantasy]["rating"]
        fantasy_description = fantasy[selected_fantasy]["description"]
        message = f"<b>Ссилка дорами:<b> {url}\n\n<b>Інформація:</b> {fantasy_description}\n\n<b>Рейтинг:</b> {fantasy_rating}"
        await bot.send_message(callback_query.message.chat.id, message, parse_mode="html")
    else:
        await bot.send_message(callback_query.message.chat.id, "Дораму не знайдено😞")


@dp.callback_query_handler(lambda c: c.data == 'historical')
async def historical_selection(callback_query: types.CallbackQuery):
    historical_choice = InlineKeyboardMarkup()
    for historical_drama in historical:
        data_size = len(historical_drama.encode('utf-8'))
        if data_size > 64:
            continue
        button = InlineKeyboardButton(text=historical_drama, callback_data=historical_drama)
        historical_choice.add(button)

    await bot.send_message(callback_query.message.chat.id, 'Оберіть жанр дорами школа:', reply_markup=historical_choice)


@dp.callback_query_handler(lambda c: c.data in historical)
async def get_historical_info(callback_query: types.CallbackQuery):
    selected_historical = callback_query.data
    if selected_historical in historical:
        await bot.send_photo(callback_query.message.chat.id, historical[selected_historical]["photo"])
        url = historical[selected_historical]["site_url"]
        historical_rating = historical[selected_historical]["rating"]
        historical_description = historical[selected_historical]["description"]
        message = f"<b>Ссилка дорами:<b> {url}\n\n<b>Інформація:</b> {historical_description}\n\n<b>Рейтинг:</b> {historical_rating}"
        await bot.send_message(callback_query.message.chat.id, message, parse_mode="html")
    else:
        await bot.send_message(callback_query.message.chat.id, "Дораму не знайдено😞")


@dp.message_handler(commands=['stop'])
async def stop_command(message: types.Message):
    await message.reply("Бот зупинено.")


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)




