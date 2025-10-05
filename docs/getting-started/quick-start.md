# ⚡ Quick Start Tutorial

Get up and running with Bifrost Trader in minutes! This tutorial will guide you through your first backtest.

## 🎯 **What You'll Accomplish**

- Set up a simple trading strategy
- Run your first backtest
- View results in the web portal
- Understand the basic workflow

## 🚀 **Step 1: Access the Web Portal**

1. **Open Browser**: Navigate to http://localhost:8006
2. **Login**: Use default credentials (admin/admin)
3. **Dashboard**: You'll see the main dashboard

## 📊 **Step 2: Create Your First Strategy**

### **Strategy Configuration**
1. **Navigate**: Go to "Strategies" → "Create New"
2. **Name**: Enter "My First Strategy"
3. **Description**: Add a brief description
4. **Symbol**: Select "AAPL" (Apple stock)
5. **Timeframe**: Choose "1D" (daily)

### **Simple Moving Average Strategy**
```python
# This is a simple moving average crossover strategy
def next(self):
    # Get current price
    price = self.data.close[0]
    
    # Calculate moving averages
    sma_short = self.sma_short[0]
    sma_long = self.sma_long[0]
    
    # Buy signal: short MA crosses above long MA
    if sma_short > sma_long and not self.position:
        self.buy()
    
    # Sell signal: short MA crosses below long MA
    elif sma_short < sma_long and self.position:
        self.sell()
```

## 🔄 **Step 3: Run Your First Backtest**

### **Backtest Configuration**
1. **Strategy**: Select "My First Strategy"
2. **Start Date**: Choose "2023-01-01"
3. **End Date**: Choose "2023-12-31"
4. **Initial Capital**: Set to $10,000
5. **Commission**: Set to 0.1%

### **Execute Backtest**
1. **Click**: "Run Backtest" button
2. **Wait**: Processing will take a few moments
3. **Results**: View the backtest results

## 📈 **Step 4: Analyze Results**

### **Performance Metrics**
- **Total Return**: Overall performance
- **Sharpe Ratio**: Risk-adjusted returns
- **Max Drawdown**: Largest peak-to-trough decline
- **Win Rate**: Percentage of profitable trades

### **Charts and Visualizations**
- **Equity Curve**: Portfolio value over time
- **Drawdown Chart**: Drawdown periods
- **Trade Analysis**: Individual trade performance
- **Risk Metrics**: Risk analysis

## 🎯 **Step 5: Explore Advanced Features**

### **Portfolio Management**
1. **Create Portfolio**: Set up a new portfolio
2. **Add Positions**: Add multiple stocks
3. **Monitor Performance**: Track portfolio metrics

### **Risk Management**
1. **Set Limits**: Configure position limits
2. **Stop Loss**: Set stop-loss orders
3. **Risk Metrics**: Monitor VaR and drawdown

### **Strategy Optimization**
1. **Parameter Tuning**: Optimize strategy parameters
2. **Walk-Forward Analysis**: Test robustness
3. **Monte Carlo**: Statistical analysis

## 🔍 **Understanding the Results**

### **Key Metrics Explained**
- **Total Return**: Percentage gain/loss over the period
- **Annualized Return**: Yearly return rate
- **Volatility**: Price fluctuation measure
- **Sharpe Ratio**: Return per unit of risk
- **Max Drawdown**: Largest loss from peak

### **Trade Analysis**
- **Number of Trades**: Total trades executed
- **Average Trade**: Average profit/loss per trade
- **Win Rate**: Percentage of profitable trades
- **Profit Factor**: Gross profit / gross loss

## 🚀 **Next Steps**

### **Explore More**
1. **Try Different Strategies**: Experiment with various approaches
2. **Multiple Symbols**: Test on different stocks
3. **Timeframes**: Try different time periods
4. **Parameters**: Optimize strategy settings

### **Advanced Features**
1. **Live Trading**: Connect to live data feeds
2. **Paper Trading**: Test strategies with live data
3. **Portfolio Management**: Manage multiple portfolios
4. **Risk Management**: Implement risk controls

### **Learning Resources**
- **[Architecture Overview](../architecture/overview.md)**: Understand the system
- **[Strategy Development](../development/backtrader-integration.md)**: Learn advanced strategies
- **[AI Reference](../reference/ai-reference.md)**: AI assistant guidelines
- **[AI Collaboration](../guides/ai-collaboration.md)**: AI-assisted development

## 🎉 **Congratulations!**

You've successfully:
- ✅ Set up your first trading strategy
- ✅ Run a complete backtest
- ✅ Analyzed the results
- ✅ Explored the web portal

**🎯 You're now ready to explore more advanced features and develop sophisticated trading strategies!**

---

**Next**: Try the [Development Overview](../development/index.md) to learn about development processes and AI-assisted development.
