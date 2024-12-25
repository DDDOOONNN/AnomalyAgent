import google.generativeai as genai
import os

genai.configure(api_key='AIzaSyC-DUwcu0XTsd-jEafCYEmlqscBsjV8DSI',transport='rest')    
model = genai.GenerativeModel('gemini-1.5-flash')    
response = model.generate_content("write a poem about the moon")    
print(response.text)