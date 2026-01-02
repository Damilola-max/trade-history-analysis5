# Trade History Analysis

A Python-based tool for analyzing trading history, calculating performance metrics, and generating visualizations.

## Features

- 📊 **Comprehensive Performance Metrics**: Calculate total P&L, win rate, profit factor, and more
- 📈 **Visual Analytics**: Generate cumulative P&L charts, daily P&L bars, and performance dashboards
- 📁 **CSV Support**: Easy import of trade history from CSV files
- 🧪 **Well-Tested**: Comprehensive unit tests for reliability
- 🎯 **Easy to Use**: Simple API and command-line interface

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Damilola-max/trade-history-analysis5.git
cd trade-history-analysis5
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

Run the analysis on sample data:
```bash
python main.py
```

Run analysis on your own CSV file:
```bash
python main.py your_trades.csv
```

## CSV Format

Your trade history CSV should have the following columns:

```csv
date,symbol,action,quantity,price
2024-01-02,AAPL,buy,100,150.00
2024-01-05,AAPL,sell,100,155.00
```

Required columns:
- `date`: Trade date (YYYY-MM-DD format)
- `symbol`: Stock/asset symbol
- `action`: Trade action (buy/sell)
- `quantity`: Number of shares/units
- `price`: Price per share/unit

## Usage

### Command Line

```bash
# Analyze trades and generate visualizations
python main.py trades.csv

# Specify output directory for plots
python main.py trades.csv --output-dir results

# Skip plot generation (stats only)
python main.py trades.csv --no-plots
```

### Python API

```python
from trade_analyzer import load_trades_from_csv, TradeAnalyzer, print_summary
from visualize import plot_performance_summary

# Load trade data
trades_df = load_trades_from_csv('trades.csv')

# Create analyzer
analyzer = TradeAnalyzer(trades_df)

# Print summary statistics
print_summary(analyzer)

# Get specific metrics
total_pnl = analyzer.get_total_pnl()
win_rate = analyzer.get_win_rate()
profit_factor = analyzer.get_profit_factor()

# Generate visualizations
plot_performance_summary(analyzer, 'dashboard.png')
```

## Performance Metrics

The tool calculates the following metrics:

- **Total P&L**: Total profit/loss across all trades
- **Win Rate**: Percentage of profitable trades
- **Average Win**: Average profit from winning trades
- **Average Loss**: Average loss from losing trades
- **Profit Factor**: Ratio of gross profit to gross loss
- **Largest Win/Loss**: Maximum profit and loss from single trades
- **Daily P&L**: Profit/loss aggregated by day
- **Cumulative P&L**: Running total of profit/loss over time

## Visualizations

The tool generates four types of visualizations:

1. **Cumulative P&L**: Line chart showing profit/loss progression over time
2. **Daily P&L**: Bar chart of daily profits and losses
3. **Win/Loss Distribution**: Histograms showing the distribution of winning and losing trades
4. **Performance Dashboard**: Comprehensive view combining all metrics and charts

## Running Tests

```bash
python -m unittest test_trade_analyzer.py
```

Or run tests with verbose output:
```bash
python -m unittest test_trade_analyzer.py -v
```

## Project Structure

```
trade-history-analysis5/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── .gitignore                  # Git ignore rules
├── trade_analyzer.py           # Core analysis module
├── visualize.py                # Visualization functions
├── main.py                     # Command-line interface
├── test_trade_analyzer.py      # Unit tests
├── sample_trades.csv           # Sample trade data
└── output/                     # Generated plots (created on run)
```

## Example Output

When you run the analysis, you'll see output like:

```
==================================================
TRADE HISTORY ANALYSIS SUMMARY
==================================================
Total Trades: 20
Total P&L: $3900.00
Win Rate: 70.00%
Winning Trades: 7
Losing Trades: 3
Average Win: $750.00
Average Loss: $-150.00
Profit Factor: 3.25
Largest Win: $1800.00
Largest Loss: $-400.00
==================================================
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.
