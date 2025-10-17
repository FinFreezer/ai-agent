def main():
    import sys
    from google import genai
    from pathlib import Path
    from dotenv import load_dotenv
    from google.genai import types
    from call_function import available_functions, call_available_function
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
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

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
    function_responses = [ ]
    print(f"Functions calls are: {response.function_calls}")
    
    if verbose:
        print(f"User prompt: {content}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if not response.function_calls:
        return response.text
    
    for function_call_part in response.function_calls:
        function_call_result = call_available_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("Empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")

        function_responses.append(function_call_result.parts[0])

        if not function_responses:
            raise Exception("no function responses generated, exiting.")

if __name__ == "__main__":
    main()
