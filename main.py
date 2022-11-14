import telebot
from telebot.types import *
from DataBase.DB import DB

# апи телеграма
bot = telebot.TeleBot("5453434987:AAHtd1yOEAjSJngk8pry2mbu7deKWT_CDPM")
# объект класса
db = DB()
# кнопка отмены
cancel_button = InlineKeyboardButton(text="Отмена", callback_data="cancel")
# кнопка меню
menu_button = InlineKeyboardButton(text="Меню", callback_data="menu")
apk_button = InlineKeyboardButton(text="Мобильное приложение", callback_data="apk")


# функция для клавиатуры героев
def heroes_keyboard(heroes_list):
    # прикрепляем клавиатуру
    # callback_data - логика кнопки
    reply_keyboard = InlineKeyboardMarkup()
    for item in heroes_list:
        hero = db.get_hero_by_id(item[0])
        reply_keyboard.add(InlineKeyboardButton(text=f'{hero[1]} {hero[2][0]}.{hero[3][0]}.', callback_data=f'heroes_{hero[0]}'))
    reply_keyboard.add(InlineKeyboardButton(text="Назад", callback_data="back_to_events"))
    return reply_keyboard


def keyboard():
    reply_keyboard = InlineKeyboardMarkup()
    for item in db.get_info_from_event():
        reply_keyboard.add(InlineKeyboardButton(text=item[1], callback_data=f'event_{item[0]}'))
        # replt_keyboard.add - добавление кнопки
    reply_keyboard.add(InlineKeyboardButton(text="Ссылка на сайт", url="https://znai-nashih.ru/"))
    reply_keyboard.add(apk_button)
    reply_keyboard.add(cancel_button)
    return reply_keyboard


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.from_user.id, "Выберите событие", reply_markup=keyboard())


@bot.message_handler(content_types=['text'])
def send_text_messages(message):
    username = message.from_user.username
    if message.text == "да":
        for i in range(1, 5):
            bot.send_message(message.from_user.id, "ты хороший")
    elif message.text == "висилица":
        with open('micro.webp', "rb") as sticker:
            bot.send_sticker(message.from_user.id, sticker)
    else:
        bot.send_message(message.from_user.id, message.text)


@bot.message_handler(content_types=['dice'])
def send_dice(message):
    bot.send_dice(message.from_user.id)


@bot.message_handler(content_types=['sticker'])
def send_sticker(message):
    sticker_id = message.sticker.file_id
    bot.send_sticker(message.from_user.id, sticker=sticker_id)


@bot.callback_query_handler(func=lambda call: True)
def buttons_callback(call):
    if "back_to_events" in call.data:
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.id,
                              text="Выберите события",
                              reply_markup=keyboard())
    elif "event" in call.data:
        event_id = call.data.split("_")[1]
        keyboard21 = heroes_keyboard(db.get_all_heroes_from_id(event_id))
        bot.edit_message_text(text="Выберите героя",
                              chat_id=call.message.chat.id,
                              message_id=call.message.id,
                              reply_markup=keyboard21)
    elif "heroes" in call.data:
        heroes_id = call.data.split("_")[1]
        hero_image = db.get_hero_by_id(heroes_id)[7]
        hero_description = db.get_hero_by_id(heroes_id)[6]
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.id)
        bot.send_photo(caption=hero_description,
                       chat_id=call.message.chat.id,
                       photo=hero_image)
        bot.send_message(text="Что-то еще?",
                         chat_id=call.message.chat.id,
                         reply_markup=keyboard())
    elif "cancel" in call.data:
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.id)
    elif "apk" in call.data:
        bot.send_document(chat_id=call.message.chat.id,
                          document=open("recources/ZnaiNashih.apk", "rb"))


bot.polling(none_stop=True, interval=0)
