import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    
    # Bot settings
    BOT_NAME = "OddsPilotBet90"
    BOT_USERNAME = "@OddsPilotBet90bot"
    
    # Cache settings
    CACHE_TTL = 300  # 5 minutes
    
    # Supported sports for betting
    SUPPORTED_SPORTS = [
        '⚽ Soccer', '🏀 Basketball', '🎾 Tennis', 
        '🏈 American Football', '⚾ Baseball', '🏒 Hockey',
        '🥊 Boxing', '🏏 Cricket', '🏉 Rugby'
    ]
    
    # Commands
    COMMANDS = {
        'start': '🚀 Start the bot and get help',
        'odds': '📊 Get AI-generated betting odds',
        'bet': '🎯 Get smart betting advice',
        'insights': '🧠 Get AI-powered insights',
        'predict': '🔮 Get match predictions',
        'compare': '📈 Compare teams',
        'tips': '💡 Get betting tips',
        'settings': '⚙️ Configure your preferences'
    }
