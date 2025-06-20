import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

if len(sys.argv) == 1 :
    print("No prompt provided. Please provide a prompt as a command line argument.")
    sys.exit(1)

user_prompt = sys.argv[1]

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=messages
)
print(response.text)

if len(sys.argv) > 2:
    if sys.argv[2] == "--verbose":
        print("User prompt:", user_prompt)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)