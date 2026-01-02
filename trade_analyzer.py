"""
Trade History Analysis Module

This module provides functionality to analyze trading history data,
calculate performance metrics, and generate visualizations.
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional


class TradeAnalyzer:
    """
    A class for analyzing trade history data and calculating performance metrics.
    
    Attributes:
        trades_df (pd.DataFrame): DataFrame containing trade history data
    """
    
    def __init__(self, trades_df: pd.DataFrame):
        """
        Initialize the TradeAnalyzer with trade data.
        
        Args:
            trades_df: DataFrame with columns: date, symbol, action, quantity, price, pnl
        """
        self.trades_df = trades_df.copy()
        self._validate_data()
        
    def _validate_data(self):
        """Validate that the trade data has required columns."""
        required_columns = ['date', 'symbol', 'action', 'quantity', 'price']
        missing_columns = [col for col in required_columns if col not in self.trades_df.columns]
        
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Ensure date column is datetime
        if not pd.api.types.is_datetime64_any_dtype(self.trades_df['date']):
            self.trades_df['date'] = pd.to_datetime(self.trades_df['date'])
    
    def calculate_pnl(self) -> pd.DataFrame:
        """
        Calculate profit and loss for each trade.
        
        Returns:
            DataFrame with added 'pnl' column
        """
        if 'pnl' not in self.trades_df.columns:
            # Group by symbol to match buy/sell pairs
            self.trades_df['pnl'] = 0.0
            
            for symbol in self.trades_df['symbol'].unique():
                symbol_trades = self.trades_df[self.trades_df['symbol'] == symbol].copy()
                symbol_trades = symbol_trades.sort_values('date')
                
                position = 0
                avg_cost = 0
                
                for idx, row in symbol_trades.iterrows():
                    if row['action'].lower() in ['buy', 'long']:
                        # Buying - update position and average cost
                        total_cost = position * avg_cost + row['quantity'] * row['price']
                        position += row['quantity']
                        avg_cost = total_cost / position if position > 0 else 0
                        self.trades_df.loc[idx, 'pnl'] = 0
                    elif row['action'].lower() in ['sell', 'short']:
                        # Selling - calculate PnL
                        pnl = row['quantity'] * (row['price'] - avg_cost)
                        self.trades_df.loc[idx, 'pnl'] = pnl
                        position -= row['quantity']
        
        return self.trades_df
    
    def get_total_pnl(self) -> float:
        """
        Calculate total profit and loss.
        
        Returns:
            Total PnL across all trades
        """
        self.calculate_pnl()
        return self.trades_df['pnl'].sum()
    
    def get_win_rate(self) -> float:
        """
        Calculate the win rate (percentage of profitable trades).
        
        Returns:
            Win rate as a percentage (0-100)
        """
        self.calculate_pnl()
        closed_trades = self.trades_df[self.trades_df['pnl'] != 0]
        
        if len(closed_trades) == 0:
            return 0.0
        
        winning_trades = len(closed_trades[closed_trades['pnl'] > 0])
        return (winning_trades / len(closed_trades)) * 100
    
    def get_average_win(self) -> float:
        """
        Calculate the average profit from winning trades.
        
        Returns:
            Average profit from winning trades
        """
        self.calculate_pnl()
        winning_trades = self.trades_df[self.trades_df['pnl'] > 0]
        
        if len(winning_trades) == 0:
            return 0.0
        
        return winning_trades['pnl'].mean()
    
    def get_average_loss(self) -> float:
        """
        Calculate the average loss from losing trades.
        
        Returns:
            Average loss from losing trades (negative value)
        """
        self.calculate_pnl()
        losing_trades = self.trades_df[self.trades_df['pnl'] < 0]
        
        if len(losing_trades) == 0:
            return 0.0
        
        return losing_trades['pnl'].mean()
    
    def get_profit_factor(self) -> float:
        """
        Calculate the profit factor (gross profit / gross loss).
        
        Returns:
            Profit factor ratio
        """
        self.calculate_pnl()
        gross_profit = self.trades_df[self.trades_df['pnl'] > 0]['pnl'].sum()
        gross_loss = abs(self.trades_df[self.trades_df['pnl'] < 0]['pnl'].sum())
        
        if gross_loss == 0:
            return float('inf') if gross_profit > 0 else 0.0
        
        return gross_profit / gross_loss
    
    def get_summary_statistics(self) -> Dict[str, float]:
        """
        Generate a comprehensive summary of trading performance.
        
        Returns:
            Dictionary containing various performance metrics
        """
        self.calculate_pnl()
        
        return {
            'total_trades': len(self.trades_df),
            'total_pnl': self.get_total_pnl(),
            'win_rate': self.get_win_rate(),
            'average_win': self.get_average_win(),
            'average_loss': self.get_average_loss(),
            'profit_factor': self.get_profit_factor(),
            'largest_win': self.trades_df['pnl'].max(),
            'largest_loss': self.trades_df['pnl'].min(),
            'total_winning_trades': len(self.trades_df[self.trades_df['pnl'] > 0]),
            'total_losing_trades': len(self.trades_df[self.trades_df['pnl'] < 0]),
        }
    
    def get_daily_pnl(self) -> pd.Series:
        """
        Calculate daily profit and loss.
        
        Returns:
            Series with daily PnL indexed by date
        """
        self.calculate_pnl()
        daily_pnl = self.trades_df.groupby(self.trades_df['date'].dt.date)['pnl'].sum()
        return daily_pnl
    
    def get_cumulative_pnl(self) -> pd.Series:
        """
        Calculate cumulative profit and loss over time.
        
        Returns:
            Series with cumulative PnL indexed by date
        """
        daily_pnl = self.get_daily_pnl()
        return daily_pnl.cumsum()


def load_trades_from_csv(filepath: str) -> pd.DataFrame:
    """
    Load trade history from a CSV file.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        DataFrame containing trade data
    """
    trades_df = pd.read_csv(filepath)
    return trades_df


def print_summary(analyzer: TradeAnalyzer):
    """
    Print a formatted summary of trading performance.
    
    Args:
        analyzer: TradeAnalyzer instance
    """
    stats = analyzer.get_summary_statistics()
    
    print("=" * 50)
    print("TRADE HISTORY ANALYSIS SUMMARY")
    print("=" * 50)
    print(f"Total Trades: {stats['total_trades']}")
    print(f"Total P&L: ${stats['total_pnl']:.2f}")
    print(f"Win Rate: {stats['win_rate']:.2f}%")
    print(f"Winning Trades: {stats['total_winning_trades']}")
    print(f"Losing Trades: {stats['total_losing_trades']}")
    print(f"Average Win: ${stats['average_win']:.2f}")
    print(f"Average Loss: ${stats['average_loss']:.2f}")
    print(f"Profit Factor: {stats['profit_factor']:.2f}")
    print(f"Largest Win: ${stats['largest_win']:.2f}")
    print(f"Largest Loss: ${stats['largest_loss']:.2f}")
    print("=" * 50)
