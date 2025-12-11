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

# ===== USA HOTELS DATABASE =====
USA_CITY_HOTELS = {
    "New York": {
        "title": "🏙️ **New York City Hotels**",
        "hotels": [
            "**Times Square Hotels** - From $199/night",
            "**Manhattan Luxury** - 30% Discount Available", 
            "**Brooklyn Budget** - From $89/night",
            "**Midtown Business** - Free Breakfast",
            "**Central Park View** - Premium Location"
        ],
        "areas": ["Times Square", "Midtown", "Downtown", "Upper East Side", "Brooklyn"],
        "deals": ["50% Off Weekends", "Free Upgrade", "Parking Included"]
    },
    "Los Angeles": {
        "title": "🌴 **Los Angeles Accommodation**", 
        "hotels": [
            "**Hollywood Luxury** - From $179/night",
            "**Beverly Hills 5-Star** - Exclusive Rates",
            "**Santa Monica Beach** - Ocean Views",
            "**Downtown LA** - 25% Discount",
            "**Universal Area** - Family Packages"
        ],
        "areas": ["Hollywood", "Beverly Hills", "Santa Monica", "Downtown LA", "West Hollywood"],
        "deals": ["Beach Access Included", "Free Parking", "Early Check-in"]
    },
    "Miami": {
        "title": "🌊 **Miami Beach Resorts**",
        "hotels": [
            "**South Beach Luxury** - From $229/night",
            "**Oceanfront Hotels** - Direct Beach Access",
            "**Downtown Miami** - Business Rates",
            "**Coconut Grove** - Tropical Setting",
            "**Brickell Luxury** - City Views"
        ],
        "areas": ["South Beach", "Miami Beach", "Downtown", "Brickell", "Coconut Grove"],
        "deals": ["Free Beach Chairs", "Pool Access", "Resort Credit"]
    },
    "Las Vegas": {
        "title": "🎰 **Las Vegas Strip Hotels**",
        "hotels": [
            "**Casino Hotels** - From $79/night",
            "**Luxury Resorts** - Suite Upgrades",
            "**Downtown Vegas** - Vintage Experience",
            "**Off-Strip Budget** - Family Friendly",
            "**Suite Hotels** - Kitchen Included"
        ],
        "areas": ["Las Vegas Strip", "Downtown", "Summerlin", "Henderson"],
        "deals": ["Free Show Tickets", "Dining Credit", "No Resort Fees"]
    },
    "Orlando": {
        "title": "🏰 **Orlando Theme Park Hotels**",
        "hotels": [
            "**Disney World Area** - Shuttle to Parks",
            "**Universal Studios** - Early Admission",
            "**International Drive** - Family Suites",
            "**Lake Buena Vista** - Water Park Access",
            "**Kissimmee Budget** - Value Packages"
        ],
        "areas": ["Disney World Area", "International Drive", "Lake Buena Vista", "Kissimmee"],
        "deals": ["Park Ticket Bundles", "Free Breakfast", "Kids Stay Free"]
    },
    "Chicago": {
        "title": "🏙️ **Chicago Downtown Hotels**",
        "hotels": [
            "**Magnificent Mile** - From $159/night",
            "**Loop Business** - Corporate Discounts",
            "**River North** - 20% Weekend Discount",
            "**Wrigleyville** - Game Day Packages",
            "**O'Hare Airport** - Free Shuttle"
        ],
        "areas": ["Magnificent Mile", "The Loop", "River North", "Gold Coast"],
        "deals": ["Free Museum Pass", "City View Upgrade", "Late Check-out"]
    }
}

# ===== HOTEL TYPE DESCRIPTIONS =====
HOTEL_TYPES = {
    "luxury": {
        "title": "⭐ **Luxury Hotels**",
        "description": "5-star hotels with premium amenities, fine dining, spa services, and exceptional service.",
        "brands": ["Four Seasons", "Ritz-Carlton", "Waldorf Astoria", "St. Regis", "Mandarin Oriental"],
        "features": ["Butler Service", "Premium Toiletries", "High-End Dining", "Spa Access", "Concierge"]
    },
    "budget": {
        "title": "💰 **Budget Hotels**",
        "description": "Affordable accommodation with basic amenities, comfortable rooms, and convenient locations.",
        "brands": ["Motel 6", "Red Roof Inn", "Super 8", "Days Inn", "Travelodge"],
        "features": ["Free WiFi", "Basic Breakfast", "Parking Available", "24-Hour Front Desk", "Pet Friendly"]
    },
    "vacation": {
        "title": "🏠 **Vacation Rentals**",
        "description": "Apartments, condos, and vacation homes with more space and home-like amenities.",
        "brands": ["Airbnb", "VRBO", "Booking.com", "HomeAway", "Vacasa"],
        "features": ["Full Kitchen", "More Space", "Privacy", "Washer/Dryer", "Living Area"]
    }
}

@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    broadcast_users.add(user_id)

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    
    # City Selection
    keyboard.add(types.InlineKeyboardButton("🗽 New York", callback_data="city_ny"))
    keyboard.add(
        types.InlineKeyboardButton("🌴 Los Angeles", callback_data="city_la"),
        types.InlineKeyboardButton("🌊 Miami", callback_data="city_miami")
    )
    keyboard.add(
        types.InlineKeyboardButton("🎰 Las Vegas", callback_data="city_vegas"),
        types.InlineKeyboardButton("🏰 Orlando", callback_data="city_orlando")
    )
    keyboard.add(types.InlineKeyboardButton("🏙️ Chicago", callback_data="city_chicago"))
    
    # Hotel Types
    keyboard.add(types.InlineKeyboardButton("⭐ Luxury", callback_data="type_luxury"))
    keyboard.add(
        types.InlineKeyboardButton("💰 Budget", callback_data="type_budget"),
        types.InlineKeyboardButton("🏠 Rentals", callback_data="type_vacation")
    )
    
    # Actions
    keyboard.add(
        types.InlineKeyboardButton("🔍 Search", callback_data="search"),
        types.InlineKeyboardButton("📢 Join Deals", url="https://t.me/flights_half_off")
    )
    keyboard.add(types.InlineKeyboardButton("💬 Contact", url="https://t.me/yrfrnd_spidy"))

    # Clean minimal message
    message_text = f"""🏨 **Hotel Finder**

Hi {message.from_user.first_name}! Find hotels in major US cities.

Select your destination or accommodation type:"""

    bot.send_message(message.chat.id, message_text, reply_markup=keyboard, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id
    
    if call.data.startswith('city_'):
        city_code = call.data.replace('city_', '')
        city_map = {
            'ny': 'New York',
            'la': 'Los Angeles',
            'miami': 'Miami',
            'vegas': 'Las Vegas',
            'orlando': 'Orlando',
            'chicago': 'Chicago'
        }
        
        if city_code in city_map:
            city = city_map[city_code]
            data = USA_CITY_HOTELS[city]
            
            # Detailed city information
            response = f"{data['title']}\n\n"
            response += "**Available Hotels:**\n" + "\n".join(data['hotels']) + "\n\n"
            response += f"**Popular Areas:** {', '.join(data['areas'])}\n\n"
            response += f"**Current Deals:** {', '.join(data['deals'])}\n\n"
            response += "**Best For:**\n"
            
            # Add best for suggestions
            if city == "New York":
                response += "• Business travelers\n• Tourists\n• Shopping trips\n• Broadway shows"
            elif city == "Los Angeles":
                response += "• Celebrity sightings\n• Beach vacations\n• Business meetings\n• Hollywood tours"
            elif city == "Miami":
                response += "• Beach holidays\n• Nightlife\n• Business conferences\n• Romantic getaways"
            elif city == "Las Vegas":
                response += "• Gambling\n• Entertainment\n• Conventions\n• Weekend trips"
            elif city == "Orlando":
                response += "• Family vacations\n• Theme park visits\n• Kids activities\n• Group trips"
            elif city == "Chicago":
                response += "• Business travel\n• Architecture tours\n• Food experiences\n• Sports events"
            
            response += "\n\n**Booking Tip:** Mid-week stays are often cheaper."
            
            # Add action buttons
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                types.InlineKeyboardButton("⭐ Luxury Options", callback_data="type_luxury"),
                types.InlineKeyboardButton("💰 Budget Options", callback_data="type_budget")
            )
            markup.add(
                types.InlineKeyboardButton("📢 Join for Rates", url="https://t.me/flights_half_off"),
                types.InlineKeyboardButton("💬 Contact for Booking", url="https://t.me/yrfrnd_spidy")
            )
            
            bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')
    
    elif call.data.startswith('type_'):
        type_code = call.data.replace('type_', '')
        
        if type_code in HOTEL_TYPES:
            data = HOTEL_TYPES[type_code]
            
            response = f"{data['title']}\n\n"
            response += f"{data['description']}\n\n"
            response += "**Popular Brands:**\n" + ", ".join(data['brands']) + "\n\n"
            response += "**Common Features:**\n" + "• " + "\n• ".join(data['features']) + "\n\n"
            
            # Add price range
            if type_code == "luxury":
                response += "**Price Range:** $200-$800+/night\n\n"
                response += "**Best For:**\n• Business executives\n• Honeymooners\n• Luxury travelers\n• Special occasions"
            elif type_code == "budget":
                response += "**Price Range:** $50-$150/night\n\n"
                response += "**Best For:**\n• Budget travelers\n• Students\n• Road trippers\n• Short stays"
            elif type_code == "vacation":
                response += "**Price Range:** $100-$500/night\n\n"
                response += "**Best For:**\n• Families\n• Groups\n• Extended stays\n• Remote workers"
            
            response += "\n\n**Tip:** Always check for cleaning fees on rentals."
            
            # Add action buttons
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                types.InlineKeyboardButton("🗽 New York", callback_data="city_ny"),
                types.InlineKeyboardButton("🌴 Los Angeles", callback_data="city_la")
            )
            markup.add(
                types.InlineKeyboardButton("📢 Join for Deals", url="https://t.me/flights_half_off"),
                types.InlineKeyboardButton("💬 Get Booking Help", url="https://t.me/yrfrnd_spidy")
            )
            
            bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')
    
    elif call.data == "search":
        response = """🔍 **Search Hotels**
        
**Popular Search Terms:**
• Hotels in New York under $150
• Miami beachfront hotels
• Las Vegas weekend deals
• Orlando Disney area hotels
• Chicago downtown luxury

**Search Tips:**
1. Specify your dates
2. Mention budget range
3. Include preferences (pool, breakfast, etc.)
4. Add number of guests

**Try searching:**
"New York hotels next weekend"
"Miami resorts with pool"
"Las Vegas suites for 2"
"Orlando family hotels"

Need help? Contact us directly!"""
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("💬 Contact for Search", url="https://t.me/yrfrnd_spidy"))
        
        bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')

# ===== ADMIN FUNCTIONS =====
@bot.message_handler(commands=['broadcast'])
def broadcast_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    if len(broadcast_users) == 0:
        bot.reply_to(message, "No users to broadcast to!")
        return
    
    msg = bot.send_message(
        ADMIN_ID, 
        f"Broadcast to {len(broadcast_users)} users\nEnter hotel deal message:"
    )
    bot.register_next_step_handler(msg, process_broadcast)

def process_broadcast(message):
    if hasattr(message, 'processed'):
        return
    message.processed = True
    
    users = list(broadcast_users)
    success = 0
    fail = 0
    
    status = bot.send_message(ADMIN_ID, "Sending broadcast...")
    
    for user_id in users:
        try:
            bot.send_message(user_id, f"🏨 **New Hotel Deal**\n\n{message.text}")
            success += 1
        except:
            fail += 1
    
    bot.edit_message_text(
        f"✅ Broadcast complete!\nSuccess: {success}\nFailed: {fail}",
        ADMIN_ID,
        status.message_id
    )

@bot.message_handler(commands=['stats'])
def stats_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    bot.send_message(ADMIN_ID, f"👥 Total users: {len(broadcast_users)}")

# ===== CHAT HANDLING =====
@bot.message_handler(func=lambda message: message.text and message.text.lower().startswith('hello'))
def hello_handler(message):
    user_id = message.from_user.id
    broadcast_users.add(user_id)
    
    user_info = f"User: {message.from_user.first_name} (@{message.from_user.username or 'no username'})"
    user_messages[message.message_id] = {
        'user_id': user_id,
        'user_info': user_info
    }
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📨 Reply", callback_data=f"admin_reply_{message.message_id}"))
    
    bot.send_message(
        ADMIN_ID,
        f"👋 New user hello\n{user_info}\nID: {user_id}\n\nMessage: {message.text}",
        reply_markup=markup
    )
    
    bot.reply_to(message, "Hello! I can help you find hotels in major US cities. Use /start to begin!")

@bot.callback_query_handler(func=lambda call: call.data.startswith('admin_reply_'))
def admin_reply_handler(call):
    message_id = int(call.data.replace('admin_reply_', ''))
    
    if message_id in user_messages:
        user_data = user_messages[message_id]
        msg = bot.send_message(ADMIN_ID, f"Reply to {user_data['user_info']}:")
        bot.register_next_step_handler(msg, send_admin_reply, user_data['user_id'])
    else:
        bot.answer_callback_query(call.id, "Message expired")

def send_admin_reply(message, user_id):
    try:
        bot.send_message(user_id, f"💬 From admin:\n\n{message.text}")
        bot.reply_to(message, "Reply sent!")
    except:
        bot.reply_to(message, "Failed to send reply")

@bot.message_handler(func=lambda message: True)
def all_messages(message):
    user_id = message.from_user.id
    broadcast_users.add(user_id)
    
    if user_id != ADMIN_ID and message.text:
        bot.reply_to(message, "Use /start to find hotels or say hello to chat with admin!")

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hotel Finder - USA Accommodation</title>
        <meta name="description" content="Find hotels in New York, Los Angeles, Miami, Las Vegas, Orlando, Chicago. Luxury, budget, and vacation rentals.">
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            .container { max-width: 600px; margin: 0 auto; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏨 Hotel Finder Bot</h1>
            <p>Find accommodation in major US cities</p>
            <p>Status: <strong style="color:green">✅ Active</strong></p>
        </div>
    </body>
    </html>
    """

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = request.get_data().decode("utf-8")
    update_obj = telebot.types.Update.de_json(update)
    bot.process_new_updates([update_obj])
    return "OK", 200

if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("Bot token required!")
    
    try:
        bot.remove_webhook()
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
            print(f"Webhook set: {webhook_url}")
        else:
            print("No domain for webhook")
            
    except Exception as e:
        print(f"Webhook error: {e}")
    
    print("Hotel bot running!")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
