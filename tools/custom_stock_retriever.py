import yfinance as yf
from agents import function_tool
from typing import Optional


def _fetch_stock_fundamentals_core(ticker: str) -> str:
    """
    Core logic to fetch and format comprehensive stock fundamentals using yfinance.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Extract key metrics with fallbacks
        price = info.get('currentPrice', info.get('regularMarketPrice', 'N/A'))
        market_cap = info.get('marketCap', 'N/A')
        pe_ratio = info.get('trailingPE', info.get('forwardPE', 'N/A'))
        beta = info.get('beta', 'N/A')
        debt_to_equity = info.get('debtToEquity', 'N/A')
        dividend_yield = info.get('dividendYield', 'N/A')
        sector = info.get('sector', 'N/A')
        
        # Format market cap for readability
        if isinstance(market_cap, (int, float)):
            # Use 'g' format specifier to handle very large numbers gracefully
            market_cap_str = f"${market_cap:,.0f}" 
        else:
            market_cap_str = str(market_cap)
        
        # Format dividend yield as percentage
        if isinstance(dividend_yield, (int, float)):
            dividend_yield_str = f"{dividend_yield * 100:.2f}%"
        else:
            dividend_yield_str = str(dividend_yield)
        
        result = f"""
Stock Fundamentals for {ticker}:
- Current Price: ${price}
- Market Cap: {market_cap_str}
- P/E Ratio: {pe_ratio}
- Beta: {beta}
- Debt-to-Equity: {debt_to_equity}
- Dividend Yield: {dividend_yield_str}
- Sector: {sector}
"""
        return result.strip()
        
    except Exception as e:
        return f"ERROR: Could not retrieve data for ticker {ticker}. Reason: {e}"

# --- TOOL 1: WRAPPER FOR AGENT USE ---
@function_tool
def get_stock_fundamentals(ticker: str) -> str:
    """
    Retrieves comprehensive stock fundamentals including price, market cap, 
    P/E ratio, beta, debt-to-equity, and dividend information.
    
    Args:
        ticker: The stock ticker symbol (e.g., 'AAPL', 'MSFT') to retrieve data for.
    
    Returns:
        A formatted string with fundamental stock data or an error message.
    """
    # Calls the safe, non-decorated core logic
    return _fetch_stock_fundamentals_core(ticker)


# --- TOOL 2: CORRECTED FINANCIAL METRICS TOOL ---
@function_tool
def get_stock_financial_metrics(ticker: str, metric_type: str = "all") -> str:
    """
    Retrieves specific financial metrics like FCF, revenue growth, or profitability ratios.
    
    Args:
        ticker: The stock ticker symbol (e.g., 'AAPL', 'MSFT').
        metric_type: Type of metric to retrieve - 'fcf' (free cash flow), 
                    'growth' (revenue/earnings growth), 'profitability' (margins), or 'all'.
    
    Returns:
        A formatted string with the requested financial metrics.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        metric_type = metric_type.lower()
        
        if metric_type in ["fcf", "cashflow", "free_cash_flow"]:
            fcf = info.get('freeCashflow', 'N/A')
            operating_cf = info.get('operatingCashflow', 'N/A')
            
            # Note: Cleaned up the formatting logic slightly for readability
            fcf_str = f"${fcf:,.0f}" if isinstance(fcf, (int, float)) else str(fcf)
            operating_cf_str = f"${operating_cf:,.0f}" if isinstance(operating_cf, (int, float)) else str(operating_cf)

            result = f"""
Cash Flow Metrics for {ticker}:
- Free Cash Flow: {fcf_str}
- Operating Cash Flow: {operating_cf_str}
"""
            return result.strip()
        
        elif metric_type in ["growth", "revenue_growth"]:
            revenue_growth = info.get('revenueGrowth', 'N/A')
            earnings_growth = info.get('earningsGrowth', 'N/A')
            
            if isinstance(revenue_growth, (int, float)):
                revenue_growth = f"{revenue_growth * 100:.2f}%"
            if isinstance(earnings_growth, (int, float)):
                earnings_growth = f"{earnings_growth * 100:.2f}%"
            
            result = f"""
Growth Metrics for {ticker}:
- Revenue Growth: {revenue_growth}
- Earnings Growth: {earnings_growth}
"""
            return result.strip()
        
        elif metric_type in ["profitability", "margins"]:
            profit_margin = info.get('profitMargins', 'N/A')
            operating_margin = info.get('operatingMargins', 'N/A')
            roe = info.get('returnOnEquity', 'N/A')
            
            if isinstance(profit_margin, (int, float)):
                profit_margin = f"{profit_margin * 100:.2f}%"
            if isinstance(operating_margin, (int, float)):
                operating_margin = f"{operating_margin * 100:.2f}%"
            if isinstance(roe, (int, float)):
                roe = f"{roe * 100:.2f}%"
            
            result = f"""
Profitability Metrics for {ticker}:
- Profit Margin: {profit_margin}
- Operating Margin: {operating_margin}
- Return on Equity (ROE): {roe}
"""
            return result.strip()
        
        else:  
            # *** CRITICAL FIX: Calling the safe, non-decorated core helper function ***
            return _fetch_stock_fundamentals_core(ticker)
            
    except Exception as e:
        return f"ERROR: Could not retrieve {metric_type} metrics for {ticker}. Reason: {e}"


# --- TOOL 3: REMAINS UNCHANGED ---
@function_tool
def check_stock_risk_indicators(ticker: str) -> str:
    """
    Checks key risk indicators for a stock including volatility, analyst ratings, and ESG risk.
    
    Args:
        ticker: The stock ticker symbol (e.g., 'AAPL', 'MSFT').
    
    Returns:
        A formatted string with risk assessment data.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        beta = info.get('beta', 'N/A')
        fifty_two_week_high = info.get('fiftyTwoWeekHigh', 'N/A')
        fifty_two_week_low = info.get('fiftyTwoWeekLow', 'N/A')
        current_price = info.get('currentPrice', info.get('regularMarketPrice', 'N/A'))
        recommendation = info.get('recommendationKey', 'N/A')
        target_mean_price = info.get('targetMeanPrice', 'N/A')
        
        if isinstance(current_price, (int, float)) and isinstance(fifty_two_week_high, (int, float)):
            distance_from_high = ((current_price - fifty_two_week_high) / fifty_two_week_high) * 100
            distance_str = f"{distance_from_high:.2f}%"
        else:
            distance_str = "N/A"
        
        result = f"""
Risk Indicators for {ticker}:
- Beta (Volatility): {beta}
- 52-Week High: ${fifty_two_week_high}
- 52-Week Low: ${fifty_two_week_low}
- Current Price: ${current_price}
- Distance from 52-Week High: {distance_str}
- Analyst Recommendation: {recommendation}
- Analyst Target Price: ${target_mean_price}
"""
        return result.strip()
        
    except Exception as e:
        return f"ERROR: Could not retrieve risk indicators for {ticker}. Reason: {e}"