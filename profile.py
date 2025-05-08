# handlers/profile.py

import random
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase init (ensure not to initialize more than once)
if not firebase_admin._apps:
    cred = credentials.Certificate("path/to/your-firebase-adminsdk.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def handle(bot, call):
    user = call.from_user
    user_id = str(user.id)

    # চেক করো ইউজার আগে থেকে আছে কিনা
    doc_ref = db.collection('users').document(user_id)
    doc = doc_ref.get()

    if doc.exists:
        user_data = doc.to_dict()
    else:
        user_data = {
            'name': user.first_name,
            'uid': f"UID{random.randint(10000, 99999)}",
            'join_date': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'telegram_id': user.id,
        }
        doc_ref.set(user_data)

    text = (
        f"**প্রোফাইল তথ্য**\n\n"
        f"নাম: `{user_data['name']}`\n"
        f"টেলিগ্রাম আইডি: `{user_data['telegram_id']}`\n"
        f"UID: `{user_data['uid']}`\n"
        f"যোগদানের তারিখ: `{user_data['join_date']}`"
    )

    bot.send_message(call.message.chat.id, text, parse_mode='Markdown')
