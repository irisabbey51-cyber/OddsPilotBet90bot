from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.ai_service import AIService
import logging

logger = logging.getLogger(__name__)
ai_service = AIService()

async def bet_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /bet command"""
    keyboard = [
        [InlineKeyboardButton("🎯 Smart Betting Advice", callback_data="bet_advice")],
        [InlineKeyboardButton("📈 Value Bet Finder", callback_data="bet_value")],
        [InlineKeyboardButton("📊 Trend Analysis", callback_data="bet_trends")],
        [InlineKeyboardButton("💡 Tips", callback_data="bet_tips")],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🎯 **Smart Betting Assistant**\n\n"
        "I use AI to help you make better betting decisions:\n"
        "✅ Personalized betting advice\n"
        "✅ Value bet identification\n"
        "✅ Risk assessment\n"
        "✅ Market trends analysis\n\n"
        "Choose an option below:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_bet_callback(query, context, data):
    """Handle bet callback queries"""
    action = data[0] if data else 'advice'
    
    await query.edit_message_text(
        "⏳ Generating AI-powered betting advice...\n"
        "Analyzing data and trends..."
    )
    
    if action == 'advice':
        advice = await ai_service.get_betting_advice(context.user_data)
        response = f"💡 **Smart Betting Advice**\n\n{advice}\n\n⚠️ **Always bet responsibly!**"
        
    elif action == 'value':
        value_bets = await ai_service.find_value_bets()
        response = f"💰 **Value Bet Opportunities**\n\n{value_bets}"
        
    elif action == 'trends':
        trends = await ai_service.get_market_trends()
        response = f"📈 **Market Trends Analysis**\n\n{trends}"
        
    elif action == 'tips':
        tips = await ai_service.get_betting_tips()
        response = f"💡 **Expert Betting Tips**\n\n{tips}"
    
    keyboard = [
        [InlineKeyboardButton("🔄 Refresh", callback_data=f"bet_{action}")],
        [InlineKeyboardButton("🔙 Back to Bet Menu", callback_data="bet_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        response,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def tips_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /tips command"""
    await update.message.reply_text(
        "⏳ Generating daily betting tips..."
    )
    
    tips = await ai_service.get_betting_tips()
    
    response = f"💡 **Daily Betting Tips**\n\n{tips}\n\n"
    response += "Remember: Knowledge is power! 📚"
    
    await update.message.reply_text(
        response,
        parse_mode='Markdown'
    )

async def process_tip_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process tip queries from text messages"""
    await update.message.reply_text(
        "💡 I can give you betting tips!\n\n"
        "Use /bet for comprehensive advice or /tips for daily tips.\n\n"
        "You can also ask me about specific games!"
    )
