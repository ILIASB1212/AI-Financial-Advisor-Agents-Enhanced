from sec_edgar_downloader import Downloader
import os
import glob
import re
import shutil
from agents import function_tool

@function_tool
def search_sec_filings_for_risk(ticker: str, risk_keyword: str) -> str:
    """
    Download and search the latest SEC 10-K and 8-K regulatory filings 
    for formal risk factor disclosures related to a specific keyword.
    
    Args:
        ticker: The stock ticker symbol (e.g., 'PFE', 'NEM', 'AAPL') to search filings for.
        risk_keyword: The keyword to search within filings (e.g., 'geopolitical', 'litigation', 'antitrust', 'regulatory').
    
    Returns:
        A formatted string with search results or indication that no risks were found.
    """
    
    temp_dir = f"./sec_filings_temp/{ticker}_{os.getpid()}"
    
    try:
        
        dl = Downloader("InvestmentAnalysisCrew", "analysis@investment.com", temp_dir)
    except Exception as e:
        return f"ERROR: Could not initialize SEC Downloader. Reason: {e}"

    try:
        # Download latest 10-K (annual report) and 8-K (current events)
        print(f"Downloading SEC filings for {ticker}...")
        dl.get("10-K", ticker, limit=1)
        dl.get("8-K", ticker, limit=1)
    except Exception as e:
        # If download fails, still try to search existing files
        print(f"Warning: Could not download all filings for {ticker}: {e}")

    mentions = []
    
    # Search all downloaded filing text files
    search_pattern = os.path.join(temp_dir, "**", "*.txt")
    filing_paths = glob.glob(search_pattern, recursive=True)
    
    if not filing_paths:
        # Cleanup and return
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        return f"ERROR: No SEC filings could be downloaded for ticker {ticker}. Ticker may be invalid or filings unavailable."
    
    for path in filing_paths:
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Find the keyword with context (100 chars on each side for better context)
                pattern = f".{{0,100}}({re.escape(risk_keyword)}).{{0,100}}"
                matches = re.findall(pattern, content, re.IGNORECASE)
                
                if matches:
                    # Determine filing type from path
                    filing_type = "10-K" if "10-k" in path.lower() else "8-K" if "8-k" in path.lower() else "Unknown"
                    
                    # Get filename for reference
                    filename = os.path.basename(path)
                    
                    mentions.append({
                        'filing': filing_type,
                        'filename': filename,
                        'context': [m.strip() for m in matches[:3]]  
                    })
                    
        except Exception as e:
            print(f"Warning: Could not read or search file {path}: {e}")
            continue

    # Cleanup temporary directory
    try:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
    except Exception as e:
        print(f"Warning: Could not cleanup temp directory: {e}")
    
    # Format results
    if mentions:
        result = f"✅ SEC RISK DISCLOSURE FOUND for '{risk_keyword}' in {ticker} filings:\n\n"
        
        for mention in mentions:
            result += f"📄 Filing Type: {mention['filing']}\n"
            result += f"File: {mention['filename']}\n"
            result += f"Mentions Found: {len(mention['context'])}\n\n"
            
            # Add context snippets
            for i, context in enumerate(mention['context'][:2], 1):  # Show first 2
                # Clean up context for readability
                clean_context = ' '.join(context.split())
                if len(clean_context) > 300:
                    clean_context = clean_context[:300] + "..."
                result += f"Context {i}: ...{clean_context}...\n\n"
        
        result += f"⚠️ RISK ASSESSMENT: The keyword '{risk_keyword}' appears in formal SEC disclosures, "
        result += f"indicating {ticker} has acknowledged this as a material risk factor."
        
        return result
    else:
        return (
            f"ℹ️ SEC FILING SEARCH RESULT for {ticker}:\n\n"
            f"No mentions of '{risk_keyword}' found in the latest 10-K or 8-K filings.\n\n"
            f"INTERPRETATION: This risk may not be formally disclosed under this specific term, "
            f"or it may not be considered material by the company. Consider searching with "
            f"alternative keywords (e.g., 'regulation' instead of 'regulatory', 'legal' instead of 'litigation')."
        )


@function_tool
def search_sec_filings_multiple_risks(ticker: str, risk_keywords: str) -> str:
    """
    Search SEC filings for multiple risk keywords at once to get a comprehensive risk assessment.
    
    Args:
        ticker: The stock ticker symbol (e.g., 'AAPL', 'MSFT') to search filings for.
        risk_keywords: Comma-separated list of keywords to search for (e.g., 'litigation,regulatory,geopolitical').
    
    Returns:
        A summary showing which risk factors were found in SEC filings.
    """
    
    # Parse keywords
    keywords = [k.strip() for k in risk_keywords.split(',')]
    
    if len(keywords) > 10:
        return "ERROR: Maximum 10 keywords allowed. Please reduce the number of search terms."
    
    temp_dir = f"./sec_filings_temp/{ticker}_{os.getpid()}"
    
    try:
        dl = Downloader("InvestmentAnalysisCrew", "analysis@investment.com", temp_dir)
        print(f"Downloading SEC filings for {ticker}...")
        dl.get("10-K", ticker, limit=1)
        dl.get("8-K", ticker, limit=1)
    except Exception as e:
        return f"ERROR: Could not download SEC filings for {ticker}. Reason: {e}"

    # Search for all keywords
    results = {}
    
    search_pattern = os.path.join(temp_dir, "**", "*.txt")
    filing_paths = glob.glob(search_pattern, recursive=True)
    
    if not filing_paths:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        return f"ERROR: No SEC filings could be downloaded for {ticker}."
    
    # Read all filing content once
    all_content = ""
    for path in filing_paths:
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                all_content += f.read().lower() + "\n"
        except Exception as e:
            continue
    
    # Search for each keyword
    for keyword in keywords:
        count = all_content.count(keyword.lower())
        results[keyword] = count
    
    # Cleanup
    try:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
    except Exception as e:
        print(f"Warning: Could not cleanup temp directory: {e}")
    
    # Format results
    output = f"📊 SEC RISK DISCLOSURE ANALYSIS for {ticker}\n"
    output += f"Filings Searched: Latest 10-K and 8-K\n\n"
    output += "Risk Factor Mentions:\n"
    output += "-" * 50 + "\n"
    
    found_risks = []
    not_found_risks = []
    
    for keyword, count in results.items():
        if count > 0:
            risk_level = "🔴 HIGH" if count > 10 else "🟡 MODERATE" if count > 3 else "🟢 LOW"
            output += f"• {keyword.upper()}: {count} mentions - {risk_level}\n"
            found_risks.append(keyword)
        else:
            output += f"• {keyword.upper()}: Not found\n"
            not_found_risks.append(keyword)
    
    output += "\n" + "=" * 50 + "\n"
    
    if found_risks:
        output += f"\n⚠️ IDENTIFIED RISKS: {', '.join(found_risks)}"
    
    if not_found_risks:
        output += f"\n✅ NO DISCLOSURE FOR: {', '.join(not_found_risks)}"
    
    output += f"\n\nOVERALL RISK PROFILE: "
    total_mentions = sum(results.values())
    
    if total_mentions > 20:
        output += "HIGH - Multiple significant risk factors disclosed"
    elif total_mentions > 5:
        output += "MODERATE - Some material risks disclosed"
    else:
        output += "LOW - Minimal formal risk disclosures for searched terms"
    
    return output