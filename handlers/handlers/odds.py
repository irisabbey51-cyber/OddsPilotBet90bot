from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.odds_api import OddsAPI
from services.cache import CacheService
from config import Config
import logging

logger = logging.getLogger(__name__)
odds_api = OddsAPI()
cache = CacheService()

async def odds_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /odds command"""
    keyboard = [
        [InlineKeyboardButton("⚽ Soccer", callback_data="odds_soccer")],
        [InlineKeyboardButton("🏀 Basketball", callback_data="odds_basketball")],
        [InlineKeyboardButton("🎾 Tennis", callback_data="odds_tennis")],
        [InlineKeyboardButton("🏈 American Football", callback_data="odds_football")],
        [InlineKeyboardButton("⚾ Baseball", callback_data="odds_baseball")],
        [InlineKeyboardButton("🏒 Hockey", callback_data="odds_hockey")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🏆 **Live Betting Odds**\n\n"
        "Select a sport to see current odds:\n"
        "*(Data updates every 60 seconds)*",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_odds_callback(query, data):
    """Handle odds callback queries"""
    sport = data[0]
    await query.edit_message_text(
        f"⏳ Fetching {sport} odds...\n"
        "Please wait a moment..."
    )
    
    odds_data = await odds_api.get_odds(sport)
    
    if not odds_data:
        await query.edit_message_text(
            f"❌ Could not fetch odds for {sport}.\n"
            "Please try again later."
        )
        return
    
    # Format odds response
    response = f"🏆 **{sport.upper()} Odds**\n\n"
    for game in odds_data[:5]:  # Show top 5 games
        response += f"**{game['home_team']} vs {game['away_team']}**\n"
        response += f"📊 {game['odds']}\n"
        response += f"📈 Last Updated: {game['time']}\n"
        response += f"🔗 [View Details]({game.get('url', '#')})\n\n"
    
    keyboard = [
        [InlineKeyboardButton("🔄 Refresh", callback_data=f"odds_refresh_{sport}")],
        [InlineKeyboardButton("📊 Betting Insights", callback_data=f"insight_odds_{sport}")],
        [InlineKeyboardButton("🔙 Back to Sports", callback_data="back_odds")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        response,
        reply_markup=reply_markup,
        parse_mode='Markdown',
        disable_web_page_preview=True
    )

async def track_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /track command"""
    await update.message.reply_text(
        "🎯 **Track a Game**\n\n"
        "Enter the game you want to track:\n"
        "Example: 'Lakers vs Warriors'\n\n"
        "I'll send you real-time updates and odds changes!",
        parse_mode='Markdown'
    )

async def process_odds_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process odds queries from text messages"""
    await update.message.reply_text(
        "🔍 Searching for odds...\n\n"
        "Use /odds to select a sport and view current betting odds."
    )
