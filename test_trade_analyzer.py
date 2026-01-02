"""
Unit tests for the trade_analyzer module.
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime
from trade_analyzer import TradeAnalyzer, load_trades_from_csv


class TestTradeAnalyzer(unittest.TestCase):
    """Test cases for TradeAnalyzer class."""
    
    def setUp(self):
        """Set up test data before each test."""
        self.sample_data = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04']),
            'symbol': ['AAPL', 'AAPL', 'GOOGL', 'GOOGL'],
            'action': ['buy', 'sell', 'buy', 'sell'],
            'quantity': [100, 100, 50, 50],
            'price': [150.0, 155.0, 120.0, 118.0]
        })
    
    def test_initialization(self):
        """Test TradeAnalyzer initialization."""
        analyzer = TradeAnalyzer(self.sample_data)
        self.assertIsNotNone(analyzer.trades_df)
        self.assertEqual(len(analyzer.trades_df), 4)
    
    def test_validation_missing_columns(self):
        """Test that validation catches missing columns."""
        invalid_data = pd.DataFrame({
            'date': ['2024-01-01'],
            'symbol': ['AAPL']
        })
        
        with self.assertRaises(ValueError) as context:
            TradeAnalyzer(invalid_data)
        
        self.assertIn('Missing required columns', str(context.exception))
    
    def test_calculate_pnl(self):
        """Test PnL calculation."""
        analyzer = TradeAnalyzer(self.sample_data)
        result = analyzer.calculate_pnl()
        
        self.assertIn('pnl', result.columns)
        # First AAPL trade: buy at 150, sell at 155 = +500
        # GOOGL trade: buy at 120, sell at 118 = -100
        expected_pnl_sum = 500 + (-100)
        self.assertAlmostEqual(result['pnl'].sum(), expected_pnl_sum, places=2)
    
    def test_get_total_pnl(self):
        """Test total PnL calculation."""
        analyzer = TradeAnalyzer(self.sample_data)
        total_pnl = analyzer.get_total_pnl()
        
        # 100 * (155 - 150) + 50 * (118 - 120) = 500 - 100 = 400
        self.assertAlmostEqual(total_pnl, 400.0, places=2)
    
    def test_get_win_rate(self):
        """Test win rate calculation."""
        analyzer = TradeAnalyzer(self.sample_data)
        win_rate = analyzer.get_win_rate()
        
        # 1 winning trade out of 2 closed trades = 50%
        self.assertAlmostEqual(win_rate, 50.0, places=2)
    
    def test_get_average_win(self):
        """Test average win calculation."""
        analyzer = TradeAnalyzer(self.sample_data)
        avg_win = analyzer.get_average_win()
        
        # Only one winning trade with profit of 500
        self.assertAlmostEqual(avg_win, 500.0, places=2)
    
    def test_get_average_loss(self):
        """Test average loss calculation."""
        analyzer = TradeAnalyzer(self.sample_data)
        avg_loss = analyzer.get_average_loss()
        
        # Only one losing trade with loss of -100
        self.assertAlmostEqual(avg_loss, -100.0, places=2)
    
    def test_get_profit_factor(self):
        """Test profit factor calculation."""
        analyzer = TradeAnalyzer(self.sample_data)
        profit_factor = analyzer.get_profit_factor()
        
        # Gross profit: 500, Gross loss: 100, Profit factor: 5.0
        self.assertAlmostEqual(profit_factor, 5.0, places=2)
    
    def test_get_summary_statistics(self):
        """Test summary statistics generation."""
        analyzer = TradeAnalyzer(self.sample_data)
        stats = analyzer.get_summary_statistics()
        
        required_keys = [
            'total_trades', 'total_pnl', 'win_rate', 'average_win',
            'average_loss', 'profit_factor', 'largest_win', 'largest_loss',
            'total_winning_trades', 'total_losing_trades'
        ]
        
        for key in required_keys:
            self.assertIn(key, stats)
        
        self.assertEqual(stats['total_trades'], 4)
        self.assertEqual(stats['total_winning_trades'], 1)
        self.assertEqual(stats['total_losing_trades'], 1)
    
    def test_get_daily_pnl(self):
        """Test daily PnL calculation."""
        analyzer = TradeAnalyzer(self.sample_data)
        daily_pnl = analyzer.get_daily_pnl()
        
        self.assertIsInstance(daily_pnl, pd.Series)
        # Should have PnL for dates with sell trades
        self.assertTrue(len(daily_pnl) > 0)
    
    def test_get_cumulative_pnl(self):
        """Test cumulative PnL calculation."""
        analyzer = TradeAnalyzer(self.sample_data)
        cumulative_pnl = analyzer.get_cumulative_pnl()
        
        self.assertIsInstance(cumulative_pnl, pd.Series)
        # Final cumulative value should equal total PnL
        self.assertAlmostEqual(cumulative_pnl.iloc[-1], analyzer.get_total_pnl(), places=2)
    
    def test_empty_dataframe(self):
        """Test handling of empty DataFrame."""
        empty_data = pd.DataFrame(columns=['date', 'symbol', 'action', 'quantity', 'price'])
        analyzer = TradeAnalyzer(empty_data)
        
        self.assertEqual(analyzer.get_total_pnl(), 0.0)
        self.assertEqual(analyzer.get_win_rate(), 0.0)
    
    def test_multiple_positions_same_symbol(self):
        """Test handling of multiple positions in the same symbol."""
        multi_position_data = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05']),
            'symbol': ['AAPL', 'AAPL', 'AAPL', 'AAPL', 'AAPL'],
            'action': ['buy', 'buy', 'sell', 'sell', 'sell'],
            'quantity': [100, 100, 50, 50, 100],
            'price': [150.0, 152.0, 160.0, 158.0, 155.0]
        })
        
        analyzer = TradeAnalyzer(multi_position_data)
        total_pnl = analyzer.get_total_pnl()
        
        # Average cost: (100*150 + 100*152) / 200 = 151
        # Sell 50 at 160: 50 * (160 - 151) = 450
        # Sell 50 at 158: 50 * (158 - 151) = 350
        # Sell 100 at 155: 100 * (155 - 151) = 400
        # Total: 450 + 350 + 400 = 1200
        self.assertAlmostEqual(total_pnl, 1200.0, places=2)


class TestLoadTradesFromCSV(unittest.TestCase):
    """Test cases for CSV loading function."""
    
    def test_load_sample_trades(self):
        """Test loading the sample trades CSV file."""
        try:
            trades_df = load_trades_from_csv('sample_trades.csv')
            self.assertIsInstance(trades_df, pd.DataFrame)
            self.assertTrue(len(trades_df) > 0)
        except FileNotFoundError:
            self.skipTest("sample_trades.csv not found")


if __name__ == '__main__':
    unittest.main()
