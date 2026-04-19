from groq import Groq
import ollama
from config import Config
from .language_detector import LanguageDetector

class GroqClient:
    def __init__(self):
        if not Config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not set in environment variables")
        
        self.client = Groq(api_key=Config.GROQ_API_KEY)
    
    def chat_completion(self, messages, temperature=None, max_tokens=None):
        try:
            response = self.client.chat.completions.create(
                model=Config.GROQ_MODEL,
                messages=messages,
                temperature=temperature or Config.GROQ_TEMPERATURE,
                max_tokens=max_tokens or Config.GROQ_MAX_TOKENS
            )
            return response.choices[0].message.content
        except Exception as e:
            if Config.FALLBACK_TO_OLLAMA:
                return self._fallback_to_ollama(messages, temperature, max_tokens)
            raise Exception(f"Error calling Groq API: {str(e)}")
    
    def _fallback_to_ollama(self, messages, temperature, max_tokens):
        try:
            # Convert messages to single prompt for Ollama
            prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
            
            response = ollama.chat(
                model=Config.OLLAMA_MODEL,
                messages=[{"role": "user", "content": prompt}]
            )
            return response['message']['content']
        except Exception as ollama_error:
            raise Exception(f"Both Groq and Ollama failed. Groq error: {str(e)}. Ollama error: {str(ollama_error)}")
    
    def get_response_with_context(self, query, context_documents):
        from llm.prompt import get_system_prompt
        
        # Detect the language of the query
        detected_language = LanguageDetector.detect_language(query)
        
        # Check for language preference requests
        if LanguageDetector.is_language_preference_request(query):
            # Detect which language is being requested
            query_lower = query.lower().strip().replace('??', '').replace('?', '')
            if 'hindi' in query_lower or 'हिंदी' in query_lower:
                return LanguageDetector.get_greeting_in_language('hi')
            elif 'marathi' in query_lower or 'मराठी' in query_lower:
                return LanguageDetector.get_greeting_in_language('mr')
            else:
                return LanguageDetector.get_greeting_in_language(detected_language)
        
        # Check if it's a greeting
        if LanguageDetector.is_greeting(query):
            greeting = LanguageDetector.get_greeting_in_language(detected_language)
            return greeting
        
        # Filter relevant context documents
        relevant_contexts = self._filter_relevant_context(query, context_documents)
        
        # Get language-specific system prompt
        system_prompt, _, disclaimer = get_system_prompt(relevant_contexts, detected_language)
        
        # Add language instruction to ensure response in the same language
        language_instruction = {
            'en': "Respond in English.",
            'hi': "हिंदी में उत्तर दें।",
            'mr': "मराठी मध्ये उत्तर द्या।"
        }
        
        messages = [
            {"role": "system", "content": system_prompt + f"\n\n{language_instruction.get(detected_language, 'Respond in English.')}"},
            {"role": "user", "content": f"Question: {query}\n\nPlease provide a comprehensive answer based on the available information."}
        ]
        
        response = self.chat_completion(messages)
        
        # Ensure the response ends with the correct disclaimer
        if not response.endswith(disclaimer):
            response += f"\n\n{disclaimer}"
        
        return response
    
    def _filter_relevant_context(self, query, context_documents):
        """
        Filter context documents to only include relevant ones for the query.
        This helps prevent hallucination by ensuring only relevant context is used.
        """
        if not context_documents:
            return []
        
        # Simple relevance check based on keyword overlap
        query_words = set(query.lower().split())
        relevant_docs = []
        
        for doc in context_documents:
            doc_lower = doc.lower()
            # Check if at least some query words appear in the document
            word_matches = sum(1 for word in query_words if len(word) > 2 and word in doc_lower)
            
            # Consider document relevant if it contains at least 2 meaningful query words
            # or if the query is very general (less than 3 meaningful words)
            meaningful_query_words = [w for w in query_words if len(w) > 2]
            
            if (len(meaningful_query_words) <= 2 and word_matches >= 1) or \
               (len(meaningful_query_words) > 2 and word_matches >= 2):
                relevant_docs.append(doc)
        
        # If no documents are relevant, return empty list to trigger fallback
        if not relevant_docs:
            return []
        
        return relevant_docs
