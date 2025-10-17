from google.genai import types
import sys
from google import genai
from pathlib import Path
from dotenv import load_dotenv
from call_function import available_functions, call_available_function
import os

def main():
    #load_dotenv(Path(__file__).parent / "api_key.env")
    load_dotenv()
    api_key = os.environ.get("API_KEY")
    verbose = False
    default_model = "gemini-2.0-flash-001"
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make use of all the available functions to try and reach a solution:

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
    """
    loops = 0
    while loops < 20:
        try:
            response = client.models.generate_content(
                model=default_model, contents=messages,
                config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
                )
            
            candidates = response.candidates
            if candidates:
                for variation in candidates:
                    messages.append(variation.content)
            if response.text:
                print(f"Final response: {response.text}")
                break
        except Exception as e:
            print(f"Something went wrong, error: {e}")
            raise Exception

    if loops > 20:
        print(f"Maximum loops '{loops}' reached.")
        sys.exit(1)
        
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
        
        messages.append(
            types.Content(
                role="user",
                parts=function_responses,
            )
        )

if __name__ == "__main__":
    main()
    """
    MAX_ITERS = 20
    iters = 0
    while True:
        iters += 1
        if iters > MAX_ITERS:
            print(f"Maximum iterations ({MAX_ITERS}) reached.")
            sys.exit(1)

        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")


def generate_content(client, messages, verbose):
    system_prompt = """
    You are a helpful AI coding agent.
    Assume you can reach the solution by calling the functions with just the context of the user prompt alone.
    Try listing and going through the files as the first step if stuck.
    When a user asks a question or makes a request, make use of all the available functions to try and reach a solution:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_available_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")

    messages.append(types.Content(role="user", parts=function_responses))


if __name__ == "__main__":
    main()