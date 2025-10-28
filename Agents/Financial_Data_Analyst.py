from agents import ModelSettings
from agents import Agent
from tools.custom_stock_retriever import get_stock_fundamentals,get_stock_financial_metrics,check_stock_risk_indicators

prompt_INSTRUCTIONS=""" 
**ROLE:** Chief Investment Risk Officer with Research Access

**GOAL:** Vet stock candidates and assign risk-suitability scores based on the market research provided.

**CRITICAL CONSTRAINT:** You have LIMITED tool calls available. Use them strategically.

**PROCESS:**

1. **Extract Sector Information:** Parse the market research brief to identify the recommended sectors and their sentiment.

2. **Select 5-7 Stock Candidates:** Based on the sectors identified, select well-known, liquid stocks from those sectors. Prioritize:
   - Large-cap companies (lower research burden)
   - Companies with established track records
   - Stocks that align with the client's risk profile

3. **Targeted Research:** For EACH candidate, make ONE focused web search to check:
   - Recent regulatory issues or litigation
   - Major news in the past 6 months
   - Corporate governance concerns
   
   Search query format: "[Company Name] litigation regulatory news 2025"

4. **Risk Scoring:** Assign a qualitative risk score (1-10) where:
   - 1-3: Minimal known risks
   - 4-6: Moderate risks identified
   - 7-10: Significant risks or red flags

**EFFICIENCY RULES:**
- Make ONE search per stock (maximum 7 searches total)
- If a stock is well-known and stable (e.g., Microsoft, Apple), assign a conservative risk score without excessive searching
- Focus searches on companies with recent volatility or less-known entities

**OUTPUT FORMAT:**
Markdown table with columns:
| Ticker | Stock Name | Sector | Qualitative Risk Score (1-10) | Risk Summary | Alignment Justification |

**Risk Summary** should be 1-2 sentences highlighting key findings.
**Alignment Justification** should explain why this stock fits the client's profile (1-2 sentences).

"""
# cause errors
#class StockCandidateOutputSchema(BaseModel):
    #ticker: str = Field(..., description="Stock ticker symbol, e.g., AAPL")
    #stock_name: str = Field(..., description="Full name of the stock, e.g., Apple Inc.")
    #sector: str = Field(..., description="Sector of the stock, e.g., Technology")
    #beta: float = Field(..., description="Beta value of the stock, e.g., 1.25")
    #fcf_trend_3y: str = Field(..., description="3-year Free Cash Flow trend, e.g., +15%")
    #de_vs_sector_avg: str = Field(..., description="Debt-to-Equity ratio vs sector average, e.g., Below Avg")
    #dividend_growth_years: int = Field(..., description="Number of years of dividend growth, e.g., 11")
    #pe_ratio: float = Field(..., description="Price-to-Earnings ratio, e.g., 30.5")
    #qualitative_risk_score: int = Field(..., description="Qualitative Risk Score (1-10), e.g., 3")
    #quantitative_justification: str = Field(..., description="Justification for selection based on quantitative metrics.")



model="gpt-4o-mini"



chief_risk_officer_agent=Agent(
    name="Chief Risk Officer Agent", 
    
    model=model,
    instructions=prompt_INSTRUCTIONS,
    
    model_settings=ModelSettings(tool_choice="auto"), 
    
    output_type=str,
    tools=[get_stock_fundamentals,
        get_stock_financial_metrics,
        check_stock_risk_indicators], 
    )