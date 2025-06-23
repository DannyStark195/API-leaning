from google import genai
from google.genai import types
from flask import current_app #gives access to the current app running and all its resources

def NOB(message):
    client = genai.Client(api_key=current_app.config["API_KEY"])
    response = client.models.generate_content(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        system_instruction= current_app.config['SYSTEM_INSTRUCTION_NOB']),
    contents= message)
    return response.text

def Dennis(message):
    client = genai.Client(api_key=current_app.config["API_KEY"])
    response = client.models.generate_content(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        system_instruction= current_app.config['SYSTEM_INSTRUCTION_DENNIS']),
    contents= message)
    return response.text