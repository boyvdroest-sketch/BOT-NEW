import os
from flask import Flask, request
import telebot
from telebot import types

# Get bot token from environment variable
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# Add your admin user ID here
ADMIN_ID = 7016264130  # Replace with your actual Telegram user ID

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Store user info for replies and broadcast
user_messages = {}
broadcast_users = set()
user_chat_states = {}  # Track user conversation states

# ===== ACCOMMODATION DATA =====
ACCOMMODATION_OFFERS = {
    "newyork": {
        "title": "🗽 **New York Hotels - Up to 60% OFF**",
        "details": """**New York City Hotel Deals** - Save up to 60% on Manhattan luxury hotels, Times Square stays, Brooklyn boutique hotels, and Midtown business accommodation.

🏨 **Hotel Discounts Available:**
• **Times Square Luxury Hotels**: 60% OFF weekend rates
• **Manhattan Boutique Hotels**: 55% discount on unique stays
• **Brooklyn Budget Hotels**: From $79/night with breakfast
• **Midtown Business Hotels**: 50% OFF corporate rates
• **Central Park View Hotels**: Premium locations discounted

📍 **Popular NYC Areas:**
Times Square | Midtown Manhattan | Downtown | Upper East Side | Brooklyn Heights

💎 **Deals Include:**
✅ Free breakfast at select hotels
✅ No resort fees
✅ Flexible cancellation
✅ Room upgrades available

🔍 **Search Keywords:** New York hotels, NYC accommodation, Manhattan luxury hotels, Times Square hotels, Brooklyn boutique hotels"""
    },
    "miami": {
        "title": "🌴 **Miami Beach Resorts - 60% Discount**",
        "details": """**Miami Beach Hotel Deals** - Up to 60% off South Beach luxury resorts, oceanfront hotels, and downtown Miami accommodation.

🏨 **Resort Discounts Available:**
• **South Beach Luxury Resorts**: 60% OFF oceanfront rooms
• **Miami Beach Art Deco Hotels**: 55% discount historic stays
• **Downtown Miami Hotels**: 50% OFF business rates
• **Brickell Luxury Hotels**: City views at discount prices
• **Coconut Grove Boutique**: 45% OFF tropical retreats

📍 **Popular Miami Areas:**
South Beach | Miami Beach | Downtown | Brickell | Coconut Grove

💎 **Deals Include:**
✅ Beach access included
✅ Pool and spa discounts
✅ Resort credit offers
✅ Free parking available

🔍 **Search Keywords:** Miami hotels, South Beach resorts, oceanfront hotels Miami, downtown Miami accommodation"""
    },
    "lasvegas": {
        "title": "🎰 **Las Vegas Strip Hotels - 60% OFF**",
        "details": """**Las Vegas Casino Hotel Deals** - Save 60% on Strip resorts, downtown casino hotels, and luxury suite accommodations.

🏨 **Casino Hotel Discounts:**
• **Strip Casino Resorts**: 60% OFF midweek rates
• **Luxury Suite Hotels**: 55% discount premium stays
• **Downtown Vintage Hotels**: 50% OFF classic experience
• **Off-Strip Budget Hotels**: From $59/night family rates
• **Suite Accommodation**: Kitchen included savings

📍 **Popular Vegas Areas:**
Las Vegas Strip | Downtown | Summerlin | Henderson | Off-Strip

💎 **Deals Include:**
✅ Free show tickets
✅ Dining credit offers
✅ No resort fees
✅ Suite upgrades available

🔍 **Search Keywords:** Las Vegas hotels, Strip casino hotels, downtown Vegas accommodation, luxury suite hotels"""
    },
    "orlando": {
        "title": "🏰 **Orlando Theme Park Hotels - 60% OFF**",
        "details": """**Orlando Hotel Deals** - Up to 60% discount on Disney area hotels, Universal Studios resorts, and family vacation accommodation.

🏨 **Theme Park Hotel Discounts:**
• **Disney World Hotels**: 60% OFF park packages
• **Universal Studios Resorts**: 55% discount early admission
• **International Drive Hotels**: 50% OFF family suites
• **Lake Buena Vista Resorts**: Water park access included
• **Kissimmee Budget Hotels**: Value packages available

📍 **Popular Orlando Areas:**
Disney World Area | International Drive | Lake Buena Vista | Kissimmee | Universal Area

💎 **Deals Include:**
✅ Park ticket bundles
✅ Free breakfast options
✅ Kids stay free offers
✅ Shuttle service included

🔍 **Search Keywords:** Orlando hotels, Disney area accommodation, Universal Studios hotels, family hotels Orlando"""
    },
    "luxury": {
        "title": "⭐ **Luxury Hotel Deals - 60% OFF Premium**",
        "details": """**Luxury Hotel Discounts** - Save up to 60% on 5-star hotels, premium resorts, and boutique luxury accommodation.

🏨 **Luxury Accommodation Deals:**
• **5-Star Luxury Hotels**: 60% OFF premium rates
• **Boutique Design Hotels**: 55% discount unique stays
• **All-Inclusive Resorts**: 50% OFF package deals
• **Spa Retreat Hotels**: Wellness packages discounted
• **Designer Suite Hotels**: Luxury amenities included

💎 **Luxury Features:**
✅ Butler service available
✅ Premium toiletries included
✅ Fine dining restaurant access
✅ Spa and wellness facilities
✅ Concierge services

🔍 **Search Keywords:** luxury hotels, 5-star hotels, boutique hotels, premium accommodation, luxury resort deals"""
    },
    "budget": {
        "title": "💰 **Budget Hotel Deals - Under $80/Night**",
        "details": """**Budget Accommodation Discounts** - Affordable hotel deals under $80 per night with up to 60% savings on comfortable stays.

🏨 **Budget Hotel Discounts:**
• **Economy Hotels**: From $49/night with 60% OFF
• **Motel Accommodation**: 55% discount roadside stays
• **Hostel Discounts**: Dorm beds from $25/night
• **Extended Stay Hotels**: Weekly rates available
• **Budget Chain Hotels**: Brand discounts applied

💎 **Budget Features:**
✅ Free WiFi included
✅ Basic breakfast options
✅ Parking available
✅ 24-hour front desk
✅ Pet friendly options

🔍 **Search Keywords:** budget hotels, cheap accommodation, affordable hotels, economy stays, discount hotels"""
    }
}

@bot.message_handler(commands=['start'])
def start_command(message):
    if message is None:
        return

    # Add user to broadcast list
    user_id = message.from_user.id
    broadcast_users.add(user_id)
    
    # Reset chat state
    user_chat_states[user_id] = 'started'

    # Create an inline keyboard
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    
    # City Hotel Deals
    keyboard.add(types.InlineKeyboardButton("🗽 New York 60% OFF", callback_data="acc_newyork"))
    keyboard.add(
        types.InlineKeyboardButton("🌴 Miami 60% OFF", callback_data="acc_miami"),
        types.InlineKeyboardButton("🎰 Vegas 60% OFF", callback_data="acc_lasvegas")
    )
    keyboard.add(
        types.InlineKeyboardButton("🏰 Orlando 60% OFF", callback_data="acc_orlando"),
        types.InlineKeyboardButton("🏙️ Chicago 60% OFF", callback_data="acc_chicago")
    )
    
    # Hotel Types
    keyboard.add(types.InlineKeyboardButton("⭐ Luxury 60% OFF", callback_data="acc_luxury"))
    keyboard.add(
        types.InlineKeyboardButton("💰 Budget 60% OFF", callback_data="acc_budget"),
        types.InlineKeyboardButton("🏠 Vacation Rentals", callback_data="acc_vacation")
    )
    
    # Contact & Channel
    button_channel = types.InlineKeyboardButton("📢 Join Deals Channel", url="https://t.me/flights_half_off")
    button_contact = types.InlineKeyboardButton("💬 Contact Admin", url="https://t.me/yrfrnd_spidy")
    keyboard.add(button_channel, button_contact)

    # Short, simple welcome message
    message_text = (
        "🏨 **Accommodation Deals - Up to 60% OFF**\n\n"
        "Find amazing hotel discounts & vacation rental offers.\n\n"
        "Select a category below for detailed deals:"
    )

    bot.send_message(message.chat.id, message_text, reply_markup=keyboard, parse_mode='Markdown')

# ===== ACCOMMODATION DETAIL HANDLERS =====
@bot.callback_query_handler(func=lambda call: call.data.startswith('acc_'))
def accommodation_handler(call):
    """Handle accommodation category clicks - show detailed info"""
    user_id = call.from_user.id
    option = call.data.replace('acc_', '')
    
    if option in ACCOMMODATION_OFFERS:
        offer = ACCOMMODATION_OFFERS[option]
        
        # Detailed response
        response = f"{offer['title']}\n\n{offer['details']}"
        
        # Action buttons
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📢 Join for Booking", url="https://t.me/flights_half_off"),
            types.InlineKeyboardButton("💬 Contact for Deal", url="https://t.me/yrfrnd_spidy")
        )
        markup.add(
            types.InlineKeyboardButton("🏨 More Hotel Deals", callback_data="acc_more"),
            types.InlineKeyboardButton("🏠 Back to Menu", callback_data="acc_back")
        )
        
        bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')
    
    elif option == "chicago":
        response = """🏙️ **Chicago Hotels - Up to 60% OFF**

**Chicago Downtown Hotel Deals** - Save up to 60% on Magnificent Mile luxury hotels, Loop business accommodation, and River North boutique stays.

🏨 **Chicago Hotel Discounts:**
• **Magnificent Mile Luxury**: 60% OFF premium rates
• **Loop Business Hotels**: 55% discount corporate stays
• **River North Boutique**: 50% OFF unique hotels
• **Gold Coast Luxury**: 45% OFF historic stays
• **Wrigleyville Budget**: Game day packages

📍 **Popular Chicago Areas:**
Magnificent Mile | The Loop | River North | Gold Coast | Lincoln Park

💎 **Deals Include:**
✅ Free museum passes
✅ City view upgrades
✅ Late check-out options
✅ Business amenities

🔍 **Search Keywords:** Chicago hotels, downtown Chicago accommodation, Magnificent Mile hotels, business hotels Chicago"""
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📢 Join for Booking", url="https://t.me/flights_half_off"),
            types.InlineKeyboardButton("💬 Contact for Deal", url="https://t.me/yrfrnd_spidy")
        )
        
        bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')
    
    elif option == "vacation":
        response = """🏠 **Vacation Rentals - Up to 60% OFF**

**Vacation Rental Deals** - Save up to 60% on apartment stays, condo rentals, beachfront villas, and mountain cabin accommodation.

🏡 **Vacation Rental Discounts:**
• **Beachfront Condos**: 60% OFF ocean view properties
• **City Apartments**: 55% discount downtown stays
• **Mountain Cabins**: 50% OFF getaway retreats
• **Luxury Villas**: 45% OFF private pool homes
• **Lake House Rentals**: Waterfront savings

🔑 **Rental Platform Deals:**
• **Airbnb**: 40% OFF first booking
• **VRBO**: 35% discount vacation homes
• **Booking.com**: Genius level discounts
• **HomeAway**: Last minute rental deals

💎 **Benefits of Rentals:**
✅ More space for families/groups
✅ Kitchen facilities available
✅ Privacy and exclusive use
✅ Often cheaper than hotels

🔍 **Search Keywords:** vacation rentals, apartment hotels, condo rentals, beachfront villas, mountain cabins"""
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📢 Join for Booking", url="https://t.me/flights_half_off"),
            types.InlineKeyboardButton("💬 Contact for Deal", url="https://t.me/yrfrnd_spidy")
        )
        
        bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')
    
    elif option == "more":
        # Show all categories
        response = """🏨 **All Accommodation Deals - Up to 60% OFF**

📍 **Popular Hotel Destinations:**
• New York City Hotels - Times Square, Manhattan, Brooklyn
• Miami Beach Resorts - South Beach, Oceanfront, Downtown
• Las Vegas Strip Hotels - Casino resorts, Luxury suites
• Orlando Theme Park Hotels - Disney, Universal, Family stays
• Chicago Downtown Hotels - Magnificent Mile, Loop, River North

🏨 **Accommodation Types:**
• Luxury Hotels - 5-star properties, premium amenities
• Budget Hotels - Affordable stays, value accommodation
• Vacation Rentals - Apartments, condos, vacation homes

💰 **Discount Categories:**
• Last Minute Hotel Deals
• Weekend Getaway Packages
• Extended Stay Discounts
• Family Vacation Bundles
• Business Travel Rates

💡 **Tip:** Book directly through our channel for best rates!"""
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("🗽 New York", callback_data="acc_newyork"),
            types.InlineKeyboardButton("🌴 Miami", callback_data="acc_miami")
        )
        markup.add(
            types.InlineKeyboardButton("🎰 Vegas", callback_data="acc_lasvegas"),
            types.InlineKeyboardButton("🏰 Orlando", callback_data="acc_orlando")
        )
        markup.add(types.InlineKeyboardButton("📢 Join Channel", url="https://t.me/flights_half_off"))
        
        bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')
    
    elif option == "back":
        # Go back to start
        start_command(call.message)

# ===== BROADCAST FEATURE =====
@bot.message_handler(commands=['broadcast'])
def broadcast_command(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ This command is for admin only!")
        return
    
    if len(broadcast_users) == 0:
        bot.reply_to(message, "❌ No users in broadcast list!")
        return
    
    # Ask admin for broadcast message
    msg = bot.send_message(
        ADMIN_ID,
        f"📢 Broadcast to {len(broadcast_users)} users\n\nPlease enter your broadcast message:"
    )
    bot.register_next_step_handler(msg, process_broadcast_message)

def process_broadcast_message(message):
    # Prevent multiple broadcasts from same message
    if hasattr(message, 'is_broadcast_processed') and message.is_broadcast_processed:
        return
    message.is_broadcast_processed = True
    
    broadcast_text = message.text
    users = list(broadcast_users)
    success_count = 0
    fail_count = 0
    
    # Send initial status
    status_msg = bot.send_message(ADMIN_ID, f"📤 Starting broadcast to {len(users)} users...")
    
    for user_id in users:
        try:
            bot.send_message(user_id, f"🏨 **New Hotel Deal Alert** 🏨\n\n{broadcast_text}")
            success_count += 1
        except Exception as e:
            fail_count += 1
            print(f"Failed to send to {user_id}: {e}")
    
    # Update status
    bot.edit_message_text(
        f"✅ Broadcast Completed!\n\n"
        f"✅ Successful: {success_count}\n"
        f"❌ Failed: {fail_count}\n"
        f"📊 Total Users: {len(users)}",
        ADMIN_ID,
        status_msg.message_id
    )

@bot.message_handler(commands=['stats'])
def stats_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    user_count = len(broadcast_users)
    bot.send_message(ADMIN_ID, f"📊 Bot Statistics:\n\n👥 Total Users: {user_count}")

# ===== CHAT HANDLERS =====
@bot.message_handler(func=lambda message: message.text and message.text.lower().startswith('hello'))
def hello_handler(message):
    user = message.from_user
    user_id = user.id
    
    # Add user to broadcast list
    broadcast_users.add(user_id)
    
    # Set chat state
    user_chat_states[user_id] = 'waiting_for_admin'
    
    user_info = f"User: {user.first_name} {user.last_name or ''} (@{user.username or 'No username'})"
    
    # Store message info for admin replies
    user_messages[message.message_id] = {
        'user_id': user.id,
        'user_info': user_info,
        'original_message': message.text
    }
    
    # Forward the "hello" message to admin with reply button
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("📨 Reply", callback_data=f"reply_{message.message_id}"))
    
    forward_text = f"👋 Someone said hello!\n\n{user_info}\nUser ID: {user.id}\n\nMessage: '{message.text}'"
    
    bot.send_message(ADMIN_ID, forward_text, reply_markup=keyboard)
    
    # Reply to the user ONLY ONCE
    bot.reply_to(message, "👋 Hello! I've notified the admin. They'll get back to you soon!\n\nYou can continue chatting here and the admin will see your messages.")

@bot.callback_query_handler(func=lambda call: call.data.startswith('reply_'))
def reply_callback_handler(call):
    message_id = int(call.data.split('_')[1])
    
    if message_id in user_messages:
        user_data = user_messages[message_id]
        
        # Ask admin to type the reply
        msg = bot.send_message(ADMIN_ID, f"💬 Type your reply for user {user_data['user_info']}:")
        
        # Register next step handler for admin's reply
        bot.register_next_step_handler(msg, process_admin_reply, user_data['user_id'])
    else:
        bot.answer_callback_query(call.id, "❌ Message data expired")

def process_admin_reply(message, user_id):
    try:
        # Send admin's reply to the user
        bot.send_message(user_id, f"📨 Message from admin:\n\n{message.text}")
        bot.reply_to(message, "✅ Reply sent successfully!")
    except Exception as e:
        bot.reply_to(message, f"❌ Failed to send reply: {str(e)}")

# Handler for forwarding user messages to admin (enable chatting)
@bot.message_handler(func=lambda message: True)
def all_messages_handler(message):
    user = message.from_user
    user_id = user.id
    
    # Don't process admin's own messages
    if user_id == ADMIN_ID:
        return
    
    # Add user to broadcast list
    broadcast_users.add(user_id)
    
    # If user has started a chat (said hello before), forward their messages to admin
    if user_chat_states.get(user_id) == 'waiting_for_admin' and message.text:
        user_info = f"User: {user.first_name} {user.last_name or ''} (@{user.username or 'No username'})"
        
        # Store message info
        user_messages[message.message_id] = {
            'user_id': user_id,
            'user_info': user_info,
            'original_message': message.text
        }
        
        # Forward message to admin with reply button
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("📨 Reply", callback_data=f"reply_{message.message_id}"))
        
        forward_text = f"💬 New message from user:\n\n{user_info}\nUser ID: {user_id}\n\nMessage: '{message.text}'"
        
        bot.send_message(ADMIN_ID, forward_text, reply_markup=keyboard)
        
        # Let user know their message was received (only if it's not a hello message)
        if not message.text.lower().startswith('hello'):
            bot.reply_to(message, "✅ Message received! Admin will reply soon.")

@app.route('/')
def home():
    return "🏨 Accommodation Bot is running!"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = request.get_data().decode("utf-8")
    update_obj = telebot.types.Update.de_json(update)
    bot.process_new_updates([update_obj])
    return "OK", 200

if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("⚠️ TELEGRAM_BOT_TOKEN environment variable is required")
    
    # Set webhook
    try:
        bot.remove_webhook()
        # For Replit/Render deployment
        replit_domain = os.environ.get("REPLIT_DEV_DOMAIN")
        render_domain = os.environ.get("RENDER_EXTERNAL_URL")
        
        if replit_domain:
            webhook_url = f"https://{replit_domain}/{TOKEN}"
        elif render_domain:
            webhook_url = f"{render_domain}/{TOKEN}"
        else:
            webhook_url = None
            
        if webhook_url:
            bot.set_webhook(url=webhook_url)
            print(f"✅ Webhook set to: {webhook_url}")
        else:
            print("⚠️ No domain found for webhook")
            
    except Exception as e:
        print(f"⚠️ Webhook setup error: {e}")
    
    print("🚀 Accommodation Bot is running!")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
