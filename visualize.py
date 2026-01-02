"""
Visualization module for trade history analysis.

This module provides functions to create charts and plots for trade analysis.
"""

import matplotlib.pyplot as plt
import pandas as pd
from typing import Optional
from trade_analyzer import TradeAnalyzer


def plot_cumulative_pnl(analyzer: TradeAnalyzer, save_path: Optional[str] = None):
    """
    Plot cumulative profit and loss over time.
    
    Args:
        analyzer: TradeAnalyzer instance
        save_path: Optional path to save the plot
    """
    cumulative_pnl = analyzer.get_cumulative_pnl()
    
    plt.figure(figsize=(12, 6))
    plt.plot(cumulative_pnl.index, cumulative_pnl.values, linewidth=2, color='blue')
    plt.axhline(y=0, color='red', linestyle='--', alpha=0.5)
    plt.title('Cumulative P&L Over Time', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Cumulative P&L ($)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {save_path}")
    else:
        plt.show()
    
    plt.close()


def plot_daily_pnl(analyzer: TradeAnalyzer, save_path: Optional[str] = None):
    """
    Plot daily profit and loss as a bar chart.
    
    Args:
        analyzer: TradeAnalyzer instance
        save_path: Optional path to save the plot
    """
    daily_pnl = analyzer.get_daily_pnl()
    
    colors = ['green' if x > 0 else 'red' for x in daily_pnl.values]
    
    plt.figure(figsize=(12, 6))
    plt.bar(range(len(daily_pnl)), daily_pnl.values, color=colors, alpha=0.7)
    plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    plt.title('Daily P&L', fontsize=16, fontweight='bold')
    plt.xlabel('Trading Day', fontsize=12)
    plt.ylabel('Daily P&L ($)', fontsize=12)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {save_path}")
    else:
        plt.show()
    
    plt.close()


def plot_win_loss_distribution(analyzer: TradeAnalyzer, save_path: Optional[str] = None):
    """
    Plot the distribution of winning and losing trades.
    
    Args:
        analyzer: TradeAnalyzer instance
        save_path: Optional path to save the plot
    """
    # Ensure PnL is calculated (method is idempotent)
    if 'pnl' not in analyzer.trades_df.columns:
        analyzer.calculate_pnl()
    trades = analyzer.trades_df[analyzer.trades_df['pnl'] != 0]['pnl']
    
    winning_trades = trades[trades > 0]
    losing_trades = trades[trades < 0]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Winning trades histogram
    if len(winning_trades) > 0:
        ax1.hist(winning_trades, bins=20, color='green', alpha=0.7, edgecolor='black')
        ax1.set_title('Winning Trades Distribution', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Profit ($)', fontsize=12)
        ax1.set_ylabel('Frequency', fontsize=12)
        ax1.grid(True, alpha=0.3)
    
    # Losing trades histogram
    if len(losing_trades) > 0:
        ax2.hist(losing_trades, bins=20, color='red', alpha=0.7, edgecolor='black')
        ax2.set_title('Losing Trades Distribution', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Loss ($)', fontsize=12)
        ax2.set_ylabel('Frequency', fontsize=12)
        ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {save_path}")
    else:
        plt.show()
    
    plt.close()


def plot_performance_summary(analyzer: TradeAnalyzer, save_path: Optional[str] = None):
    """
    Create a comprehensive performance summary dashboard.
    
    Args:
        analyzer: TradeAnalyzer instance
        save_path: Optional path to save the plot
    """
    stats = analyzer.get_summary_statistics()
    cumulative_pnl = analyzer.get_cumulative_pnl()
    daily_pnl = analyzer.get_daily_pnl()
    
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
    
    # Cumulative P&L
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(cumulative_pnl.index, cumulative_pnl.values, linewidth=2, color='blue')
    ax1.axhline(y=0, color='red', linestyle='--', alpha=0.5)
    ax1.set_title('Cumulative P&L Over Time', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Date', fontsize=10)
    ax1.set_ylabel('Cumulative P&L ($)', fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='x', rotation=45)
    
    # Daily P&L
    ax2 = fig.add_subplot(gs[1, :])
    colors = ['green' if x > 0 else 'red' for x in daily_pnl.values]
    ax2.bar(range(len(daily_pnl)), daily_pnl.values, color=colors, alpha=0.7)
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    ax2.set_title('Daily P&L', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Trading Day', fontsize=10)
    ax2.set_ylabel('Daily P&L ($)', fontsize=10)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Win/Loss Pie Chart
    ax3 = fig.add_subplot(gs[2, 0])
    win_loss_data = [stats['total_winning_trades'], stats['total_losing_trades']]
    ax3.pie(win_loss_data, labels=['Winning', 'Losing'], 
            autopct='%1.1f%%', colors=['green', 'red'], startangle=90)
    ax3.set_title('Win/Loss Ratio', fontsize=14, fontweight='bold')
    
    # Statistics Table
    ax4 = fig.add_subplot(gs[2, 1])
    ax4.axis('off')
    
    table_data = [
        ['Total Trades', f"{stats['total_trades']}"],
        ['Total P&L', f"${stats['total_pnl']:.2f}"],
        ['Win Rate', f"{stats['win_rate']:.2f}%"],
        ['Avg Win', f"${stats['average_win']:.2f}"],
        ['Avg Loss', f"${stats['average_loss']:.2f}"],
        ['Profit Factor', f"{stats['profit_factor']:.2f}"],
    ]
    
    table = ax4.table(cellText=table_data, cellLoc='left',
                     colWidths=[0.5, 0.5], loc='center',
                     bbox=[0, 0, 1, 1])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    
    # Style the table
    for i in range(len(table_data)):
        table[(i, 0)].set_facecolor('#E0E0E0')
        table[(i, 0)].set_text_props(weight='bold')
    
    ax4.set_title('Performance Statistics', fontsize=14, fontweight='bold', pad=20)
    
    plt.suptitle('Trade Performance Dashboard', fontsize=18, fontweight='bold', y=0.995)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Dashboard saved to {save_path}")
    else:
        plt.show()
    
    plt.close()
