from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.ai_service import AIService
import logging

logger = logging.getLogger(__name__)
ai_service = AIService()

async def insights_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /insights command"""
    keyboard = [
        [InlineKeyboardButton("🤖 AI Game Analysis", callback_data="insight_ai")],
        [InlineKeyboardButton("📊 Market Trends", callback_data="insight_trends")],
        [InlineKeyboardButton("📈 Team Performance", callback_data="insight_teams")],
        [InlineKeyboardButton("🎯 Predictions", callback_data="insight_predictions")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🧠 **AI-Powered Insights**\n\n"
        "Get advanced betting analytics:\n"
        "✅ Machine learning predictions\n"
        "✅ Historical data analysis\n"
        "✅ Pattern recognition\n"
        "✅ Smart recommendations\n\n"
        "Select an insight type:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_insight_callback(query, data):
    """Handle insight callback queries"""
    insight_type = data[0]
    
    await query.edit_message_text(
        "⏳ Generating AI insights...\n"
        "Analyzing data and patterns..."
    )
    
    if insight_type == 'ai':
        analysis = await ai_service.get_game_analysis()
        response = f"🤖 **AI Game Analysis**\n\n{analysis}"
        
    elif insight_type == 'trends':
        trends = await ai_service.get_market_trends()
        response = f"📊 **Market Trends**\n\n{trends}"
        
    elif insight_type == 'teams':
        teams = await ai_service.get_team_performance()
        response = f"📈 **Team Performance Analysis**\n\n{teams}"
        
    elif insight_type == 'predictions':
        predictions = await ai_service.get_predictions()
        response = f"🎯 **Predictions**\n\n{predictions}"
    
    keyboard = [
        [InlineKeyboardButton("🔄 Refresh", callback_data=f"insight_{insight_type}")],
        [InlineKeyboardButton("🔙 Back to Insights", callback_data="back_insights")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        response,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
