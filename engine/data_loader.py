import pandas as pd
import os

def load_data():
    """
    Load the three CSV files into pandas DataFrames.
    
    Returns:
        tuple: (companies_df, contacts_df, opportunities_df)
    """
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    
    # Load companies data
    companies_path = os.path.join(data_dir, 'companies_1000.csv')
    companies_df = pd.read_csv(companies_path)
    
    # Load contacts data
    contacts_path = os.path.join(data_dir, 'contacts_1000.csv')
    contacts_df = pd.read_csv(contacts_path)
    
    # Load opportunities data
    opportunities_path = os.path.join(data_dir, 'opportunities_1000.csv')
    opportunities_df = pd.read_csv(opportunities_path)
    
    return companies_df, contacts_df, opportunities_df 