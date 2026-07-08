# Accessible Trip Planner Agent

An intelligent AI-powered travel planning assistant designed specifically for wheelchair users and people with accessibility needs. The app uses Google's Gemini AI with real-time web search to provide detailed, accessible itineraries.



## Features

- **AI-Powered Planning**: Uses Google Gemini 2.5 Flash for intelligent trip planning
- **Real-Time Web Search**: Searches for wheelchair accessibility info, accessible entrances, ramps, and restroom facilities
- **Interactive UI**: Built with Gradio for an intuitive user experience
- **Agentic Loop**: Multi-step reasoning process to gather comprehensive accessibility information
- **Detailed Itineraries**: Generates encouraging and detailed travel plans with accessibility considerations

## Tech Stack

- **Google Generative AI** (Gemini API)
- **Gradio** - Interactive web UI
- **DuckDuckGo Search** - Privacy-focused web search
- **Python 3.8+**

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd accessibility_trip_planner
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your Google Gemini API key:
   ```
   Gemini_Api_Key=your_api_key_here
   ```

## 🔒 Security Note

**IMPORTANT**: Never commit your `.env` file or API keys to GitHub. The `.gitignore` file is configured to prevent this, but always verify sensitive information is not exposed before pushing to any repository.

## Usage

Run the application:
```bash
python agent.py
```

The Gradio interface will launch in your browser (typically at `http://localhost:7860`)

1. Enter your travel destination and goals
2. Click "Generate Accessible Itinerary"
3. The AI agent will search for accessibility information and create a detailed plan
4. View the itinerary and agent reasoning logs

### Example Input
```
Plan a half-day trip to downtown Chicago. I want to visit Millennium Park and the Art Institute. I need wheelchair-accessible entrances and accessible restrooms.
```

## How It Works

1. **User Input**: Accepts travel goals from the user
2. **Agent Loop**: Runs up to 5 steps of reasoning:
   - Analyzes the travel request
   - Calls web search tool to find accessibility information
   - Gathers real-world data about locations
   - Combines information into a comprehensive itinerary
3. **Output**: Generates detailed, encouraging travel plans with accessibility details

## Project Structure

```
accessibility_trip_planner/
├── agent.py              # Main application
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not committed)
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Configuration

### Max Steps
The agent runs a maximum of 5 steps to find enough information. Adjust in `agent.py`:
```python
max_steps = 5  # Line 65
```

### Temperature
Controls AI creativity (0-1). Currently set to 0.2 for focused, factual responses:
```python
temperature=0.2  # Line 60
```

## Dependencies Explained

- **google-genai**: Google's Gemini API client
- **gradio**: Web UI framework for ML applications
- **python-dotenv**: Load environment variables from .env files
- **duckduckgo-search**: Privacy-focused web search
- **requests**: HTTP library for API calls

## Troubleshooting

### "API key not found" error
- Ensure `.env` file exists in the project root
- Verify `Gemini_Api_Key` is set correctly
- Check that `.env` is NOT listed in `.gitignore` (it should be)

### Web search not working
- Check internet connection
- Verify DuckDuckGo search is accessible in your region
- Check API rate limits

