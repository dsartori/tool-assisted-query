import os
import json
from qwen_agent.agents import Assistant
from wikipedia_tool import WikipediaTool
from duckduckgo_tool import DuckDuckGoTool
from microsoft_docs_tool import MicrosoftDocsTool

def run_tool_assisted_query(prompt: str, enable_thinking: bool = True):
    """
    Run a tool-assisted LLM query using Qwen-Agent
    
    Args:
        prompt: User query string
        enable_thinking: Whether to use thinking mode
        
    Returns:
        Final response content
    """
    # Define LLM configuration (Ollama endpoint)
    llm_cfg = {
        'type': 'custom',  # Explicitly specify custom endpoint
        'model': 'qwen3:14b',
        'model_type': 'qwenvl_oai',  # Specify model type for compatibility
        'model_server': 'http://host.docker.internal:11434/v1',  
        'api_key': 'EMPTY',
        'generate_cfg': {
            'max_tokens': 32768,
            'temperature': 0.6 if enable_thinking else 0.7,
            'top_p': 0.95 if enable_thinking else 0.8
        }
    }
    
    # Create agent with tools
    agent = Assistant(
        llm=llm_cfg,
        function_list=[WikipediaTool(), DuckDuckGoTool(), MicrosoftDocsTool()]
    )
    
    # Run the agent with iteration limit and retries
    import time
    messages = [{'role': 'user', 'content': prompt}]
    response = []
    max_retries = 3
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            for chunk in agent.run(messages=messages, call_kwargs={'max_rounds': 99}):
                response.extend(chunk)
            break  # Exit loop if successful
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt+1} failed: {str(e)}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                raise  # Re-raise the last exception if all retries fail
    
    # Extract final response
    if response and isinstance(response, list):
        # The last message in the response list is the final answer
        final_response = response[-1].get('content', '')
    else:
        final_response = "No response generated"
    
    return final_response

if __name__ == "__main__":
    # Get config from environment variables
    user_prompt = os.getenv("USER_PROMPT", "Hello, how are you?")
    enable_thinking = os.getenv("ENABLE_THINKING", "true").lower() == "true"
    
    # Run the query
    response = run_tool_assisted_query(user_prompt, enable_thinking)
    print(response)
