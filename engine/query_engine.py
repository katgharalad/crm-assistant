import pandas as pd
from datetime import datetime
from rapidfuzz import process

def get_best_company_match(company_name, companies_df):
    """
    Get the best company match using fuzzy matching.
    
    Args:
        company_name (str): Company name to search for
        companies_df (pd.DataFrame): Companies dataframe
        
    Returns:
        str: Best matching company name or None
    """
    choices = companies_df['Name'].tolist()
    match, score, _ = process.extractOne(company_name, choices)
    return match if score > 70 else None

def check_status(companies_df, company_name):
    """
    Check the status of a company.
    
    Args:
        companies_df (pd.DataFrame): Companies dataframe
        company_name (str): Name of the company to check
        
    Returns:
        dict: Dictionary containing stage, program, and last_contacted information
    """
    # Use fuzzy matching to find the best company match
    best_match = get_best_company_match(company_name, companies_df)
    
    if best_match is None:
        return {
            "error": f"Company '{company_name}' not found in the database. Try searching for a company from the list."
        }
    
    # Get the company data
    company = companies_df[companies_df['Name'] == best_match].iloc[0]
    
    return {
        "company_name": company['Name'],
        "stage": company['Stage'],
        "program": company['Program'],
        "last_contacted": company['Last_Contacted'],
        "industry": company['Industry'],
        "total_funding": company['Total_Funding'],
        "location": company['Location']
    }

def last_funding_event(opps_df, companies_df, company_name):
    """
    Find the most recent closed funding round for a company.
    
    Args:
        opps_df (pd.DataFrame): Opportunities dataframe
        companies_df (pd.DataFrame): Companies dataframe
        company_name (str): Name of the company to check
        
    Returns:
        dict: Dictionary containing funding event information
    """
    # Use fuzzy matching to find the best company match
    best_match = get_best_company_match(company_name, companies_df)
    
    if best_match is None:
        return {
            "error": f"Company '{company_name}' not found in the database. Try searching for a company from the list."
        }
    
    company = companies_df[companies_df['Name'] == best_match].iloc[0]
    company_id = company['Company_ID']
    
    # Find closed won opportunities for this company
    company_opps = opps_df[
        (opps_df['Company_ID'] == company_id) & 
        (opps_df['Stage'] == 'Closed Won')
    ]
    
    if company_opps.empty:
        return {
            "company_name": company['Name'],
            "message": "No closed funding rounds found for this company."
        }
    
    # Sort by date and get the most recent
    company_opps['Date_Closed'] = pd.to_datetime(company_opps['Date_Closed'])
    latest_funding = company_opps.sort_values('Date_Closed', ascending=False).iloc[0]
    
    return {
        "company_name": company['Name'],
        "funding_type": latest_funding['Type'],
        "amount": latest_funding['Amount'],
        "date_closed": latest_funding['Date_Closed'].strftime('%Y-%m-%d'),
        "total_closed_rounds": len(company_opps)
    }

def last_contact(contacts_df, company_name, companies_df):
    """
    Find the date of last meeting with any contact from the company.
    
    Args:
        contacts_df (pd.DataFrame): Contacts dataframe
        company_name (str): Name of the company to check
        companies_df (pd.DataFrame): Companies dataframe
        
    Returns:
        dict: Dictionary containing last contact information
    """
    # Use fuzzy matching to find the best company match
    best_match = get_best_company_match(company_name, companies_df)
    
    if best_match is None:
        return {
            "error": f"Company '{company_name}' not found in the database. Try searching for a company from the list."
        }
    
    company = companies_df[companies_df['Name'] == best_match].iloc[0]
    company_id = company['Company_ID']
    
    # Find contacts for this company
    company_contacts = contacts_df[contacts_df['Company_ID'] == company_id]
    
    if company_contacts.empty:
        return {
            "company_name": company['Name'],
            "message": "No contacts found for this company."
        }
    
    # Convert dates and find the most recent meeting
    company_contacts['Last_Meeting'] = pd.to_datetime(company_contacts['Last_Meeting'])
    latest_contact = company_contacts.sort_values('Last_Meeting', ascending=False).iloc[0]
    
    return {
        "company_name": company['Name'],
        "last_contact_date": latest_contact['Last_Meeting'].strftime('%Y-%m-%d'),
        "contact_name": latest_contact['Name'],
        "contact_role": latest_contact['Role'],
        "total_contacts": len(company_contacts)
    } 