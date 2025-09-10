import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import call_function, available_functions
from prompts import system_prompt

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

user_prompt = sys.argv[1]

def run_prompt():
    if len(sys.argv) < 2:
        print("Error: no prompt found")
        sys.exit(1)

    user_prompt = sys.argv[1]
    verbose = "--verbose" in sys.argv
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    done = False
    loop = 0
    while loop < 20 and not done:
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                )
            )
            for candidate in response.candidates:
                messages.append(candidate.content)

            if response.function_calls:
                for function_call_part in response.function_calls:
                    function_call_result = call_function(function_call_part, verbose=verbose) 
                    messages.append(types.Content(role="user", parts=function_call_result.parts))

                    if (not function_call_result.parts
                        or not getattr(function_call_result.parts[0], "function_response", None)
                        or function_call_result.parts[0].function_response.response is None):
                        raise RuntimeError("Function call did not return a function_response")
                        
                    if verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
            elif response.text:
                print(response.text)
                messages.append(types.Content(role="model", parts=[types.Part(text=response.text)]))
                done = True
            loop += 1

            if verbose:
                print(f"User prompt: {user_prompt}")
                print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
                print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
        except Exception as e:
            return f"Error: {e}"
        

if __name__ == "__main__":
    run_prompt()