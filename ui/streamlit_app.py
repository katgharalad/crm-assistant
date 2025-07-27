#!/usr/bin/env python3
"""
CRM Chat Assistant - Streamlit Web App

This Streamlit app provides a web interface for the CRM Chat Assistant,
allowing users to query CRM data using natural language through an
interactive web UI.
"""

import streamlit as st
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from engine.data_loader import load_data
from llm_engine.intent_parser import IntentParser
from engine.query_engine import check_status, last_funding_event, last_contact, get_best_company_match

# Page configuration
st.set_page_config(
    page_title="CRM Chat Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def load_crm_data():
    """
    Load CRM data and initialize the intent parser.
    Cached to avoid reloading on every interaction.
    """
    try:
        # Load data
        companies_df, contacts_df, opportunities_df = load_data()
        
        # Initialize intent parser
        parser = IntentParser()
        
        return companies_df, contacts_df, opportunities_df, parser
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None, None, None

def format_status_response(result):
    """
    Format status check response for Streamlit display.
    
    Args:
        result (dict): Status check result
        
    Returns:
        str: Formatted markdown response
    """
    if "error" in result:
        return f"❌ **Error:** {result['error']}"
    
    return f"""
### 📊 Company Status Report

| **Field** | **Value** |
|-----------|-----------|
| **Company** | {result['company_name']} |
| **Industry** | {result['industry']} |
| **Location** | {result['location']} |
| **Stage** | {result['stage']} |
| **Program** | {result['program']} |
| **Total Funding** | ${result['total_funding']:,} |
| **Last Contacted** | {result['last_contacted']} |
"""

def format_funding_response(result):
    """
    Format funding event response for Streamlit display.
    
    Args:
        result (dict): Funding event result
        
    Returns:
        str: Formatted markdown response
    """
    if "error" in result:
        return f"❌ **Error:** {result['error']}"
    
    if "message" in result:
        return f"ℹ️ **{result['company_name']}:** {result['message']}"
    
    return f"""
### 💰 Latest Funding Event

| **Field** | **Value** |
|-----------|-----------|
| **Company** | {result['company_name']} |
| **Funding Type** | {result['funding_type']} |
| **Amount** | ${result['amount']:,} |
| **Date Closed** | {result['date_closed']} |
| **Total Closed Rounds** | {result['total_closed_rounds']} |
"""

def format_contact_response(result):
    """
    Format contact response for Streamlit display.
    
    Args:
        result (dict): Contact result
        
    Returns:
        str: Formatted markdown response
    """
    if "error" in result:
        return f"❌ **Error:** {result['error']}"
    
    if "message" in result:
        return f"ℹ️ **{result['company_name']}:** {result['message']}"
    
    return f"""
### 👥 Last Contact Information

| **Field** | **Value** |
|-----------|-----------|
| **Company** | {result['company_name']} |
| **Last Contact Date** | {result['last_contact_date']} |
| **Contact Name** | {result['contact_name']} |
| **Contact Role** | {result['contact_role']} |
| **Total Contacts** | {result['total_contacts']} |
"""

def process_query(user_input, companies_df, contacts_df, opportunities_df, parser):
    """
    Process user query and return formatted response.
    
    Args:
        user_input (str): User's input text
        companies_df (pd.DataFrame): Companies data
        contacts_df (pd.DataFrame): Contacts data
        opportunities_df (pd.DataFrame): Opportunities data
        parser (IntentParser): Intent parser instance
        
    Returns:
        tuple: (response_text, response_type)
    """
    # Parse intent
    parsed = parser.parse_intent(user_input)
    
    if not parsed["intent"]:
        return f"""
### 🤔 Intent Not Recognized

I couldn't understand what you're asking for.  
**Confidence:** {parsed['confidence']:.2f}

**Try asking about:**
• Company status: *"What is the status of [Company Name]?"*
• Funding events: *"When did [Company Name] last raise funding?"*
• Contact history: *"When was [Company Name] last contacted?"*
""", "warning"
    
    if not parsed["company"]:
        return f"""
### ❓ Company Name Missing

I understood you want to know about: **{parsed['intent']}**  
But I couldn't identify which company you're asking about.

**Please include the company name in your question.**  
**Example:** *"What is the status of Bowman-Campbell?"*
""", "warning"
    
    # Route to appropriate query function
    if parsed["intent"] == "check_status":
        result = check_status(companies_df, parsed["company"])
        if "error" in result:
            # Show some sample companies to help the user
            sample_companies = companies_df['Name'].head(10).tolist()
            return f"{result['error']}\n\n**📋 Sample companies in database:**\n" + "\n".join([f"• {company}" for company in sample_companies]), "error"
        return format_status_response(result), "success"
    
    elif parsed["intent"] == "last_funding":
        result = last_funding_event(opportunities_df, companies_df, parsed["company"])
        if "error" in result:
            # Show some sample companies to help the user
            sample_companies = companies_df['Name'].head(10).tolist()
            return f"{result['error']}\n\n**📋 Sample companies in database:**\n" + "\n".join([f"• {company}" for company in sample_companies]), "error"
        return format_funding_response(result), "success"
    
    elif parsed["intent"] == "last_contact":
        result = last_contact(contacts_df, parsed["company"], companies_df)
        if "error" in result:
            # Show some sample companies to help the user
            sample_companies = companies_df['Name'].head(10).tolist()
            return f"{result['error']}\n\n**📋 Sample companies in database:**\n" + "\n".join([f"• {company}" for company in sample_companies]), "error"
        return format_contact_response(result), "success"
    
    else:
        return f"❌ **Unknown intent:** {parsed['intent']}", "error"

def main():
    """
    Main Streamlit app function.
    """
    # Header
    st.title("🤖 CRM Chat Assistant")
    st.markdown("**Ask about startup status, funding rounds, last contact, and more using natural language**")
    
    # Load data and parser
    with st.spinner("Loading CRM data and initializing models..."):
        companies_df, contacts_df, opportunities_df, parser = load_crm_data()
    
    if companies_df is None:
        st.error("Failed to load CRM data. Please check your data files.")
        return
    
    # Display data summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Companies", len(companies_df))
    with col2:
        st.metric("Contacts", len(contacts_df))
    with col3:
        st.metric("Opportunities", len(opportunities_df))
    
    st.divider()
    
    # Query input section
    st.subheader("💬 Ask a Question")
    
    # Example queries
    with st.expander("📋 Example Questions"):
        st.markdown("""
        **Company Status:**
        - "What is the status of Bowman-Campbell?"
        - "Show me the status of King and Sons"
        - "What's going on with Spears LLC?"
        
        **Funding Events:**
        - "When did Bowman-Campbell last raise funding?"
        - "What was King and Sons' last funding round?"
        - "Show me Spears LLC's funding history"
        
        **Contact History:**
        - "When was Bowman-Campbell last contacted?"
        - "When did we last meet with King and Sons?"
        - "Show me contact history for Spears LLC"
        """)
    
    # Text input
    user_query = st.text_input(
        "Enter your question:",
        placeholder="e.g., What is the status of Bowman-Campbell?",
        key="user_query"
    )
    
    # Process query when submitted
    if user_query:
        with st.spinner("Processing your question..."):
            response_text, response_type = process_query(
                user_query, companies_df, contacts_df, opportunities_df, parser
            )
        
        # Display response based on type
        if response_type == "success":
            st.success("✅ Query processed successfully!")
            st.markdown(response_text)
        elif response_type == "warning":
            st.warning("⚠️ Query processed with issues")
            st.markdown(response_text)
        elif response_type == "error":
            st.error("❌ Error processing query")
            st.markdown(response_text)
    
    # Sidebar with additional information
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        This CRM Chat Assistant uses:
        - **Natural Language Processing** with sentence transformers
        - **Fuzzy Company Matching** for flexible name recognition
        - **Semantic Intent Recognition** to understand your questions
        
        The system can answer questions about:
        - Company status and stage
        - Funding rounds and amounts
        - Contact history and meetings
        """)
        
        st.header("🔧 Technical Details")
        st.markdown(f"""
        - **Companies loaded:** {len(companies_df)}
        - **Contacts loaded:** {len(contacts_df)}
        - **Opportunities loaded:** {len(opportunities_df)}
        - **Intent templates:** {len(parser.templates)}
        """)
        
        # Show sample companies
        st.header("📋 Sample Companies")
        sample_companies = companies_df['Name'].head(15).tolist()
        for company in sample_companies:
            st.text(f"• {company}")

if __name__ == "__main__":
    main() 