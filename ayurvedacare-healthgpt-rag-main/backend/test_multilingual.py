#!/usr/bin/env python3
"""
Test script for multilingual functionality
Tests language detection and responses in English, Hindi, and Marathi
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm.language_detector import LanguageDetector

def test_language_detection():
    """Test language detection functionality"""
    
    test_cases = [
        # English test cases
        ("I have fever", "en"),
        ("hello", "en"),
        ("I have headache", "en"),
        ("What should I do for cold?", "en"),
        
        # Hindi test cases
        ("मुझे बुखार है", "hi"),
        ("नमस्ते", "hi"),
        ("मुझे सिरदर्द है", "hi"),
        ("खांसी के लिए क्या करूं?", "hi"),
        
        # Marathi test cases
        ("मला ताप आला आहे", "mr"),
        ("नमस्कार", "mr"),
        ("मला डोकेदुखी आहे", "mr"),
        ("खोकल्यासाठी काय करावे?", "mr"),
    ]
    
    print("Testing Language Detection:")
    print("=" * 50)
    
    all_passed = True
    for text, expected_lang in test_cases:
        detected = LanguageDetector.detect_language(text)
        status = "✅" if detected == expected_lang else "❌"
        print(f"{status} '{text}' -> {detected} (expected: {expected_lang})")
        if detected != expected_lang:
            all_passed = False
    
    print("\nTesting Greeting Detection:")
    print("=" * 50)
    
    greeting_tests = [
        ("hello", True),
        ("नमस्ते", True),
        ("नमस्कार", True),
        ("I have fever", False),
        ("मुझे बुखार है", False),
        ("मला ताप आला आहे", False),
    ]
    
    for text, expected_greeting in greeting_tests:
        is_greeting = LanguageDetector.is_greeting(text)
        status = "✅" if is_greeting == expected_greeting else "❌"
        print(f"{status} '{text}' -> Greeting: {is_greeting} (expected: {expected_greeting})")
        if is_greeting != expected_greeting:
            all_passed = False
    
    print("\nTesting Multilingual Greetings:")
    print("=" * 50)
    
    for lang_code in ['en', 'hi', 'mr']:
        greeting = LanguageDetector.get_greeting_in_language(lang_code)
        disclaimer = LanguageDetector.get_disclaimer_in_language(lang_code)
        print(f"\n{LanguageDetector.get_language_name(lang_code)} ({lang_code}):")
        print(f"  Greeting: {greeting}")
        print(f"  Disclaimer: {disclaimer}")
    
    return all_passed

if __name__ == "__main__":
    success = test_language_detection()
    print(f"\n{'='*50}")
    if success:
        print("🎉 All tests passed!")
    else:
        print("❌ Some tests failed!")
    sys.exit(0 if success else 1)
