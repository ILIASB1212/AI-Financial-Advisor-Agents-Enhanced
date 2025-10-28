import yfinance as yf
from agents import function_tool

@function_tool
def calculate_historical_correlation(ticker_1: str, ticker_2: str, period: str = "1y") -> str:
    """
    Calculate the historical correlation coefficient between two stocks' daily returns 
    for portfolio diversification assessment.
    
    Args:
        ticker_1: The first stock ticker symbol (e.g., 'PG', 'AAPL').
        ticker_2: The second stock ticker symbol (e.g., 'KO', 'MSFT').
        period: The historical period for calculation. Options: '1mo', '3mo', '6mo', '1y', '2y', '3y', '5y'. Default is '1y'.
    
    Returns:
        A formatted string with the correlation coefficient and diversification assessment.
    """
    try:
        data = yf.download([ticker_1, ticker_2], period=period, progress=False)
        
        if data.empty:
            return f"ERROR: Could not retrieve data for {ticker_1} and/or {ticker_2} over period {period}."
        
        returns = data['Close'].pct_change().dropna()
        
        if ticker_1 not in returns.columns or ticker_2 not in returns.columns:
            return f"ERROR: Could not retrieve sufficient data for one or both tickers ({ticker_1}, {ticker_2}) over the period {period}."
        
        if returns.empty or len(returns) < 20:
            return f"ERROR: Insufficient data points for correlation calculation. Need at least 20 trading days, got {len(returns)}."
        
        correlation = returns.corr().loc[ticker_1, ticker_2]
        
        if correlation < 0:
            interpretation = "EXCELLENT diversification (negative correlation - moves in opposite directions)"
        elif correlation < 0.3:
            interpretation = "VERY GOOD diversification (low positive correlation)"
        elif correlation < 0.5:
            interpretation = "GOOD diversification (moderate-low correlation)"
        elif correlation < 0.7:
            interpretation = "FAIR diversification (moderate correlation)"
        elif correlation < 0.85:
            interpretation = "LIMITED diversification (high correlation)"
        else:
            interpretation = "POOR diversification (very high correlation - moves almost identically)"
        
        return f"""Historical Correlation Analysis:
- Tickers: {ticker_1} vs {ticker_2}
- Period: {period}
- Correlation Coefficient (ρ): {correlation:.3f}
- Data Points: {len(returns)} trading days
- Diversification Assessment: {interpretation}

Interpretation: A correlation of {correlation:.3f} means the stocks move {"together" if correlation > 0.5 else "somewhat independently"}. {"Consider these for portfolio diversification." if correlation < 0.7 else "These stocks may provide limited diversification benefits."}"""
    
    except Exception as e:
        return f"ERROR: Failed to calculate correlation for {ticker_1} and {ticker_2}. Reason: {e}"


@function_tool
def calculate_portfolio_correlation_matrix(tickers: str, period: str = "1y") -> str:
    """
    Calculate a correlation matrix for multiple stocks to assess overall portfolio diversification.
    
    Args:
        tickers: Comma-separated list of stock ticker symbols (e.g., 'AAPL,MSFT,GOOGL,TSLA').
        period: The historical period for calculation. Options: '1mo', '3mo', '6mo', '1y', '2y', '3y', '5y'. Default is '1y'.
    
    Returns:
        A formatted correlation matrix showing relationships between all stock pairs.
    """
    try:
        ticker_list = [t.strip().upper() for t in tickers.split(',')]
        
        if len(ticker_list) < 2:
            return "ERROR: Please provide at least 2 tickers separated by commas."
        
        if len(ticker_list) > 10:
            return "ERROR: Maximum 10 tickers allowed for correlation matrix calculation."
        
        data = yf.download(ticker_list, period=period, progress=False)
        
        if data.empty:
            return f"ERROR: Could not retrieve data for the provided tickers over period {period}."
        
        returns = data['Close'].pct_change().dropna()
        
        missing_tickers = [t for t in ticker_list if t not in returns.columns]
        if missing_tickers:
            return f"ERROR: Could not retrieve data for: {', '.join(missing_tickers)}"
        
        if len(returns) < 20:
            return f"ERROR: Insufficient data points. Need at least 20 trading days, got {len(returns)}."
        
        corr_matrix = returns.corr()
        
        result = f"""Portfolio Correlation Matrix ({period})
Data Points: {len(returns)} trading days
"""
        
        # Create header row
        header = "Ticker  | " + " | ".join([f"{t:6s}" for t in ticker_list])
        separator = "-" * len(header)
        result += f"\n{header}\n{separator}\n"
        
        for ticker in ticker_list:
            row = f"{ticker:7s} | "
            row += " | ".join([f"{corr_matrix.loc[ticker, t]:6.3f}" for t in ticker_list])
            result += row + "\n"
        
        avg_corr = corr_matrix.values[corr_matrix.values != 1.0].mean()
        result += f"\n📊 Average Correlation: {avg_corr:.3f}"
        
        if avg_corr < 0.3:
            result += "\n✅ EXCELLENT portfolio diversification"
        elif avg_corr < 0.5:
            result += "\n✅ GOOD portfolio diversification"
        elif avg_corr < 0.7:
            result += "\n⚠️  MODERATE portfolio diversification"
        else:
            result += "\n❌ LIMITED portfolio diversification - consider more diverse holdings"
        
        return result
    
    except Exception as e:
        return f"ERROR: Failed to calculate correlation matrix. Reason: {e}"