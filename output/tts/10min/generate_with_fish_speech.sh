#!/bin/bash
# Batch TTS generation using Fish Speech API
# Prerequisites:
#   1. Setup references: python scripts/setup_fish_references.py
#   2. Start API server: cd fish-speech && python tools/api_server.py --device cpu

set -e

# Segment 1: INTRODUCTION
echo 'Generating 01_Izaac_INTRODUCTION.wav...'
python ../../../fish-speech/tools/api_client.py \
  --text "$(cat 01_Izaac_INTRODUCTION.txt)" \
  --reference_id izaac \
  --output 01_Izaac_INTRODUCTION \
  --format wav \
  --no-play

# Segment 2: THE PROBLEM
echo 'Generating 02_Izaac_THE_PROBLEM.wav...'
python ../../../fish-speech/tools/api_client.py \
  --text "$(cat 02_Izaac_THE_PROBLEM.txt)" \
  --reference_id izaac \
  --output 02_Izaac_THE_PROBLEM \
  --format wav \
  --no-play

# Segment 3: OUR SOLUTION
echo 'Generating 03_Izaac_OUR_SOLUTION.wav...'
python ../../../fish-speech/tools/api_client.py \
  --text "$(cat 03_Izaac_OUR_SOLUTION.txt)" \
  --reference_id izaac \
  --output 03_Izaac_OUR_SOLUTION \
  --format wav \
  --no-play

# Segment 4: DEMO: Account Creation & Dashboard
echo 'Generating 04_Izaac_DEMO_Account_Creation_&_Dashboard.wav...'
python ../../../fish-speech/tools/api_client.py \
  --text "$(cat 04_Izaac_DEMO_Account_Creation_&_Dashboard.txt)" \
  --reference_id izaac \
  --output 04_Izaac_DEMO_Account_Creation_&_Dashboard \
  --format wav \
  --no-play

# Segment 5: DEMO: Email Aggregation
echo 'Generating 05_Izaac_DEMO_Email_Aggregation.wav...'
python ../../../fish-speech/tools/api_client.py \
  --text "$(cat 05_Izaac_DEMO_Email_Aggregation.txt)" \
  --reference_id izaac \
  --output 05_Izaac_DEMO_Email_Aggregation \
  --format wav \
  --no-play

# Segment 6: DEMO: Password Rotation Automation
echo 'Generating 06_Izaac_DEMO_Password_Rotation_Automation.wav...'
python ../../../fish-speech/tools/api_client.py \
  --text "$(cat 06_Izaac_DEMO_Password_Rotation_Automation.txt)" \
  --reference_id izaac \
  --output 06_Izaac_DEMO_Password_Rotation_Automation \
  --format wav \
  --no-play

# Segment 7: DEMO: Testing Environment
echo 'Generating 07_Ken_DEMO_Testing_Environment.wav...'
python ../../../fish-speech/tools/api_client.py \
  --text "$(cat 07_Ken_DEMO_Testing_Environment.txt)" \
  --reference_id ken \
  --output 07_Ken_DEMO_Testing_Environment \
  --format wav \
  --no-play

# Segment 8: DEMO: Unified Inbox
echo 'Generating 08_Izaac_DEMO_Unified_Inbox.wav...'
python ../../../fish-speech/tools/api_client.py \
  --text "$(cat 08_Izaac_DEMO_Unified_Inbox.txt)" \
  --reference_id izaac \
  --output 08_Izaac_DEMO_Unified_Inbox \
  --format wav \
  --no-play

# Segment 9: SECURITY & PRIVACY
echo 'Generating 09_Jules_SECURITY_&_PRIVACY.wav...'
python ../../../fish-speech/tools/api_client.py \
  --text "$(cat 09_Jules_SECURITY_&_PRIVACY.txt)" \
  --reference_id jules \
  --output 09_Jules_SECURITY_&_PRIVACY \
  --format wav \
  --no-play

# Segment 10: DEMO: Password Vault
echo 'Generating 10_Aaron_DEMO_Password_Vault.wav...'
python ../../../fish-speech/tools/api_client.py \
  --text "$(cat 10_Aaron_DEMO_Password_Vault.txt)" \
  --reference_id aaron \
  --output 10_Aaron_DEMO_Password_Vault \
  --format wav \
  --no-play

# Segment 11: DEMO: Mobile Sync
echo 'Generating 11_Aaron_DEMO_Mobile_Sync.wav...'
python ../../../fish-speech/tools/api_client.py \
  --text "$(cat 11_Aaron_DEMO_Mobile_Sync.txt)" \
  --reference_id aaron \
  --output 11_Aaron_DEMO_Mobile_Sync \
  --format wav \
  --no-play

# Segment 12: CONCLUSION
echo 'Generating 12_Izaac_CONCLUSION.wav...'
python ../../../fish-speech/tools/api_client.py \
  --text "$(cat 12_Izaac_CONCLUSION.txt)" \
  --reference_id izaac \
  --output 12_Izaac_CONCLUSION \
  --format wav \
  --no-play

