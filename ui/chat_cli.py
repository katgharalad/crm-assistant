import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from llm_engine.intent_parser import IntentParser
from engine.query_engine import check_status, last_funding_event, last_contact

class ChatCLI:
    def __init__(self, companies_df, contacts_df, opportunities_df):
        """
        Initialize the CLI interface with data and intent parser.
        
        Args:
            companies_df (pd.DataFrame): Companies data
            contacts_df (pd.DataFrame): Contacts data
            opportunities_df (pd.DataFrame): Opportunities data
        """
        self.companies_df = companies_df
        self.contacts_df = contacts_df
        self.opportunities_df = opportunities_df
        self.parser = IntentParser()
    
    def format_status_response(self, result):
        """
        Format status check response for display.
        
        Args:
            result (dict): Status check result
            
        Returns:
            str: Formatted response
        """
        if "error" in result:
            return f"❌ {result['error']}"
        
        return f"""
📊 **Company Status Report**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏢 **Company**: {result['company_name']}
🏭 **Industry**: {result['industry']}
📍 **Location**: {result['location']}
📈 **Stage**: {result['stage']}
🎯 **Program**: {result['program']}
💰 **Total Funding**: ${result['total_funding']:,}
📅 **Last Contacted**: {result['last_contacted']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    def format_funding_response(self, result):
        """
        Format funding event response for display.
        
        Args:
            result (dict): Funding event result
            
        Returns:
            str: Formatted response
        """
        if "error" in result:
            return f"❌ {result['error']}"
        
        if "message" in result:
            return f"ℹ️  {result['company_name']}: {result['message']}"
        
        return f"""
💰 **Latest Funding Event**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏢 **Company**: {result['company_name']}
📊 **Funding Type**: {result['funding_type']}
💵 **Amount**: ${result['amount']:,}
📅 **Date Closed**: {result['date_closed']}
📈 **Total Closed Rounds**: {result['total_closed_rounds']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    def format_contact_response(self, result):
        """
        Format contact response for display.
        
        Args:
            result (dict): Contact result
            
        Returns:
            str: Formatted response
        """
        if "error" in result:
            return f"❌ {result['error']}"
        
        if "message" in result:
            return f"ℹ️  {result['company_name']}: {result['message']}"
        
        return f"""
👥 **Last Contact Information**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏢 **Company**: {result['company_name']}
📅 **Last Contact Date**: {result['last_contact_date']}
👤 **Contact Name**: {result['contact_name']}
🎯 **Contact Role**: {result['contact_role']}
📊 **Total Contacts**: {result['total_contacts']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    def process_query(self, user_input):
        """
        Process user query and return formatted response.
        
        Args:
            user_input (str): User's input text
            
        Returns:
            str: Formatted response
        """
        # Parse intent
        parsed = self.parser.parse_intent(user_input)
        
        if not parsed["intent"]:
            return f"""
🤔 **Intent Not Recognized**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
I couldn't understand what you're asking for. 
Confidence: {parsed['confidence']:.2f}

Try asking about:
• Company status: "What is the status of [Company Name]?"
• Funding events: "When did [Company Name] last raise funding?"
• Contact history: "When was [Company Name] last contacted?"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        if not parsed["company"]:
            return f"""
❓ **Company Name Missing**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
I understood you want to know about: {parsed['intent']}
But I couldn't identify which company you're asking about.

Please include the company name in your question.
Example: "What is the status of Bowman-Campbell?"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        # Route to appropriate query function
        if parsed["intent"] == "check_status":
            result = check_status(self.companies_df, parsed["company"])
            if "error" in result:
                # Show some sample companies to help the user
                sample_companies = self.companies_df['Name'].head(10).tolist()
                return f"{result['error']}\n\n📋 **Sample companies in database:**\n" + "\n".join([f"• {company}" for company in sample_companies])
            return self.format_status_response(result)
        
        elif parsed["intent"] == "last_funding":
            result = last_funding_event(self.opportunities_df, self.companies_df, parsed["company"])
            if "error" in result:
                # Show some sample companies to help the user
                sample_companies = self.companies_df['Name'].head(10).tolist()
                return f"{result['error']}\n\n📋 **Sample companies in database:**\n" + "\n".join([f"• {company}" for company in sample_companies])
            return self.format_funding_response(result)
        
        elif parsed["intent"] == "last_contact":
            result = last_contact(self.contacts_df, parsed["company"], self.companies_df)
            if "error" in result:
                # Show some sample companies to help the user
                sample_companies = self.companies_df['Name'].head(10).tolist()
                return f"{result['error']}\n\n📋 **Sample companies in database:**\n" + "\n".join([f"• {company}" for company in sample_companies])
            return self.format_contact_response(result)
        
        else:
            return f"❌ Unknown intent: {parsed['intent']}"
    
    def run(self):
        """
        Run the CLI interface loop.
        """
        print("""
🤖 **CRM Chat Assistant**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Welcome! I can help you query your CRM data using natural language.

Example questions:
• "What is the status of Bowman-Campbell?"
• "When did King and Sons last raise funding?"
• "When was Spears LLC last contacted?"

Type 'quit' or 'exit' to leave.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
        
        while True:
            try:
                user_input = input("\n💬 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye! Thanks for using the CRM Chat Assistant.")
                    break
                
                if not user_input:
                    continue
                
                # Process the query
                response = self.process_query(user_input)
                print(f"\n{response}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Thanks for using the CRM Chat Assistant.")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                print("Please try again with a different question.") 