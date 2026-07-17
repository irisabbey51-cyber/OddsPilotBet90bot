from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.ai_service import AIService
import logging

logger = logging.getLogger(__name__)
ai_service = AIService()

async def odds_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /odds command"""
    keyboard = [
        [InlineKeyboardButton("⚽ Soccer", callback_data="odds_soccer")],
        [InlineKeyboardButton("🏀 Basketball", callback_data="odds_basketball")],
        [InlineKeyboardButton("🎾 Tennis", callback_data="odds_tennis")],
        [InlineKeyboardButton("🏈 American Football", callback_data="odds_football")],
        [InlineKeyboardButton("⚾ Baseball", callback_data="odds_baseball")],
        [InlineKeyboardButton("🏒 Hockey", callback_data="odds_hockey")],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "📊 **AI-Generated Betting Odds**\n\n"
        "Select a sport to see AI-powered odds analysis:\n"
        "*Based on historical data and current trends*",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_odds_callback(query, context, data):
    """Handle odds callback queries"""
    sport = data[0] if data else "soccer"
    
    await query.edit_message_text(
        f"⏳ Analyzing {sport} odds with AI...\n"
        "Processing historical data and current trends..."
    )
    
    # Get AI-generated odds
    odds_data = await ai_service.generate_odds(sport)
    
    if not odds_data:
        await query.edit_message_text(
            f"❌ Could not generate odds for {sport}.\n"
            "Please try again later or select another sport.",
            parse_mode='Markdown'
        )
        return
    
    response = f"📊 **{sport.upper()} - AI Odds Analysis**\n\n"
    response += odds_data
    
    keyboard = [
        [InlineKeyboardButton("🔄 Refresh", callback_data=f"odds_{sport}")],
        [InlineKeyboardButton("📈 Get Analysis", callback_data=f"insight_odds_{sport}")],
        [InlineKeyboardButton("🔙 Back to Sports", callback_data="odds_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        response,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def process_odds_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process odds queries from text messages"""
    await update.message.reply_text(
        "🔍 I'll help you find odds for any match!\n\n"
        "Please use /odds to select a sport, or type:\n"
        "• 'odds for [Team A] vs [Team B]'\n"
        "• '[Team A] vs [Team B] odds'\n\n"
        "I'll generate AI-powered odds analysis!"
    )
