import streamlit as st

# Set page configuration with a modern theme (must be the first Streamlit command)
st.set_page_config(
    page_title="AI Expense Tracker",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

import json
import os
import google.generativeai as genai
from dotenv import load_dotenv
import datetime

# Custom CSS for modern, responsive design
st.markdown("""
    <style>
    /* Main container */
    .main {
        max-width: 500px;
        margin: 0 auto;
        padding: 0.25rem;
    }
    
    /* Card styling */
    .card {
        background: white;
        border-radius: 8px;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
        padding: 0.75rem;
        margin-bottom: 0.75rem;
    }
    
    /* Input form */
    .stTextInput>div>div>input {
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 16px !important;
    }
    
    /* Buttons */
    .stButton>button {
        border-radius: 6px !important;
        padding: 0.3rem 0.8rem !important;
        font-weight: 500 !important;
        width: 100%;
        font-size: 0.85rem !important;
        margin: 0.2rem 0 !important;
    }
    
    /* Expense items */
    .expense-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.4rem 0;
        border-bottom: 1px solid #f5f5f5;
        margin: 0.2rem 0;
    }
    
    .expense-item:last-child {
        border-bottom: none;
    }
    
    .expense-amount {
        font-weight: 600;
        color: #2e7d32;
        font-size: 0.95rem;
    }
    
    .expense-category {
        font-size: 0.8rem;
        color: #666;
        background: #f5f5f5;
        padding: 0.2rem 0.5rem;
        border-radius: 12px;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main {
            padding: 0.15rem;
            max-width: 100%;
        }
        .card {
            padding: 0.6rem;
            margin: 0.4rem;
            border-radius: 6px;
        }
        h1 {
            font-size: 1.4rem !important;
            margin: 0.3rem 0 !important;
        }
        h3 {
            font-size: 1rem !important;
            margin: 0.2rem 0 !important;
        }
        .expense-item {
            padding: 0.3rem 0;
        }
    }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.3s ease-out forwards;
    }
    </style>
""", unsafe_allow_html=True)

# Load environment variables from .env file
load_dotenv()

def get_expense_details_from_ai(user_text):
    """
    Sends user input to the Gemini API to extract expense details.
    """
    try:
        # Configure the Google API key
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            st.error("Google API key not found. Please check your .env file.")
            return None
            
        genai.configure(api_key=google_api_key)

        # The prompt for the model
        prompt = f"""
        Extract the expense details from the following sentence.
        Return the output as a clean JSON object with the keys: 
        - "description" (string): A brief description of the expense
        - "amount" (float): The amount spent
        - "category" (string): One of these categories: 
          Food & Dining (restaurants, groceries, coffee), 
          Shopping (clothing, electronics, personal items),
          Transportation (fuel, public transport, taxis),
          Housing (rent, mortgage, maintenance),
          Bills & Utilities (electricity, water, internet, phone),
          Health & Wellness (doctor, medicine, gym, personal care),
          Entertainment (movies, games, subscriptions),
          Education (tuition, books, courses),
          Travel (flights, hotels, vacations),
          Other (anything that doesn't fit above categories)

        If any information is missing, make a reasonable assumption.
        Only return the JSON object, nothing else.

        Sentence: "{user_text}"
        """

        # Initialize the model and get the response
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        
        # Clean the response to get just the JSON part
        response_text = response.text.strip()
        if response_text.startswith('```json'):
            response_text = response_text[7:-3].strip()
        
        # Parse the JSON response
        expense_data = json.loads(response_text)
        return expense_data

    except json.JSONDecodeError as e:
        st.error(f"Failed to parse AI response: {e}")
        st.error(f"Raw response: {response.text if 'response' in locals() else 'No response'}")
        return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def format_currency(amount):
    """Format amount as Indian Rupees"""
    return f"₹{float(amount):,.2f}"

def get_category_color(category):
    """Get color for category badge"""
    colors = {
        'Food & Dining': '#4CAF50',      # Green
        'Shopping': '#9C27B0',           # Purple
        'Transportation': '#2196F3',     # Blue
        'Housing': '#FF9800',            # Orange
        'Bills & Utilities': '#00BCD4',  # Cyan
        'Health & Wellness': '#F44336',  # Red
        'Entertainment': '#E91E63',      # Pink
        'Education': '#3F51B5',          # Indigo
        'Travel': '#009688',             # Teal
        'Other': '#9E9E9E'               # Grey
    }
    return colors.get(category, '#9E9E9E')  # Default grey

def main():
    # Main container
    st.markdown('<div class="main">', unsafe_allow_html=True)
    
    # Header - Simplified and compact
    st.markdown("""
    <div style='text-align: center; margin: 0.5rem 0;'>
        <h1 style='margin: 0.2rem 0; font-size: 1.6rem;'>💸 Expense Tracker</h1>
        <p style='color: #666; margin: 0.1rem 0 0.8rem 0; font-size: 0.9rem;'>Track your spending with AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state for expenses if it doesn't exist
    if 'expenses' not in st.session_state:
        st.session_state.expenses = []
    
    # Current balance card
    total_spent = sum(expense.get('amount', 0) for expense in st.session_state.expenses)
    
    # Main card for expense input
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Add New Expense")
        
        with st.form("expense_form"):
            col1, col2 = st.columns([3, 1])
            with col1:
                user_input = st.text_input(
                    "Describe your expense",
                    placeholder="e.g., Spent $25 on dinner at Italian restaurant",
                    label_visibility="collapsed"
                )
            with col2:
                st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
                submit_button = st.form_submit_button("Add", use_container_width=True)
        
        if submit_button and user_input:
            with st.spinner(""):
                expense_data = get_expense_details_from_ai(user_input)
                
                if expense_data:
                    # Add timestamp and update the session state
                    expense_data['date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    expense_data['id'] = len(st.session_state.expenses) + 1
                    st.session_state.expenses.insert(0, expense_data)
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)  # Close card
    
    # Expenses list
    if st.session_state.expenses:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            
            # Summary row
            total = sum(expense.get('amount', 0) for expense in st.session_state.expenses)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"### ₹{total:,.0f}")
                st.caption("Total spent")
            with col2:
                st.markdown(f"### {len(st.session_state.expenses)}")
                st.caption("Transactions")
            
            st.markdown("---")
            
            # Expenses list
            for expense in st.session_state.expenses:
                col1, col2 = st.columns([4, 2])
                with col1:
                    st.markdown(f"**{expense['description']}**")
                    st.markdown(f"<div style='color: #666; font-size: 0.9rem;'>{expense['date']}</div>", unsafe_allow_html=True)
                with col2:
                    amount = float(expense.get('amount', 0))
                    category = expense.get('category', 'Other')
                    st.markdown(f"""
                    <div style='text-align: right; line-height: 1.3;'>
                        <div style='font-size: 0.95rem; font-weight: 600; color: #2e7d32;'>₹{amount:,.0f}</div>
                        <div style='background-color: {get_category_color(category)}15; color: {get_category_color(category)}; 
                                    padding: 1px 5px; border-radius: 4px; font-size: 0.7rem; display: inline-block;'>{category}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
            
            # Clear all button
            if st.button("Clear All Expenses", use_container_width=True, type="secondary"):
                st.session_state.expenses = []
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)  # Close card
    else:
        with st.container():
            st.markdown('<div class="card" style="text-align: center; padding: 3rem 1rem;">', unsafe_allow_html=True)
            st.markdown("### No expenses yet")
            st.markdown("<div style='color: #666; margin: 0.5rem 0; font-size: 0.9rem;'>Add your first expense to get started</div>", unsafe_allow_html=True)
            st.markdown("<div style='font-size: 0.85rem; color: #666;'>💡 Try: \"₹200 lunch at McDonald's\" or \"₹450 on groceries\"</div>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close main container

if __name__ == "__main__":
    main()
