#!/bin/bash

# Simple wrapper to check for the API key and run the ai_generator.py

if [ -z "$GEMINI_API_KEY" ]; then
  echo "Error: GEMINI_API_KEY environment variable is not set."
  echo "Please set it using: export GEMINI_API_KEY='your_api_key_here'"
  echo "Or pass it directly: python3 ai_generator.py --api-key 'your_api_key_here' ..."
  exit 1
fi

echo "GEMINI_API_KEY found. Running AI generator..."

# Pass all arguments to the python script
python3 ai_generator.py "$@"
