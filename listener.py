from google import genai
client = genai.Client(api_key="AIzaSyD1oRY5_Ut1dT3L73tj-c752yfDMMTzA18")
for m in client.models.list():
    print(f"mdoelo disponible: {m.name}")