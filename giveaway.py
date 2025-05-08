# handlers/giveaway.py

from telebot.types import ForceReply
from firebase_admin import firestore

db = firestore.client()

# Step 1: Giveaway চেকার
def handle(bot, call):
    user_id = str(call.from_user.id)
    user_ref = db.collection("users").document(user_id)
    user_data = user_ref.get().to_dict()

    referred = user_data.get("referred_count", 0)
    name = user_data.get("name", "Unknown")

    if referred < 20:
        bot.send_message(call.message.chat.id,
            f"প্রিয় {name}, আপনি এখন পর্যন্ত {referred} জনকে রেফার করেছেন।\n\n"
            "Giveaway পেতে হলে কমপক্ষে ২০ জন রেফার করতে হবে।\n\n"
            "আপনার রেফার লিংক ব্যবহার করে আরও বন্ধু ইনভাইট করুন।"
        )
    else:
        msg = bot.send_message(call.message.chat.id,
            f"{name}, আপনি {referred} জনকে রেফার করেছেন!\n\n"
            "Giveaway ক্লেইম করতে আপনার UID নাম্বার দিন।",
            reply_markup=ForceReply(selective=True)
        )
        bot.register_next_step_handler(msg, process_uid)

# Step 2: UID প্রসেসর
def process_uid(message):
    uid = message.text
    name = message.from_user.first_name

    # চাইলে Firebase-এ UID সেভ করা যায়
    user_id = str(message.from_user.id)
    user_ref = db.collection("users").document(user_id)
    user_ref.update({"submitted_uid": uid})

    bot = message.bot  # Access bot from message context
    bot.send_message(
        message.chat.id,
        f"ধন্যবাদ {name}!\nআপনার UID `{uid}` আমরা গ্রহণ করেছি।\nআপনার ১২০০ ডায়মন্ড গিভওয়ে রিভিউ হচ্ছে!",
        parse_mode="Markdown"
    )
