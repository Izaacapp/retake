#!/usr/bin/env python3
"""
Create highly professional rewrites for ALL segments
Based on professional speaking principles:
1. Sentence Fluency - combine choppy ideas into flowing prose
2. Confidence & Certainty - direct statements, no hedging
3. Clarity - accessible to non-technical audiences  
4. Active Voice - engaging, direct
5. Remove Fillers - no "obviously," "so," "essentially," "like"
"""
import json
from pathlib import Path

# Highly professional rewrites - hand-crafted improvements
REWRITES = {
    # IZAAC / Zoom user segments
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
    
    25: "This is the first screen users see when entering our platform.",
    
    26: "Let me show you the account creation process. Users review our terms of service and generate their credentials.",
    
    27: "The system generates secure credentials that users save locally. They download the key file needed to access the platform.",
    
    28: "Now I'll demonstrate the login process.",
    
    29: "I'll use the credentials we just generated.",
    
    30: "After successful authentication, users arrive at the main dashboard.",
    
    31: "The dashboard provides access to the platform's key features, including the mail service.",
    
    32: "The first step for any user is to aggregate their existing email accounts. This centralizes their digital identity and allows our system to function.",
    
    33: "We support multiple email providers, allowing users to aggregate all their accounts into one centralized location.",
    
    34: "I'll demonstrate by connecting my Gmail account.",
    
    36: "This requires an app password from the email provider, a process that is often unnecessarily complex. To streamline this, we provide direct links to the exact settings page for each provider. Once the app password is generated, users simply enter their credentials, as I'm demonstrating now with my Gmail account.",
    
    37: "We are connecting via the IMAP protocol. For users who prefer it, we also support POP3, giving you flexibility in how you access and control your email data.",
    
    38: "This gives you complete control over your data. For this demonstration, I'll use the IMAP protocol and add my account here.",
    
    39: "The system is now verifying the connection.",
    
    40: "The verification confirms a successful connection. For the IMAP protocol, we use Dovecot, which is an email server requirement.",
    
    41: "We also use Postfix for mail handling. The verification confirms the connection was successful, and my account is now synced.",
    
    42: "With the account successfully connected and syncing, I'll now navigate to the password rotation module. The system is now actively monitoring the connected inbox for relevant emails.",
    
    43: "This pulls emails from the account I just connected.",
    
    44: "As you can see, a verification code has arrived. This demonstrates the targeted website integration.",
    
    45: "Now I'll show you the demonstration website.",
    
    46: "Actually, Ken will demonstrate the testing website.",
    
    # KEN / Kenith Philip segments
    47: "Building complex applications presents unique challenges.",
    
    48: "One significant challenge is testing. Testing our automation on mainstream platforms would result in immediate account suspension. For this reason, we developed a dedicated testing environment - a dummy website that replicates real-world password reset flows. Let me demonstrate how this works.",
    
    49: "I have a test account configured here that I will use for the demonstration.",
    
    50: "I will now log in to show you the interface.",
    
    51: "As you can see, once logged in, we have a clean interface displaying basic account information: username, email, and profile details. Another key feature I want to highlight is our password generator.",
    
    52: "The password generator creates strong, secure passwords while giving users full control over the format. Users can choose between random passwords that mix letters, numbers, and special characters for maximum security, or memorable passphrases that are easier to remember. A slider allows customization of password length to meet different security requirements.",
    
    53: "While our automated password rotation handles this process automatically, we also give users the choice to manually override the system and select their own password if they prefer. I will now hand it back to Izaac.",
    
    # IZAAC continues
    54: "Thank you, Ken. Now that you've seen the password generator, I'll show you how the email inbox works.",
    
    55: "This is the unified inbox interface. Here, users see a consolidated view of all emails from their connected accounts. In this demonstration, you're seeing one connected account, but users can integrate multiple providers into this single, manageable dashboard.",
    
    56: "Our system intelligently parses these emails to automatically detect and extract verification codes. This is the key that enables the automation of the password reset process.",
    
    57: "This automation completely eliminates the need for users to manually visit dozens of websites to change their passwords after a breach.",
    
    58: "Instead of spending hours addressing breaches across multiple services, the system handles everything automatically.",
    
    59: "That's an overview of the email platform.",
    
    # JULES / Jhuiwensley Belizaire segments
    60: "Hello, I'm Jules. I work on security and API architecture.",
    
    62: "I want to discuss our platform's terms of use and security approach.",
    
    63: "When you sign up to use our service,",
    
    64: "we ask that you agree to our terms of use. This ensures you understand",
    
    65: "that by using our application, you consent to providing us with",
    
    66: "your email credentials so we can access them on your behalf.",
    
    67: "We have a privacy-focused architecture. We do not track",
    
    68: "any of your personal information. Everything is end-to-end encrypted.",
    
    69: "We want to ensure that you receive comprehensive security",
    
    70: "from top to bottom.",
    
    # AARON / Devon Villalona segments  
    14: "I will now demonstrate the desktop features built with Electron.",
    
    18: "Let me show you the breach report feature. We use the Have I Been Pwned API",
    
    19: "to search for breach reports. I'll demonstrate using my own email.",
    
    22: "The breach report displays comprehensive data on compromised accounts, including millions of affected users. It provides article links and detailed information, showing users the full scope of breaches associated with their email address.",
    
    23: "From here, I can return to the dashboard.",
    
    24: "Now let's discuss Aether Mail.",
    
    76: "Returning to the Electron desktop application, I'll show you the password vault and how to access it.",
    
    77: "There are two authentication methods. You can see the biometric fingerprint reader for Apple devices, or use your master password that you received during registration. Let me access the vault now.",
    
    78: "Here, you can import emails and passwords into the vault using various formats. We support manual entry, LastPass CSV, and 45 different password manager formats across four standard export types.",
    
    80: "Let me show you an example import.",
    
    82: "Successfully imported six entries.",
    
    83: "The passwords are now stored in the vault. Everything in the Electron application automatically syncs with mobile,",
    
    84: "ensuring feature parity across all platforms. The vault automatically locks when you navigate away for security.",
    
    85: "Your data remains protected.",
    
    86: "The vault stays locked until you authenticate again. Now let me discuss",
    
    87: "the CVE Security Alerts. This feature uses an API in conjunction with the breach report. It allows you to search detailed breach reports from the Have I Been Pwned database.",
    
    88: "This provides comprehensive details about specific breaches. For example, if you were affected by a Walmart breach,",
    
    91: "you can see the full details here. The report shows comprehensive information about what happened and the severity of the breach.",
    
    92: "Next, I'll demonstrate our mobile sync, implementation, and features.",
    
    141: "Here is our mobile implementation built with Flutter. I'll log in now. You'll see we have Face ID for biometric authentication, providing access to all the platform's features.",
    
    142: "Let me navigate to the breach report.",
    
    144: "I'll use Jared's email for this demonstration.",
    
    145: "Let me show you Jared's breach report.",
    
    146: "As you can see, Jared's email has significant exposure across multiple breaches.",
    
    147: "Now I'll show the password vault. The vault uses Face ID instead of fingerprint authentication on iOS. As you can see, it's automatically synced with the passwords we imported on desktop.",
    
    148: "The CVE feature works identically on mobile.",
    
    150: "This demonstrates the mobile implementation",
    
    151: "that stays in perfect sync with our Electron desktop application.",
    
    # JARED / Jared Zayas segments
    170: "That concludes our project demonstration. Thank you for your attention.",
    
    176: "That concludes our presentation and demonstration of our project. Thank you for your attention.",
    
    # FINAL
    182: "That concludes our presentation. Thank you.",
}

def create_highly_professional_transcript():
    """Create one JSON file with original + highly_professional rewrites"""
    
    print("🎯 Creating Highly Professional Transcript Rewrites\n")
    print("   Based on professional speaking principles:")
    print("   ✅ Sentence Fluency: Flowing, combined ideas")
    print("   ✅ Confidence: Direct, certain statements")
    print("   ✅ Clarity: Accessible language")
    print("   ✅ Active Voice: Engaging communication")
    print("   ✅ No Fillers: Removed 'obviously', 'so', 'essentially'\n")
    
    # Load original transcript
    input_file = Path('output/original/corrected_transcript.json')
    with open(input_file) as f:
        segments = json.load(f)
    
    print(f"📖 Loaded {len(segments)} segments from {input_file}")
    
    # Add highly_professional field to each segment
    rewritten_count = 0
    for segment in segments:
        seg_id = segment['id']
        
        if seg_id in REWRITES:
            segment['highly_professional'] = REWRITES[seg_id]
            rewritten_count += 1
        else:
            # For segments without custom rewrite, use corrected version
            segment['highly_professional'] = segment.get('corrected', segment['original'])
    
    # Save to new file
    output_file = Path('output/original/professional_transcript.json')
    with open(output_file, 'w') as f:
        json.dump(segments, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Created {output_file}")
    print(f"   📊 Total segments: {len(segments)}")
    print(f"   🎨 Custom rewrites: {rewritten_count}")
    print(f"   🤖 Using corrected: {len(segments) - rewritten_count}")
    
    # Show some examples
    print("\n📝 Example Improvements:\n")
    examples = [0, 3, 48, 52]
    for seg_id in examples:
        seg = next((s for s in segments if s['id'] == seg_id), None)
        if seg:
            print(f"ID {seg_id} | {seg['speaker']}")
            print(f"❌ Original:")
            print(f"   {seg['original'][:100]}...")
            print(f"✅ Highly Professional:")
            print(f"   {seg['highly_professional'][:100]}...")
            print()
    
    return output_file

if __name__ == "__main__":
    output_file = create_highly_professional_transcript()
    print(f"\n📁 Output: {output_file}")
    print("\n💡 This file contains ALL segments with 'highly_professional' rewrites")
    print("   Use this for TTS generation to get polished, professional audio")
