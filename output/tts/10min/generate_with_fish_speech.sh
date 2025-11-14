#!/bin/bash
# Batch TTS generation using Fish Speech API
# Make sure Fish Speech server is running: python tools/api_server.py

set -e

# Segment 1: INTRODUCTION
echo 'Generating 01_Izaac_INTRODUCTION.wav...'
python fish-speech/tools/api_client.py \
  --text "$(cat output/tts/10min/01_Izaac_INTRODUCTION.txt)" \
  --reference_audio models/izaac_voice_embedding.npy \
  --output output/tts/10min/01_Izaac_INTRODUCTION \
  --format wav \
  --play False

# Segment 2: THE PROBLEM
echo 'Generating 02_Izaac_THE_PROBLEM.wav...'
python fish-speech/tools/api_client.py \
  --text "$(cat output/tts/10min/02_Izaac_THE_PROBLEM.txt)" \
  --reference_audio models/izaac_voice_embedding.npy \
  --output output/tts/10min/02_Izaac_THE_PROBLEM \
  --format wav \
  --play False

# Segment 3: OUR SOLUTION
echo 'Generating 03_Izaac_OUR_SOLUTION.wav...'
python fish-speech/tools/api_client.py \
  --text "$(cat output/tts/10min/03_Izaac_OUR_SOLUTION.txt)" \
  --reference_audio models/izaac_voice_embedding.npy \
  --output output/tts/10min/03_Izaac_OUR_SOLUTION \
  --format wav \
  --play False

# Segment 4: DEMO: Account Creation & Dashboard
echo 'Generating 04_Izaac_DEMO_Account_Creation_&_Dashboard.wav...'
python fish-speech/tools/api_client.py \
  --text "$(cat output/tts/10min/04_Izaac_DEMO_Account_Creation_&_Dashboard.txt)" \
  --reference_audio models/izaac_voice_embedding.npy \
  --output output/tts/10min/04_Izaac_DEMO_Account_Creation_&_Dashboard \
  --format wav \
  --play False

# Segment 5: DEMO: Email Aggregation
echo 'Generating 05_Izaac_DEMO_Email_Aggregation.wav...'
python fish-speech/tools/api_client.py \
  --text "$(cat output/tts/10min/05_Izaac_DEMO_Email_Aggregation.txt)" \
  --reference_audio models/izaac_voice_embedding.npy \
  --output output/tts/10min/05_Izaac_DEMO_Email_Aggregation \
  --format wav \
  --play False

# Segment 6: DEMO: Password Rotation Automation
echo 'Generating 06_Izaac_DEMO_Password_Rotation_Automation.wav...'
python fish-speech/tools/api_client.py \
  --text "$(cat output/tts/10min/06_Izaac_DEMO_Password_Rotation_Automation.txt)" \
  --reference_audio models/izaac_voice_embedding.npy \
  --output output/tts/10min/06_Izaac_DEMO_Password_Rotation_Automation \
  --format wav \
  --play False

# Segment 7: DEMO: Testing Environment
echo 'Generating 07_Ken_DEMO_Testing_Environment.wav...'
python fish-speech/tools/api_client.py \
  --text "$(cat output/tts/10min/07_Ken_DEMO_Testing_Environment.txt)" \
  --reference_audio models/ken_voice_embedding.npy \
  --output output/tts/10min/07_Ken_DEMO_Testing_Environment \
  --format wav \
  --play False

# Segment 8: DEMO: Unified Inbox
echo 'Generating 08_Izaac_DEMO_Unified_Inbox.wav...'
python fish-speech/tools/api_client.py \
  --text "$(cat output/tts/10min/08_Izaac_DEMO_Unified_Inbox.txt)" \
  --reference_audio models/izaac_voice_embedding.npy \
  --output output/tts/10min/08_Izaac_DEMO_Unified_Inbox \
  --format wav \
  --play False

# Segment 9: SECURITY & PRIVACY
echo 'Generating 09_Jules_SECURITY_&_PRIVACY.wav...'
python fish-speech/tools/api_client.py \
  --text "$(cat output/tts/10min/09_Jules_SECURITY_&_PRIVACY.txt)" \
  --reference_audio models/jules_voice_embedding.npy \
  --output output/tts/10min/09_Jules_SECURITY_&_PRIVACY \
  --format wav \
  --play False

# Segment 10: DEMO: Password Vault
echo 'Generating 10_Aaron_DEMO_Password_Vault.wav...'
python fish-speech/tools/api_client.py \
  --text "$(cat output/tts/10min/10_Aaron_DEMO_Password_Vault.txt)" \
  --reference_audio models/aaron_voice_embedding.npy \
  --output output/tts/10min/10_Aaron_DEMO_Password_Vault \
  --format wav \
  --play False

# Segment 11: DEMO: Mobile Sync
echo 'Generating 11_Aaron_DEMO_Mobile_Sync.wav...'
python fish-speech/tools/api_client.py \
  --text "$(cat output/tts/10min/11_Aaron_DEMO_Mobile_Sync.txt)" \
  --reference_audio models/aaron_voice_embedding.npy \
  --output output/tts/10min/11_Aaron_DEMO_Mobile_Sync \
  --format wav \
  --play False

# Segment 12: CONCLUSION
echo 'Generating 12_Izaac_CONCLUSION.wav...'
python fish-speech/tools/api_client.py \
  --text "$(cat output/tts/10min/12_Izaac_CONCLUSION.txt)" \
  --reference_audio models/izaac_voice_embedding.npy \
  --output output/tts/10min/12_Izaac_CONCLUSION \
  --format wav \
  --play False

