#!/usr/bin/env python3
"""
CRM Chat Assistant - Main Entry Point

This script loads CRM data from CSV files and starts an interactive
CLI interface for querying the data using natural language.
"""

import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(__file__))

from engine.data_loader import load_data
from ui.chat_cli import ChatCLI

def main():
    """
    Main function that loads data and starts the CLI interface.
    """
    print("🚀 Starting CRM Chat Assistant...")
    print("📊 Loading data from CSV files...")
    
    try:
        # Load the data
        companies_df, contacts_df, opportunities_df = load_data()
        
        print(f"✅ Loaded {len(companies_df)} companies")
        print(f"✅ Loaded {len(contacts_df)} contacts")
        print(f"✅ Loaded {len(opportunities_df)} opportunities")
        print("🎯 Initializing intent parser...")
        
        # Create and run the CLI interface
        cli = ChatCLI(companies_df, contacts_df, opportunities_df)
        cli.run()
        
    except FileNotFoundError as e:
        print(f"❌ Error: Could not find data files. Make sure the CSV files are in the 'data' directory.")
        print(f"   Details: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please check that all required dependencies are installed:")
        print("   pip install -r requirements.txt")
        sys.exit(1)

if __name__ == "__main__":
    main() 