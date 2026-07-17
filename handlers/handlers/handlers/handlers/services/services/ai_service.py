import openai
from config import Config
import logging

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY
        
    async def get_betting_advice(self):
        """Get betting advice using OpenAI"""
        try:
            prompt = """
            Provide smart betting advice focusing on:
            1. Key factors to consider before placing a bet
            2. Risk management strategies
            3. Value betting opportunities
            4. Common mistakes to avoid
            
            Keep it concise and practical.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional sports betting analyst."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"AI service error: {e}")
            return self._get_mock_advice()
    
    async def get_game_analysis(self):
        """Get game analysis"""
        try:
            prompt = """
            Provide a detailed game analysis including:
            1. Team form and recent performance
            2. Head-to-head statistics
            3. Key players and injuries
            4. Predicted outcome
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a sports analyst providing detailed game analysis."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"AI analysis error: {e}")
            return self._get_mock_analysis()
    
    async def get_pick_of_day(self):
        """Get pick of the day"""
        return """
        🏆 **Pick of the Day**
        
        **Game:** Lakers vs Celtics
        **Pick:** Lakers to win (-150)
        **Confidence:** 70%
        
        **Why?**
        • Lakers have won 7 of last 10 games
        • Home court advantage
        • Key players in good form
        • Historical matchup favors Lakers
        
        📊 **Risk Level:** Medium
        💰 **Value Rating:** 7/10
        """
    
    def _get_mock_advice(self):
        return """
        💡 **Smart Betting Tips**
        
        1. 📊 **Do Your Research**
           Always analyze team form, injuries, and historical matchups before betting.
        
        2. 💰 **Bankroll Management**
           Never bet more than 1-2% of your total bankroll on a single bet.
        
        3. 🔍 **Look for Value**
           Compare odds across multiple bookmakers to find the best value.
        
        4. 🧠 **Stay Emotion-Free**
           Make decisions based on data and analysis, not emotions.
        
        Remember: Bet responsibly! 🎯
        """
    
    def _get_mock_analysis(self):
        return """
        📊 **Game Analysis**
        
        **Team A vs Team B**
        
        📈 **Recent Form:**
        • Team A: W W L W D (3 wins in last 5)
        • Team B: L W W L L (2 wins in last 5)
        
        🔑 **Key Factors:**
        • Team A has home advantage
        • Team B missing key player due to injury
        • Historical: Team A leads 3-2 in last 5 meetings
        
        🎯 **Prediction:** Team A likely to win
        📊 **Confidence:** 65%
        
        📉 **Risk Factors:** Weather conditions might affect gameplay
        """
