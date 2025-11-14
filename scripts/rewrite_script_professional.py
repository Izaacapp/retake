#!/usr/bin/env python3
"""
Professional script rewriter - make us sound coherent and professional
Uses AI/advanced grammar to fix stutters, fillers, and improve flow
"""
import json
import re
from pathlib import Path
from typing import List, Dict

class ProfessionalScriptRewriter:
    """Rewrite scripts to be professional and coherent"""
    
    def __init__(self):
        self.improvements = []
    
    def fix_technical_terms(self, text: str) -> str:
        """Fix technical terminology and product names"""
        fixes = {
            # Product names
            r'\bether\s*mail\b': 'Aether Mail',
            r'\bethermail\b': 'Aether Mail',
            r'\bgo\s*trigger\b': 'Go Trigger',
            r'\bdeeply\s*profound\b': 'Deeply Profound',
            
            # Technical terms
            r'\bpw\b': 'password',
            r'\bpws\b': 'passwords',
            r'\bauth\b': 'authentication',
            r'\bapi\b': 'API',
            r'\bui\b': 'UI',
            r'\bux\b': 'UX',
            r'\bdb\b': 'database',
            r'\brepo\b': 'repository',
            
            # Common issues
            r'\bgonna\b': 'going to',
            r'\bwanna\b': 'want to',
            r'\bgotta\b': 'have to',
            r'\bkinda\b': 'kind of',
            r'\bsorta\b': 'sort of',
        }
        
        result = text
        for pattern, replacement in fixes.items():
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        
        return result
    
    def remove_stutters_and_fillers(self, text: str) -> str:
        """Remove stutters, fillers, and hesitations"""
        
        # Remove filler words
        fillers = [
            r'\bum+\b', r'\buh+\b', r'\ber+\b', r'\bah+\b',
            r'\blike\b(?!\s+\w+ing)',  # Keep "like" if followed by gerund
            r'\byou\s+know\b',
            r'\bI\s+mean\b',
            r'\bbasically\b',
            r'\bactually\b',
            r'\bobviously\b',
            r'\bliterally\b',
            r'\bjust\b',
            r'\breally\b',
            r'\bvery\b',
            r'\bso\b(?=\s*,)',  # "so," at start
        ]
        
        result = text
        for filler in fillers:
            result = re.sub(filler, '', result, flags=re.IGNORECASE)
        
        # Remove repeated words (stutters)
        result = re.sub(r'\b(\w+)\s+\1\b', r'\1', result, flags=re.IGNORECASE)
        
        # Clean up multiple spaces and punctuation
        result = re.sub(r'\s+', ' ', result)
        result = re.sub(r'\s+([.,!?;:])', r'\1', result)
        result = re.sub(r'([.,!?;:])\1+', r'\1', result)  # Multiple punctuation
        
        return result.strip()
    
    def improve_sentence_flow(self, text: str) -> str:
        """Improve sentence structure and flow"""
        
        # Fix common speaking patterns
        improvements = {
            # Remove trailing conjunctions
            r'\s+(and|but|so|or)\s*[.,]': '.',
            
            # Fix "So," at start
            r'^\s*So,?\s*': '',
            r'^\s*And\s+': '',
            r'^\s*But\s+': '',
            
            # Fix "..." → proper pause
            r'\.{2,}': '.',
            r'\s*…\s*': '. ',
            
            # Fix incomplete sentences ending with "..."
            r'\.\.\.$': '.',
        }
        
        result = text
        for pattern, replacement in improvements.items():
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        
        # Capitalize after periods
        sentences = re.split(r'([.!?]\s+)', result)
        result = ''.join(
            s.capitalize() if i % 2 == 0 else s 
            for i, s in enumerate(sentences)
        )
        
        return result.strip()
    
    def make_professional(self, text: str) -> str:
        """Convert casual speech to professional presentation"""
        
        replacements = {
            # Casual → Professional
            r'\blet\'s\b': 'we will',
            r'\bwe\'re\b': 'we are',
            r'\bwe\'ll\b': 'we will',
            r'\bwe\'ve\b': 'we have',
            r'\bthat\'s\b': 'that is',
            r'\bit\'s\b': 'it is',
            r'\bhere\'s\b': 'here is',
            r'\bthere\'s\b': 'there is',
            r'\bcan\'t\b': 'cannot',
            r'\bwon\'t\b': 'will not',
            r'\bdon\'t\b': 'do not',
            r'\bdoesn\'t\b': 'does not',
            r'\bisn\'t\b': 'is not',
            
            # Improve phrasing
            r'\bcheck out\b': 'review',
            r'\blook at\b': 'examine',
            r'\bshow you\b': 'demonstrate',
            r'\bgo over\b': 'discuss',
            r'\btalk about\b': 'discuss',
        }
        
        result = text
        for pattern, replacement in replacements.items():
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        
        return result
    
    def add_professional_transitions(self, segments: List[str]) -> List[str]:
        """Add smooth transitions between segments"""
        
        transitions = [
            "First, let me demonstrate",
            "Next, we'll explore",
            "Now, observe",
            "Here you can see",
            "As shown here",
            "Moving forward",
            "Additionally",
            "Furthermore",
        ]
        
        # This would intelligently add transitions
        # For now, we'll return segments as-is
        return segments
    
    def process_full_script(self, text: str) -> tuple[str, List[str]]:
        """Apply all improvements to a script"""
        
        original = text
        
        # Step 1: Fix technical terms
        result = self.fix_technical_terms(text)
        if result != text:
            self.improvements.append("Fixed technical terminology")
        
        # Step 2: Remove fillers and stutters
        result = self.remove_stutters_and_fillers(result)
        
        # Step 3: Improve flow
        result = self.improve_sentence_flow(result)
        
        # Step 4: Make professional
        result = self.make_professional(result)
        
        # Final cleanup
        result = result.strip()
        if not result.endswith('.'):
            result += '.'
        
        # Ensure proper capitalization
        if result:
            result = result[0].upper() + result[1:]
        
        return result, self.improvements


def rewrite_all_segments():
    """Rewrite all Izaac and Ken segments professionally"""
    
    print("✍️  Professional Script Rewriter\n")
    print("Making you sound coherent, professional, and seamless\n")
    print("="*70 + "\n")
    
    # Load segments
    with open('output/izaac_segments.json') as f:
        izaac_segments = json.load(f)
    
    with open('output/ken_segments.json') as f:
        ken_segments = json.load(f)
    
    rewriter = ProfessionalScriptRewriter()
    
    # Process Izaac's demo segments
    print("🎤 Processing Izaac's segments...\n")
    
    izaac_demo = [s for s in izaac_segments if s['id'] >= 25 and s['id'] <= 45]
    izaac_rewritten = []
    
    for seg in izaac_demo[:10]:  # First 10 for demo
        original = seg['corrected']
        professional, improvements = rewriter.process_full_script(original)
        
        izaac_rewritten.append({
            'id': seg['id'],
            'start': seg['start'],
            'end': seg['end'],
            'original': seg['original'],
            'corrected': seg['corrected'],
            'professional': professional,
            'improvements': improvements
        })
        
        print(f"[{seg['id']}] Segment rewritten:")
        print(f"   Before: {original[:80]}...")
        print(f"   After:  {professional[:80]}...")
        print()
    
    # Process Ken's segments
    print("\n🎤 Processing Ken's segments...\n")
    
    ken_demo = [s for s in ken_segments if s['id'] >= 48]
    ken_rewritten = []
    
    for seg in ken_demo:
        original = seg['corrected']
        professional, improvements = rewriter.process_full_script(original)
        
        ken_rewritten.append({
            'id': seg['id'],
            'start': seg['start'],
            'end': seg['end'],
            'original': seg['original'],
            'corrected': seg['corrected'],
            'professional': professional,
            'improvements': improvements
        })
        
        print(f"[{seg['id']}] Segment rewritten:")
        print(f"   Before: {original[:80]}...")
        print(f"   After:  {professional[:80]}...")
        print()
    
    # Save professional scripts
    output_dir = Path("output/tts_scripts")
    
    # Save Izaac's professional script
    with open(output_dir / 'izaac_professional.txt', 'w') as f:
        for seg in izaac_rewritten:
            f.write(f"{seg['professional']}\n")
    
    with open(output_dir / 'izaac_professional.json', 'w') as f:
        json.dump(izaac_rewritten, f, indent=2)
    
    # Save Ken's professional script
    with open(output_dir / 'ken_professional.txt', 'w') as f:
        for seg in ken_rewritten:
            f.write(f"{seg['professional']}\n")
    
    with open(output_dir / 'ken_professional.json', 'w') as f:
        json.dump(ken_rewritten, f, indent=2)
    
    # Update TTS config with professional versions
    with open(output_dir / 'tts_config.json') as f:
        config = json.load(f)
    
    config['izaac']['professional_segments'] = izaac_rewritten
    config['ken']['professional_segments'] = ken_rewritten
    
    with open(output_dir / 'tts_config_professional.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("\n" + "="*70)
    print(f"✅ Professional scripts created!")
    print(f"\n📁 Saved to:")
    print(f"   {output_dir}/izaac_professional.txt")
    print(f"   {output_dir}/ken_professional.txt")
    print(f"   {output_dir}/tts_config_professional.json")
    print("\n🎯 Use these for TTS generation to sound professional!")


if __name__ == "__main__":
    rewrite_all_segments()
