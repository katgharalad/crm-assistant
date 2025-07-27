# Intent templates for the CRM Chat Assistant
TEMPLATES = {
    "check_status": [
        "What is the status of [company]?",
        "Show me the status of [company]",
        "What's the current status of [company]?",
        "Tell me about [company] status",
        "How is [company] doing?",
        "What stage is [company] in?",
        "What program is [company] in?",
        "Show me status of [company]",
        "What is [company] status?",
        "Status of [company]",
        "How is [company] doing?",
        "What's [company] status?",
        "Tell me about [company]",
        "Show me [company] information",
        "What's going on with [company]?",
        "Current status of [company]?",
        "Tell me the status of [company]",
        "What's happening with [company]?",
        "Give me [company] status",
        "Show [company] status",
        "What's the deal with [company]?",
        "How's [company] doing?",
        "What's up with [company]?",
        "Tell me about [company]'s status",
        "What's [company]'s current status?",
        "Status update for [company]",
        "What's the latest on [company]?",
        "How is [company] performing?",
        "What's [company]'s situation?",
        "Give me an update on [company]"
    ],
    "last_funding": [
        "When did [company] last raise funding?",
        "What was [company]'s last funding round?",
        "When was [company]'s most recent funding?",
        "Show me [company]'s last funding event",
        "What's the latest funding for [company]?",
        "When did [company] last get funding?",
        "Tell me about [company]'s funding history",
        "When did [company] last raise money?",
        "What's [company]'s latest funding?",
        "Show me [company] funding",
        "When was [company]'s last funding?",
        "Funding for [company]",
        "Last funding round for [company]",
        "When did [company] last get investment?",
        "What's [company]'s most recent funding?",
        "Show me [company]'s funding rounds",
        "When was [company]'s latest funding?",
        "Tell me about [company]'s funding",
        "What funding did [company] get?",
        "When did [company] raise money last?",
        "Show [company] funding history",
        "What's the latest funding round for [company]?",
        "When was [company]'s most recent investment?",
        "Tell me about [company]'s investments",
        "What's [company]'s funding status?",
        "Show me [company]'s investment history",
        "When did [company] last receive funding?",
        "What's [company]'s funding timeline?",
        "Tell me about [company]'s capital raises"
    ],
    "last_contact": [
        "When was [company] last contacted?",
        "When did we last meet with [company]?",
        "What's the last contact date for [company]?",
        "When was the last meeting with [company]?",
        "Show me last contact with [company]",
        "When did we last talk to [company]?",
        "What's the most recent contact with [company]?",
        "When was [company] last contacted?",
        "Last contact with [company]",
        "When did we last contact [company]?",
        "Show me contact history for [company]",
        "Last meeting with [company]",
        "Contact date for [company]",
        "When did we last speak with [company]?",
        "What's the latest contact with [company]?",
        "Show me [company] contact history",
        "When was our last interaction with [company]?",
        "Tell me about [company] contact",
        "What's the last communication with [company]?",
        "When did we last reach out to [company]?",
        "Show me [company] interactions",
        "What's the most recent meeting with [company]?",
        "When was [company] last reached out to?",
        "Tell me about [company] communications",
        "What's the latest interaction with [company]?",
        "Show me [company] communication history",
        "When did we last connect with [company]?",
        "What's [company]'s contact timeline?",
        "Tell me about [company]'s recent contacts",
        "When was [company] last touched base with?"
    ]
}

def get_all_templates():
    """
    Get all intent templates flattened into a list.
    
    Returns:
        list: List of all template strings
    """
    all_templates = []
    for intent, templates in TEMPLATES.items():
        all_templates.extend(templates)
    return all_templates

def get_intent_for_template(template):
    """
    Get the intent for a given template.
    
    Args:
        template (str): Template string
        
    Returns:
        str: Intent name
    """
    for intent, templates in TEMPLATES.items():
        if template in templates:
            return intent
    return None 