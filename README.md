# AI-Powered Expense Tracker

A smart expense tracking application that uses Google's Gemini AI to automatically categorize expenses from natural language input.

## Features

- Natural language expense entry (e.g., "Spent $15 on lunch at McDonald's")
- Automatic expense categorization
- Simple and intuitive interface
- Built with Streamlit for easy deployment

## Prerequisites

- Python 3.8 or higher
- Google API key with access to the Gemini API

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/expense-tracker-ai.git
   cd expense-tracker-ai
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   # source venv/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file:
   - Copy `.env.example` to `.env`
   - Add your Google API key:
     ```
     GOOGLE_API_KEY="your-google-api-key-here"
     ```

## Running the Application

1. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to `http://localhost:8501`

## Deployment to Hugging Face Spaces

1. Push your code to a GitHub repository
2. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
3. Click "Create new Space"
4. Select "Streamlit" as the SDK
5. Connect your GitHub repository
6. Add your `GOOGLE_API_KEY` as a secret in the Space settings
7. Deploy!

## How to Use

1. Enter your expense in natural language (e.g., "Spent $25 on dinner at Italian restaurant")
2. Click "Add Expense"
3. The AI will automatically categorize your expense
4. View your expense history below the input form
5. Use "Clear All Expenses" to start over

## License

MIT
