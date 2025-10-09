def main():
    import sys
    from google import genai
    from pathlib import Path
    from dotenv import load_dotenv
    from google.genai import types
    #load_dotenv(Path(__file__).parent / "api_key.env")
    load_dotenv()

    import os
    api_key = os.environ.get("API_KEY")
    verbose = False
    default_model = "gemini-2.0-flash-001"
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

    """client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=default_model, contents=messages,
        )

    if verbose:
        print(f"User prompt: {content}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    print(response.text)"""

if __name__ == "__main__":
    main()
