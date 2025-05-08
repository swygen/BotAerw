# handlers/coupon.py

from telebot.types import ForceReply

# কোডগুলো এখানে রাখা (চাইলে Firebase থেকেও নিতে পারো)
VALID_COUPONS = ["FREE100", "DIAMOND20", "TOPUPX"]

def handle(bot, call):
    msg = bot.send_message(
        call.message.chat.id,
        "আমাদের ওয়েবসাইট (https://topup-buzz.netlify.app/) থেকে টপ আপ করার পর প্রাপ্ত Coupon Code টি লিখুন।",
        reply_markup=ForceReply(selective=True)
    )
    bot.register_next_step_handler(msg, process_coupon)

def process_coupon(message):
    coupon = message.text.strip()
    user = message.from_user
    chat_id = message.chat.id

    if coupon in VALID_COUPONS:
        msg = (
            f"অভিনন্দন {user.first_name}!\n"
            f"আপনার Coupon `{coupon}` সঠিক।\n"
            f"আপনি বোনাস ডায়মন্ড পেয়ে গেছেন!"
        )
    else:
        msg = (
            f"ভুল Coupon Code `{coupon}`!\n"
            f"দয়া করে ওয়েবসাইট থেকে পাওয়া সঠিক কোড লিখুন।"
        )

    message.bot.send_message(chat_id, msg, parse_mode="Markdown")
