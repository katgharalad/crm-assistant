   CRM Chat Assistant 

A local CRM Chat Assistant that mimics querying a Salesforce CRM system using natural language. The assistant loads mock CSV data (companies, contacts, opportunities) and allows you to ask questions about company status, funding events, and contact history using conversational language.

 Project Goal

This system demonstrates how to build a natural language interface for CRM data without requiring direct Salesforce API integration. It's designed to be modular, allowing you to easily swap the CSV backend with live API calls in the future.

 Quick Start

 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

 Installation

1. Clone or download the project 
   ```bash
   cd crmautomation
   ```

2. Install dependencies 
   ```bash
   pip install -r requirements.txt
   ```

3. Run the assistant 

   CLI Version: 
   ```bash
   python main.py
   ```

   Web App Version: 
   ```bash
   streamlit run ui/streamlit_app.py
   ```

The CLI version will load the CSV data and start an interactive CLI session. The web app version provides a beautiful web interface accessible through your browser.

 Data Structure

The system works with three CSV files in the `data/` directory:

- `companies_1000.csv` : Company information including name, industry, stage, program, funding, etc.
-  `contacts_1000.csv` : Contact information including name, role, company association, and last meeting dates
-  `opportunities_1000.csv` : Funding opportunities including stage, type, amount, and closure dates

      Example Questions

Here are some example questions you can ask the assistant:

       Company Status Queries
- "What is the status of BioGenix Labs?"
- "Show me the status of TechFlow AI"
- "What's the current status of AgriFlow AI?"
- "How is GreenNode Energy doing?"
- "What stage is Quantum Robotics in?"

       Funding Event Queries
- "When did BioGenix Labs last raise funding?"
- "What was TechFlow AI's last funding round?"
- "When was AgriFlow AI's most recent funding?"
- "Show me GreenNode Energy's last funding event"
- "What's the latest funding for Quantum Robotics?"

       Contact History Queries
- "When was BioGenix Labs last contacted?"
- "When did we last meet with TechFlow AI?"
- "What's the last contact date for AgriFlow AI?"
- "When was the last meeting with GreenNode Energy?"
- "When did we last talk to Quantum Robotics?"

     Architecture

The system is built with a modular architecture:

```
crmautomation/
├── data/                       CSV data files
├── engine/                     Data processing and query logic
│   ├── data_loader.py         Loads CSV files into DataFrames
│   └── query_engine.py        Query functions for different intents
├── llm_engine/                Natural language processing
│   ├── intent_parser.py       Uses sentence-transformers for intent matching
│   └── template_mapper.py     Defines intent templates
├── ui/                        User interface
│   ├── chat_cli.py            CLI interface
│   └── streamlit_app.py       Web interface
├── main.py                    Main entry point
├── requirements.txt           Python dependencies
└── README.md                 This file
```

      Key Features

       1. Natural Language Processing
- Uses `sentence-transformers` with the `all-MiniLM-L6-v2` model
- Semantic similarity matching for intent recognition
- Pattern-based company name extraction

       2. Modular Query System
- `check_status()`: Returns company stage, program, and last contacted date
- `last_funding_event()`: Returns most recent closed funding round
- `last_contact()`: Returns date of last meeting with any contact

       3. Extensible Design
- Easy to add new intent templates
- Modular architecture for future API integration
- Clean separation of concerns

      Intent Templates

The system recognizes three main types of intents:

1.  `check_status` : Queries about company current status
2.  `last_funding` : Queries about funding events
3.  `last_contact` : Queries about contact history

Each intent has multiple template variations to improve recognition accuracy.

      Future Enhancements

This system is designed to be easily extensible:

-  Streamlit UI : Web interface using Streamlit (implemented!)
-  Salesforce API : Replace CSV backend with live Salesforce REST API
-  Additional Intents : Add more query types (e.g., pipeline analysis, forecasting)
-  Advanced NLP : Integrate with more sophisticated language models
-  Data Visualization : Add charts and graphs for data insights

      Development

       Adding New Intents

1. Add new templates to `llm_engine/template_mapper.py`
2. Create corresponding query function in `engine/query_engine.py`
3. Add routing logic in `ui/chat_cli.py`

      Testing

The system includes error handling for:
- Missing company names
- Unrecognized intents
- Data not found scenarios
- Invalid input formats

      License

This project is for educational and demonstration purposes.

     Contributing

Feel free to extend this system with additional features or improvements!

---

 Happy CRM Querying! 
