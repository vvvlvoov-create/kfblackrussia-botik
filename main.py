import os
import logging
from datetime import datetime, time
import pytz
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Конфигурация
BOT_TOKEN = os.environ.get('BOT_TOKEN', '7719252121:AAEUyzzdo1JjYVfNv1uN_Y7PQFHR6de3T1o')
MOSCOW_TZ = pytz.timezone('Europe/Moscow')
BOT_USERNAME = 'kfblackrussiabot_bot'

# Данные серверов
SERVERS = {
    '👮‍♂Череповец': 'Череповец', '🐀Магадан': 'Магадан', '🏰 ᴘᴏᴅᴏʟsᴋ': 'Подольск',
    '🏙 sᴜʀɢᴜᴛ': 'Сургут', '🏍 ɪᴢʜᴇᴠsᴋ': 'Ижевск', '🎄 ᴛᴏᴍsᴋ': 'Томск',
    '🐿 ᴛᴠᴇʀ': 'Тверь', '🐦‍🔥 ᴠᴏʟᴏɢᴅᴀ': 'Вологда', '🦁 ᴛᴀɢᴀɴʀᴏɢ': 'Таганрог',
    '🌼 ɴᴏᴠɢᴏʀᴏᴅ': 'Новгород', '🫐 ᴋᴀʟᴜɢᴀ': 'Калуга', '😹 ᴠʟᴀᴅɪᴍɪʀ': 'Владимир',
    '🐲 ᴋᴏsᴛʀᴏᴍᴀ': 'Кострома', '🦎 ᴄʜɪᴛᴀ': 'Чита', '🧣 ᴀsᴛʀᴀᴋʜᴀɴ': 'Астрахань',
    '👜 ʙʀᴀᴛsᴋ': 'Братск', '🥐 ᴛᴀᴍʙᴏᴡ': 'Тамбов', '🥽 ʏᴀᴋᴜᴛsᴋ': 'Якутск',
    '🍭 ᴜʟʏᴀɴᴏᴠsᴋ': 'Ульяновск', '🎈 ʟɪᴘᴇᴛsᴋ': 'Липецк', '💦 ʙᴀʀɴᴀᴜʟ': 'Барнаул',
    '🏛 ʏᴀʀᴏsʟᴀᴠʟ': 'Ярославль', '🦅 ᴏʀᴇʟ': 'Орел', '🧸 ʙʀʏᴀɴsᴋ': 'Брянск',
    '🪭 ᴘsᴋᴏᴡ': 'Псков', '🫚 sᴍᴏʟᴇɴsᴋ': 'Смоленск', '🪼 sᴛᴀᴠʀᴏᴘᴏʟ': 'Ставрополь',
    '🪅 ɪᴠᴀɴᴏᴠᴏ': 'Иваново', '🪸 ᴛᴏʟʏᴀᴛᴛɪ': 'Тольятти', '🐋 ᴛʏᴜᴍᴇɴ': 'Тюмень',
    '🌺 ᴋᴇᴍᴇʀᴏᴠᴏ': 'Кемерово', '🔫 ᴋɪʀᴏᴠ': 'Киров', '🍖 ᴏʀᴇɴʙᴜʀɢ': 'Оренбург',
    '🥋 ᴀʀᴋʜᴀɴɢᴇʟsᴋ': 'Архангельск', '🃏 ᴋᴜʀsᴋ': 'Курск', '🎳 ᴍᴜʀᴍᴀɴsᴋ': 'Мурманск',
    '🎷 ᴘᴇɴᴢᴀ': 'Пенза', '🎭 ʀʏᴀᴢᴀɴ': 'Рязань', '⛳ ᴛᴜʟᴀ': 'Тула', '🏟 ᴘᴇʀᴍ': 'Пермь',
    '🐨 ᴋʜᴀʙᴀʀᴏᴠsᴋ': 'Хабаровск', '🪄 ᴄʜᴇʙᴏᴋsᴀʀ': 'Чебоксары', '🖇 ᴋʀᴀsɴᴏʏᴀʀsᴋ': 'Красноярск',
    '🕊 ᴄʜᴇʟʏᴀʙɪɴsᴋ': 'Челябинск', '👒 ᴋᴀʟɪɴɪɴɢʀᴀᴅ': 'Калининград', '🧶 ᴠʟᴀᴅɪᴠᴏsᴛᴏᴋ': 'Владивосток',
    '🌂 ᴠʟᴀᴅɪᴋᴀᴡᴋᴀᴢ': 'Владикавказ', '⛑️ ᴍᴀᴋʜᴀᴄʜᴋᴀʟᴀ': 'Махачкала', '🎓 ʙᴇʟɢᴏʀᴏᴅ': 'Белгород',
    '👑 ᴠᴏʀᴏɴᴇᴢʜ': 'Воронеж', '🎒 ᴠᴏʟɢᴏɢʀᴀᴅ': 'Волгоград', '🌪 ɪʀᴋᴜᴛsᴋ': 'Иркутск',
    '🪙 ᴏᴍsᴋ': 'Омск', '🐉 sᴀʀᴀᴛᴏᴠ': 'Саратов', '🍙 ɢʀᴏᴢɴʏ': 'Грозный',
    '🍃 ɴᴏᴠᴏsɪʙ': 'Новосибирск', '🪿 ᴀʀᴢᴀᴍᴀs': 'Арзамас', '🪻 ᴋʀᴀsɴᴏᴅᴀʀ': 'Краснодар',
    '📗 ᴇᴋʙ': 'Екатеринбург', '🪺 ᴀɴᴀᴘᴀ': 'Анапа', '🍺 ʀᴏsᴛᴏᴠ': 'Ростов',
    '🎧 sᴀᴍᴀʀᴀ': 'Самара', '🏛 ᴋᴀᴢᴀɴ': 'Казань', '🌊 sᴏᴄʜɪ': 'Сочи',
    '🌪 ᴜғᴀ': 'Уфа', '🌉 sᴘʙ': 'Санкт-Петербург', '🌇 ᴍᴏsᴄᴏᴡ': 'Москва',
    '🤎 ᴄʜᴏᴄᴏ': 'Шоко', '📕 ᴄʜɪʟʟɪ': 'Чилли', '❄ ɪᴄᴇ': 'Айс',
    '📓 ɢʀᴀʏ': 'Грей', '📘 ᴀǫᴜᴀ': 'Аква', '🩶 ᴘʟᴀᴛɪɴᴜᴍ': 'Платинум',
    '💙 ᴀᴢᴜʀᴇ': 'Азуре', '💛️ ɢᴏʟᴅ': 'Голд', '❤‍🔥 ᴄʀɪᴍsᴏɴ': 'Кримсон',
    '🩷 ᴍᴀɢᴇɴᴛᴀ': 'Магента', '🤍 ᴡʜɪᴛᴇ': 'Вайт', '💜 ɪɴᴅɪɢᴏ': 'Индиго',
    '🖤 ʙʟᴀᴄᴋ': 'Блэк', '🍒 ᴄʜᴇʀʀʏ': 'Черри', '💕 ᴘɪɴᴋ': 'Пинк',
    '🍋 ʟɪᴍᴇ': 'Лайм', '💜 ᴘᴜʀᴘʟᴇ': 'Пурпл', '🧡 ᴏʀᴀɴɢᴇ': 'Оранж',
    '💛 ʏᴇʟʟᴏᴡ': 'Еллоу', '💙 ʙʟᴜᴇ': 'Блу', '💚 ɢʀᴇᴇɴ': 'Грин',
    '❤‍🩹 ʀᴇᴅ': 'Ред'
}

# Глобальные переменные
user_states = {}
rr_entries = []
pd_entries = {'house': [], 'garage': []}

def create_server_keyboard():
    """Создает клавиатуру с серверами (4 колонки)"""
    keyboard = []
    for i in range(0, len(SERVERS), 4):
        row = [InlineKeyboardButton(emoji, callback_data=f"server_{name}") 
               for emoji, name in list(SERVERS.items())[i:i+4]]
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

def create_main_menu():
    """Создает главное меню"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 Заполнить RR лист", callback_data="fill_rr")],
        [InlineKeyboardButton("🏥 Заполнить PD лист", callback_data="fill_pd")]
    ])

def create_pd_category_keyboard():
    """Создает клавиатуру выбора категории для PD"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 Дома", callback_data="pd_house")],
        [InlineKeyboardButton("🚗 Гаражи", callback_data="pd_garage")]
    ])

def create_house_time_keyboard():
    """Создает клавиатуру выбора времени для домов"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("15:00", callback_data="time_15"), InlineKeyboardButton("17:00", callback_data="time_17")],
        [InlineKeyboardButton("20:00", callback_data="time_20"), InlineKeyboardButton("22:00", callback_data="time_22")]
    ])

def create_garage_time_keyboard():
    """Создает клавиатуру выбора времени для гаражей (БЕЗ 22:00)"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("14:00", callback_data="time_14"), InlineKeyboardButton("16:00", callback_data="time_16")],
        [InlineKeyboardButton("19:00", callback_data="time_19")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    await update.message.reply_text(
        "Привет! Это бот для автолистов кф \"Чёрная Россия\", выберите действие.",
        reply_markup=create_main_menu()
    )

async def list_rr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает текущий RR лист"""
    rr_text = "📋 ТЕКУЩИЙ RR ЛИСТ:\n\n"
    server_entries = {}
    
    for entry in rr_entries:
        if ' - ' in entry:
            server, desc = entry.split(' - ', 1)
            server_entries.setdefault(server, []).append(desc)
    
    for emoji, name in SERVERS.items():
        entries = server_entries.get(name, [])
        rr_text += f"{emoji} - {', '.join(entries) if entries else ''}\n"
    
    await update.message.reply_text(rr_text)

async def list_pd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает текущий PD лист"""
    pd_text = "🏥 ТЕКУЩИЙ PD ЛИСТ:\n\n🏠 House\n"
    pd_text += "\n".join(f"• {entry}" for entry in pd_entries['house']) or "-\n"
    pd_text += "\n🚗 Garage\n"
    pd_text += "\n".join(f"• {entry}" for entry in pd_entries['garage']) or "-"
    await update.message.reply_text(pd_text)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    data = query.data
    
    if data == "fill_rr":
        now = datetime.now(MOSCOW_TZ).time()
        if time(5, 1) <= now <= time(23, 59):
            await query.message.reply_text("Сообщение не найдено❌")
            return
        
        user_states[user_id] = {'type': 'rr', 'step': 'server'}
        await query.message.reply_text("Выберите сервер:", reply_markup=create_server_keyboard())
        
    elif data == "fill_pd":
        now = datetime.now(MOSCOW_TZ).time()
        if time(0, 0) <= now <= time(5, 0):
            await query.message.reply_text("Сообщение не найдено❌")
            return
        
        user_states[user_id] = {'type': 'pd', 'step': 'category'}
        await query.message.reply_text("Привет, выбери категорию слета:", reply_markup=create_pd_category_keyboard())
    
    elif data.startswith("pd_"):
        user_states[user_id]['step'] = 'time'
        user_states[user_id]['category'] = 'house' if 'house' in data else 'garage'
        keyboard = create_house_time_keyboard() if user_states[user_id]['category'] == 'house' else create_garage_time_keyboard()
        await query.message.reply_text("Выберите время:", reply_markup=keyboard)
    
    elif data.startswith("time_"):
        user_states[user_id]['step'] = 'server'
        time_map = {'14': '14:00', '15': '15:00', '16': '16:00', '17': '17:00', '19': '19:00', '20': '20:00', '22': '22:00'}
        user_states[user_id]['time'] = time_map[data.split('_')[1]]
        await query.message.reply_text("Отлично, укажите сервер:", reply_markup=create_server_keyboard())
    
    elif data.startswith("server_"):
        server_name = data.split('_', 1)[1]
        user_states[user_id]['server'] = server_name
        user_states[user_id]['step'] = 'description'
        await query.message.reply_text("Напишите что слетает:")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений"""
    user_id = update.message.from_user.id
    
    if user_id in user_states and user_states[user_id]['step'] == 'description':
        user_data = user_states[user_id]
        description = update.message.text
        
        if user_data['type'] == 'rr':
            entry = f"{user_data['server']} - {description}"
            rr_entries.append(entry)
            await update.message.reply_text(f"✅ Добавлено в RR лист:\n{entry}")
        else:
            category_name = 'Дома' if user_data['category'] == 'house' else 'Гаражи'
            entry = f"{user_data['server']} - {user_data['time']} - {description}"
            pd_entries[user_data['category']].append(entry)
            await update.message.reply_text(f"✅ Добавлено в PD лист ({category_name}):\n{entry}")
        
        del user_states[user_id]
    else:
        await update.message.reply_text("Пожалуйста, используйте кнопки меню:", reply_markup=create_main_menu())

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    logger.error(f"Ошибка: {context.error}", exc_info=context.error)

def main():
    """Основная функция"""
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN не установлен!")
        return
    
    logger.info("🚀 Бот запускается...")
    
    try:
        application = Application.builder().token(BOT_TOKEN).build()
        
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("list_rr", list_rr))
        application.add_handler(CommandHandler("list_pd", list_pd))
        application.add_handler(CallbackQueryHandler(button_handler))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        application.add_error_handler(error_handler)
        
        logger.info("✅ Бот успешно запущен!")
        application.run_polling()
        
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
        logger.info("🔄 Перезапуск через 10 секунд...")
        import time
        time.sleep(10)
        main()

if __name__ == "__main__":
    main()
