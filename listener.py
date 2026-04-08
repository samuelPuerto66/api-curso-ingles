from google import genai
client = genai.Client(api_key="AIzaSyB6-ZRuv4u5fEGChgSM9roWnnp-oo4iXD8")
for m in client.models.list():
    print(f"Modelo disponible: {m.name}")