import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from config import Config
from handlers.start import start_command, settings_command, handle_settings_callback
from handlers.odds import odds_command, handle_odds_callback, process_odds_query
from handlers.bets import bet_command, handle_bet_callback, tips_command, process_tip_query
from handlers.insights import insights_command, predict_command, compare_command, handle_insight_callback, handle_predict_callback, process_predict_query
import asyncio

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class OddsPilotBot:
    def __init__(self):
        self.application = Application.builder().token(Config.TELEGRAM_TOKEN).build()
        self.setup_handlers()
        
    def setup_handlers(self):
        """Setup all command handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", start_command))
        self.application.add_handler(CommandHandler("odds", odds_command))
        self.application.add_handler(CommandHandler("bet", bet_command))
        self.application.add_handler(CommandHandler("insights", insights_command))
        self.application.add_handler(CommandHandler("predict", predict_command))
        self.application.add_handler(CommandHandler("compare", compare_command))
        self.application.add_handler(CommandHandler("tips", tips_command))
        self.application.add_handler(CommandHandler("settings", settings_command))
        
        # Callback query handler for inline buttons
        self.application.add_handler(CallbackQueryHandler(self.handle_callback))
        
        # Message handlers
        self.application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, 
            self.handle_text
        ))
        
        # Error handler
        self.application.add_error_handler(self.error_handler)
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline button callbacks"""
        query = update.callback_query
        await query.answer()
        
        data = query.data.split('_')
        action = data[0]
        
        if action == 'odds':
            await handle_odds_callback(query, context, data[1:])
        elif action == 'bet':
            await handle_bet_callback(query, context, data[1:])
        elif action == 'insight':
            await handle_insight_callback(query, context, data[1:])
        elif action == 'predict':
            await handle_predict_callback(query, context, data[1:])
        elif action == 'back':
            await self.handle_back_callback(query, context)
        elif action == 'settings':
            await handle_settings_callback(query, context, data[1:])
    
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages"""
        text = update.message.text.lower()
        
        # Check for specific keywords
        if any(word in text for word in ['odds', 'betting', 'game', 'match']):
            await process_odds_query(update, context)
        elif any(word in text for word in ['predict', 'prediction', 'win']):
            await process_predict_query(update, context)
        elif any(word in text for word in ['tip', 'advice', 'help']):
            await process_tip_query(update, context)
        else:
            await update.message.reply_text(
                f"🤖 Welcome to {Config.BOT_NAME}!\n\n"
                "I'm your AI-powered betting assistant. Here's what I can do:\n\n"
                "📊 /odds - Get AI-generated betting odds\n"
                "🎯 /bet - Get smart betting advice\n"
                "🧠 /insights - AI-powered game insights\n"
                "🔮 /predict - Get match predictions\n"
                "📈 /compare - Compare two teams\n"
                "💡 /tips - Get betting tips\n\n"
                "Just send me a message about any game or team!"
            )
    
    async def handle_back_callback(self, query, context):
        """Handle back button callback"""
        keyboard = [
            [
                InlineKeyboardButton("📊 Odds", callback_data="odds_menu"),
                InlineKeyboardButton("🎯 Bet", callback_data="bet_menu")
            ],
            [
                InlineKeyboardButton("🧠 Insights", callback_data="insight_menu"),
                InlineKeyboardButton("🔮 Predict", callback_data="predict_menu")
            ],
            [
                InlineKeyboardButton("💡 Tips", callback_data="bet_tips"),
                InlineKeyboardButton("⚙️ Settings", callback_data="settings_menu")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"🎯 **{Config.BOT_NAME} - Main Menu**\n\n"
            "Your AI-powered betting assistant!\n"
            "Choose an option below:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Update {update} caused error {context.error}")
        
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "⚠️ An error occurred. Please try again later.\n\n"
                "If the problem persists, use /start to restart the bot."
            )
    
    def run(self):
        """Start the bot"""
        logger.info(f"Starting {Config.BOT_NAME} bot...")
        self.application.run_polling()

if __name__ == '__main__':
    bot = OddsPilotBot()
    bot.run()
