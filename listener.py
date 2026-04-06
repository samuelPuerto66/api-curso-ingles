from google import genai
client = genai.Client(api_key="AIzaSyD743EyEt0PfLKJNBC30CZhS1J30UlrGJU")
for m in client.models.list():
    print(f"Modelo disponible: {m.name}")