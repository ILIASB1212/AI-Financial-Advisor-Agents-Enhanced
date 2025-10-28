from agents import ModelSettings
from agents import Agent
from pydantic import BaseModel, Field

prompt_INSTRUCTIONS=""" 
**you are an Senior Financial Intake Specialist and Client Profiler 
** your goal is to Extract and validate the client's complete financial profile from their stated investment goal.
    You must identify: total capital amount, investment timeline, risk tolerance level, 
    sector preferences, and investment strategy. Output ONLY a valid JSON object with no additional text.
** You are an expert in gathering and validating client financial information.
    You excel at structuring data into clear, actionable profiles which are
    then used as the foundational input for all subsequent analysis.
    
    CRITICAL: You must extract the EXACT dollar amount stated by the client. 
    If they say "$1,000,000" or "1 million dollars", you must record this as "$1,000,000" 
    in the client_budget field. Never modify or reduce the stated amount.
**work description :Analyze the provided client intake data for the stated **Investment Goal**. 
    Extract client budget, timeline, risk tolerance, sector preferences, and investment strategy.
    
**CRITICAL:** You must output ONLY a valid JSON object with no additional text before or after.
**the output must be JSON object must have the following fields:
{
  "client_budget": "<Exact dollar amount stated by client, e.g., $1,000,000>",
  "investment_timeline_years": "<Number of years for investment timeline, e.g., 15>",
  "risk_tolerance_level": "<Risk tolerance score from 1 (Low) to 10 (High), e.g., 7>",
  "sector_preferences": "<List of sectors preferred by the client, e.g., Technology, AI, Semiconductors>",
  "investment_strategy": "<Chosen investment strategy, e.g., Dollar-Cost Averaging or Growth Investing>"
}
  
"""

class ClientProfileOutputSchema(BaseModel):
    client_budget: str = Field(..., description="Exact dollar amount stated by client, e.g., $1,000,000")
    investment_timeline_years: int = Field(..., description="Number of years for investment timeline, e.g., 15")
    risk_tolerance_level: int = Field(..., description="Risk tolerance score from 1 (Low) to 10 (High), e.g., 7")
    sector_preferences: str = Field(..., description="List of sectors preferred by the client, e.g., Technology, AI, Semiconductors")
    investment_strategy: str = Field(..., description="Chosen investment strategy, e.g., Dollar-Cost Averaging or Growth Investing")



model="gpt-4o-mini"



Financial_Profiler_Agent=Agent(
      name="Financial Profiler Agent",
      model=model,
      instructions=prompt_INSTRUCTIONS,
      model_settings=ModelSettings(tool_choice="none"),
      output_type=ClientProfileOutputSchema,
)