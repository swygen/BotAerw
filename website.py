# handlers/website.py

def handle(bot, call):
    user_id = str(call.from_user.id)
    user = db.collection("users").document(user_id).get().to_dict()

    msg = (
        f"নাম: {user.get('name')}\n"
        f"টেলিগ্রাম আইডি: {user.get('telegram_id')}\n\n"
        "কম দামে বেশি ডায়মন্ড টপ আপ করতে আমাদের ওয়েবসাইট ভিজিট করুন:\n"
        "👉 https://topup-buzz.netlify.app/"
    )

    bot.send_message(call.message.chat.id, msg)
