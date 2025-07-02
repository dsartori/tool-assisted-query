import requests
import json
from qwen_agent.tools.base import BaseTool, register_tool

@register_tool('MicrosoftDocs')
class MicrosoftDocsTool(BaseTool):
    description = 'Search official Microsoft/Azure documentation to find relevant content'
    parameters = [{
        'name': 'question',
        'type': 'string',
        'description': 'Question about Microsoft/Azure products, services, platforms, developer tools, frameworks, or APIs',
        'required': True
    }]

    def call(self, params: str | dict, **kwargs) -> str:
        # Handle both string and dictionary parameter formats
        if isinstance(params, str):
            try:
                # Try to parse as JSON
                params_dict = json.loads(params)
                if isinstance(params_dict, str):
                    # If it's a string, use it as the question
                    question = params_dict
                else:
                    # If it's a dictionary, extract the question
                    question = params_dict.get("question", "")
            except json.JSONDecodeError:
                # If not valid JSON, treat the string as the question
                question = params
        else:
            # It's a dictionary
            question = params.get("question", "")
        
        if not question:
            raise ValueError("Missing 'question' parameter")
        
        # Call MCP proxy endpoint
        url = 'http://host.docker.internal:8000/microsoft.docs.mcp/microsoft_docs_search'
        payload = {"question": question}
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.text
