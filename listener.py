from google import genai
client = genai.Client(api_key="AIzaSyBsDJxT8AzTZ9N67US7YLQ7s2flb6nPcjY")
for m in client.models.list():
    print(f"Modelo disponible: {m.name}")