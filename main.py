#!/usr/bin/env python3
"""
Main script for trade history analysis.

This script demonstrates how to use the trade_analyzer module to analyze
trading history and generate visualizations.
"""

import sys
import argparse
from pathlib import Path
from trade_analyzer import load_trades_from_csv, TradeAnalyzer, print_summary
from visualize import (
    plot_cumulative_pnl,
    plot_daily_pnl,
    plot_win_loss_distribution,
    plot_performance_summary
)


def main():
    """Main function to run trade history analysis."""
    parser = argparse.ArgumentParser(
        description='Analyze trade history and generate performance reports'
    )
    parser.add_argument(
        'csv_file',
        nargs='?',
        default='sample_trades.csv',
        help='Path to CSV file containing trade history (default: sample_trades.csv)'
    )
    parser.add_argument(
        '--output-dir',
        default='output',
        help='Directory to save visualization plots (default: output)'
    )
    parser.add_argument(
        '--no-plots',
        action='store_true',
        help='Skip generating visualization plots'
    )
    
    args = parser.parse_args()
    
    # Check if CSV file exists
    csv_path = Path(args.csv_file)
    if not csv_path.exists():
        print(f"Error: File '{args.csv_file}' not found.")
        print("\nUsage: python main.py [csv_file] [--output-dir DIR] [--no-plots]")
        print("\nExpected CSV format:")
        print("date,symbol,action,quantity,price")
        print("2024-01-02,AAPL,buy,100,150.00")
        print("2024-01-05,AAPL,sell,100,155.00")
        sys.exit(1)
    
    try:
        # Load trade data
        print(f"Loading trade data from '{args.csv_file}'...")
        trades_df = load_trades_from_csv(args.csv_file)
        print(f"Loaded {len(trades_df)} trades")
        
        # Create analyzer
        analyzer = TradeAnalyzer(trades_df)
        
        # Print summary statistics
        print("\n")
        print_summary(analyzer)
        
        # Generate visualizations
        if not args.no_plots:
            output_dir = Path(args.output_dir)
            output_dir.mkdir(exist_ok=True)
            
            print(f"\nGenerating visualizations in '{args.output_dir}/' directory...")
            
            plot_cumulative_pnl(analyzer, output_dir / 'cumulative_pnl.png')
            plot_daily_pnl(analyzer, output_dir / 'daily_pnl.png')
            plot_win_loss_distribution(analyzer, output_dir / 'win_loss_distribution.png')
            plot_performance_summary(analyzer, output_dir / 'performance_dashboard.png')
            
            print("\nAll visualizations generated successfully!")
        
        print("\nAnalysis complete!")
        
    except Exception as e:
        print(f"\nError during analysis: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
