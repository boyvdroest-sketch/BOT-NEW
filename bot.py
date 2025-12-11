import os
from flask import Flask, request
import telebot
from telebot import types

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_ID = 7016264130
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

user_messages = {}
broadcast_users = set()
user_chat_states = {}

# ==================== SEO-OPTIMIZED START (ACCOMMODATION FOCUS) ====================
@bot.message_handler(commands=['start'])
def start_command(message):
    if message is None:
        return
    user_id = message.from_user.id
    broadcast_users.add(user_id)
    user_chat_states[user_id] = 'started'

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("New York", callback_data="nyc"),
        types.InlineKeyboardButton("Miami", callback_data="miami"),
        types.InlineKeyboardButton("Las Vegas", callback_data="vegas"),
        types.InlineKeyboardButton("Orlando", callback_data="orlando"),
        types.InlineKeyboardButton("Luxury Hotels", callback_data="luxury"),
        types.InlineKeyboardButton("Airbnb & Villas", callback_data="airbnb")
    )
    markup.add(types.InlineKeyboardButton("Join Channel – Daily Deals", url="https://t.me/flights_half_off"))

    short_text = (
        "*ACCOMMODATION DEALS – UP TO 60% OFF* \n\n"
        "Hotels • Resorts • Airbnb • Motels • Vacation Homes\n\n"
        "Tap any city below to see today’s exclusive discounts:\n\n"
        "cheap hotels usa • discount accommodation • hotel deals • airbnb discount • last minute stays"
    )

    bot.send_message(message.chat.id, short_text, reply_markup=markup, parse_mode='Markdown')

# ==================== DETAILED OFFERS ON CLICK (SEO + CONVERSION) ====================
@bot.callback_query_handler(func=lambda call: True)
def callback_deals(call):
    offers = {
        "nyc": "*NEW YORK CITY – UP TO 60% OFF*\n\n"
               "• Times Square hotels from $79/night\n"
               "• Manhattan 4★ from $109\n"
               "• Brooklyn budget stays from $59\n\n"
               "Secret codes active today only",

        "miami": "*MIAMI BEACH – UP TO 55% OFF*\n\n"
                 "• Oceanfront resorts from $99\n"
                 "• South Beach luxury from $139\n"
                 "• Art Deco boutique from $79\n\n"
                 "Flash sale ends tonight",

        "vegas": "*LAS VEGAS STRIP – UP TO 60% OFF*\n\n"
                 "• Bellagio, Caesars, MGM from $39\n"
                 "• Suite upgrades included\n"
                 "• Free play + dining credits\n\n"
                 "Limited rooms left",

        "orlando": "*ORLANDO – UP TO 58% OFF*\n\n"
                   "• Disney & Universal area hotels\n"
                   "• Free shuttle + breakfast deals\n"
                   "• Family suites from $89\n\n"
                   "Perfect for theme park trips",

        "luxury": "*LUXURY 5-STAR HOTELS USA*\n\n"
                  "• Ritz-Carlton, Four Seasons, Waldorf\n"
                  "• Up to 60% off + free upgrades\n"
                  "• Spa credits & late checkout\n\n"
                  "Exclusive member rates",

        "airbnb": "*AIRBNB & VACATION HOMES*\n\n"
                  "• Beach houses, city lofts, mountain cabins\n"
                  "• Extra 15–40% off with promo codes\n"
                  "• Private pools, hot tubs, views\n\n"
                  "Book before hosts raise prices"
    }

    if call.data in offers:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Get Today’s Booking Links", url="https://t.me/flights_half_off"))
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=offers[call.data],
            reply_markup=markup,
            parse_mode='Markdown'
        )
    bot.answer_callback_query(call.id)

# ==================== YOUR ORIGINAL CODE BELOW – 100% UNTOUCHED ====================

# ===== BROADCAST FEATURE =====
@bot.message_handler(commands=['broadcast'])
def broadcast_command(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "This command is for admin only!")
        return
    if len(broadcast_users) == 0:
        bot.reply_to(message, "No users in broadcast list!")
        return
    msg = bot.send_message(ADMIN_ID, f"Broadcast to {len(broadcast_users)} users\n\nPlease enter your broadcast message:")
    bot.register_next_step_handler(msg, process_broadcast_message)

def process_broadcast_message(message):
    if hasattr(message, 'is_broadcast_processed') and message.is_broadcast_processed:
        return
    message.is_broadcast_processed = True
    broadcast_text = message.text
    users = list(broadcast_users)
    success_count = fail_count = 0
    status_msg = bot.send_message = bot.send_message(ADMIN_ID, f"Starting broadcast to {len(users)} users...")
    for user_id in users:
        try:
            bot.send_message(user_id, f"Announcement:\n\n{broadcast_text}")
            success_count += 1
        except:
            fail_count += 1
    bot.edit_message_text(
        f"Broadcast Completed!\n\nSuccessful: {success_count}\nFailed: {fail_count}\nTotal: {len(users)}",
        ADMIN_ID, status_msg.message_id
    )

@bot.message_handler(commands=['stats'])
def stats_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    bot.send_message(ADMIN_ID, f"Bot Statistics:\n\nTotal Users: {len(broadcast_users)}")

# ===== CHAT HANDLERS (unchanged) =====
# ... (all your hello, reply, forwarding logic stays exactly the same)

@bot.message_handler(func=lambda m: m.text and m.text.lower().startswith('hello'))
def hello_handler(message):
    user = message.from_user
    user_id = user.id
    broadcast_users.add(user_id)
    user_chat_states[user_id] = 'waiting_for_admin'
    user_info = f"User: {user.first_name} {user.last_name or ''} (@{user.username or 'No username'})"
    user_messages[message.message_id] = {'user_id': user_id, 'user_info': user_info, 'original_message': message.text}
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Reply", callback_data=f"reply_{message.message_id}")
    forward_text = f"Someone said hello!\n\n{user_info}\nUser ID: {user.id}\n\nMessage: '{message.text}'"
    bot.send_message(ADMIN_ID, forward_text, reply_markup=keyboard)
    bot.reply_to(message, "Hello! I've notified the admin. They'll reply soon!\nYou can keep chatting.")

@bot.callback_query_handler(func=lambda call: call.data.startswith('reply_'))
def reply_callback_handler(call):
    message_id = int(call.data.split('_')[1])
    if message_id in user_messages:
        user_data = user_messages[message_id]
        msg = bot.send_message(ADMIN_ID, f"Type your reply for {user_data['user_info']}:")
        bot.register_next_step_handler(msg, process_admin_reply, user_data['user_id'])
    else:
        bot.answer_callback_query(call.id, "Message expired")

def process_admin_reply(message, user_id):
    try:
        bot.send_message(user_id, f"Message from admin:\n\n{message.text}")
        bot.reply_to(message, "Reply sent!")
    except Exception as e:
        bot.reply_to(message, f"Failed: {e}")

@bot.message_handler(func=lambda message: True)
def all_messages_handler(message):
    user_id = message.from_user.id
    if user_id == ADMIN_ID:
        return
    broadcast_users.add(user_id)
    if user_chat_states.get(user_id) == 'waiting_for_admin' and message.text:
        user_info = f"User: {message.from_user.first_name} (@{message.from_user.username or 'No username'})"
        user_messages[message.message_id] = {'user_id': user_id, 'user_info': user_info, 'original_message': message.text}
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("Reply", callback_data=f"reply_{message.message_id}"))
        forward_text = f"New message:\n\n{user_info}\nID: {user_id}\n\n'{message.text}'"
        bot.send_message(ADMIN_ID, forward_text, reply_markup=keyboard)
        if not message.text.lower().startswith('hello'):
            bot.reply_to(message, "Message received! Admin will reply soon.")

# ==================== WEBHOOK & FLASK (unchanged) ====================
@app.route('/')
def home():
    return "Bot is running!"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = request.get_data().decode("utf-8")
    update_obj = telebot.types.Update.de_json(update)
    bot.process_new_updates([update_obj])
    return "OK", 200

if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("TELEGRAM_BOT_TOKEN is required")
    try:
        bot.remove_webhook()
        domain = os.environ.get("REPLIT_DEV_DOMAIN") or os.environ.get("RENDER_EXTERNAL_URL")
        if domain:
            webhook_url = f"https://{domain}/{TOKEN}"
            bot.set_webhook(url=webhook_url)
            print(f"Webhook: {webhook_url}")
    except Exception as e:
        print(f"Webhook error: {e}")
    print("Bot is running!")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
