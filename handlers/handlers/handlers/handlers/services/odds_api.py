import aiohttp
import json
from datetime import datetime
from config import Config
import logging

logger = logging.getLogger(__name__)

class OddsAPI:
    def __init__(self):
        self.api_key = Config.ODDS_API_KEY
        self.base_url = Config.ODDS_API_BASE_URL
        
    async def get_odds(self, sport):
        """Fetch odds from external API"""
        try:
            # Using The Odds API (free tier)
            # You can replace with your preferred odds API
            endpoint = f"{self.base_url}/sports"
            
            # This is a mock response - replace with actual API call
            # For production, use real API integration
            mock_odds = self._get_mock_odds(sport)
            return mock_odds
            
        except Exception as e:
            logger.error(f"Error fetching odds: {e}")
            return None
    
    def _get_mock_odds(self, sport):
        """Generate mock odds data"""
        # This is for demonstration - replace with real API
        mock_data = {
            'soccer': [
                {
                    'home_team': 'Team A',
                    'away_team': 'Team B',
                    'odds': 'Home: 2.10 | Draw: 3.40 | Away: 3.80',
                    'time': datetime.now().strftime('%Y-%m-%d %H:%M')
                },
                {
                    'home_team': 'Team C',
                    'away_team': 'Team D',
                    'odds': 'Home: 1.85 | Draw: 3.60 | Away: 4.20',
                    'time': datetime.now().strftime('%Y-%m-%d %H:%M')
                }
            ],
            'basketball': [
                {
                    'home_team': 'Lakers',
                    'away_team': 'Celtics',
                    'odds': 'Lakers: -150 | Celtics: +130',
                    'time': datetime.now().strftime('%Y-%m-%d %H:%M')
                }
            ]
        }
        return mock_data.get(sport, [])
