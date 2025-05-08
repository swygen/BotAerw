# captcha_callback.py

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from firebase_admin import firestore
import random
from datetime import datetime

db = firestore.client()

def handle_captcha(bot, call):
    _, answer, ref_id = call.data.split(":")
    user = call.from_user
    user_id = str(user.id)

    if answer != "9":
        bot.answer_callback_query(call.id, "ভুল উত্তর! আবার চেষ্টা করুন।", show_alert=True)
        return

    # চেক করো ইউজার আগেই আছে কিনা
    user_ref = db.collection("users").document(user_id)
    if not user_ref.get().exists:
        user_ref.set({
            "name": user.first_name,
            "telegram_id": user.id,
            "uid": f"UID{random.randint(10000, 99999)}",
            "join_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "referred_count": 0
        })

        # রেফার যুক্ত করো
        if ref_id and ref_id != user_id:
            ref_user_ref = db.collection("users").document(ref_id)
            ref_data = ref_user_ref.get()
            if ref_data.exists:
                prev = ref_data.to_dict().get("referred_count", 0)
                ref_user_ref.update({"referred_count": prev + 1})

    # Inline মেনু
    menu = InlineKeyboardMarkup(row_width=2)
    menu.add(
        InlineKeyboardButton("প্রোফাইল", callback_data="profile"),
        InlineKeyboardButton("রেফার", callback_data="refer"),
        InlineKeyboardButton("ওয়েবসাইট", callback_data="website"),
        InlineKeyboardButton("Apply Giveaway", callback_data="giveaway"),
        InlineKeyboardButton("Support X", url="https://t.me/SuportX_team_24"),
        InlineKeyboardButton("Coupon Code", callback_data="coupon")
    )

    bot.edit_message_text(
        "ভেরিফিকেশন সফল! আপনাকে স্বাগতম টপ-আপ বটে!",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=menu
    )
