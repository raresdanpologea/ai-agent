import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from openai import OpenAI

infile_path = "questions.txt"
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

def queryGemini(queries):
    """
    Queries the Gemini API with a list of queries and returns the responses.

    :param queries: List of queries to send to the Gemini API
    :return: List of responses from the Gemini API
    """
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    outfile_path = "answersGemini.txt"

    with open(outfile_path, 'w') as outfile:
        prompt_tokens = 0
        response_tokens = 0
        for query in queries:
            outfile.write(f"Query: {query}") # Write the query to the output file
            messages = [
                types.Content(role="user", parts=[types.Part(text=query)]),
            ]
            response = client.models.generate_content(
                model='gemini-2.0-flash-001', contents=messages
            )
            outfile.write(response.text) # Write the response to the output file

            prompt_tokens += response.usage_metadata.prompt_token_count
            response_tokens += response.usage_metadata.candidates_token_count
            outfile.write(f"\n\nTotal prompt tokens: {prompt_tokens}\n")
            outfile.write(f"Total response tokens: {response_tokens}\n")
    print("Gemini done!")

def queryMistral(queries):
    """
    Queries the Mistral API with a list of queries and returns the responses.

    :param queries: List of queries to send to the Mistral API
    :return: List of responses from the Mistral API
    """
    outfile_path = "answersMistral.txt"
    load_dotenv()

    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY")
    )

    with open("answersMistral.txt", 'w') as outfile:
        prompt_tokens = 0
        response_tokens = 0
        for query in queries:
            outfile.write(f"Query: {query}") # Write the query to the output file

            completion = client.chat.completions.create(
            extra_headers={},
            extra_body={},
            model="mistralai/mistral-small-3.2-24b-instruct:free",
            messages=[
                {
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": query
                    },
                ]
                }
            ]
            )
            response = completion.choices[0].message.content
            outfile.write(response) # Write the response to the output file

            # prompt_tokens += response.usage.prompt_tokens
            # response_tokens += response.usage.completion_tokens
            # outfile.write(f"\n\nTotal prompt tokens: {prompt_tokens}\n")
            # outfile.write(f"Total response tokens: {response_tokens}\n")
    print("Mistral done!")

def queryR1(queries):
    """
    Queries the R1 API with a list of queries and returns the responses.

    :param queries: List of queries to send to the R1 API
    :return: List of responses from the R1 API
    """
    outfile_path = "answersR1.txt"
    load_dotenv()

    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
    )

    with open("answersR1.txt", 'w') as outfile:
        prompt_tokens = 0
        response_tokens = 0
        for query in queries:
            outfile.write(f"Query: {query}") # Write the query to the output file

            completion = client.chat.completions.create(
            extra_headers={},
            extra_body={},
            model="deepseek/deepseek-r1-0528:free",
            messages=[
                {
                "role": "user",
                "content": query
                }
            ]
            )
            response = completion.choices[0].message.content
            outfile.write(response) # Write the response to the output file

            # prompt_tokens += response.usage.prompt_tokens
            # response_tokens += response.usage.completion_tokens
            # outfile.write(f"\n\nTotal prompt tokens: {prompt_tokens}\n")
            # outfile.write(f"Total response tokens: {response_tokens}\n")   
    print("R1 done!")

queries = file_to_list(infile_path, separator)
queryGemini(queries)
queryMistral(queries)
queryR1(queries)