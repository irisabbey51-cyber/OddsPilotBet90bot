import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Config
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

# AI Service Functions
async def get_ai_response(prompt, context_text=""):
    """Get response from OpenAI"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a sports betting assistant providing odds, predictions, and betting advice."},
                {"role": "user", "content": f"{prompt}\n\nContext: {context_text}"}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"OpenAI error: {e}")
        return None

# Start Command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = (
        f"🎯 **Welcome to OddsPilotBet90, {user.first_name}!**\n\n"
        "I'm your AI-powered betting assistant!\n\n"
        "**Commands:**\n"
        "📊 /odds - Get AI betting odds\n"
        "🎯 /bet - Get betting advice\n"
        "🧠 /insights - Game insights\n"
        "🔮 /predict - Match predictions\n"
        "💡 /tips - Daily betting tips\n"
        "⚙️ /settings - Settings\n\n"
        "Just type any game or team name!"
    )
    keyboard = [
        [InlineKeyboardButton("📊 Odds", callback_data="odds"), InlineKeyboardButton("🎯 Bet", callback_data="bet")],
        [InlineKeyboardButton("🧠 Insights", callback_data="insights"), InlineKeyboardButton("🔮 Predict", callback_data="predict")],
        [InlineKeyboardButton("💡 Tips", callback_data="tips"), InlineKeyboardButton("⚙️ Settings", callback_data="settings")]
    ]
    await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

# Odds Command
async def odds_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Generating AI odds analysis...")
    
    prompt = "Generate realistic betting odds for today's top sports matches. Include moneyline, spread, and over/under for 3 different sports."
    response = await get_ai_response(prompt)
    
    if response:
        await update.message.reply_text(f"📊 **AI Betting Odds**\n\n{response}", parse_mode='Markdown')
    else:
        await update.message.reply_text("📊 **Sample Odds**\n\n⚽ Soccer: Team A -150 vs Team B +130\n🏀 Basketball: Lakers -2.5 (-110)\n🎾 Tennis: Player A -120 vs Player B +100")

# Bet Command
async def bet_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Getting smart betting advice...")
    
    prompt = "Provide smart betting advice including bankroll management, value betting tips, and common mistakes to avoid."
    response = await get_ai_response(prompt)
    
    if response:
        await update.message.reply_text(f"🎯 **Betting Advice**\n\n{response}", parse_mode='Markdown')
    else:
        await update.message.reply_text("🎯 **Tips**\n\n1. Only bet 1-3% of bankroll\n2. Research before betting\n3. Look for value in odds\n4. Stay disciplined")

# Insights Command
async def insights_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Generating AI insights...")
    
    prompt = "Provide detailed sports betting insights including team performance analysis, market trends, and key factors to consider."
    response = await get_ai_response(prompt)
    
    if response:
        await update.message.reply_text(f"🧠 **AI Insights**\n\n{response}", parse_mode='Markdown')
    else:
        await update.message.reply_text("🧠 **Key Insights**\n\n• Home teams win 55% of games\n• Favorites cover spread 48% of time\n• Overs hit 52% of games\n• Form is more important than history")

# Predict Command
async def predict_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Making AI predictions...")
    
    prompt = "Predict the outcomes of today's major sports matches. Include confidence levels and reasoning."
    response = await get_ai_response(prompt)
    
    if response:
        await update.message.reply_text(f"🔮 **Match Predictions**\n\n{response}", parse_mode='Markdown')
    else:
        await update.message.reply_text("🔮 **Prediction Tips**\n\n• Look at recent form\n• Check injury reports\n• Consider home advantage\n• Weather can impact games")

# Tips Command
async def tips_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Generating daily tips...")
    
    prompt = "Provide daily betting tips including tip of the day, strategic advice, and what to watch for."
    response = await get_ai_response(prompt)
    
    if response:
        await update.message.reply_text(f"💡 **Daily Tips**\n\n{response}", parse_mode='Markdown')
    else:
        await update.message.reply_text("💡 **Tip of the Day**\n\nAlways bet with your head, not your heart. Research is key!")

# Settings Command
async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🏟️ Set Sport", callback_data="set_sport")],
        [InlineKeyboardButton("🔔 Notifications", callback_data="notifications")],
        [InlineKeyboardButton("🔙 Back", callback_data="back")]
    ]
    await update.message.reply_text("⚙️ **Settings**\n\nCustomize your experience:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

# Handle Callbacks
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "odds":
        await odds_command(update, context)
    elif data == "bet":
        await bet_command(update, context)
    elif data == "insights":
        await insights_command(update, context)
    elif data == "predict":
        await predict_command(update, context)
    elif data == "tips":
        await tips_command(update, context)
    elif data == "settings" or data == "set_sport" or data == "notifications":
        keyboard = [
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="back")]
        ]
        await query.edit_message_text("⚙️ Settings saved!", reply_markup=InlineKeyboardMarkup(keyboard))
    elif data == "back":
        keyboard = [
            [InlineKeyboardButton("📊 Odds", callback_data="odds"), InlineKeyboardButton("🎯 Bet", callback_data="bet")],
            [InlineKeyboardButton("🧠 Insights", callback_data="insights"), InlineKeyboardButton("🔮 Predict", callback_data="predict")],
            [InlineKeyboardButton("💡 Tips", callback_data="tips"), InlineKeyboardButton("⚙️ Settings", callback_data="settings")]
        ]
        await query.edit_message_text("🎯 **OddsPilotBet90 - Main Menu**", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

# Handle Text Messages
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    
    if " vs " in text:
        await update.message.reply_text(f"⏳ Analyzing {text}...")
        prompt = f"Analyze the matchup between {text}. Provide predictions, key factors, and who you think will win."
        response = await get_ai_response(prompt, text)
        
        if response:
            await update.message.reply_text(f"📊 **Match Analysis**\n\n{response}", parse_mode='Markdown')
        else:
            await update.message.reply_text(f"📊 **Analysis for {text}**\n\nI'll analyze this matchup for you! Use /predict for detailed predictions.")
    else:
        await update.message.reply_text(
            "🤖 I'm your betting assistant!\n\n"
            "Try these commands:\n"
            "📊 /odds - Betting odds\n"
            "🎯 /bet - Betting advice\n"
            "🧠 /insights - Game insights\n"
            "🔮 /predict - Predictions\n"
            "💡 /tips - Daily tips\n\n"
            "Or type 'Team A vs Team B' for analysis!"
        )

# Error Handler
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text("⚠️ An error occurred. Please try again.")

# Main
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("odds", odds_command))
    app.add_handler(CommandHandler("bet", bet_command))
    app.add_handler(CommandHandler("insights", insights_command))
    app.add_handler(CommandHandler("predict", predict_command))
    app.add_handler(CommandHandler("tips", tips_command))
    app.add_handler(CommandHandler("settings", settings_command))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_error_handler(error_handler)
    
    logger.info("Bot started! 🚀")
    app.run_polling()

if __name__ == "__main__":
    main()
