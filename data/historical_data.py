import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional

class HistoricalDataManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.logger = logging.getLogger(__name__)

    def fetch_historical_data(self, 
                            symbol: str, 
                            start_date: str,
                            end_date: str,
                            interval: str = '1d') -> pd.DataFrame:
        """Fetch historical price and volatility data"""
        try:
            # First check if data exists in database
            cached_data = self.db_manager.get_historical_data(
                symbol, start_date, end_date
            )
            
            if cached_data is not None:
                self.logger.info(f"Retrieved cached data for {symbol}")
                return cached_data
            
            # If not in database, fetch from yfinance
            ticker = yf.Ticker(symbol)
            data = ticker.history(start=start_date, 
                                end=end_date, 
                                interval=interval)
            
            # Add additional calculations
            data['Returns'] = data['Close'].pct_change()
            data['RealizedVol'] = self._calculate_realized_volatility(data)
            
            # Fetch VIX data for implied volatility
            vix_data = yf.download('^VIX', start=start_date, end=end_date)
            data['ImpliedVol'] = vix_data['Close'] / 100
            
            # Store in database
            self.db_manager.store_historical_data(symbol, data)
            
            return data
            
        except Exception as e:
            self.logger.error(f"Error fetching historical data: {str(e)}")
            raise

    def _calculate_realized_volatility(self, 
                                     data: pd.DataFrame, 
                                     window: int = 20) -> pd.Series:
        """Calculate rolling realized volatility"""
        return data['Returns'].rolling(window=window).std() * \
               (252 ** 0.5)
