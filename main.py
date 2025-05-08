import telebot
from telebot import types
import random
from datetime import datetime
from handlers import profile, refer, website, giveaway, coupon
from keep_alive import keep_alive

# Bot Token
API_TOKEN = '7253542728:AAEIogTgHz1gBmM3pLfpWqho--z_gpiUSMQ'
bot = telebot.TeleBot(API_TOKEN)

user_data = {}  # ক্যাপচা ভেরিফাই করার জন্য

# Start Command
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    if message.text.startswith("/start ") and len(message.text.split()) > 1:
        referrer_id = message.text.split()[1]
        # রেফার সংরক্ষণ করতে Firebase ব্যবহার করতে হবে
    if user_id not in user_data:
        num1 = random.randint(1, 9)
        num2 = random.randint(1, 9)
        user_data[user_id] = num1 + num2
        bot.send_message(user_id, f"ভেরিফিকেশনের জন্য: {num1} + {num2} = ?")
    else:
        send_welcome(message)

# Captcha Validation
@bot.message_handler(func=lambda m: m.chat.id in user_data)
def verify_captcha(message):
    answer = message.text
    correct = user_data[message.chat.id]
    if answer.isdigit() and int(answer) == correct:
        del user_data[message.chat.id]
        send_welcome(message)
    else:
        bot.send_message(message.chat.id, "ভুল উত্তর। আবার চেষ্টা করুন।")

# Welcome + Inline Keyboard
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("Profile", callback_data='profile'),
        types.InlineKeyboardButton("Refar", callback_data='refer'),
        types.InlineKeyboardButton("Website", callback_data='website'),
        types.InlineKeyboardButton("Apply Giveaway", callback_data='giveaway'),
        types.InlineKeyboardButton("Support X", url='https://t.me/SuportX_team_24'),
        types.InlineKeyboardButton("Coupon Code", callback_data='coupon')
    )
    bot.send_message(message.chat.id, f"স্বাগতম, {message.from_user.first_name}! নিচের অপশনগুলো ব্যবহার করুন:", reply_markup=markup)

# Inline Keyboard Callback Handler
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'profile':
        profile.handle(bot, call)
    elif call.data == 'refer':
        refer.handle(bot, call)
    elif call.data == 'website':
        website.handle(bot, call)
    elif call.data == 'giveaway':
        giveaway.handle(bot, call)
    elif call.data == 'coupon':
        coupon.handle(bot, call)

# Keep Alive (Render এ সার্ভার সচল রাখতে)
keep_alive()

# Start polling
bot.infinity_polling()
