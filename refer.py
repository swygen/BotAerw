# handlers/refer.py

from firebase_admin import firestore

db = firestore.client()

def handle(bot, call):
    user = call.from_user
    user_id = str(user.id)

    # ইউজারের ডেটা আনো
    user_ref = db.collection('users').document(user_id)
    user_data = user_ref.get().to_dict()

    # রেফার কাউন্ট আনো, না থাকলে 0
    referred_count = user_data.get('referred_count', 0)

    # রেফার লিংক তৈরি করো
    refer_link = f"https://t.me/YourBotUsername?start={user_id}"

    text = (
        f"**রেফার প্রোগ্রাম**\n\n"
        f"আপনার রেফার লিংক:\n`{refer_link}`\n\n"
        f"এই লিংক শেয়ার করুন বন্ধুর সাথে।\n"
        f"২০ জন রেফার করলে আপনি পাবেন ১২০০ ডায়মন্ড গিভওয়ে!\n\n"
        f"আপনি এখন পর্যন্ত `{referred_count}` জনকে রেফার করেছেন।"
    )

    bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
