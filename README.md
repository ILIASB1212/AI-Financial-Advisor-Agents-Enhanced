📊 AI Investment Research Assistant

This project is a multi-agent pipeline built using the OpenAI Agents SDK and Streamlit to generate comprehensive, data-driven investment recommendations. It analyzes a client's profile, conducts market research, vets stocks quantitatively and qualitatively, determines a final portfolio allocation, and outputs a professional report—all automatically.

🚀 Key Features

6-Step Agent Pipeline: Automates financial analysis from client intake to final report.

Tool-Augmented Agents: Uses yfinance, Google Search, Alpha Vantage, and SEC Edgar Downloader for real-time data access.

Dockerized: Ready for easy deployment and reproducible environments.

Streamlit UI: Provides a clean interface for user input and report viewing.

🛠️ Prerequisites

To run this application, you need to have the following installed:

Python 3.10+

Docker and Docker Compose

API Keys for the following services (required for the agents to function):

OpenAI API Key (For Agent LLM calls)

Google Custom Search API Key and Custom Search Engine ID (CX)

Alpha Vantage API Key (For supplementary financial data)

📦 Local Setup (Docker)

The recommended way to run this application is using Docker, as it handles all Python dependencies and environment setup automatically.

1. Project Structure

Ensure your project directory looks like this (excluding .venv and .env):

.
├── Agents/
├── tools/
├── app.py
├── docker-compose.yml
├── Dockerfile
└── requirements.txt


2. Configure Environment Variables

Create a file named .env in the root directory (where docker-compose.yml is located) and populate it with your API keys.

# .env
OPENAI_API_KEY="sk-..."
GOOGLE_API_KEY="AIza..."
AV_API_KEY="YOUR_ALPHA_VANTAGE_API_KEY"


3. Build and Run the Container

Execute the following commands from your project root directory:

Build the Docker Image:

docker-compose build


Start the Application Container:

docker-compose up -d


The application will now be running in the background.

4. Access the Application

Open your web browser and navigate to:

http://localhost:8501


🛑 Stopping the Application

To stop the container and clean up the network:

docker-compose down
