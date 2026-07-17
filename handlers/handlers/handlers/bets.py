from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.ai_service import AIService

ai_service = AIService()

async def bet_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /bet command"""
    keyboard = [
        [
            InlineKeyboardButton("📊 Smart Betting Advice", callback_data="bet_advice"),
            InlineKeyboardButton("🎯 Pick of the Day", callback_data="bet_pick")
        ],
        [
            InlineKeyboardButton("📈 Trends Analysis", callback_data="bet_trends"),
            InlineKeyboardButton("💰 Value Bets", callback_data="bet_value")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🎯 **Betting Assistant**\n\n"
        "I'll help you make smarter betting decisions:\n"
        "✅ Analysis of upcoming games\n"
        "✅ Value bet identification\n"
        "✅ Risk assessment\n"
        "✅ Expert predictions\n\n"
        "Choose an option below:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_bet_callback(query, data):
    """Handle bet callback queries"""
    action = data[0]
    
    if action == 'advice':
        await query.edit_message_text(
            "⏳ Generating personalized betting advice...\n"
            "Analyzing recent games and trends..."
        )
        
        advice = await ai_service.get_betting_advice()
        
        response = (
            "💡 **Smart Betting Advice**\n\n"
            f"{advice}\n\n"
            "⚠️ **Remember:** Always bet responsibly and within your limits."
        )
        
        keyboard = [
            [InlineKeyboardButton("🔄 Refresh Advice", callback_data="bet_advice")],
            [InlineKeyboardButton("📊 More Insights", callback_data="insight_ai")],
            [InlineKeyboardButton("🔙 Back", callback_data="back_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            response,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    elif action == 'pick':
        # Generate pick of the day
        pick = await ai_service.get_pick_of_day()
        await query.edit_message_text(
            f"🎯 **Pick of the Day**\n\n{pick}\n\n"
            "Good luck with your bets! 🍀",
            parse_mode='Markdown'
        )
