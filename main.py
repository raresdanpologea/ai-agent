import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

infile_path = "questions.txt"
outfile_path = "answers.txt"
separator = ","

def file_to_list(file_path, separator=','):
    """
    Reads a file with string-separated values and converts it to a list of strings.

    :param file_path: Path to the input file
    :param separator: Character used to separate values (default is ',')
    :return: List of strings
    """
    try:
        with open(infile_path, 'r') as infile:
            # Read the file contents and split into a list
            contents = infile.read().strip()
            values_list = [value.strip() for value in contents.split(separator) if value.strip()]
            return values_list
    except FileNotFoundError:
        print("Error: File not found.")
        return []

queries = file_to_list(infile_path, separator)

# if len(sys.argv) == 1 :
#     print("No prompt provided. Please provide a prompt as a command line argument.")
#     sys.exit(1)

# user_prompt = sys.argv[1]

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

with open(outfile_path, 'w') as outfile:
    prompt_tokens = 0
    response_tokens = 0
    for query in queries:
        outfile.write(f"Query: {query}") # Write the query to the output file
        messages = [
            #types.Content(role="user", parts=[types.Part(text=user_prompt)]),
            types.Content(role="user", parts=[types.Part(text=query)]),
        ]
        

        response = client.models.generate_content(
            model='gemini-2.0-flash-001', contents=messages
        )

        prompt_tokens += response.usage_metadata.prompt_token_count
        response_tokens += response.usage_metadata.candidates_token_count

        outfile.write(response.text) # Write the response to the output file
    outfile.write(f"\n\nTotal prompt tokens: {prompt_tokens}\n")
    outfile.write(f"Total response tokens: {response_tokens}\n")
    print("Done!")

# if len(sys.argv) > 2:
#     if sys.argv[2] == "--verbose":
#         print("User prompt:", user_prompt)
#         print("Prompt tokens:", response.usage_metadata.prompt_token_count)
#         print("Response tokens:", response.usage_metadata.candidates_token_count)