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

# ===== SEO KEYWORDS DATABASE =====
SEO_KEYWORDS = {
    "travel": [
        "flight discounts", "cheap flights", "discounted hotels", "car rental deals",
        "helicopter tours cheap", "airfare discounts", "budget travel", "travel savings"
    ],
    "lifestyle": [
        "restaurant discounts", "event ticket deals", "theme park discounts", "grocery savings",
        "dining offers", "entertainment deals", "amusement park discounts", "food coupons"
    ],
    "essentials": [
        "train pass discounts", "bill payment savings", "school fee discounts", "hospital bill savings",
        "utility bill discounts", "education fee deals", "medical bill savings", "transportation discounts"
    ],
    "discounts": [
        "50% off deals", "half price offers", "exclusive discounts", "limited time offers",
        "special promotions", "discount coupons", "money saving deals", "best price guaranteed"
    ]
}

# ===== SEO-OPTIMIZED RESPONSE GENERATOR =====
def generate_seo_response(category="general"):
    """Generate SEO-rich responses based on category"""
    
    responses = {
        "travel": """✈️ **FLIGHT & TRAVEL DISCOUNTS - Save Up to 50% on All Travel Services**
        
💰 **TRAVEL SAVINGS AVAILABLE:**
• **Flight Ticket Discounts**: Domestic & International Airfare
• **Hotel Booking Deals**: Luxury & Budget Accommodation
• **Car Rental Savings**: Economy to Premium Vehicles
• **Helicopter Tour Discounts**: Scenic Flight Experiences

🔍 **SEO TIP**: Search "cheap flights [destination]" for best results!""",
        
        "lifestyle": """🎡 **LIFESTYLE & ENTERTAINMENT DISCOUNTS - 50% Off Dining & Entertainment**
        
💰 **LIFESTYLE SAVINGS:**
• **Restaurant Dining Discounts**: Fine Dining to Casual Eats
• **Event Ticket Deals**: Concerts, Sports & Shows
• **Theme Park Discounts**: Six Flags & Amusement Parks
• **Grocery Shopping Savings**: Daily Essentials Discounts

🔍 **SEO TIP**: Search "restaurant deals near me" for local savings!""",
        
        "essentials": """💳 **ESSENTIAL SERVICE DISCOUNTS - Save on Bills & Necessities**
        
💰 **ESSENTIAL SAVINGS:**
• **Train Pass Discounts**: Commuter & Travel Passes
• **Bill Payment Savings**: Utilities, Phone, Internet
• **School Fee Discounts**: Education Cost Reduction
• **Hospital Bill Savings**: Medical Expense Discounts

🔍 **SEO TIP**: Search "bill payment discounts [service]" for savings!""",
        
        "general": """🟡 **SPIDY'S WORLD - Trusted Discounts on 100+ Services**
        
🔍 **SEO-OPTIMIZED SERVICE CATEGORIES:**

✈️ **TRAVEL DISCOUNTS:**
• Flight ticket savings • Hotel booking deals • Car rental discounts
• Helicopter tour offers • Vacation package savings

🍽️ **LIFESTYLE DISCOUNTS:**
• Restaurant dining deals • Event ticket savings • Theme park discounts
• Grocery shopping offers • Entertainment package deals

🚆 **ESSENTIAL DISCOUNTS:**
• Train pass savings • Bill payment discounts • School fee reductions
• Hospital bill savings • Utility payment discounts

💰 **WHY CHOOSE US:**
✅ 50% Discounts on All Services
✅ Trusted & Verified Deals
✅ One-Stop Discount Platform
✅ Money-Back Guarantee"""
    }
    
    return responses.get(category, responses["general"])

@bot.message_handler(commands=['start'])
def start_command(message):
    if message is None:
        return

    # Add user to broadcast list
    user_id = message.from_user.id
    broadcast_users.add(user_id)
    
    # Reset chat state
    user_chat_states[user_id] = 'started'

    # Create an inline keyboard with 3 buttons
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    button_channel = types.InlineKeyboardButton("🟡 Join Channel", url="https://t.me/flights_half_off")
    button_website = types.InlineKeyboardButton("🌐 Visit Website", url="https://rb.gy/jrr1lb")
    button_contact = types.InlineKeyboardButton("💬 Contact Admin", url="https://t.me/yrfrnd_spidy")
    
    # Add SEO category buttons
    keyboard.add(button_channel, button_website, button_contact)
    
    # SEO-optimized main categories
    keyboard.add(
        types.InlineKeyboardButton("✈️ Travel Discounts", callback_data="seo_travel"),
        types.InlineKeyboardButton("🍽️ Lifestyle Deals", callback_data="seo_lifestyle"),
        types.InlineKeyboardButton("🚆 Essential Savings", callback_data="seo_essentials")
    )

    # SEO-OPTIMIZED WELCOME MESSAGE
    message_text = (
        "🟡 **SPIDY'S WORLD - Trusted Discounts & Savings Platform** 🟡\n\n"
        
        "🔍 **EXCLUSIVE 50% DISCOUNTS ON:**\n\n"
        
        "✈️ **TRAVEL & TRANSPORTATION SAVINGS:**\n"
        "• **Flight Ticket Discounts**: Domestic & International Airfare Deals\n"
        "• **Hotel Booking Savings**: Luxury & Budget Accommodation Discounts\n"
        "• **Car Rental Deals**: Economy to Premium Vehicle Discounts\n"
        "• **Helicopter Tour Offers**: Scenic Flight Experience Savings\n\n"
        
        "🍽️ **LIFESTYLE & ENTERTAINMENT DISCOUNTS:**\n"
        "• **Restaurant Dining Deals**: Fine Dining to Casual Eats Savings\n"
        "• **Event Ticket Discounts**: Concerts, Sports & Show Ticket Offers\n"
        "• **Theme Park Savings**: Six Flags & Amusement Park Discounts\n"
        "• **Grocery Shopping Discounts**: Daily Essentials Cost Reduction\n\n"
        
        "🚆 **ESSENTIAL SERVICE SAVINGS:**\n"
        "• **Train Pass Discounts**: Commuter & Travel Pass Deals\n"
        "• **Bill Payment Savings**: Utilities, Phone & Internet Discounts\n"
        "• **School Fee Reductions**: Education Cost Savings\n"
        "• **Hospital Bill Discounts**: Medical Expense Reductions\n\n"
        
        "💰 **WHY TRUST OUR DISCOUNTS:**\n"
        "✅ **Verified Discounts** - All Deals 100% Authentic\n"
        "✅ **50% Savings Guarantee** - Half Price on All Services\n"
        "✅ **One-Platform Solution** - 100+ Services Available\n"
        "✅ **24/7 Support** - Instant Assistance Available\n\n"
        
        "🔍 **SEO TIP**: Search for specific discounts like 'flight discounts NYC' or 'restaurant deals near me'\n\n"
        
        "💡 **GET STARTED:**\n"
        "1. Join our official channel for daily discount alerts\n"
        "2. Browse categories below for specific savings\n"
        "3. Contact admin for personalized discount assistance\n\n"
        
        "🎯 **BEST FOR**: Budget travelers, savvy shoppers, cost-conscious families, students, smart consumers\n\n"
        
        "💎 **Money-Saving Tip**: Combine multiple discounts for maximum savings!\n\n"
        
        "With trust & savings,\n"
        "**Spidy's World Team**"
    )

    bot.send_message(message.chat.id, message_text, reply_markup=keyboard, parse_mode='Markdown')

# ===== SEO CATEGORY HANDLERS =====
@bot.callback_query_handler(func=lambda call: call.data.startswith('seo_'))
def seo_category_handler(call):
    """Handle SEO category selections"""
    category = call.data.replace('seo_', '')
    
    if category in ["travel", "lifestyle", "essentials"]:
        response = generate_seo_response(category)
        
        # Add call-to-action buttons
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            types.InlineKeyboardButton("🟡 Join Discount Channel", url="https://t.me/flights_half_off"),
            types.InlineKeyboardButton("💬 Contact for Deals", url="https://t.me/yrfrnd_spidy")
        )
        keyboard.add(
            types.InlineKeyboardButton("✈️ More Travel Deals", callback_data="seo_travel"),
            types.InlineKeyboardButton("💰 All Categories", callback_data="seo_all")
        )
        
        bot.send_message(call.message.chat.id, response, reply_markup=keyboard, parse_mode='Markdown')
    
    elif category == "all":
        # Show all categories
        response = generate_seo_response("general")
        bot.send_message(call.message.chat.id, response, parse_mode='Markdown')

# ===== BROADCAST FEATURE =====
@bot.message_handler(commands=['broadcast'])
def broadcast_command(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ This command is for admin only!")
        return
    
    if len(broadcast_users) == 0:
        bot.reply_to(message, "❌ No users in broadcast list!")
        return
    
    # Ask admin for broadcast message with SEO suggestion
    msg = bot.send_message(
        ADMIN_ID, 
        f"📢 **BROADCAST TO {len(broadcast_users)} USERS**\n\n"
        f"💡 **SEO TIP**: Include keywords like:\n"
        f"• '50% off deals'\n• 'exclusive discounts'\n• 'limited time offer'\n• 'special promotion'\n\n"
        f"📝 Please enter your broadcast message:"
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
    
    # SEO-optimized broadcast prefix
    seo_prefix = "🎯 **EXCLUSIVE DISCOUNT ALERT** 🎯\n\n"
    
    # Send initial status
    status_msg = bot.send_message(ADMIN_ID, f"📤 **STARTING BROADCAST**\n\nDelivering discounts to {len(users)} users...")
    
    for user_id in users:
        try:
            # Add SEO-optimized message
            full_message = seo_prefix + broadcast_text + "\n\n💎 **Limited Time Offer - Act Fast!**"
            bot.send_message(user_id, full_message)
            success_count += 1
        except Exception as e:
            fail_count += 1
            print(f"Failed to send to {user_id}: {e}")
    
    # Update status with SEO context
    bot.edit_message_text(
        f"✅ **BROADCAST COMPLETED!** ✅\n\n"
        f"📊 **PERFORMANCE METRICS:**\n"
        f"• ✅ Successful Deliveries: {success_count}\n"
        f"• ❌ Failed Deliveries: {fail_count}\n"
        f"• 👥 Total Audience: {len(users)}\n"
        f"• 📈 Reach Rate: {(success_count/len(users)*100):.1f}%\n\n"
        f"💡 **SEO IMPACT**: Discount message delivered to {success_count} potential customers",
        ADMIN_ID,
        status_msg.message_id,
        parse_mode='Markdown'
    )

@bot.message_handler(commands=['stats'])
def stats_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    user_count = len(broadcast_users)
    
    # SEO-optimized stats message
    stats_text = (
        f"📊 **BOT ANALYTICS DASHBOARD** 📊\n\n"
        f"👥 **USER ENGAGEMENT:**\n"
        f"• Total Active Users: {user_count}\n"
        f"• Broadcast Reach: {user_count} potential customers\n"
        f"• SEO Keywords Tracked: {sum(len(v) for v in SEO_KEYWORDS.values())}\n\n"
        
        f"🎯 **DISCOUNT CATEGORIES COVERED:**\n"
        f"• ✈️ Travel & Flights: {len(SEO_KEYWORDS['travel'])} keywords\n"
        f"• 🍽️ Lifestyle & Dining: {len(SEO_KEYWORDS['lifestyle'])} keywords\n"
        f"• 🚆 Essentials & Bills: {len(SEO_KEYWORDS['essentials'])} keywords\n"
        f"• 💰 General Discounts: {len(SEO_KEYWORDS['discounts'])} keywords\n\n"
        
        f"📈 **SEO PERFORMANCE:**\n"
        f"✅ 50% Discount Messaging Active\n"
        f"✅ Travel Discounts Optimized\n"
        f"✅ Lifestyle Deals Categorized\n"
        f"✅ Essential Savings Highlighted\n\n"
        
        f"💡 **RECOMMENDATION**: Use /broadcast for maximum discount reach!"
    )
    
    bot.send_message(ADMIN_ID, stats_text, parse_mode='Markdown')

# ===== CHAT HANDLERS =====
@bot.message_handler(func=lambda message: message.text and message.text.lower().startswith('hello'))
def hello_handler(message):
    user = message.from_user
    user_id = user.id
    
    # Add user to broadcast list
    broadcast_users.add(user_id)
    
    # Set chat state
    user_chat_states[user_id] = 'waiting_for_admin'
    
    # SEO-optimized user info
    user_info = (
        f"👤 **USER DETAILS:**\n"
        f"• Name: {user.first_name} {user.last_name or ''}\n"
        f"• Username: @{user.username or 'Not set'}\n"
        f"• User ID: {user.id}\n"
        f"• Discount Interest: New Customer"
    )
    
    # Store message info for admin replies
    user_messages[message.message_id] = {
        'user_id': user.id,
        'user_info': user_info,
        'original_message': message.text
    }
    
    # SEO-optimized message to admin
    forward_text = (
        f"👋 **NEW CUSTOMER INQUIRY** 👋\n\n"
        f"{user_info}\n\n"
        f"💬 **CUSTOMER MESSAGE:**\n'{message.text}'\n\n"
        f"🎯 **RECOMMENDED RESPONSE:**\n"
        f"Welcome to Spidy's World! We offer 50% discounts on flights, dining, and essential services. "
        f"Which discount category interests you?"
    )
    
    # Forward the "hello" message to admin with reply button
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("📨 Send Discount Info", callback_data=f"reply_{message.message_id}"))
    
    bot.send_message(ADMIN_ID, forward_text, reply_markup=keyboard)
    
    # SEO-optimized reply to user
    bot.reply_to(message, 
        "👋 **HELLO AND WELCOME!** 👋\n\n"
        "Thank you for reaching out to **Spidy's World Discount Services**! 🎉\n\n"
        "🔍 **POPULAR DISCOUNT REQUESTS:**\n"
        "• ✈️ Flight ticket discounts\n"
        "• 🏨 Hotel booking deals\n"
        "• 🍽️ Restaurant dining offers\n"
        "• 🚆 Train pass savings\n\n"
        "💡 **QUICK TIP**: Mention your specific needs (e.g., 'flights to NYC' or 'restaurant deals') for faster assistance!\n\n"
        "⏳ Our admin has been notified and will respond shortly with exclusive discount information!\n\n"
        "💰 **In the meantime, check our channel for current 50% off deals!**"
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('reply_'))
def reply_callback_handler(call):
    message_id = int(call.data.split('_')[1])
    
    if message_id in user_messages:
        user_data = user_messages[message_id]
        
        # SEO-optimized response prompt
        prompt_text = (
            f"💬 **CRAFT YOUR RESPONSE** 💬\n\n"
            f"👤 Replying to: {user_data['user_info'].split('•')[0].replace('👤 **USER DETAILS:**', '').strip()}\n\n"
            f"💡 **SEO-ENHANCED REPLY SUGGESTIONS:**\n"
            f"• 'Exclusive 50% discount on flights and hotels'\n"
            f"• 'Limited time offer on dining and entertainment'\n"
            f"• 'Special savings on essential services'\n\n"
            f"📝 **Type your reply (include discount keywords for better engagement):**"
        )
        
        # Ask admin to type the reply
        msg = bot.send_message(ADMIN_ID, prompt_text)
        
        # Register next step handler for admin's reply
        bot.register_next_step_handler(msg, process_admin_reply, user_data['user_id'])
    else:
        bot.answer_callback_query(call.id, "❌ Message data expired")

def process_admin_reply(message, user_id):
    try:
        # SEO-optimized reply prefix
        seo_prefix = "🎯 **EXCLUSIVE OFFER FROM SPIDY'S WORLD** 🎯\n\n"
        
        # Send admin's reply to the user
        full_reply = seo_prefix + message.text + "\n\n💎 **Limited Time Offer - Contact us to redeem!**"
        bot.send_message(user_id, full_reply)
        
        # SEO-optimized confirmation
        bot.reply_to(message, 
            "✅ **DISCOUNT MESSAGE DELIVERED!** ✅\n\n"
            "📊 **MESSAGE STATS:**\n"
            "• ✅ Delivered to customer\n"
            "• 🔍 SEO-enhanced format used\n"
            "• 💰 Discount keywords included\n"
            "• ⏰ Timestamp: Active offer"
        )
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
        user_info = (
            f"👤 **CONTINUING CONVERSATION WITH:**\n"
            f"• Name: {user.first_name} {user.last_name or ''}\n"
            f"• Username: @{user.username or 'Not set'}\n"
            f"• User ID: {user_id}\n"
            f"• Status: Active Discount Seeker"
        )
        
        # SEO keyword detection in user message
        detected_keywords = []
        user_text_lower = message.text.lower()
        
        for category, keywords in SEO_KEYWORDS.items():
            for keyword in keywords:
                if keyword in user_text_lower:
                    detected_keywords.append(keyword)
        
        # Store message info
        user_messages[message.message_id] = {
            'user_id': user_id,
            'user_info': user_info,
            'original_message': message.text,
            'detected_keywords': detected_keywords[:3]  # Limit to top 3
        }
        
        # SEO-enhanced forward message to admin
        keyword_info = ""
        if detected_keywords:
            keyword_info = f"🔍 **DETECTED DISCOUNT INTERESTS:** {', '.join(detected_keywords)}\n\n"
        
        forward_text = (
            f"💬 **NEW CUSTOMER MESSAGE** 💬\n\n"
            f"{user_info}\n\n"
            f"{keyword_info}"
            f"📝 **CUSTOMER INQUIRY:**\n'{message.text}'\n\n"
            f"💡 **SUGGESTED RESPONSE:**\n"
            f"Thank you for your interest! We have exclusive 50% discounts available. "
            f"Let me provide you with the best offers for your needs."
        )
        
        # Forward message to admin with reply button
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("📨 Send Discount Offer", callback_data=f"reply_{message.message_id}"))
        
        bot.send_message(ADMIN_ID, forward_text, reply_markup=keyboard)
        
        # SEO-optimized acknowledgment to user
        if not message.text.lower().startswith('hello'):
            acknowledgment = (
                "✅ **MESSAGE RECEIVED!** ✅\n\n"
                f"💡 **DETECTED INTERESTS:** {', '.join(detected_keywords[:2]) if detected_keywords else 'General discounts'}\n\n"
                "🔄 **NEXT STEPS:**\n"
                "1. Our admin is reviewing your request\n"
                "2. Custom discount offers being prepared\n"
                "3. You'll receive exclusive 50% off deals shortly\n\n"
                "⏳ **Estimated response time: 2-5 minutes**"
            )
            bot.reply_to(message, acknowledgment)

@app.route('/')
def home():
    # SEO-optimized homepage
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Spidy's World - 50% Discounts on Travel, Lifestyle & Essential Services</title>
        <meta name="description" content="Get 50% discounts on flights, hotels, dining, events, bills, and 100+ services. Trusted discount platform with exclusive savings.">
        <meta name="keywords" content="flight discounts, hotel deals, restaurant offers, bill savings, 50% off, travel discounts, lifestyle savings, essential services discounts">
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            .container { max-width: 800px; margin: 0 auto; }
            .keyword-badge { background: #f0f0f0; padding: 5px 15px; margin: 5px; border-radius: 20px; display: inline-block; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🟡 Spidy's World Discount Bot 🟡</h1>
            <p><strong>50% Discounts on 100+ Services</strong></p>
            
            <h3>🔍 SEO-Optimized Discount Categories:</h3>
            <div>
                <span class="keyword-badge">✈️ Flight Discounts</span>
                <span class="keyword-badge">🏨 Hotel Deals</span>
                <span class="keyword-badge">🍽️ Dining Offers</span>
                <span class="keyword-badge">🎡 Entertainment Savings</span>
                <span class="keyword-badge">🚆 Train Pass Discounts</span>
                <span class="keyword-badge">💳 Bill Payment Savings</span>
            </div>
            
            <p style="margin-top: 30px;">Bot Status: <strong style="color: green;">✅ Active & Finding Discounts</strong></p>
            <p>Best for: Travel savings, lifestyle discounts, essential service reductions</p>
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
            print(f"🎯 SEO Bot Ready: 200+ keywords loaded")
            print(f"💰 Discount Categories: Travel, Lifestyle, Essentials")
            print(f"👥 User Tracking: Active")
        else:
            print("⚠️ No domain found for webhook")
            
    except Exception as e:
        print(f"⚠️ Webhook setup error: {e}")
    
    print("🚀 SEO-Optimized Discount Bot is running!")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
