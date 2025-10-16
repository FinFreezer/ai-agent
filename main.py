def main():
    import sys
    from google import genai
    from pathlib import Path
    from dotenv import load_dotenv
    from google.genai import types
    from functions.get_files_info import schema_get_files_info
    from call_function import available_functions
    #load_dotenv(Path(__file__).parent / "api_key.env")
    load_dotenv()

    import os
    api_key = os.environ.get("API_KEY")
    verbose = False
    default_model = "gemini-2.0-flash-001"
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
   
    input = sys.argv
    if len( sys.argv ) < 2:
        print("Error, not enough arguments.")
        exit(1)

    if sys.argv[-1] == "--verbose":
        content = ''.join(sys.argv[1:-1])
        verbose = True
    else:
        content = sys.argv[1]
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=content)]),
    ]
    #content = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    print("Hello from ai-agent!")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=default_model, contents=messages,
        config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
    ),
        )

    if verbose:
        print(f"User prompt: {content}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if not response.function_calls:
        return response.text
    
    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")

if __name__ == "__main__":
    main()
