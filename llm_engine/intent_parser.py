import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from .template_mapper import get_all_templates, get_intent_for_template

class IntentParser:
    def __init__(self):
        """
        Initialize the intent parser with sentence transformer model.
        """
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.templates = get_all_templates()
        self.template_embeddings = None
        self._compute_template_embeddings()
    
    def _compute_template_embeddings(self):
        """
        Pre-compute embeddings for all templates.
        """
        print(f"Loading {len(self.templates)} templates...")
        print(f"First few templates: {self.templates[:5]}")
        self.template_embeddings = self.model.encode(self.templates)
    
    def extract_company_name(self, user_input):
        """
        Extract company name from user input using simple pattern matching.
        
        Args:
            user_input (str): User's input text
            
        Returns:
            str: Extracted company name or None
        """
        # Common patterns for company names
        patterns = [
            r'of\s+([A-Z][a-zA-Z\s&\-\'\.]+?)(?:\?|$|\s|,)',
            r'with\s+([A-Z][a-zA-Z\s&\-\'\.]+?)(?:\?|$|\s|,)',
            r'for\s+([A-Z][a-zA-Z\s&\-\'\.]+?)(?:\?|$|\s|,)',
            r'([A-Z][a-zA-Z\s&\-\'\.]+?)\'s',
            r'([A-Z][a-zA-Z\s&\-\'\.]+?)\s+(?:status|funding|contact)',
            r'(?:what|when|how|show|tell)\s+(?:is|was|did|does)\s+(?:the\s+)?(?:status|funding|contact)\s+(?:of\s+)?([A-Z][a-zA-Z\s&\-\'\.]+?)(?:\?|$|\s|,)',
            r'(?:when\s+)?(?:did|was)\s+([A-Z][a-zA-Z\s&\-\'\.]+?)\s+(?:last|most\s+recent)',
            r'([A-Z][a-zA-Z\s&\-\'\.]+?)\s+(?:last|most\s+recent)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                company_name = match.group(1).strip()
                # Clean up the company name
                company_name = re.sub(r'[^\w\s&\-\'\.]', '', company_name).strip()
                if len(company_name) > 2:  # Minimum length check
                    return company_name
        
        # Fallback: try to find any capitalized words that might be company names
        words = user_input.split()
        potential_companies = []
        for i, word in enumerate(words):
            if word[0].isupper() and len(word) > 2:
                # Look for multi-word company names
                company_parts = [word]
                for j in range(i + 1, min(i + 4, len(words))):
                    if words[j][0].isupper() and not words[j].lower() in ['the', 'and', 'or', 'for', 'with', 'of', 'in', 'on', 'at', 'to', 'from', 'by', 'about', 'like', 'as', 'is', 'was', 'are', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must', 'shall']:
                        company_parts.append(words[j])
                    else:
                        break
                if len(company_parts) > 0:
                    potential_companies.append(' '.join(company_parts))
        
        # Return the longest potential company name
        if potential_companies:
            return max(potential_companies, key=len)
        
        return None
    
    def find_best_match(self, user_input, threshold=0.3):
        """
        Find the best matching template for user input.
        
        Args:
            user_input (str): User's input text
            threshold (float): Similarity threshold for matching
            
        Returns:
            tuple: (best_template, similarity_score, intent)
        """
        # Encode user input
        user_embedding = self.model.encode([user_input])
        
        # Calculate similarities
        similarities = cosine_similarity(user_embedding, self.template_embeddings)[0]
        
        # Find best match
        best_idx = np.argmax(similarities)
        best_similarity = similarities[best_idx]
        best_template = self.templates[best_idx]
        best_intent = get_intent_for_template(best_template)
        
        # Debug logging
        print(f"Intent matched: {best_intent} with confidence: {best_similarity:.3f}")
        print(f"Best template: {best_template}")
        print(f"Best index: {best_idx}")
        
        if best_similarity >= threshold:
            return best_template, best_similarity, best_intent
        else:
            return None, best_similarity, None
    
    def parse_intent(self, user_input):
        """
        Parse user input to extract intent and company name.
        
        Args:
            user_input (str): User's input text
            
        Returns:
            dict: Dictionary with intent and company information
        """
        # Extract company name
        company_name = self.extract_company_name(user_input)
        
        # Find best matching intent
        best_template, similarity, intent = self.find_best_match(user_input)
        
        result = {
            "intent": intent,
            "company": company_name,
            "confidence": similarity,
            "matched_template": best_template
        }
        
        return result 