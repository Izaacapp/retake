"""
Grammar correction and text improvement
"""
from pathlib import Path
from typing import List, Dict
import re


class GrammarCorrector:
    """Fix grammar and improve text quality"""
    
    def __init__(self):
        self.corrections = {}
        print("📝 Grammar Corrector initialized")
    
    def correct_text(self, text: str) -> str:
        """
        Correct grammar and improve text
        
        Args:
            text: Input text to correct
        
        Returns:
            Corrected text
        """
        # Basic corrections
        corrected = text
        
        # Fix common issues
        corrections = {
            r'\bgonna\b': 'going to',
            r'\bwanna\b': 'want to',
            r'\bgotta\b': 'have to',
            r'\bkinda\b': 'kind of',
            r'\bsorta\b': 'sort of',
            r'\byeah\b': 'yes',
            r'\bok\b': 'okay',
            r'\bum\b': '',
            r'\buh\b': '',
            r'\ber\b': '',
            r'\bahh?\b': '',
        }
        
        for pattern, replacement in corrections.items():
            corrected = re.sub(pattern, replacement, corrected, flags=re.IGNORECASE)
        
        # Clean up multiple spaces
        corrected = re.sub(r'\s+', ' ', corrected).strip()
        
        # Capitalize first letter
        if corrected:
            corrected = corrected[0].upper() + corrected[1:]
        
        return corrected
    
    def improve_professional_tone(self, text: str) -> str:
        """
        Make text more professional
        
        Args:
            text: Input text
        
        Returns:
            Professionally toned text
        """
        improvements = {
            r'we\'re gonna': 'we will',
            r'we\'ll': 'we will',
            r'can\'t': 'cannot',
            r'won\'t': 'will not',
            r'don\'t': 'do not',
            r'doesn\'t': 'does not',
            r'isn\'t': 'is not',
            r'aren\'t': 'are not',
        }
        
        improved = text
        for pattern, replacement in improvements.items():
            improved = re.sub(pattern, replacement, improved, flags=re.IGNORECASE)
        
        return improved
    
    def remove_filler_words(self, text: str) -> str:
        """Remove filler words and hesitations"""
        fillers = [
            r'\bum+\b', r'\buh+\b', r'\ber+\b', r'\bah+\b',
            r'\blike\b(?!\s+\w+ing)', r'\byou know\b', 
            r'\bI mean\b', r'\bbasically\b', r'\bactually\b'
        ]
        
        cleaned = text
        for filler in fillers:
            cleaned = re.sub(filler, '', cleaned, flags=re.IGNORECASE)
        
        # Clean up spacing
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        cleaned = re.sub(r'\s+([.,!?])', r'\1', cleaned)
        
        return cleaned
    
    def fix_transcript_errors(self, text: str) -> str:
        """
        Fix common transcription errors
        
        Args:
            text: Transcribed text
        
        Returns:
            Corrected text
        """
        # Product/company name corrections
        corrections = {
            'ether mail': 'Aether Mail',
            'ethermail': 'Aether Mail',
            'go trigger': 'Go Trigger',
            'deeply profound': 'Deeply Profound',
            'dp profound': 'Deeply Profound',
        }
        
        corrected = text
        for wrong, right in corrections.items():
            corrected = re.sub(
                r'\b' + re.escape(wrong) + r'\b',
                right,
                corrected,
                flags=re.IGNORECASE
            )
        
        return corrected
    
    def process_full_script(self, text: str) -> str:
        """
        Apply all corrections to a script
        
        Args:
            text: Input script
        
        Returns:
            Fully corrected script
        """
        print(f"📝 Processing script ({len(text)} chars)...")
        
        # Apply all corrections
        result = self.fix_transcript_errors(text)
        result = self.correct_text(result)
        result = self.remove_filler_words(result)
        result = self.improve_professional_tone(result)
        
        print(f"✅ Script processed ({len(result)} chars)")
        return result
