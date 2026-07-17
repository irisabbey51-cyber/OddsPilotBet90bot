from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.ai_service import AIService
import logging

logger = logging.getLogger(__name__)
ai_service = AIService()

async def insights_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /insights command"""
    keyboard = [
        [InlineKeyboardButton("🤖 Game Analysis", callback_data="insight_game")],
        [InlineKeyboardButton("📊 Team Performance", callback_data="insight_team")],
        [InlineKeyboardButton("📈 Market Trends", callback_data="insight_trends")],
        [InlineKeyboardButton("🔮 Predictions", callback_data="predict_menu")],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_menu")]
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

async def predict_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /predict command"""
    keyboard = [
        [InlineKeyboardButton("⚽ Soccer Match", callback_data="predict_soccer")],
        [InlineKeyboardButton("🏀 Basketball Match", callback_data="predict_basketball")],
        [InlineKeyboardButton("🎾 Tennis Match", callback_data="predict_tennis")],
        [InlineKeyboardButton("🏈 Football Match", callback_data="predict_football")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🔮 **AI Match Predictions**\n\n"
        "Select a sport for AI-powered predictions:\n"
        "*Based on historical data and current form*",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def compare_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /compare command"""
    await update.message.reply_text(
        "📈 **Team Comparison Tool**\n\n"
        "To compare two teams, send:\n"
        "`Team A vs Team B`\n\n"
        "Example: `Lakers vs Celtics`\n\n"
        "I'll provide a detailed AI analysis comparing both teams!",
        parse_mode='Markdown'
    )

async def handle_insight_callback(query, context, data):
    """Handle insight callback queries"""
    insight_type = data[0] if data else 'game'
    
    await query.edit_message_text(
        "⏳ Generating AI insights...\n"
        "Analyzing data and patterns..."
    )
    
    if insight_type == 'game':
        analysis = await ai_service.get_game_analysis()
        response = f"🎯 **Game Analysis**\n\n{analysis}"
    elif insight_type == 'team':
        teams = await ai_service.get_team_performance()
        response = f"📊 **Team Performance Analysis**\n\n{teams}"
    elif insight_type == 'trends':
        trends = await ai_service.get_market_trends()
        response = f"📈 **Market Trends**\n\n{trends}"
    elif insight_type == 'odds':
        sport = data[1] if len(data) > 1 else "soccer"
        odds = await ai_service.generate_odds(sport)
        response = f"📊 **Odds Analysis**\n\n{odds}"
    
    keyboard = [
        [InlineKeyboardButton("🔄 Refresh", callback_data=f"insight_{insight_type}")],
        [InlineKeyboardButton("🔙 Back to Insights", callback_data="insight_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        response,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_predict_callback(query, context, data):
    """Handle prediction callback queries"""
    sport = data[0] if data else "soccer"
    
    await query.edit_message_text(
        f"⏳ Generating {sport} predictions with AI..."
    )
    
    predictions = await ai_service.get_predictions(sport)
    
    response = f"🔮 **{sport.upper()} Predictions**\n\n{predictions}\n\n"
    response += "📊 *These predictions are AI-generated based on data analysis*"
    
    keyboard = [
        [InlineKeyboardButton("🔄 Refresh", callback_data=f"predict_{sport}")],
        [InlineKeyboardButton("🔙 Back", callback_data="predict_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        response,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def process_predict_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process prediction queries from text messages"""
    await update.message.reply_text(
        "🔮 I can predict match outcomes!\n\n"
        "Use /predict to select a sport, or type:\n"
        "• 'predict [Team A] vs [Team B]'\n"
        "• 'who will win [Team A] vs [Team B]'\n\n"
        "I'll give you AI-powered predictions!"
    )
