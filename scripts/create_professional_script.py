#!/usr/bin/env python3
"""
Create HIGHLY professional scripts for TTS - polished, confident, and clear
This implements improvements based on professional speaking best practices:
1. Sentence Fluency: Combine related ideas into flowing sentences
2. Confidence & Certainty: Replace hesitant language with direct statements
3. Clarity: Accessible to non-technical audiences
4. Active Voice: More engaging and direct
5. Remove Conversational Fillers: Eliminate "obviously," "so," "like," "boom"
"""
import json
from pathlib import Path

# Highly professional segment rewrites based on analysis
HIGHLY_PROFESSIONAL_REWRITES = {
    # Opening and Introduction (Izaac)
    0: "Good morning. We are Deeply Profound, a research security group founded with a singular mission: to solve one of the most critical and pervasive problems in cybersecurity today.",
    1: "Our work began with a fundamental question: How can we effectively remediate security breaches when user credentials are compromised across dozens of different services?",
    2: "The core problem we're addressing is the credential breach crisis.",
    3: "The core issue is that a single data breach can trigger a cascade of security risks. When people reuse passwords, one compromised credential can expose their accounts across dozens of unrelated platforms.",
    4: "Manual password rotation is time-consuming and error-prone. Users must visit each website individually to reset their passwords.",
    5: "This creates verification code chaos. Each service sends reset codes via email, requiring constant inbox monitoring. Email providers also scan your messages, exposing sensitive verification codes and compromising your privacy.",
    6: "When credentials are breached on one platform, password reuse means the breach compromises accounts across multiple unrelated services.",
    7: "The reality is that most people do not rotate their passwords after breaches because the process is too difficult and time-consuming.",
    8: "Our solution is a two-part platform. The first component is Aether Mail, an aggregated and private email service.",
    9: "The second component is a secure password vault, which works in tandem with Aether Mail to fully automate security remediation.",
    11: "Let's now transition to a live demonstration of the platform, starting with the password vault.",
    
    # Platform Demo (Izaac continues)
    32: "The first step for any user is to aggregate their existing email accounts. This centralizes their digital identity and allows our system to function.",
    36: "This requires an app password from the email provider, a process that is often unnecessarily complex. To streamline this, we provide direct links to the exact settings page for each provider. Once the app password is generated, the user simply enters their credentials, as I'm demonstrating now with my Gmail account.",
    37: "We are connecting via the IMAP protocol. For users who prefer it, we also support POP3, giving you flexibility in how you access and control your email data.",
    42: "With the account successfully connected and syncing, I'll now navigate to the password rotation module. The system is now actively monitoring the connected inbox for relevant emails.",
    55: "This is the unified inbox interface. Here, users see a consolidated view of all emails from their connected accounts. In this case, you're seeing one connected account, but users can integrate multiple providers into this single, manageable dashboard.",
    56: "Our system intelligently parses these emails to automatically detect and extract verification codes. This is the key that enables the automation of the password reset process.",
    57: "This automation completely eliminates the need for users to manually visit dozens of websites to change their passwords after a breach.",
    
    # Ken's Section - Testing Website & Password Generator  
    47: "Building complex applications presents unique challenges.",
    48: "One significant challenge is testing. Testing our automation on mainstream platforms would result in immediate account suspension. For this reason, we developed a dedicated testing environment - a dummy website that replicates real-world password reset flows. Let me demonstrate how this works.",
    49: "I have a test account configured here that I will use for the demonstration.",
    50: "I will now log in to show you the interface.",
    51: "As you can see, once logged in, we have a clean interface displaying basic account information: username, email, and profile details. Another key feature I want to highlight is our password generator.",
    52: "The password generator creates strong, secure passwords while giving users full control over the format. Users can choose between random passwords that mix letters, numbers, and special characters for maximum security, or memorable passphrases that are easier to remember. A slider allows customization of password length to meet different security requirements.",
    53: "While our automated password rotation handles this process automatically, we also give users the choice to manually override the system and select their own password if they prefer. I will now hand it back to Izaac.",
    
    # Conclusion
    182: "That concludes our presentation and demonstration of the Deeply Profound platform. Thank you.",
}

def remove_filler_words(text):
    """Remove conversational fillers and hesitant language"""
    replacements = {
        # Conversational fillers
        'obviously': '',
        'essentially': '',
        'basically': '',
        'so...': '',
        'like,': ',',
        'boom': '',
        'crazy': 'interesting',
        
        # Hesitant language
        'kind of': '',
        'sort of': '',
        'I think': '',
        'I guess': '',
        'maybe': '',
        
        # Contractions (make formal)
        "gonna": "going to",
        "wanna": "want to",
        "kinda": "kind of",
        "don't": "do not",
        "won't": "will not",
        "can't": "cannot",
        "I'll": "I will",
        "we'll": "we will",
        "you'll": "you will",
        "we're": "we are",
        "you're": "you are",
        "it's": "it is",
        
        # Fix product names
        "EtherMail": "Aether Mail",
        "Pope Protocol": "POP3",
    }
    
    result = text
    for old, new in replacements.items():
        result = result.replace(old, new)
    
    # Clean up extra spaces
    while '  ' in result:
        result = result.replace('  ', ' ')
    
    return result.strip()

def make_professional_sentence(text):
    """Convert choppy/casual text into professional flowing sentences"""
    # Remove leading conversational words
    text = text.strip()
    for prefix in ['So,', 'So ', 'And,', 'And ']:
        if text.startswith(prefix):
            text = text[len(prefix):].strip()
    
    # Ensure proper capitalization
    if text and not text[0].isupper():
        text = text[0].upper() + text[1:]
    
    return text

def rewrite_professional(segments, speaker_name):
    """Rewrite segments into highly professional, fluid script"""
    
    # Group by speaker and context
    speaker_segments = [s for s in segments if speaker_name.lower() in s['speaker'].lower()]
    
    professional_segments = []
    
    for seg in speaker_segments:
        original = seg['original']
        corrected = seg.get('corrected', original)
        seg_id = seg['id']
        
        # Check if we have a custom highly professional rewrite
        if seg_id in HIGHLY_PROFESSIONAL_REWRITES:
            highly_professional = HIGHLY_PROFESSIONAL_REWRITES[seg_id]
        else:
            # Generate professional version
            # Start with corrected version if available
            highly_professional = corrected
            
            # Apply transformations
            highly_professional = remove_filler_words(highly_professional)
            highly_professional = make_professional_sentence(highly_professional)
        
        professional_segments.append({
            'id': seg['id'],
            'start': seg['start'],
            'end': seg['end'],
            'speaker': seg['speaker'],
            'original': original,
            'corrected': corrected,
            'professional': seg.get('professional', corrected),  # Keep old professional if exists
            'highly_professional': highly_professional,
            'duration': seg['end']
        })
    
    return professional_segments


def main():
    """Create highly professional scripts for each speaker"""
    
    print("🎯 Creating HIGHLY PROFESSIONAL scripts with improvements:\n")
    print("   ✅ Sentence Fluency: Flowing, combined ideas")
    print("   ✅ Confidence: Direct, certain statements")
    print("   ✅ Clarity: Accessible language")
    print("   ✅ Active Voice: Engaging communication")
    print("   ✅ No Fillers: Removed 'obviously', 'so', 'essentially', etc.\n")
    
    # Load original transcript
    with open('output/original/corrected_transcript.json') as f:
        segments = json.load(f)
    
    # Map speakers
    speaker_map = {
        'izaac': 'Zoom user',
        'aaron': 'Devon Villalona',
        'ken': 'Kenith Philip',
        'jules': 'Jhuiwensley Belizaire',
        'jared': 'Jared Zayas'
    }
    
    total_custom_rewrites = 0
    total_segments = 0
    
    # Create professional scripts for each
    for name, speaker_id in speaker_map.items():
        print(f"✍️  Writing highly professional script for {name.upper()}...")
        
        prof_segments = rewrite_professional(segments, speaker_id)
        
        if prof_segments:
            # Count custom rewrites
            custom_rewrites = sum(1 for seg in prof_segments if seg['id'] in HIGHLY_PROFESSIONAL_REWRITES)
            total_custom_rewrites += custom_rewrites
            total_segments += len(prof_segments)
            
            # Save to speaker's folder
            output_file = Path(f'output/speakers/{name}/transcripts/{name}_highly_professional.json')
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w') as f:
                json.dump(prof_segments, f, indent=2, ensure_ascii=False)
            
            print(f"   ✅ {len(prof_segments)} segments ({custom_rewrites} custom rewrites) → {output_file}")
            
            # Show comparison example
            if prof_segments:
                # Find a segment with custom rewrite
                custom_seg = next((s for s in prof_segments if s['id'] in HIGHLY_PROFESSIONAL_REWRITES), None)
                if custom_seg:
                    print(f"\n   📝 Example Improvement (ID {custom_seg['id']}):")
                    print(f"   ❌ Original: {custom_seg['original'][:80]}...")
                    print(f"   ✅ Highly Professional: {custom_seg['highly_professional'][:80]}...")
        
        print()
    
    print("=" * 80)
    print(f"✅ Highly professional scripts created!")
    print(f"   📊 Total segments processed: {total_segments}")
    print(f"   🎨 Custom rewrites: {total_custom_rewrites}")
    print(f"   🤖 Auto-cleaned: {total_segments - total_custom_rewrites}")
    print()
    print("💡 Key improvements made:")
    print("   • Removed conversational fillers (so, obviously, essentially)")
    print("   • Replaced hesitant language with confident statements")
    print("   • Combined choppy sentences into flowing prose")
    print("   • Made technical terms accessible")
    print("   • Used active voice for engagement")
    print()
    print("📁 Output location: output/speakers/*/transcripts/*_highly_professional.json")


if __name__ == "__main__":
    main()
