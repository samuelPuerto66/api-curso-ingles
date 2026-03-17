"""Google AI Listener - Utility script to list available Gemini models.

This script connects to Google AI Studio API and displays
all available models that can be used with the AI CLI.
Usage: python listener.py
"""
from google import genai

# Initialize the Google AI client with API key
client = genai.Client(api_key="AIzaSyD1oRY5_Ut1dT3L73tj-c752yfDMMTzA18")

# List all available models
for m in client.models.list():
    print(f"modelo disponible: {m.name}")