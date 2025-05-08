# start.py

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from firebase_admin import firestore
import random
from datetime import datetime

db = firestore.client()

# Captcha প্রশ্ন ও অপশন
captcha_options = ["8", "9", "10"]
correct_answer = "9"

def send_captcha(bot, message, ref_id=None):
    markup = InlineKeyboardMarkup()
    for opt in captcha_options:
        markup.add(InlineKeyboardButton(text=opt, callback_data=f"captcha:{opt}:{ref_id if ref_id else 'none'}"))
    
    bot.send_message(
        message.chat.id,
        "নিচের প্রশ্নের সঠিক উত্তর দিন:\n\n**3 + 6 = ?**",
        reply_markup=markup,
        parse_mode="Markdown"
    )

def handle_start(bot, message):
    args = message.text.split()
    ref_id = args[1] if len(args) > 1 else None
    send_captcha(bot, message, ref_id)
