from dotenv import load_dotenv
from agents import Runner, trace
import os
import asyncio
import streamlit as st
from Agents.client_recipt import Financial_Profiler_Agent
from Agents.Market_Research_Analyst import financial_analyst
from Agents.Financial_Data_Analyst import chief_risk_officer_agent
from Agents.Risk_Management_Specialist import risk_management_specialist
from Agents.Investment_Strategist import portfolio_manager_agent
from Agents.Final_Report_Generator import final_report_agent
import logging

# Setup logging for verbose output
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# Enable agents SDK logging
logging.getLogger("agents").setLevel(logging.DEBUG)
logging.getLogger("openai").setLevel(logging.DEBUG)

# Load environment variables
load_dotenv()

# Set API keys
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
# Alpha Vantage API key
os.environ["AV_API_KEY"] = os.getenv("AV_API_KEY")  

# Streamlit UI
st.set_page_config(
    page_title="Investment Research Assistant",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI Investment Research Assistant")
st.markdown("---")

# Input section
st.subheader("Investment Goal Input")
query = st.text_area(
    "Describe your investment goal:",
    placeholder="Example: I want to invest $1,000,000 over 15 years in Technology and Semiconductors sectors with a risk tolerance of 7/10 using Growth Investing strategy.",
    height=150,
    key="query_input"
)

col1, col2 = st.columns([1, 5])
with col1:
    start_button = st.button("🚀 Start Analysis", type="primary")

st.markdown("---")

if start_button and query:
    async def main():
        try:
            with trace("investment_analysis_trace"):
                
                # Progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # ============================================================
                # STEP 1: Financial Profiler Agent
                # ============================================================
                status_text.text("Step 1/6: Analyzing client profile...")
                progress_bar.progress(10)
                
                with st.expander("📋 Step 1: Client Profile Extraction", expanded=False):
                    st.info("Extracting and validating investment parameters...")
                    
                    print(f"\n{'='*70}")
                    print(f"STEP 1: FINANCIAL PROFILER AGENT")
                    print(f"Query: {query}")
                    print(f"{'='*70}\n")
                    
                    client_profile_result = await Runner.run(
                        Financial_Profiler_Agent, 
                        f"Client Investment Goal: {query}",
                        max_turns=20
                    )
                    
                    client_profile = client_profile_result.final_output
                    
                    print(f"\n{'='*70}")
                    print(f"CLIENT PROFILE OUTPUT:")
                    print(client_profile)
                    print(f"{'='*70}\n")
                    
                    st.success("✅ Client profile extracted successfully")
                    st.json(client_profile.dict() if hasattr(client_profile, 'dict') else str(client_profile))
                
                progress_bar.progress(20)
                
                # ============================================================
                # STEP 2: Market Research Analyst Agent
                # ============================================================
                status_text.text("Step 2/6: Conducting market research...")
                progress_bar.progress(30)
                
                with st.expander("🔍 Step 2: Market Research & Sector Analysis", expanded=False):
                    st.info("Analyzing market trends and sector performance...")
                    
                    print(f"\n{'='*70}")
                    print(f"STEP 2: MARKET RESEARCH ANALYST AGENT")
                    print(f"{'='*70}\n")
                    
                    market_research_prompt = f"""
                    Based on the following client profile, conduct comprehensive market research:
                    
                    {client_profile}
                    
                    Analyze the requested sectors and provide a detailed market research brief.
                    """
                    
                    market_research_result = await Runner.run(
                        financial_analyst, 
                        market_research_prompt,
                        max_turns=40
                    )
                    
                    market_research = market_research_result.final_output
                    
                    print(f"\n{'='*70}")
                    print(f"MARKET RESEARCH OUTPUT:")
                    print(market_research[:500] + "..." if len(str(market_research)) > 500 else market_research)
                    print(f"{'='*70}\n")
                    
                    st.success("✅ Market research completed")
                    st.markdown(market_research)
                
                progress_bar.progress(40)
                
                # ============================================================
                # STEP 3: Financial Data Analyst Agent
                # ============================================================
                status_text.text("Step 3/6: Analyzing stock candidates...")
                progress_bar.progress(50)
                
                with st.expander("📈 Step 3: Stock Candidate Analysis", expanded=False):
                    st.info("Vetting stock candidates with quantitative metrics...")
                    
                    print(f"\n{'='*70}")
                    print(f"STEP 3: FINANCIAL DATA ANALYST AGENT")
                    print(f"{'='*70}\n")
                    
                    stock_analysis_prompt = f"""
                    Client Profile:
                    {client_profile}
                    
                    Market Research Brief:
                    {market_research}
                    
                    Based on the market research, select 5-7 stock candidates and perform quantitative analysis.
                    """
                    
                    stock_analysis_result = await Runner.run(
                        chief_risk_officer_agent, 
                        stock_analysis_prompt,
                        max_turns=100  # Increased for multiple stock lookups
                    )
                    
                    stock_candidates = stock_analysis_result.final_output
                    
                    print(f"\n{'='*70}")
                    print(f"STOCK CANDIDATES OUTPUT:")
                    print(stock_candidates)
                    print(f"{'='*70}\n")
                    
                    st.success("✅ Stock candidate analysis completed")
                    
                    # Display as table if it's a list
                    if isinstance(stock_candidates, list):
                        import pandas as pd
                        df = pd.DataFrame([item.dict() if hasattr(item, 'dict') else item for item in stock_candidates])
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.markdown(stock_candidates)
                
                progress_bar.progress(60)
                
                # ============================================================
                # STEP 4: Risk Management Specialist Agent
                # ============================================================
                status_text.text("Step 4/6: Conducting risk assessment...")
                progress_bar.progress(70)
                
                with st.expander("⚠️ Step 4: Qualitative Risk Assessment", expanded=False):
                    st.info("Evaluating regulatory, legal, and geopolitical risks...")
                    
                    print(f"\n{'='*70}")
                    print(f"STEP 4: RISK MANAGEMENT SPECIALIST AGENT")
                    print(f"{'='*70}\n")
                    
                    risk_assessment_prompt = f"""
                    Client Profile:
                    {client_profile}
                    
                    Stock Candidates:
                    {stock_candidates}
                    
                    Perform comprehensive qualitative risk vetting on each stock candidate.
                    Use SEC filings and web search to identify litigation, regulatory, and geopolitical risks.
                    """
                    
                    risk_assessment_result = await Runner.run(
                        risk_management_specialist, 
                        risk_assessment_prompt,
                        max_turns=100  # Increased for SEC filing searches per stock
                    )
                    
                    risk_vetted_stocks = risk_assessment_result.final_output
                    
                    print(f"\n{'='*70}")
                    print(f"RISK ASSESSMENT OUTPUT:")
                    print(risk_vetted_stocks)
                    print(f"{'='*70}\n")
                    
                    st.success("✅ Risk assessment completed")
                    st.markdown(risk_vetted_stocks)
                
                progress_bar.progress(80)
                
                # ============================================================
                # STEP 5: Investment Strategist Agent
                # ============================================================
                status_text.text("Step 5/6: Building portfolio allocation...")
                progress_bar.progress(85)
                
                with st.expander("💼 Step 5: Portfolio Allocation Strategy", expanded=False):
                    st.info("Creating optimized portfolio allocation...")
                    
                    print(f"\n{'='*70}")
                    print(f"STEP 5: INVESTMENT STRATEGIST AGENT")
                    print(f"{'='*70}\n")
                    
                    portfolio_allocation_prompt = f"""
                    Client Profile:
                    {client_profile}
                    
                    Market Research:
                    {market_research}
                    
                    Risk-Vetted Stock Candidates:
                    {risk_vetted_stocks}
                    
                    Create a final portfolio allocation plan with exact percentages, investment amounts, 
                    and share calculations using current market prices.
                    """
                    
                    portfolio_result = await Runner.run(
                        portfolio_manager_agent, 
                        portfolio_allocation_prompt,
                        max_turns=60
                    )
                    
                    portfolio_allocation = portfolio_result.final_output
                    
                    print(f"\n{'='*70}")
                    print(f"PORTFOLIO ALLOCATION OUTPUT:")
                    print(portfolio_allocation)
                    print(f"{'='*70}\n")
                    
                    st.success("✅ Portfolio allocation completed")
                    st.markdown(portfolio_allocation)
                
                progress_bar.progress(90)
                
                # ============================================================
                # STEP 6: Final Report Generator Agent
                # ============================================================
                status_text.text("Step 6/6: Generating final investment report...")
                progress_bar.progress(95)
                
                with st.expander("📄 Step 6: Final Investment Report", expanded=True):
                    st.info("Compiling comprehensive investment recommendation report...")
                    
                    print(f"\n{'='*70}")
                    print(f"STEP 6: FINAL REPORT GENERATOR AGENT")
                    print(f"{'='*70}\n")
                    
                    final_report_prompt = f"""
                    Compile a professional, client-ready investment report using:
                    
                    Client Profile:
                    {client_profile}
                    
                    Market Research Brief:
                    {market_research}
                    
                    Risk Assessment:
                    {risk_vetted_stocks}
                    
                    Portfolio Allocation:
                    {portfolio_allocation}
                    
                    Generate a complete, polished report following all formatting requirements.
                    """
                    
                    final_report_result = await Runner.run(
                        final_report_agent, 
                        final_report_prompt,
                        max_turns=30
                    )
                    
                    final_report = final_report_result.final_output
                    
                    print(f"\n{'='*70}")
                    print(f"FINAL REPORT GENERATED")
                    print(f"{'='*70}\n")
                    
                    st.success("✅ Final report generated successfully")
                    st.markdown(final_report)
                
                progress_bar.progress(100)
                status_text.text("✅ Analysis Complete!")
                
                # ============================================================
                # Download Report Option
                # ============================================================
                
                
                print(f"\n{'='*70}")
                print(f"ANALYSIS PIPELINE COMPLETED SUCCESSFULLY")
                print(f"{'='*70}\n")
                
        except Exception as e:
            print(f"\n{'='*70}")
            print(f"ERROR OCCURRED: {str(e)}")
            print(f"{'='*70}\n")
            st.error(f"❌ An error occurred: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
    
    # Run the async pipeline
    asyncio.run(main())

elif start_button and not query:
    st.warning("⚠️ Please enter your investment goal before starting the analysis.")

# Sidebar information
with st.sidebar:
    st.header("ℹ️ How It Works")
    st.markdown("""
    ### Analysis Pipeline:
    
    1. **Client Profiler** - Extracts investment parameters
    2. **Market Research** - Analyzes sector trends
    3. **Stock Analysis** - Vets candidates quantitatively
    4. **Risk Assessment** - Evaluates qualitative risks
    5. **Portfolio Design** - Creates allocation strategy
    6. **Report Generation** - Compiles final recommendation
    
    ### Requirements:
    - Investment budget
    - Timeline (years)
    - Risk tolerance (1-10)
    - Sector preferences
    - Investment strategy
    """)
    
    st.markdown("---")
    st.markdown("**Powered by OpenAI Agents SDK**")