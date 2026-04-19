import re

class LanguageDetector:
    @staticmethod
    def detect_language(text):
        """
        Detect the language of the input text
        Returns: 'en', 'hi', 'mr', or 'en' as default
        """
        text = text.lower().strip()
        
        # Hindi-specific keywords (more specific than Marathi)
        hindi_keywords = [
            'मुझे', 'तुम्हें', 'मैं', 'तुम', 'है', 'हैं', 'करूं', 'करें', 'क्या', 'कब', 'कहां', 
            'कैसे', 'क्यों', 'जिससे', 'जिसमें', 'लिए', 'पर', 'से', 'का', 'की', 'के', 'गया', 'गई',
            'बुखार', 'सिरदर्द', 'पेटदर्द', 'खांसी', 'जुकाम', 'दमा', 'सर्दी', 'दवा', 'डॉक्टर', 'इलाज',
            'नमस्ते', 'प्रणाम', 'धन्यवाद', 'शुभ', 'प्रभात', 'संध्या', 'दिन'
        ]
        
        # Marathi-specific keywords
        marathi_keywords = [
            'मला', 'तुम्हाला', 'मी', 'तुम्ही', 'आहे', 'आहात', 'करू', 'करा', 'काय', 'कधी', 'कुठे',
            'कसे', 'का', 'कोणत्या', 'ज्याच्या', 'ज्यात', 'साठी', 'वर', 'पासून', 'चा', 'ची', 'चे',
            'गेला', 'गेली', 'गेले', 'ताप', 'डोकेदुखी', 'पोटदुखी', 'खोकला', 'जुकाम', 'दमा', 'सर्दी',
            'औषध', 'डॉक्टर', 'उपचार', 'नमस्कार', 'धन्यवाद', 'शुभ', 'प्रभात', 'संध्या', 'दिवस'
        ]
        
        # Check for Hindi keywords first (more specific)
        hindi_count = sum(1 for keyword in hindi_keywords if keyword in text)
        marathi_count = sum(1 for keyword in marathi_keywords if keyword in text)
        
        # If we found specific language keywords, use them
        if hindi_count > marathi_count:
            return 'hi'
        elif marathi_count > hindi_count:
            return 'mr'
        
        # Fallback to script-based detection with preference for Marathi
        # since many words are shared between the languages
        if re.search(r'[अ-ह]', text):  # Devanagari script detected
            # Default to Marathi when script matches but keywords are unclear
            # as Marathi is more likely in this context
            return 'mr'
        
        # Default to English
        return 'en'
    
    @staticmethod
    def get_language_name(lang_code):
        """Get full language name from code"""
        languages = {
            'en': 'English',
            'hi': 'Hindi',
            'mr': 'Marathi'
        }
        return languages.get(lang_code, 'English')
    
    @staticmethod
    def get_greeting_in_language(lang_code):
        """Get appropriate greeting based on language"""
        greetings = {
            'en': "Hello! 👋 I'm AyurvedaCare, your AI health assistant. How can I help you today?",
            'hi': "नमस्ते! 👋 मैं आयुर्वेदकेयर हूं, आपका AI स्वास्थ्य सहायक। आज मैं आपकी कैसे मदद कर सकता हूं?",
            'mr': "नमस्कार! 👋 मी आयुर्वेदकेयर आहे, तुमचा AI आरोग्य सहायक. आज मी तुमची कशी मदत करू शकतो?"
        }
        return greetings.get(lang_code, greetings['en'])
    
    @staticmethod
    def get_disclaimer_in_language(lang_code):
        """Get medical disclaimer in the detected language"""
        disclaimers = {
            'en': "Remember to consult healthcare professionals for personal medical advice.",
            'hi': "व्यक्तिगत चिकित्सा सलाह के लिए स्वास्थ्य देखभाल पेशेवरों से परामर्श करें।",
            'mr': "वैयक्तिक वैद्यकीय सल्ल्यासाठी आरोग्य सेवा व्यावसायिकांशी सल्ला करा."
        }
        return disclaimers.get(lang_code, disclaimers['en'])
    
    @staticmethod
    def is_greeting(text):
        """Check if the text is a greeting in any supported language"""
        text = text.lower().strip()
        greetings = [
            # English
            'hi', 'hello', 'hey', 'heyy', 'heyyy', 'yo', 'good morning', 'good afternoon', 'good evening',
            # Hindi
            'नमस्ते', 'नमस्कार', 'हेलो', 'हाय', 'सुप्रभात', 'शुभ दिन', 'शुभ संध्या',
            # Marathi
            'नमस्कार', 'हाय', 'हेलो', 'सुप्रभात', 'शुभ दिन', 'शुभ संध्या'
        ]
        return any(greeting in text for greeting in greetings)
    
    @staticmethod
    def is_language_preference_request(text):
        """Check if user is requesting to speak in a specific language"""
        text = text.lower().strip()
        language_requests = [
            'kya hum hindi mei baat kre',
            'kya hum hindi mei baat kre??',
            'kya hum hindi mei baat kre ?',
            'can we speak in hindi',
            'can we speak in marathi', 
            'marathi madhe bolu ka',
            'मराठी मध्ये बोलू शकाल का',
            'हिंदी में बात कर सकते हैं',
            'hindi me baat kare',
            'hindi mein baat karen',
            'marathi madhe bolu shakto ka'
        ]
        
        # Normalize the text for comparison
        normalized_text = text.replace('??', '').replace('?', '').strip()
        return any(request in normalized_text or normalized_text in request for request in language_requests)
