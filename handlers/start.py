from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    
    welcome_text = (
        f"🎯 **Welcome to OddsPilotBet90, {user.first_name}!**\n\n"
        "I'm your AI-powered betting assistant that helps you:\n"
        "✅ Get AI-generated betting odds\n"
        "✅ Receive smart betting advice\n"
        "✅ Get game predictions and insights\n"
        "✅ Compare teams and analyze matches\n"
        "✅ Get daily betting tips\n\n"
        "**How to use me:**\n"
        "• Type a game name (e.g., 'Lakers vs Celtics')\n"
        "• Use commands like /odds, /bet, /predict\n"
        "• Ask me anything about betting!\n\n"
        "🚀 Let's make smarter bets together!"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("📊 Get Odds", callback_data="odds_menu"),
            InlineKeyboardButton("🎯 Bet Advice", callback_data="bet_menu")
        ],
        [
            InlineKeyboardButton("🧠 Insights", callback_data="insight_menu"),
            InlineKeyboardButton("🔮 Predictions", callback_data="predict_menu")
        ],
        [
            InlineKeyboardButton("💡 Tips", callback_data="bet_tips"),
            InlineKeyboardButton("⚙️ Settings", callback_data="settings_menu")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    
    # Store user info
    context.user_data['user_id'] = user.id
    context.user_data['username'] = user.username
    context.user_data['preferences'] = {
        'sport': 'All',
        'notifications': True
    }

async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /settings command"""
    keyboard = [
        [InlineKeyboardButton("🏟️ Set Favorite Sport", callback_data="settings_sport")],
        [InlineKeyboardButton("🔔 Toggle Notifications", callback_data="settings_notifications")],
        [InlineKeyboardButton("🌍 Set Language", callback_data="settings_language")],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "⚙️ **Settings**\n\n"
        "Customize your betting assistant experience:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_settings_callback(query, context, data):
    """Handle settings callback queries"""
    action = data[0] if data else None
    
    if action == 'sport':
        keyboard = []
        sports = ['⚽ Soccer', '🏀 Basketball', '🎾 Tennis', '🏈 Football', '⚾ Baseball']
        for sport in sports:
            keyboard.append([InlineKeyboardButton(sport, callback_data=f"settings_set_sport_{sport}")])
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="settings_menu")])
        
        await query.edit_message_text(
            "🏟️ **Select Your Favorite Sport**\n\n"
            "I'll focus on providing insights for this sport:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    elif action == 'set_sport':
        sport = data[1] if len(data) > 1 else "All"
        context.user_data['preferences']['sport'] = sport
        await query.edit_message_text(
            f"✅ Favorite sport set to: {sport}\n\n"
            "I'll provide more focused insights for this sport!",
            parse_mode='Markdown'
        )
