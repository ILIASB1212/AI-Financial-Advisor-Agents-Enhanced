from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import os
from agents import function_tool

@function_tool
def get_supplementary_financial_data(ticker: str, data_point: str) -> str:
    """
    Retrieves specific supplementary financial data points like current price, volume, or technical indicators using Alpha Vantage.
    
    Args:
        ticker: The stock ticker symbol (e.g., 'PG', 'UNH') to retrieve data for.
        data_point: The specific data point to retrieve (e.g., 'price', 'volume', '50day SMA').
    
    Returns:
        A string with the requested financial data or an error message.
    """
    
    if not os.getenv("AV_API_KEY"):
        return "ERROR: AV_API_KEY is not set in environment variables."

    try:
        ts = TimeSeries(key=os.getenv("AV_API_KEY"), output_format='json')
        ti = TechIndicators(key=os.getenv("AV_API_KEY"), output_format='json')
    except Exception as e:
        return f"ERROR: Alpha Vantage API initialization failed. {e}"

    data_point_lower = data_point.lower().replace(" ", "_")
    
    try:
        # Handle different data point requests
        if data_point_lower in ["price", "close", "latest_price", "current_price"]:
            data, _ = ts.get_quote_endpoint(symbol=ticker)
            if not data:
                return f"ERROR: Could not find quote data for ticker {ticker}."
            
            value = data.get('05. price', 'N/A')
            return f"Latest closing price for {ticker}: ${value}"
        
        elif data_point_lower in ["open", "open_price"]:
            data, _ = ts.get_quote_endpoint(symbol=ticker)
            if not data:
                return f"ERROR: Could not find quote data for ticker {ticker}."
            
            value = data.get('02. open', 'N/A')
            return f"Opening price for {ticker}: ${value}"
        
        elif data_point_lower in ["volume", "trading_volume"]:
            data, _ = ts.get_quote_endpoint(symbol=ticker)
            if not data:
                return f"ERROR: Could not find quote data for ticker {ticker}."
            
            value = data.get('06. volume', 'N/A')
            return f"Trading volume for {ticker}: {value}"
        
        elif data_point_lower in ["high", "day_high"]:
            data, _ = ts.get_quote_endpoint(symbol=ticker)
            if not data:
                return f"ERROR: Could not find quote data for ticker {ticker}."
            
            value = data.get('03. high', 'N/A')
            return f"Day high for {ticker}: ${value}"
        
        elif data_point_lower in ["low", "day_low"]:
            data, _ = ts.get_quote_endpoint(symbol=ticker)
            if not data:
                return f"ERROR: Could not find quote data for ticker {ticker}."
            
            value = data.get('04. low', 'N/A')
            return f"Day low for {ticker}: ${value}"
            
        elif "sma" in data_point_lower or "moving_average" in data_point_lower:
            data, _ = ti.get_sma(symbol=ticker, interval='daily', time_period=50, series_type='close')
            
            if not data or 'Technical Analysis: SMA' not in data:
                return f"ERROR: Could not retrieve SMA data for ticker {ticker}."
            
            latest_timestamp = next(iter(data['Technical Analysis: SMA']))
            sma_value = data['Technical Analysis: SMA'][latest_timestamp]['SMA']
            
            return f"The 50-day Simple Moving Average (SMA) for {ticker} is: ${sma_value}"
        
        elif "rsi" in data_point_lower:
            data, _ = ti.get_rsi(symbol=ticker, interval='daily', time_period=14, series_type='close')
            
            if not data or 'Technical Analysis: RSI' not in data:
                return f"ERROR: Could not retrieve RSI data for ticker {ticker}."
            
            latest_timestamp = next(iter(data['Technical Analysis: RSI']))
            rsi_value = data['Technical Analysis: RSI'][latest_timestamp]['RSI']
            
            return f"The 14-day Relative Strength Index (RSI) for {ticker} is: {rsi_value}"
            
        else:
            return (f"Data point '{data_point}' is not recognized. "
                   f"Available options: 'price', 'open', 'high', 'low', 'volume', '50day SMA', 'RSI'. "
                   f"Please specify one of these for ticker {ticker}.")

    except Exception as e:
        return f"API ERROR: Failed to retrieve '{data_point}' for {ticker}. Reason: {e}"